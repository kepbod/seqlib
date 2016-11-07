'''
Testing parse.py
'''

import os
from tests.help_test import check_file
from seqlib.ngs import fetch_juncfile, bam_to_bedgraph


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
    junc = fetch_juncfile('data/junc.bam', min=5)
    check_file(junc, 'data/junc_min.bed')
    os.remove(junc)


def test_bam_to_bedgraph():
    '''
    Testing bam_to_bedgraph()
    '''
    bg = bam_to_bedgraph('data/test.bam')
    check_file(bg, 'data/unstranded.bg')
    os.remove(bg)
    bg = bam_to_bedgraph('data/test.bam', scale=True)
    check_file(bg, 'data/unstranded_scale.bg')
    os.remove(bg)
    pbg, mbg = bam_to_bedgraph('data/test.bam', stranded=True)
    check_file(pbg, 'data/plusS.bg')
    os.remove(pbg)
    check_file(mbg, 'data/minusS.bg')
    os.remove(mbg)
