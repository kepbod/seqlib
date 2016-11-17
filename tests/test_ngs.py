'''
Testing parse.py
'''

import os
import os.path
import pytest
from seqlib.ngs import fetch_juncfile, bam_to_bedgraph


def test_fetch_juncfile():
    '''
    Testing fetch_juncfile()
    '''
    junc = fetch_juncfile(pytest.helper.pytest.helper.data_path('junc.bam'))
    pytest.helper.check_file(junc,
                             pytest.helper.data_path('junc_unstranded.bed'))
    os.remove(junc)
    junc = fetch_juncfile(pytest.helper.data_path('junc.bam'), stranded=True)
    pytest.helper.check_file(junc,
                             pytest.helper.data_path('junc_stranded.bed'))
    os.remove(junc)
    junc = fetch_juncfile(pytest.helper.data_path('junc.bam'), min=5)
    pytest.helper.check_file(junc, pytest.helper.data_path('junc_min.bed'))
    os.remove(junc)
    junc = fetch_juncfile(pytest.helper.data_path('junc.bam'), uniq=True)
    pytest.helper.check_file(junc, pytest.helper.data_path('junc_uniq.bed'))
    os.remove(junc)


def test_bam_to_bedgraph():
    '''
    Testing bam_to_bedgraph()
    '''
    bg = bam_to_bedgraph(pytest.helper.data_path('test.bam'))
    pytest.helper.check_file(bg, pytest.helper.data_path('unstranded.bg'))
    os.remove(bg)
    bg = bam_to_bedgraph(pytest.helper.data_path('test.bam'), scale=True)
    pytest.helper.check_file(bg,
                             pytest.helper.data_path('unstranded_scale.bg'))
    os.remove(bg)
    pbg, mbg = bam_to_bedgraph(pytest.helper.data_path('test.bam'),
                               stranded=True)
    pytest.helper.check_file(pbg, pytest.helper.data_path('plusS.bg'))
    os.remove(pbg)
    pytest.helper.check_file(mbg, pytest.helper.data_path('minusS.bg'))
    os.remove(mbg)
