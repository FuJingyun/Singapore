'''
调整一个目录下的n个文件夹中的所有图片的大小
Author ： Fu Jingyun
'''
import os
import random
import shutil
from PIL import Image
import re
 

#实现抽取和文件移动
def copyFile(fileDir,tarDir):
    pathDir = os.listdir(fileDir)
    filenumber=len(pathDir)         #统计目录下总文件数量
    rate=0.2                        #抽取图片的比例
    picknumber=int(filenumber*rate) #按照给定比例从文件夹中取一定数量图片
    sample = random.sample(pathDir, picknumber)
    for name in sample:
        shutil.move(fileDir + name, tarDir + name)
 
def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files


#给定操作目录
path='C:/Users/NExT/Desktop/New_BF&S_train_ok'
newpath = 'C:/Users/NExT/Desktop/CP_NBF&S_train_ok'


#建立新文件夹
if not os.path.exists(newpath):
    os.mkdir(newpath)
dir = os.listdir(path)
#j = 0


#调用函数实现文件移动
#for file in dirs: 
#    j=j+1
#    tarDir =newpath + '/'+ str(j)
#    os.mkdir(tarDir)
#    tarDir =tarDir + '/'
#    fileDir = path +'/'+file+'/'
#    copyFile(fileDir,tarDir)




num_files_rec = 0 #路径下文件数量,包括子文件夹里的文件数量，不包括空文件夹

i=1
iphone5_width=299
iphone5_depth=299

for file in dir: 
     number=1
     subfile = path+'/'+file
     newsubpath = newpath+'/'+file
     if not os.path.exists(newsubpath):
         os.mkdir(newsubpath)
     filelist = list_all_files(subfile)
     namenum = 1
     for k in range(0,len(filelist)):
         temppath=filelist[k]
         if os.path.isfile(temppath):
             im=Image.open(temppath)
             w,h=im.size
             
             if w>iphone5_width:
#        print pic
#        print "图片名称为"+pic+"图片被修改"
                 h_new=int(iphone5_width*h/w)
                 w_new=iphone5_width
                 out = im.resize((w_new,h_new),Image.ANTIALIAS)
                 new_path=newsubpath+'/'+str(namenum)+temppath[-4:]
                 out.save(new_path)
                 namenum+=1

             elif h>iphone5_depth:
                 w_new=int(iphone5_depth*w/h)
                 h_new=iphone5_depth
                 out = im.resize((w_new,h_new),Image.ANTIALIAS)
                 new_path=newsubpath+'/'+str(namenum)+temppath[-4:]
                 out.save(new_path)
                 namenum+=1

             
#             torchvision.transforms.Resize(299),
#             torchvision.transforms.RandomResizedCrop(224),
#             torchvision.transforms.RandomHorizontalFlip(),
#             torchvision.transforms.ToTensor(),
#             torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
         

         
         

        
         
         
         
         
         
         
         
         
         
         
         
         
         
          
         
     

