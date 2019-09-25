import torch
import torchvision
from PIL import Image
import copy
import pretrainedmodels
import time
from datetime import timedelta
import pathlib
from datetime import datetime
from tfboardlogger import Logger
import math, os
import warnings
import json
import sys

if len(sys.argv) < 2:
    print(sys.argv)
    exit(1)

with open(sys.argv[1], "rt") as infile:
    training_config = json.load(infile)

warnings.filterwarnings('ignore', "(Possibly )? corrupt EXIF data", UserWarning)
# use cuda if available
device = torch.device("cuda:{}".format(
    training_config["which_gpu"]) if torch.cuda.is_available() and "which_gpu" in training_config else "cpu")

dataset_prefix = training_config["dataset_prefix"]
timestamp_prefix = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

# using resnet50
model_name = training_config["model_name"]  # could be fbresnet152 or inceptionresnetv2
model = pretrainedmodels.__dict__[model_name](num_classes=1000, pretrained='imagenet')

logging_model_params = training_config["logging_model_params"]
snapshot_every_n_epoch = training_config["snapshot_every_n_epoch"]

# freeze 1 to 6 of resnet50
# ct = 0
# for child in model.children():
#    ct += 1
#    if ct < 7:
#        for param in child.parameters():
#            param.requires_grad = False
#    else:
#        for param in child.parameters():
#            param.requires_grad = True


# tensorboard logger
tlogger = Logger('./files/snapshot/{}-{}'.format(dataset_prefix, timestamp_prefix))

# batch sizes
train_batchsz = training_config["train_batchsz"]
val_batchsz = training_config["val_batchsz"]

# hyper-params
start_lr = training_config["start_lr"]
patience_epoch = training_config["patience_epoch"]

print("Training batch size:{}, Validation batch size:{}".format(train_batchsz, val_batchsz))

# transforms
train_transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize(299),
    torchvision.transforms.RandomResizedCrop(224),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
val_transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize(299),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
print("Reading in training images")
# training dataloader
data_folder_dir = training_config["data_folder_dir"]
food_data = torchvision.datasets.ImageFolder(data_folder_dir, train_transform)
food_data_classes = food_data.classes
train_dataloader = torch.utils.data.DataLoader(food_data, batch_size=train_batchsz, shuffle=True, num_workers=8)
num_classes = len(food_data_classes)

test_dataloader = None
phases = ['train']

# testset dataloader
testdata_folder_dir = training_config["testdata_folder_dir"]
if len(testdata_folder_dir) > 1:
    foodtest_data = torchvision.datasets.ImageFolder(testdata_folder_dir, val_transform)
    test_dataloader = torch.utils.data.DataLoader(foodtest_data, batch_size=val_batchsz, shuffle=True, num_workers=4)
    phases.append('val')
    if num_classes != len(foodtest_data.classes):
        print("Validation set has different number of classes than training set!")
        exit(1)

model.avgpool = torch.nn.AdaptiveAvgPool2d(1)
last_layer_num_feat = model.last_linear.in_features
model.last_linear = torch.nn.Linear(last_layer_num_feat, num_classes)

# resume training from checkpoint
if "resume_checkpoint" in training_config and len(training_config["resume_checkpoint"]):
    print("Resuming from checkpoint:", training_config["resume_checkpoint"])
    model.load_state_dict(torch.load(training_config["resume_checkpoint"]))
    model.eval()

model = model.to(device)
# merging dataloaders
dataloader = {'train': train_dataloader, 'val': test_dataloader}

# loss fn
criterion = torch.nn.CrossEntropyLoss()
# optimiser
# optimiser = torch.optim.SGD(model.parameters(), lr = 0.01, momentum=0.9)
optimiser = torch.optim.Adam(model.parameters(), lr=start_lr)
# scheduler to decay LR by a factor of 0.1 every 40 epochs
lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimiser, verbose=True, patience=patience_epoch)


def get_lr(optimiser):
    for param_grp in optimiser.param_groups:
        return param_grp['lr']


# training model
num_epochs = 1300

best_model_weights = copy.deepcopy(model.state_dict())

# hardcoding an absurdly big number so any loss value will be smaller
lowest_loss = 99999990.0

since = time.time()
batch_running_time = time.time()
# track history if training
torch.set_grad_enabled(True)

if dataloader['val'] is None:
    print("Num of batches for training:", len(dataloader['train']))
else:
    print("Num of batches for training:", len(dataloader['train']), "for testing:", len(dataloader['val']))

snapshot_path = "./files/snapshot"
pathlib.Path(snapshot_path).mkdir(parents=True, exist_ok=True)

print("Model used:", model_name)
print("Training for dataset {} starts".format(dataset_prefix))
print("Using Adam optimiser. Beginning lr:{:.4f}, dropping lr by {} every 1 epoch(s) with no drop in loss".format(
    get_lr(optimiser), 0.1))
print("Number of classes in '{}':{}".format(data_folder_dir, num_classes))

logger_batch_sz = int(math.ceil(len(dataloader['train']) * 0.01))
print("Time start:{}, logging every {} mini batch".format(timestamp_prefix, logger_batch_sz))

