'''
Testing parse.py
'''

import os.path
from seqlib.parse import Junc


def test_junc(tmpdir):
    junc_bed = tmpdir.join('junc.bed')
    junc_bed.write('\t'.join(['chr1', '17045', '17615', 'junc/11', '0', '+',
                              '17045', '17615', '0,0,0', '2', '10,10',
                              '0,560']))
    chrom, start, end, strand, read = list(Junc(os.path.join(str(tmpdir),
                                                             'junc.bed')))[0]
    assert chrom == 'chr1'
    assert start == 17055
    assert end == 17605
    assert strand == '+'
    assert read == 11
