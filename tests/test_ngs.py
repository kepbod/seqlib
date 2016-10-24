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
    junc = fetch_juncfile('data/junc.bam')
    check_file(junc, 'data/junc_unstranded.bed')
    os.remove(junc)
    junc = fetch_juncfile('data/junc.bam', stranded=True)
    check_file(junc, 'data/junc_stranded.bed')
    os.remove(junc)
