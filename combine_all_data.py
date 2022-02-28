import numpy as np
import h5py
from glob import glob
from data_understanding import save_meta_data,read_meta_data
from tqdm import tqdm

id_class = {'building':0, 'vegetation':1, 'ground':2}
metadata_json = glob("T**.json")

def append_xyz_rgb_class_ins_id(new_data,old_data):
    xyz = np.append(old_data[0],new_data[0],axis=0)
    rgb = np.append(old_data[1],new_data[1],axis=0)
    class_id = np.append(old_data[2],new_data[2])
    ins_id = np.append(old_data[3],new_data[3])
    return xyz,rgb,class_id,ins_id

def read_xyz_rgb_class_ins_id(class_,inst_ids_keys,index,metadata,path,new_data=None):
    if class_ == "building":
        xyz_rgb = np.load(metadata[class_][inst_ids_keys[index]][path],allow_pickle=True)
    else: 
        xyz_rgb = np.loadtxt(f"Dataset/{metadata[class_][inst_ids_keys[index]][path]}")
    vec_size = xyz_rgb.shape[0]
    ins_id = np.zeros(vec_size,dtype="uint16")
    ins_id.fill(int(inst_ids_keys[index])) 
    class_id= np.zeros(vec_size,dtype="uint16")
    class_id.fill(int(id_class[class_]))
    if new_data:
        return append_xyz_rgb_class_ins_id(new_data,[xyz_rgb[:,:3],xyz_rgb[:,3:6].astype("int"),class_id,ins_id])
    return [xyz_rgb[:,:3],xyz_rgb[:,3:6].astype("int"),class_id,ins_id]

def data_combine_all_class_to_area(building,vegetation,ground,axis=0):
    buff = np.append(building,vegetation,axis=axis)
    buff = np.append(buff,ground,axis=axis)
    # buff = np.append(buff,undefined,axis=axis)
    return buff
def combine_all_class_to_area(building,vegetation,ground):
    return [data_combine_all_class_to_area(building[0],vegetation[0],ground[0],axis=0),
        data_combine_all_class_to_area(building[1],vegetation[1],ground[1],axis=0),
        data_combine_all_class_to_area(building[2],vegetation[2],ground[2],axis=None),
        data_combine_all_class_to_area(building[3],vegetation[3],ground[3],axis=None)]

if __name__ == "__main__":
    for area in tqdm(metadata_json):
        metadata = read_meta_data(area)
        for class_ in metadata.keys():
            # print(class_)
            if class_ == "building" :
                # continue
                inst_ids_keys = list(metadata[class_].keys())
                buff_data =  read_xyz_rgb_class_ins_id(class_="building",path="path_all_data",inst_ids_keys=inst_ids_keys,index=0,metadata=metadata)
                for idx in range(1,len(inst_ids_keys)):
                    buff_data = read_xyz_rgb_class_ins_id(class_="building",path="path_all_data",inst_ids_keys=inst_ids_keys,index=idx,metadata=metadata,new_data=buff_data)
                building=buff_data
            if class_ == "vegetation" :
                # continue
                inst_ids_keys = list(metadata[class_].keys())
                buff_data =  read_xyz_rgb_class_ins_id(class_="vegetation",path="path",inst_ids_keys=inst_ids_keys,index=0,metadata=metadata)
                try:
                    for idx in range(1,len(inst_ids_keys)):
                        buff_data = read_xyz_rgb_class_ins_id(class_="vegetation",path="path",inst_ids_keys=inst_ids_keys,index=idx,metadata=metadata,new_data=buff_data)
                except:
                    pass
                vegetation=buff_data
            if class_ == "ground" :
                # continue
                inst_ids_keys = list(metadata[class_].keys())
                buff_data =  read_xyz_rgb_class_ins_id(class_="ground",path="path",inst_ids_keys=inst_ids_keys,index=0,metadata=metadata)
                try:
                    for idx in range(1,len(inst_ids_keys)):
                        buff_data = read_xyz_rgb_class_ins_id(class_="ground",path="path",inst_ids_keys=inst_ids_keys,index=idx,metadata=metadata,new_data=buff_data)
                except:
                    pass
                ground=buff_data
            # if class_ == "undefined":
            #     # continue
            #     inst_ids_keys = list(metadata[class_].keys())
            #     buff_data =  read_xyz_rgb_class_ins_id(class_="undefined",path="path",inst_ids_keys=inst_ids_keys,index=0,metadata=metadata)
            #     try:
            #         for idx in range(1,len(inst_ids_keys)):
            #             buff_data = read_xyz_rgb_class_ins_id(class_="undefined",path="path",inst_ids_keys=inst_ids_keys,index=idx,metadata=metadata,new_data=buff_data)
            #     except:
            #         pass
            #     undefined=buff_data
        xyz,rgb,class_id,ins_id= combine_all_class_to_area(building,vegetation,ground)
        test_all = np.append(xyz,rgb, axis=1)
        np.savetxt(f"{area[:-5]}.txt",test_all,fmt="%1.9f %1.9f %1.9f %d %d %d")
        f = h5py.File(f"{area[:-5]}.h5", 'w')
        f.create_dataset('xyz', data=xyz)
        f.create_dataset('colour', data=rgb)
        f.create_dataset('class_id', data=class_id)
        f.create_dataset('ins_id', data=ins_id)
        f.close()

