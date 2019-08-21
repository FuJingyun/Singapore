'''
Use packaged library to get pictures from Google, the details of pictures can be
given to the programme by editing the csv file
'''

from icrawler.builtin import GoogleImageCrawler
import os
import datetime
from preprocess_csv_Google import pre_process_csv
import pandas as pd
import pathlib

#----------------------------------------------Image Retrieval------------------------------------------------------#   
    #2 inputs: 1.a directory to store all images which are crawled
    #          2.a food list dataframe
    
def img_retrieval(food_df):  
    date = datetime.datetime.now()
    format_date = date.strftime('%d-%B-%Y')
    lst = format_date.split('-')
    month = lst[1][0:3]
    final_date = lst[0] + month + lst[2]
    #get current path of preprocess_csv.py and then get its folder name
    curr_path = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.join(curr_path,'Image_Crawling')
    #all images will be stored in path
    path = os.path.join(new_path, 'Images')
    #check if such path exists
    pathlib.Path(path).mkdir(parents=True,exist_ok=True)
    for i,row in food_df.iterrows():
        #get ITEM_NO
        item_no = row['ITEM_NO']
        #get DIETLENS_CHOSEN_NAME
        diet_name = row['DIETLENS_CHOSEN_NAME']
        #get FOOD_ALT_NAMES, all variations of a food name is now stored in a list
        food_alt_names = row['FOOD_ALT_NAMES'].split('|')
        #create folder to store images related to DIETLENS_CHOSEN_NAME & ITEM_NO
        storage_folder = os.path.join(path, str(item_no) + '_' + diet_name)
        if os.path.isdir(storage_folder) == False:
            os.mkdir(storage_folder)


        for f_name in food_alt_names:
            f_name = f_name.strip()
            #for each alternative name, create its own folder to store images attached to the name
            sub_folder = os.path.join(storage_folder, f_name)
            if os.path.isdir(sub_folder) == False:
                os.mkdir(sub_folder)
            os.chdir(sub_folder)
            #create a text file to record the following:
            statement = f_name + "_google_"+final_date
            with open('record.txt', 'w+', encoding='utf-8') as f:
                f.write(statement)
            #initialise crawler
            g_img_crawler = GoogleImageCrawler(feeder_threads=1,parser_threads=2,downloader_threads=4,storage={'root_dir':sub_folder})
            g_img_crawler.crawl(f_name,max_num=800)

if __name__ == "__main__":
    csv = './to_crawl.csv'
    food_df = pd.read_csv(csv)
    img_retrieval(food_df)