'''
Use COCO API to implement select given type of pictures from COCO dataset.
Following code is based on the guidence of COCO API with some modification according to practical need
使用COCO API 实现从COCO数据集中筛选目标种类的图片，本代码基于COCO API 例程，根据实际实际使用需求改写
'''


#%matplotlib inline
from pycocotools.coco import COCO
import skimage.io as io
import pylab
import os  
import shutil 
#from glob import glob
#import matplotlib.pyplot as plt
#import numpy as np


pylab.rcParams['figure.figsize'] = (10.0, 8.0) 
dataDir='C:/Users/NExT/Desktop/COCO'
dataType='train2014'
annFile='%s/annotations/instances_%s.json'%(dataDir,dataType)  #给定json文件路径


# initialize COCO api for instance annotations 初始化
coco=COCO(annFile)


## display COCO categories and supercategories
#cats = coco.loadCats(coco.getCatIds())
#nms=[cat['name'] for cat in cats]
#print 'COCO categories: \n\n',' '.join(nms)
#nms = set([cat['supercategory'] for cat in cats])
#print 'COCO supercategories: \n', ' '.join(nms)


# get all images containing given categories, select one at random
#筛选图像内容种类符合要求的内容ID
catIds = coco.getCatIds(catNms=['plate']);
catIds=list(set(catIds))


#maybename=['bottle','plate','wine glass','cup','fork','knife','spoon',bowl]
#foodname=['apple', 'banana',  'hot dog', 'orange', 'sandwich','broccoli','carrot','pizza','donut','cake']
#
#for j in range(len(foodname)):
#    newids=coco.getCatIds(catNms=foodname[j]);
#    print(newids)
#    catIds.extend(newids)


#根据内容ID筛选出符合要求的图片ID
imgIds = coco.getImgIds(catIds=catIds );
imgs = coco.loadImgs(imgIds)
print(imgs[2]['file_name'])


#给定路径
path = 'C:/Users/NExT/Desktop/COCO/train2014'
new_path = 'C:/Users/NExT/Desktop/new'
 

#文件操作，移动目标文件至指定文件夹
for i in range(len(imgIds)):
    file_path = path+'/'+imgs[i]['file_name']
    new_file_path = new_path+ '/'+ imgs[i]['file_name']
    if os.path.exists(file_path):
        shutil.copy(file_path,new_file_path)
        os.remove(file_path)
    




#for root, dirs, files in os.walk(path):
#    for i in range(len(files)):
#        if (files[i][-3:] == 'jpg') or (files[i][-3:] == 'png') or (files[i][-3:] == 'JPG'):
#            file_path = root+'/'+files[i]  
#            new_file_path = new_path+ '/'+ str(j)+'.'+files[i][-3:]
#            shutil.copy(file_path,new_file_path)
#            j+=1

