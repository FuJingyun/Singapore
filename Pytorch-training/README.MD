# Training multi-class classifier (Non-Docker)

## Overview
Steps to take
- Verify the images are readable by Python Imaging Library
- Split the Dataset into training and evaluation set
- Add execution permission for `entrypoint.sh`
- Edit training json configuration `training_config.json`
- Begin training by running `./entrypoint.sh training_config.json`
- Edit report generation json configuration `val_config.json`
- Run validate model report generator by running `python -u val_model.py --conf val_config.json`

## Preprocessing
Preprocessing only needs to be done once on a dataset. If the dataset was cleaned/updated recently, or you wish to sample a new subset of images, you may run the preprocessing steps again.
#### Step 1
Activate conda environment `conda activate pytorch1.0`
#### Step 2
Verify the images are readable by PIL `python -u 1_CopyingOkayImages.py <dataset_path> <new_dataset_path>` 
##### Example `python -u 1_CopyingOkayImages.py /media/Share/singgee/Pytorch-training/files/Demo /media/Share/singgee/Pytorch-training/files/Demo_checked`
#### Step 3
Split the dataset into training and validation set `python -u 2_SplittingWholeDataset.py <new_dataset_path_whole_set> <new_dataset_path_training_set>`
##### Example `python -u 2_SplittingWholeDataset.py /media/Share/singgee/Pytorch-training/files/Demo_checked /media/Share/singgee/Pytorch-training/files/Demo_training`
#### Step 4 Appending `_val` by rename folder to prevent misunderstanding
##### Example `mv /media/Share/singgee/Pytorch-training/files/Demo_checked /media/Share/singgee/Pytorch-training/files/Demo_val`

## Train model
After splitting the dataset, you may proceed to train a model. Often you will need to train a set of models as it is not a [convex-optimization problem](https://en.wikipedia.org/wiki/Convex_optimization), to get a model with lower `loss`. Everytime one training session is run, a new model will be trained starting with the pretrained model taken from online. These models are stored under `files/snaphot`.
#### Step 1
Edit the configuration file `files/training_config.json`. Ensure that the `data_folder_dir` points to your training dataset, and `testdata_folder_dir` points to your validation dataset. You may also need to set the GPU number at `which_gpu`. Use `nvidia-smi` to check GPU availability.

#### Step 2
Run the following command to add execution permission for shell script
```
chmod +x entrypoint.sh
```
#### Step 3
Commence training by running the command 
```
nohup ./entrypoint.sh training_config.json &
```

#### Step 4
Check the progress of the training using the `tail` command.
```
tail -n 950 -f nohup.out
``` 
You may terminate the training prematurely when the loss value stops dropping.

#### Step 5 
To terminate training, simply kill the parent process by running the following command `kill {parent_PID}`

##  Validate model
After training a model, you may evaluate it using the `validation` set generated from the `Preprocessing` step, or actual trial images to test its performance (do not need to do preprocessing on the trial images).
#### Step 1
Edit the configuration file `post-training/val_config.conf`. Ensure that `model_path` points to the model's weights located in `files/snapshot` and `dataset_path` points to the folder containing the images for validation.

#### Step 2
Running the python script by doing `python -u val_model.py --conf val_config.json`
