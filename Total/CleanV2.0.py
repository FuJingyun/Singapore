'''
选取符合要求的图片，清除exif,可保留原文件格式（Movepic_same),或统一转化为jpg格式保存（Movepic)
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
path='C:/Users/NExT/Desktop/Change_merged'
newpath = 'C:/Users/NExT/Desktop/Change_cleaned'
problempath= 'C:/Users/NExT/Desktop/Problem_0917'


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


def Movepic_same(temppath,namenum,newsubpath,k):
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
    return namenum

def Movepic(temppath,namenum,newsubpath,k):
    if os.path.isfile(temppath):
         if IsValidImage(temppath):
             try:
                 piexif.remove(temppath)
                 i = Image.open(temppath)
                 i=i.convert("RGB")
                 if temppath[-4]=='.':   
                     dst=newsubpath+'/'+str(k)+'.jpg'
#                             namenum+=1
#                   shutil.copy(temppath, dst)
                     i.save(dst)
                 elif temppath[-5]=='.':
                     dst=newsubpath+'/'+str(k)+'.jpg'
#                             namenum+=1
#                   shutil.copy(temppath, dst)
                     i.save(dst)
             except:
                 i = Image.open(temppath)
                 i=i.convert("RGB")
                 if temppath[-4]=='.':   
                     dst=problempath+'/'+str(namenum)+'.jpg'
                     namenum+=1
#                   shutil.copy(temppath, dst)
                     i.save(dst)
                 elif temppath[-5]=='.':
                     dst=problempath+'/'+str(namenum)+'.jpg'
                     namenum+=1
#                   shutil.copy(temppath, dst)
                     i.save(dst)
    return namenum


for file in dir: 
     number=1
     subfile = path+'/'+file
     newsubpath = newpath+'/'+file
     if not os.path.exists(newsubpath):
         os.mkdir(newsubpath)
     filelist = list_all_files(subfile)
     namenum = 1
     for k in range(0,len(filelist)):
         if  os.path.exists(path+'/'+file+'/'+ str(k)+'.jpeg'):
              temppath = path+'/'+file+'/'+ str(k)+'.jpeg'
              namenum = Movepic(temppath,namenum,newsubpath,k)
         elif   os.path.exists(path+'/'+file+'/'+ str(k)+'.JPEG'):
              temppath = path+'/'+file+'/'+ str(k)+'.JPEG'
              namenum = Movepic(temppath,namenum,newsubpath,k)
         elif   os.path.exists(path+'/'+file+'/'+ str(k)+'.jpg'):
              temppath = path+'/'+file+'/'+ str(k)+'.jpg'
              namenum = Movepic(temppath,namenum,newsubpath,k)
         elif   os.path.exists(path+'/'+file+'/'+ str(k)+'.JPG'):
              temppath = path+'/'+file+'/'+ str(k)+'.JPG'
              namenum = Movepic(temppath,namenum,newsubpath,k)
         elif   os.path.exists(path+'/'+file+'/'+ str(k)+'.png'):
              temppath = path+'/'+file+'/'+ str(k)+'.png'
              namenum = Movepic(temppath,namenum,newsubpath,k)
         elif   os.path.exists(path+'/'+file+'/'+ str(k)+'.PNG'):
              temppath = path+'/'+file+'/'+ str(k)+'.PNG'
              namenum = Movepic(temppath,namenum,newsubpath,k)
             
     
                 
                

             
             
#             png = Image.open(object.logo.path)
#             png.load() # required for png.split()
#
#             background = Image.new("RGB", png.size, (255, 255, 255))
#             background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
#             background.save('foo.jpg', 'JPEG', quality=80)
#             print img.size  #图片的尺寸
#             print img.mode  #图片的模式
#             print img.format  #图片的格式
             
#             
#             shutil.copy(temppath,newsubpath+'/'+str(namenum)+temppath[-4:])  #复制至新路径
#             namenum+=1   
         

         
         

        
         
         
         
         
         
         
         
         
         
         
         
         
         
          
         
     

