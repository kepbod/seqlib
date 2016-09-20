import sys
import os.path
import shutil


def check_dir(dir):
    '''
    Check directory
    '''
    if os.path.isdir(dir):
        dir_path = os.path.abspath(dir)
    else:
        sys.exit('Error: your directory %s is wrong!' % dir)
    return dir_path


def create_dir(dir):
    '''
    Check and create directory
    '''
    if os.path.isdir(dir):
        if os.listdir(dir):
            print('Warning: the directory %s is not empty!' % dir)
        shutil.rmtree(dir)
    os.mkdir(dir)
