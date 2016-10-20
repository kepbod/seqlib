'''
Set up some stuff for unit testing
'''

import os


def setup_package():
    print('#tests.__init__: Start testing')
    os.chdir('tests')


def teardown_package():
    print('#tests.__init__: End testing')
