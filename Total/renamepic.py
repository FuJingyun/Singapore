'''
实现将给定目录下的所有文件进行数字顺序重命名，同时保持扩展名不变
Author ： Fu Jingyun
'''
import os

path_name='C:/Users/NExT/Desktop/add/59_Banana'  #path_name :表示你需要批量改的文件夹

i=1 #从几开始对文件夹内文件重命名


for item in os.listdir(path_name):  #进入到文件夹内，对每个文件进行循环遍历
    os.rename(os.path.join(path_name,item),os.path.join(path_name,(str(i)+'.jpeg')))  #os.path.join(path_name,item)表示找到每个文件的绝对路径并进行拼接操作
    i+=1