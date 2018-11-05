import numpy as np
import pandas as pd
from multiprocessing import Pool

def get_dbSNP_version(dataframe):
    for column in list(dataframe):
        if "rs_dbSNP" in column:
            return column[-3:]
            
def get_hg_version(dataframe):
    bigger_value = "0"
    for column in list(dataframe):
        if(("hg" in column) and (column[2:4] > bigger_value)):
            bigger_value = column[2:4]
    return bigger_value

def read_csv(filename):
    return pd.read_csv(filename, sep='\t')

def get_column_information_rate(dataframe):
    info_dict = {}
    for column_name in list(dataframe):
        info_dict[column_name] = 0

    for row_index,row in dataframe.iterrows():
        for column_index in range(len(row.index)):
            value = dataframe.loc[row_index].values[column_index]
            if type(value) == str:
                if((value == '.') or ("./" in value)):             
                    info_dict[row.index[column_index]] += 1
                    
    for i in info_dict:
        info_dict[i] = [(1 - info_dict[i]/dataframe.shape[0]) * 100]
    
    return pd.DataFrame.from_dict(info_dict)

def parallelize_information_rate(df, num_partitions, num_cores):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(get_column_information_rate, df_split))
    pool.close()
    pool.join()
    return df.mean()

def parallelize_read_csv(file_names, num_cores):
    pool = Pool(num_cores)
    df = pd.concat(pool.map(read_csv, file_names))
    pool.close()
    pool.join()
    return df