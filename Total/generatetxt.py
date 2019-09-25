'''
将给定文件夹下的所有文件名称记录在txt文件中
Author ： Fu Jingyun
'''
import os


#给定excel表格路径
paths= "C:/Users/NExT/Desktop/simpleconv3/data/val/0"


#读取目录以及排序
f=open('val_shuffle.txt', 'w')
filenames=os.listdir(paths)
filenames.sort()


#写文件操作
for filename in filenames:
    out_path="./data/val/0/" + filename+" 0"
    f.write(out_path+'\n')
f.close()