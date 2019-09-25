'''
实现根据xml文件将标注框内的图片提取，并且生成上下左右移动设定百分比后的图
'''
import xml.etree.ElementTree as ET
import os
import random
import shutil
import numpy as np
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import scipy.misc



def load_pascal_annotation(filename):
        """
        Load image and bounding boxes info from XML file in the PASCAL VOC
        format.
        """
        #filename = os.path.join(self._data_path, 'Annotations', index + '.xml')
        tree = ET.parse(filename)
        objs = tree.findall('object')
        # if not self.config['use_diff']:
        #     # Exclude the samples labeled as difficult
        #     non_diff_objs = [
        #         obj for obj in objs if int(obj.find('difficult').text) == 0]
        #     # if len(non_diff_objs) != len(objs):
        #     #     print 'Removed {} difficult objects'.format(
        #     #         len(objs) - len(non_diff_objs))
        #     objs = non_diff_objs
        # exlcude unused cls

        ori_num_objs = len(objs)
        num_objs = 0
        for obj in objs:
            try:               
                num_objs += 1
            except:
                continue
        # assert num_objs == 0


        num_objs = num_objs  # len(objs)

        boxes = np.zeros((num_objs, 4), dtype=np.uint16)
        gt_classes = np.zeros((num_objs), dtype=np.int32)       
        # "Seg" area for pascal is just the box area
        seg_areas = np.zeros((num_objs), dtype=np.float32)
        ishards = np.zeros((num_objs), dtype=np.int32)
        cls_list = []
        # Load object bounding boxes into a data frame.
        ix = 0
        for obj in objs:
            bbox = obj.find('bndbox')
            # Make pixel indexes 0-based
            # the range of food label is (0, width) which may cause by bugs in labelimg 1.4
            x1 = max(0.0, float(bbox.find('xmin').text) - 1)
            y1 = max(0.0, float(bbox.find('ymin').text) - 1)
            x2 = float(bbox.find('xmax').text) - 1
            y2 = float(bbox.find('ymax').text) - 1

            diffc = obj.find('difficult')
            difficult = 0 if diffc == None else int(diffc.text)
            cls = obj.find('name').text.lower().strip().strip("<").strip(">")
            cls = cls.replace('/', '')
            cls_list.append(cls)
            boxes[ix, :] = [x1, y1, x2, y2]
            
            ix += 1 
        return boxes, cls_list


picpath = 'C:/Users/NExT/Desktop/Lixi'
newpath = 'C:/Users/NExT/Desktop/Lixi_classes'

if not os.path.exists(newpath):
    os.mkdir(newpath)
dir = os.listdir(picpath)

pic_num = 1

if __name__ == '__main__':
    # foodName:
    # dir_dict = {}
    for file in dir: 
        if file[-3:]=='xml':
            xml_path = picpath+'/'+file
            str1 = file[:-3]
            img_path = picpath+'/'+str1 + 'jpg'
            boxes, cls_list = load_pascal_annotation(xml_path)            
            im = mpimg.imread(img_path) 
            for i in range(len(boxes)):
                #crop
                box = boxes[i]
                x1= box[0]
                x2=box[2]
                y1=box[1]
                y2=box[3]
                try:
                    crop = im[y1:y2, x1:x2]
                    #cls naem = 
                    cls_name = cls_list[i]
                    save_folder = newpath+'/'+cls_name
                    if not os.path.exists(save_folder):
                        os.mkdir(save_folder)
                    scipy.misc.imsave(save_folder+'/'+str(pic_num)+'.jpg', crop)                
                    pic_num+=1
                except:
                    print(img_path)

    
    
    
    
     
    
    
    
        
    
    
    
    