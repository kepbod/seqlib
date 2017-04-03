'''
Some help functions and classes
'''

import sys
import os
import requests
import hashlib

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['check_option', 'run_command', 'download_file', 'check_md5']


def check_option(n, msg):
    '''
    Check the number of options.
    '''
    if len(sys.argv) != n:
        sys.exit(msg)


def run_command(command, message):
    '''
    Run command.
    '''
    return_code = os.system(command) >> 8
    if return_code:
        sys.exit(message)


def download_file(local_file, url, chunk_size=1024):
    '''
    Download file.
    http://stackoverflow.com/a/16696317
    '''
    r = requests.get(url, stream=True)
    with open(local_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)


def check_md5(local_file, md5):
    '''
    Check MD5.
    '''
    return hashlib.md5(open(local_file, 'rb').read()).hexdigest() == md5


if __name__ == '__main__':
    import doctest
    doctest.testmod()
