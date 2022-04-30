import numpy as np
import glob
import json
import os
from tqdm import tqdm

def read_txt(path_file):
    try:
        data = np.loadtxt(path_file,delimiter=",")
    except:
        data = np.loadtxt(path_file)
    return data 

def split_name_file(file_data):
    class_name,ins_id = file_data.split("/")[-1].split("_")
    return class_name,ins_id[:-4]

def create_array_class_ins_id(data_row_dim,class_name,ins_id):
    class_ins_id = np.zeros((data_row_dim,2))
    class_ins_id[:,0].fill(id_class[class_name.lower()])
    class_ins_id[:,1].fill(int(ins_id))
    return class_ins_id

def read_data_class_ins_id(file_data):
    data = read_txt(file_data)[:,:6]
    class_name,ins_id= split_name_file(file_data)
    data = np.hstack((data,\
        create_array_class_ins_id(data.shape[0],class_name,ins_id)))
    return data

id_class = {'building':0, 'vegetation':1, 'ground':2,'undefined':3}
folder_dataset_clean = "Dataset_clean"

if __name__ == "__main__":
    folders_data = glob.glob(f"{folder_dataset_clean}/**")[3:]
    for i,_ in enumerate(folders_data):
        print(folders_data[i])
        files_data = glob.glob(f"{folders_data[i]}/**.txt")
        for idx,_ in enumerate(files_data):
            print((files_data[idx]))
            if idx ==0 :
                data =read_data_class_ins_id(files_data[idx])
            else :
                data = np.vstack((data,\
                    read_data_class_ins_id(files_data[idx])))
        data = data[np.lexsort((data[:,0],data[:,1]))]
        txt_name = files_data[idx].split("/")[1]
        np.savetxt(
            f"{txt_name}.txt",
            data,
            fmt="%1.9f %1.9f %1.9f %d %d %d %d %d"
            )