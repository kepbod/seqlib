import os
import os.path
import sys
import contextlib


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
    if filename:
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
