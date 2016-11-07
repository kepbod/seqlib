'''
Some help functions and classes
'''

import sys
import os

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


def check_option(n, msg):
    '''
    Check the number of options.
    '''
    if len(sys.argv) != n:
        sys.exit(msg)


def run_command(command, message):
    return_code = os.system(command) >> 8
    if return_code:
        sys.exit(message)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
