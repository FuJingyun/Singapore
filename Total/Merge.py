'''
从一个目录下的n个文件夹中的所有文件以及子目录中的文件整合到一级子目录中
Author ： Fu Jingyun
'''
import os
import random
import shutil
 

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
path='C:/Users/NExT/Desktop/Change'
newpath = 'C:/Users/NExT/Desktop/Change_merged'


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
             if temppath[-4]=='.':
                 shutil.copy(temppath,newsubpath+'/'+str(namenum)+temppath[-4:])  #复制至新路径
                 namenum+=1  
             elif temppath[-5]=='.':
                 shutil.copy(temppath,newsubpath+'/'+str(namenum)+temppath[-5:])  #复制至新路径
                 namenum+=1 
         

         
         

        
         
         
         
         
         
         
         
         
         
         
         
         
         
          
         
     

