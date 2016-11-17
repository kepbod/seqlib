'''
Testing parse.py
'''

import os
import os.path
from pytest.helper import data_path, check_file
from seqlib.ngs import fetch_juncfile, bam_to_bedgraph


def test_fetch_juncfile():
    '''
    Testing fetch_juncfile()
    '''
    junc = fetch_juncfile(data_path('junc.bam'))
    check_file(junc, data_path('junc_unstranded.bed'))
    os.remove(junc)
    junc = fetch_juncfile(data_path('junc.bam'), stranded=True)
    check_file(junc, data_path('junc_stranded.bed'))
    os.remove(junc)
    junc = fetch_juncfile(data_path('junc.bam'), min=5)
    check_file(junc, data_path('junc_min.bed'))
    os.remove(junc)
    junc = fetch_juncfile(data_path('junc.bam'), uniq=True)
    check_file(junc, data_path('junc_uniq.bed'))
    os.remove(junc)


def test_bam_to_bedgraph(data_folder):
    '''
    Testing bam_to_bedgraph()
    '''
    bg = bam_to_bedgraph(data_path('test.bam'))
    check_file(bg, data_path('unstranded.bg'))
    os.remove(bg)
    bg = bam_to_bedgraph(data_path('test.bam'), scale=True)
    check_file(bg, data_path('unstranded_scale.bg'))
    os.remove(bg)
    pbg, mbg = bam_to_bedgraph(data_path('test.bam'), stranded=True)
    check_file(pbg, data_path('plusS.bg'))
    os.remove(pbg)
    check_file(mbg, data_path('minusS.bg'))
    os.remove(mbg)
