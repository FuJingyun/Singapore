import pandas as pd

#----------------------------pre-processing csv & convert into pandas df data structure-----------------------------#

#accepts absolute path of csv file; returns a pandas df which contains info from processed csv file
def pre_process_csv(abs_path_csv):
    food_list_csv = abs_path_csv
    food_df = pd.read_csv(food_list_csv)
    #get all column names
    col_names = list(food_df.columns.values)
    name_lst = []
#drop unwanted columns, you may customise this for loop to suit your needs
    for name in col_names:
        if name != 'ITEM_NO' and name != 'DIETLENS_CHOSEN_NAME' and name !='FOOD_ALT_NAMES':
            food_df.drop([name], axis=1, inplace=True)
    food_df = food_df[food_df.FOOD_ALT_NAMES.notnull()]
    return food_df




