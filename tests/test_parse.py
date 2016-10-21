'''
Testing parse.py
'''

import os
from tests.help_test import check_file
from seqlib.ngs import fetch_juncfile


def test_fetch_juncfile():
    '''
    Testing fetch_juncfile()
    '''
    fetch_juncfile('data/junc.bam')
    check_file('data/junc_junc.bed', 'data/junc_unstranded.bed')
    os.remove('data/junc_junc.bed')
    fetch_juncfile('data/junc.bam', stranded=True)
    check_file('data/junc_junc.bed', 'data/junc_stranded.bed')
    os.remove('data/junc_junc.bed')
