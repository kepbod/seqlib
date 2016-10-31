'''
Some help functions and classes
'''

import sys

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


def check_option(n, msg):
    '''
    Check the number of options.
    '''
    if len(sys.argv) != n:
        sys.exit(msg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
