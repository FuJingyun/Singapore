from PIL import Image
from shutil import copyfile
import pathlib
import os, glob, sys

if len(sys.argv) < 3:
    print("Usage: {} (datasetsrc_dir) (destination_dir) [Optional: threshold, default=300]".format(sys.argv[0]))
    exit(1)
 
srcPath = sys.argv[1]
dstPath = sys.argv[2]
if len(sys.argv) == 4:
    threshold = int(sys.argv[3])
else:
    threshold = 300

if srcPath[-1] != '/':
    srcPath = srcPath + '/'
if dstPath[-1] != '/':
    dstPath = dstPath + '/'

# for regular dataset (Have ID and name as folder name)
def dataset_list(path_to_dataset, keep_folder_id = []):
    ret_dict = {}
    for outer_folder in os.scandir(path_to_dataset):
        try:
            folder_id, food_name = outer_folder.name.split("_")
        except Exception as e:
            print(outer_folder.name, e)
            folder_id = outer_folder.name
        print("processing",outer_folder.path,"folder_id:",folder_id)
        try:
            folder_id = int(folder_id)
        except:
            print("Invalid folder id:",outer_folder.name)
        if len(keep_folder_id) and not folder_id in keep_folder_id:
            print("skipping",outer_folder.path,"it is marked as to skip")
            continue
        print("including",outer_folder.name, outer_folder.path)
        ret_dict[outer_folder.name] = []
        for file in glob.iglob(outer_folder.path+'/**/*.jpg', recursive=True):
            if not "@eaDir" in file:
                ret_dict[outer_folder.name].append(file)
        for file in glob.iglob(outer_folder.path+'/**/*.jpeg', recursive=True):
            if not "@eaDir" in file:
                ret_dict[outer_folder.name].append(file)
        for file in glob.iglob(outer_folder.path+'/**/*.JPEG', recursive=True):
            if not "@eaDir" in file:
                ret_dict[outer_folder.name].append(file)
        for file in glob.iglob(outer_folder.path+'/**/*.JPG', recursive=True):
            if not "@eaDir" in file:
                ret_dict[outer_folder.name].append(file)
    return ret_dict

    
if __name__ == "__main__":
    dataset = dataset_list(srcPath)
    for food_name, imgs_list in dataset.items():
        counter = 0
        for img_path in imgs_list:
            try:
                i = Image.open(img_path)
                i.convert("RGB")
                dst = img_path.replace(srcPath, dstPath)
                pathlib.Path(dst).parent.mkdir(parents=True, exist_ok=True)
                copyfile(img_path, dst)
                counter += 1
                if counter >= threshold:
                    break
            except Exception as e:
                print(e, "Error opening file:", img_path)
        print("Done processing",food_name)
