'''
从一个目录下的n个文件夹中，分别随机抽取m图片，剪切到新的n个文件夹，并按数字顺序重命名
这n个文件夹中可能含有多重子目录
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
path='C:/Users/NExT/Desktop/Change_cleaned'
newpath = 'C:/Users/NExT/Desktop/Change_test'


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
for file in dir: 
     number=1
     subfile = path+'/'+file
     newsubpath = newpath+'/'+file
     if not os.path.exists(newsubpath):
         os.mkdir(newsubpath)
     #print(subfile)         
#     print(i)
#     i=i+1 
     num_files_rec = 0     
     for root,dirs,files in os.walk(subfile):   
         for each in files:    
             num_files_rec += 1
#     print(num_files_rec) 
     selectrate=0.2
     picknum=int(num_files_rec*selectrate) #统计子目录下的总文件个数,计算训练集数量
     filelist = list_all_files(subfile) #调用函数获得总文件目录
#     print(filelist)
     nlist = list(range(0,len(filelist)))
     numlist=random.sample(nlist, picknum)
#     print(numlist)
     rest = [x for x in nlist if x not in numlist]
#     print(rest)
     for j in range(0,picknum):
         temppath=filelist[numlist[j]]
         if temppath[-4]=='.':
             if os.path.isfile(temppath):
                  shutil.move(temppath,newsubpath+'/'+str(number)+temppath[-4:])
                  number=number+1
             else:
                  while not os.path.isfile(temppath):
                      onenewnum=random.choice(rest)
                      rest.remove(onenewnum)
                      temppath=filelist[numlist[onenewnum]]
                  shutil.move(temppath,newsubpath+'/'+str(number)+temppath[-4:])
                  number=number+1 
         elif temppath[-5]=='.':
             if os.path.isfile(temppath):
                  shutil.move(temppath,newsubpath+'/'+str(number)+temppath[-5:])
                  number=number+1
             else:
                  while not os.path.isfile(temppath):
                      onenewnum=random.choice(rest)
                      rest.remove(onenewnum)
                      temppath=filelist[numlist[onenewnum]]
                  shutil.move(temppath,newsubpath+'/'+str(number)+temppath[-5:])
                  number=number+1 
             
         

         