'''
随机从给定目录抽取m张或给定比例的图片移动到新个文件夹，并按数字顺序重命名
用于深度学习过程中从给定目录下抽取一定数量图片制作训练集和验证集、测试集。
Author ： Fu Jingyun
'''
import os
import random
import shutil
 
 
def copyFile(fileDir,tarDir):
    pathDir = os.listdir(fileDir)
    filenumber=len(pathDir)
    rate=0.2                        #自定义抽取图片的比例
    picknumber=int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
    sample = random.sample(pathDir, picknumber)
    for name in sample:
        shutil.move(fileDir + '/'+name, tarDir +'/'+ name)
 
 
#给定操作路径
path='C:/Users/NExT/Desktop/UEC_test_total'
newpath = 'C:/Users/NExT/Desktop/UEC_select'
os.mkdir(newpath)
copyFile(path,newpath)