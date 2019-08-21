import pandas as pd
import os
from preprocess_csv_Google import pre_process_csv



#-----------------------------------------Partition food_df---------------------------------------------------------------#
#2 inputs: 1. A dataframe 
#          2. Number of segments to partition the given dataframe
#  result: store csv files in directory when you run preprocess_csv.py file

def partition(food_df, num_subsets):
    curr_folder = os.path.dirname(os.path.abspath(__file__))
    has_remainder = False
    remainder = len(food_df) % num_subsets
    #step is equal to the number of elements in each subset without remainder
    step = len(food_df) // num_subsets 
    if  remainder != 0:
        has_remainer = True
        #get the the last n rows of food_df, where n == remainer
        last_n_rows = food_df.tail(remainder)
        #get rid of last n rows which are extracted
        food_df = food_df[:-len(last_n_rows)]

    for i in range(0, len(food_df), step):
        file_name = os.path.join(curr_folder,'subset_'+str(i) +'.csv') 
        #the number of rows to extract in each iteration is: i + step
        rows = food_df[i: i+step]
        #if there is any remainder, append the remainder rows to the 1st subset
        if has_remainder == True and i == 0:
            final = pd.concat([rows, last_n_rows])
            final.to_csv(file_name)
        rows.to_csv(file_name)

if __name__ == "__main__":
    #get pre-process food_df, change csv variable assignment as needed
    csv = 'C:\\Users\\NUS\\Desktop\\image_crawling\\food_list.csv'
    food_df = pre_process_csv(csv)
    print(len(food_df))
    num_partition = 3
    partition(food_df, num_partition)

    