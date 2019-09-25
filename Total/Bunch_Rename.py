'''
从一个目录下的n个文件夹中的所有文件以及子目录中的文件整合到一级子目录中
Author ： Fu Jingyun
'''
import piexif
import os, glob, sys
import pathlib
import random
import shutil
from PIL import Image
 

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

def IsValidImage(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid



#给定操作目录
path='C:/Users/NExT/Desktop/New_BF_test'
newpath = 'C:/Users/NExT/Desktop/New_BF_test_ok'
problempath= 'C:/Users/NExT/Desktop/problem'


#建立新文件夹
if not os.path.exists(newpath):
    os.mkdir(newpath)
dir = os.listdir(path)

if not os.path.exists(problempath):
    os.mkdir(problempath)

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
for file in dir: 
     number=1
     subfile = path+'/'+file
     newsubpath = newpath+'/'+file
     if not os.path.exists(newsubpath):
         os.mkdir(newsubpath)
     filelist = list_all_files(subfile)
     namenum = 1
     for k in range(0,len(filelist)):
         temppath=path+'/'+file+'/'+ str(k)+'.jpg'
         if  os.path.exists(temppath):
             if os.path.isfile(temppath):
                 if IsValidImage(temppath):
                     try:
                         piexif.remove(temppath)
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=newsubpath+'/'+str(k)+temppath[-4:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=newsubpath+'/'+str(k)+temppath[-5:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                     except:
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=problempath+'/'+str(namenum)+temppath[-4:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=problempath+'/'+str(namenum)+temppath[-5:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
         elif  os.path.exists(path+'/'+file+'/'+ str(k)+'JPEG'):
             os.rename(path+'/'+file+'/'+ str(k)+'JPEG',path+'/'+file+'/'+ str(k)+'.JPEG')
             temppath=path+'/'+file+'/'+ str(k)+'.JPEG'
             if os.path.isfile(temppath):
                 if IsValidImage(temppath):
                     try:
                         piexif.remove(temppath)
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=newsubpath+'/'+str(k)+temppath[-4:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=newsubpath+'/'+str(k)+temppath[-5:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                     except:
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=problempath+'/'+str(namenum)+temppath[-4:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=problempath+'/'+str(namenum)+temppath[-5:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
         elif os.path.exists(path+'/'+file+'/'+ str(k)+'.jpeg'):
             temppath=path+'/'+file+'/'+ str(k)+'.jpeg'
             if os.path.isfile(temppath):
                 if IsValidImage(temppath):
                     try:
                         piexif.remove(temppath)
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=newsubpath+'/'+str(k)+temppath[-4:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=newsubpath+'/'+str(k)+temppath[-5:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                     except:
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=problempath+'/'+str(namenum)+temppath[-4:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=problempath+'/'+str(namenum)+temppath[-5:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
         elif os.path.exists(path+'/'+file+'/'+ str(k)+'.JPEG'):
             temppath=path+'/'+file+'/'+ str(k)+'.JPEG'
             if os.path.isfile(temppath):
                 if IsValidImage(temppath):
                     try:
                         piexif.remove(temppath)
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=newsubpath+'/'+str(k)+temppath[-4:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=newsubpath+'/'+str(k)+temppath[-5:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                     except:
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=problempath+'/'+str(namenum)+temppath[-4:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=problempath+'/'+str(namenum)+temppath[-5:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
         elif os.path.exists(path+'/'+file+'/'+ str(k)+'.JPG'):
             temppath=path+'/'+file+'/'+ str(k)+'.JPG'
             if os.path.isfile(temppath):
                 if IsValidImage(temppath):
                     try:
                         piexif.remove(temppath)
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=newsubpath+'/'+str(k)+temppath[-4:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=newsubpath+'/'+str(k)+temppath[-5:]
#                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                     except:
                         i = Image.open(temppath)
                         i=i.convert("RGB")
                         if temppath[-4]=='.':   
                             dst=problempath+'/'+str(namenum)+temppath[-4:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)
                         elif temppath[-5]=='.':
                             dst=problempath+'/'+str(namenum)+temppath[-5:]
                             namenum+=1
        #                   shutil.copy(temppath, dst)
                             i.save(dst)                   