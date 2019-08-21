'''
将path路径下的所有子路径中的图片文件复制到新文件夹new_path，同时按数字顺序重命名被复制的文件
Author ： Fu Jingyun
'''
import os  
import shutil 
 

path = 'C:/Users/NExT/Desktop/UEC_test'  #原文件路径
new_path = 'C:/Users/NExT/Desktop/UEC_test_total'  #目标路径
os.mkdir(new_path)  #创建目标路径
j=1  

for root, dirs, files in os.walk(path):
    for i in range(len(files)):
#        if (files[i][-3:] == 'jpg') or (files[i][-3:] == 'png') or (files[i][-3:] == 'JPG'):
        if(files[i][-4] == '.' and files[i][-3] != 't'):  #判断当前文件是否为需要的文件
            file_path = root+'/'+files[i]  
            new_file_path = new_path+ '/'+ str(j)+'.'+files[i][-3:]  #重命名目标图片
            shutil.copy(file_path,new_file_path)  #复制至新路径
            j+=1


            
            
            
            
            
