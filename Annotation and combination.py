import numpy as np
import glob
import json
import os
import tqdm

def save_meta_data(file_name,dict_file):
    with open(f'{file_name}.json', 'w') as fp:
        json.dump(dict_file, fp,  indent=4)
        
def read_meta_data (path):
    with open(path, 'r') as j:
        contents = json.loads(j.read())
        return contents

folder_dataset_clean = "Dataset_clean"
folders_data = os.listdir(folder_dataset_clean)
folder_dataset_buff  = "Dataset_buff_clean"
if __name__ == "__main__":
    for folder_data in folders_data :
        dict_jumlah_data = {}
        os.makedirs(f"{folder_dataset_buff}/{folder_data}",exist_ok=True)
        path_folder_data = os.path.join(folder_dataset_clean,folder_data)
        list_datas = os.listdir(path_folder_data)
        print(f"Proses Folder {folder_data}")
        for data_name_file in tqdm.tqdm(list_datas):
            path_data = os.path.join(folder_dataset_clean,folder_data,data_name_file)
            with open(path_data,"r") as f:
                data =f.readlines()
            f.close()
            dict_jumlah_data[data_name_file[:-4]] = data[0].strip()
            data =data[1:]
            with open(os.path.join(folder_dataset_buff,folder_data,data_name_file),"w+") as f:
                for i in data:
                    f.writelines(i)
            f.close()
        save_meta_data(os.path.join(folder_dataset_buff,folder_data,f"{folder_data}.json"),dict_jumlah_data)
