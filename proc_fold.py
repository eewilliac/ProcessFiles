import configparser
import sys
import os
import uuid
import shutil
import pathlib
import zipfile


files_to_process = []

def config_parser_test():
    config = configparser.ConfigParser()
    config.read('app.config')
    source_value = config.get('FileSection', 'source')     
    source_value = "source_value:{}".format(source_value)
    print(source_value)

def get_params():
    config = configparser.ConfigParser()
    config.read('app.config')
    source_value = config.get('FileSection', 'source')     
    file_type = config.get("FileSection","type")
    destination_value = config.get("FileSection",'destination')
    return file_type, source_value, destination_value


#verify if the destination volume exists.
def destination_volume_exists():
    config = configparser.ConfigParser()
    config.read('app.config')
    destination_volume_value = config.get("FileSection","destination")
    return os.path.exists(destination_volume_value)

def files_exist_for_processing(aFolder,file_type):
    directory = os.fsencode(aFolder)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(file_type):
            return True
    return False
    
def source_volume_and_files_exists():
    config = configparser.ConfigParser()
    config.read('app.config')
    source_volume_value = config.get("FileSection","source")
    file_type = config.get("FileSection","type")
    volume_exists = os.path.exists(source_volume_value)
    files_exist = files_exist_for_processing(source_volume_value,file_type)
    if volume_exists and files_exist:
        return True
    else:
        return False

#if source files and destination volume exist.
#we start collecting the names of the files.
def collect_file_fqpath(source_folder,file_type):
    for current_file in os.listdir(source_folder):
        if current_file.endswith(file_type):
            files_to_process.append(os.path.join(source_folder, current_file))            
    return files_to_process

def create_dest_dir(dir_name,destination_dir):
    directory = dir_name
    new_dir = os.path.join(destination_dir,directory)
    os.mkdir(new_dir)
    return new_dir

def move_all_files(list_of_files,dest_dir):
    print("start compression")
    new_zip_file_name = dest_dir+'zip'
    with zipfile.ZipFile(new_zip_file_name,mode='w') as zf:
        for curr_file in list_of_files:
            disp_string = "processing:{}".format(str(curr_file))
            print(disp_string,end='\r')
            zf.write(curr_file)
    zfile = pathlib.Path(new_zip_file_name)
    zfile.rename(zfile.with_suffix('.sql'))
    print("last cleanup")
    for curr_file in list_of_files:
        os.remove(curr_file)        


def main():
    if (source_volume_and_files_exists()):
        print("start")
        file_type,source_value,destination_value = get_params()
        list_of_files = collect_file_fqpath(source_folder=source_value,file_type=file_type)
        new_folder_name = "empty_"+uuid.uuid4().hex
        new_folder = create_dest_dir(dir_name=new_folder_name,destination_dir=destination_value)
        move_all_files(list_of_files,new_folder)
        print("done!")
    else:
        print("we have a problem!")
        

if __name__ == "__main__":
    main()