'''
Testing parse.py
'''

import os
import os.path
from tests.utils import check_file
from seqlib.ngs import fetch_juncfile, bam_to_bedgraph


def test_fetch_juncfile(data_folder):
    '''
    Testing fetch_juncfile()
    '''
    junc = fetch_juncfile(os.path.join(data_folder, 'data/junc.bam'))
    check_file(junc, os.path.join(data_folder, 'data/junc_unstranded.bed'))
    os.remove(junc)
    junc = fetch_juncfile(os.path.join(data_folder, 'data/junc.bam'),
                          stranded=True)
    check_file(junc, os.path.join(data_folder, 'data/junc_stranded.bed'))
    os.remove(junc)
    junc = fetch_juncfile(os.path.join(data_folder, 'data/junc.bam'), min=5)
    check_file(junc, os.path.join(data_folder, 'data/junc_min.bed'))
    os.remove(junc)
    junc = fetch_juncfile(os.path.join(data_folder, 'data/junc.bam'),
                          uniq=True)
    check_file(junc, os.path.join(data_folder, 'data/junc_uniq.bed'))
    os.remove(junc)


def test_bam_to_bedgraph(data_folder):
    '''
    Testing bam_to_bedgraph()
    '''
    bg = bam_to_bedgraph(os.path.join(data_folder, 'data/test.bam'))
    check_file(bg, os.path.join(data_folder, 'data/unstranded.bg'))
    os.remove(bg)
    bg = bam_to_bedgraph(os.path.join(data_folder, 'data/test.bam'),
                         scale=True)
    check_file(bg, os.path.join(data_folder, 'data/unstranded_scale.bg'))
    os.remove(bg)
    pbg, mbg = bam_to_bedgraph(os.path.join(data_folder, 'data/test.bam'),
                               stranded=True)
    check_file(pbg, os.path.join(data_folder, 'data/plusS.bg'))
    os.remove(pbg)
    check_file(mbg, os.path.join(data_folder, 'data/minusS.bg'))
    os.remove(mbg)
