'''
统计一个目录下的n个文件夹中的子文件数目
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
path='C:/Users/NExT/Desktop/New_BF&S_train_ok'
newpath = 'C:/Users/NExT/Desktop/test'


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


#for root, dirs, files in os.walk(path):
#    print(files)
#        if (files[i][-3:] == 'jpg') or (files[i][-3:] == 'png') or (files[i][-3:] == 'JPG'):
#        if(files[i][-4] == '.' and files[i][-3] != 't'):  #判断当前文件是否为需要的文件
#            file_path = root+'/'+files[i]  
#            new_file_path = new_path+ '/'+ str(j)+'.'+files[i][-3:]  #重命名目标图片
#            shutil.copy(file_path,new_file_path)  #复制至新路径
#            j+=1

num_files_rec = 0 #路径下文件数量,包括子文件夹里的文件数量，不包括空文件夹

i=1
f = open('C:/Users/NExT/Desktop/train_NUM.txt','w')

for file in dir: 
     number=1
     subfile = path+'/'+file
#     newsubpath = newpath+'/'+file
#     if not os.path.exists(newsubpath):
#         os.mkdir(newsubpath)
     #print(subfile)         
#     print(i)
#     i=i+1 
     num_files_rec = 0     
     for root,dirs,files in os.walk(subfile):   
         for each in files:    
             num_files_rec += 1
     print(file+' num: '+str(num_files_rec))
     f.write(file+' num: '+str(num_files_rec)+'\n')
f.close()
    
             
         

         