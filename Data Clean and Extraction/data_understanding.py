import json



def save_meta_data(file_name,dict_file):
    with open(f'{file_name}.json', 'w') as fp:
        json.dump(dict_file, fp,  indent=4)
        
def read_meta_data (path):
    with open(path, 'r') as j:
        contents = json.loads(j.read())
        return contents