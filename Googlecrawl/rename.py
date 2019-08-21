import os
import io
import shutil


#source: abs path source folder
#destination: abs path destination folder
#merge causes files in source to be transferred to destination
def merge(source, destination):
    os.chdir(source)
    #get all files in source
    s_file_list = os.listdir(source)
    for f in s_file_list:
        shutil.move(f, destination)



#takes in path to images and name of text_file
def rename(path, text_file):
    #change to path directory
    os.chdir(path)

    #get all images w/o the .txt file
    all_files = os.listdir(path)
    img_lst = [ele for ele in all_files if '.txt' not in ele]
    #get number of images in path
    num_img = len(img_lst)
    
    #get .txt file
    txt = [ele for ele in all_files if '.txt' in ele][0]
    #extract info from txt
    with io.open(text_file, encoding='utf-8') as file:
        data = file.read()

    
    #following loop performs renaming operation
    for i in range(num_img):
        #get original name
        ori_name = img_lst[i]
        #form new name
        new_name = str(i) + '_' + data +'.jpg'
        #renaming
        os.rename(ori_name, new_name)




