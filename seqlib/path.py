'''
Path relevant functions and classes
'''

import sys
import os.path
import shutil
import contextlib

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'

__all__ = ['which', 'smart_write', 'smart_open', 'check_dir', 'create_dir']

def which(program):
    '''
    Check the path of external programs, and source codes are modified from
    https://github.com/infphilo/tophat/blob/master/src/tophat.py.
    '''
    def is_executable(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        progpath = os.path.join(path, program)
        if is_executable(progpath):
            return progpath
    return None


@contextlib.contextmanager
def smart_write(filename=None):
    '''
    Smart open output file.
    '''
    if filename and filename != '-' and filename != 'stdout':
        fn = open(filename, 'w')
    else:
        fn = sys.stdout
    try:
        yield fn
    finally:
        if fn is not sys.stdout:
            fn.close()


@contextlib.contextmanager
def smart_open(filename=None):
    '''
    Smart open input file.
    '''
    if filename and filename != '-' and filename != 'stdin':
        fn = open(filename, 'r')
    else:
        fn = sys.stdin
    try:
        yield fn
    finally:
        if fn is not sys.stdin:
            fn.close()


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
    return os.path.abspath(dir)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
