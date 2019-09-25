'''
从n个文件夹中，分别随机抽取m图片，剪切到新的n个文件夹，并按数字顺序重命名
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
 

#给定操作目录
path='C:/Users/NExT/Desktop/food-101/images'
newpath = 'C:/Users/NExT/Desktop/fod101_test'


#建立新文件夹
os.mkdir(newpath)
dirs = os.listdir(path)
j = 0


#调用函数实现文件移动
for file in dirs: 
    j=j+1
    tarDir =newpath + '/'+ str(j)
    os.mkdir(tarDir)
    tarDir =tarDir + '/'
    fileDir = path +'/'+file+'/'
    copyFile(fileDir,tarDir)