if os.path.isfile("{}/{}-classes.txt".format(snapshot_path, dataset_prefix)):
    tmpSet = set()
    with open("{}/{}-classes.txt".format(snapshot_path, dataset_prefix), "rt", encoding="utf8") as infile:
        for class_name_str in infile.readlines():
            tmpSet.add(class_name_str.strip())
    tmpDiff = [x for x in food_data_classes if x not in tmpSet]
    if len(tmpDiff) > 0:
        with open("{}/{}-classes-{}.txt".format(snapshot_path, dataset_prefix, timestamp_prefix), "wt",
                  encoding="utf16") as outfile:
            for class_name in food_data_classes:
                outfile.write("{}\n".format(class_name))
else:
    with open("{}/{}-classes.txt".format(snapshot_path, dataset_prefix), "wt", encoding="utf8") as outfile:
        for class_name in food_data_classes:
            try:
                outfile.write("{}\n".format(class_name))
            except Exception as e:
                print("Classname:", class_name, "Exception message:", e)
                exit(1)

for epoch in range(num_epochs):
    print("Epoch: {}/{}".format(epoch + 1, num_epochs))
    print("=" * 55)  # print equal sign 55 times as a divider

    for phase in phases:
        if phase == 'train':
            model.train()
        else:
            model.eval()
        # just training for now, will include validation later
        running_loss = 0.0
        running_corrects = 0.0

        for batch_idx, (imgs, labels) in enumerate(dataloader[phase]):
            batch_running_time = time.time()
            input_imgs = imgs.to(device)
            labels = labels.to(device)

            # zero the parameter gradients
            optimiser.zero_grad()

            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(input_imgs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                if phase == 'train':
                    loss.backward()
                    optimiser.step()

            running_loss += loss.item() * input_imgs.size(0)
            accuracy = (labels == preds.squeeze()).float().mean()
            running_corrects += torch.sum(preds == labels.data)
            batch_time_elapsed = time.time() - batch_running_time

            if batch_idx and not batch_idx % logger_batch_sz:
                print(
                    "{} Batch:{}, loss:{:.5f}, batch running time: {:.0f}:{:02d}".format(phase, batch_idx, loss.item(),
                                                                                         batch_time_elapsed / 60,
                                                                                         running_corrects % 60))
                tlogger.scalar_summary('{}-running_loss'.format(phase), loss.item() * input_imgs.size(0),
                                       batch_idx + 1 + epoch * len(dataloader[phase]))
                # tlogger.scalar_summary('{}-accuracy'.format(phase), accuracy, batch_idx+1+epoch*len(dataloader[phase]))
                if logging_model_params:
                    for tag, value in model.named_parameters():
                        tag = tag.replace('.', '/')
                        tlogger.histo_summary("{}/".format(phase) + tag, value.data.cpu().numpy(),
                                              batch_idx + 1 + epoch * len(dataloader[phase]))
                        if not value.grad is None:
                            tlogger.histo_summary("{}/".format(phase) + tag + '/grad', value.grad.cpu().numpy(),
                                                  batch_idx + 1 + epoch * len(dataloader[phase]))

        epoch_loss = running_loss / (len(dataloader[phase].dataset))
        epoch_acc = running_corrects / (len(dataloader[phase].dataset))
        time_elapsed = time.time() - since

        tlogger.scalar_summary('{}-epoch_running_loss'.format(phase), epoch_loss, epoch + 1)
        # tlogger.scalar_summary('{}-epoch_accuracy'.format(phase), epoch_acc, epoch+1)

        # deep copy the model
        if (phase == 'val' or len(phases) == 1) and lowest_loss > epoch_loss:
            lowest_loss = epoch_loss
            best_model_weights = copy.deepcopy(model.state_dict())
            print(
                "Lowest loss so far:{}, snapshotting weights to BestWeight-{}-{}.pth".format(epoch_loss, dataset_prefix,
                                                                                             timestamp_prefix))
            torch.save(best_model_weights,
                       "{}/BestWeight-{}-{}.pth".format(snapshot_path, dataset_prefix, timestamp_prefix))
        if phase == 'val' or len(phases) == 1:
            lr_scheduler.step(epoch_loss)

        # snapshot the model every 2 iterations
        if epoch and not epoch % snapshot_every_n_epoch:
            torch.save(model.state_dict(),
                       "{}/{}-{}/{}-{}-{}.pth".format(snapshot_path, dataset_prefix, timestamp_prefix, dataset_prefix,
                                                      timestamp_prefix, epoch + 1))

        print("-" * 50)
        # print("{} Epoch:{}, Loss: {:.4f}, Acc: {:.4f}, lr: {:.8f}, Total running time: {:.0f}:{:.0f}".format(phase, epoch+1, epoch_loss, epoch_acc, get_lr(optimiser), time_elapsed / 60, time_elapsed % 60))
        print("{} Epoch:{}, Loss: {:.4f}, lr: {:.8f}, Total running time: {:.0f}:{:.0f}".format(phase, epoch + 1,
                                                                                                epoch_loss,
                                                                                                get_lr(optimiser),
                                                                                                time_elapsed / 60,
                                                                                                time_elapsed % 60))

time_elapsed = time.time() - since
print('Training complete in {}'.format(timedelta(seconds=time_elapsed)))
torch.save(best_model_weights, "BestWeight-{}-{}.pth".format(dataset_prefix, timestamp_prefix))
