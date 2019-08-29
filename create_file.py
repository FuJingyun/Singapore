'''
根据excel表格的指定一列，生成对应那一列中各单元格名称的子文件夹
Author ： Fu Jingyun
'''
import  xlrd
import os
 
workbook = xlrd.open_workbook(r'C:/Users/NExT/Desktop/Cat.xlsx')
print(workbook.sheet_names())            #查看所有sheet名称
sheet1 = workbook.sheet_by_index(0)      #用索引取第1个sheet
 
#cell_00 = sheet1.cell_value(0,0)    #读取第1行第1列数据
#row0 = sheet1.row_values(0)         #读取第1行数据
nrows = sheet1.nrows                #读取行数

newpath='C:/Users/NExT/Desktop/VAL'

if not os.path.exists(newpath):
    os.mkdir(newpath)


for i in range(nrows):         #循环逐行打印
    cell = sheet1.cell_value(i,0)
    file_name = newpath +'/'+ cell
    os.mkdir(file_name)
