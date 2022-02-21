# from msilib.schema import Directory
import os
import glob
import argparse
import json
import re

parser = argparse.ArgumentParser(description='Used for rename folder.')
parser.add_argument('-file',action="store",
                    type=str,
                    default="T_315500_234500_NW",
                    help='Directory of dst folder')


args = parser.parse_args()
foldername = args.file
meta_log = foldername+".txt"

def save_meta_data(file_name,dict_file):
    with open(f'{file_name}.json', 'w') as fp:
        json.dump(dict_file, fp,  indent=4)
        
def read_meta_data (path):
    with open(path, 'r') as j:
        contents = json.loads(j.read())
        return contents

def main(foldername,meta_log):
    os.makedirs(f"{foldername}",exist_ok=True)
    
    with open(meta_log,'r') as f:
        raw_log = f.readlines()

    for i,d in enumerate(raw_log):
        if re.search("SUBSAMPLING",d):
            index = i+3
            break
    dict_file ={}


    for i in range(index,len(raw_log)-1,4):
        buff_name = raw_log[i][10:].strip().split("(")[-1][:-1] 
        buff_points_agg = int(raw_log[i+1][10:].strip().split(" ")[1])
        old_path = raw_log[i+3][10:].strip().split("'")[1]
        new_path = f"{foldername}/{buff_name}.txt"
        dict_file[buff_name] ={"path":new_path,"jumlah_point":buff_points_agg}
        os.rename(old_path, new_path)

    save_meta_data(f"{foldername}/meta_data",dict_file)

if __name__ == "__main__":
    print(foldername)
    main(foldername,meta_log)