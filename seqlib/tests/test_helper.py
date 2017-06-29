'''
Testing helper.py
'''

import pytest
from seqlib.helper import check_md5


def test_check_md5():
    '''
    Testing check_md5()
    '''
    test_f = pytest.helpers.data_path('test.bam')
    assert check_md5(test_f, '2d055eb6c7ad9779c3e875b121376e90')
