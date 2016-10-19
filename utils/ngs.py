'''
NGS relevant functions and classes
'''

import sys
import os.path
import pysam
import pybedtools


def check_fasta(fa):
    '''
    Check fasta files.
    http://pysam.readthedocs.io/en/latest/api.html?highlight=faidx#fasta-files
    '''
    if not os.path.isfile(fa):
        sys.exit('No such file: %s!' % fa)
    if not os.path.isfile(fa + '.fai'):
        pysam.faidx(fa)
    return pysam.FastaFile(fa)


def check_bam(bam):
    '''
    Check bam files.
    http://pysam.readthedocs.io/en/latest/api.html?highlight=faidx#sam-bam-files
    '''
    if not os.path.isfile(bam):
        sys.exit('No such file: %s!' % bam)
    if not os.path.isfile(bam + '.bai'):
        pysam.index(bam)
    return pysam.AlignmentFile(bam, 'rb')


def check_bed(bed):
    '''
    Check bed files.
    http://pysam.readthedocs.io/en/latest/api.html?highlight=faidx#tabix-files
    '''
    if not os.path.isfile(bed):
        sys.exit('No such file: %s!' % bed)
    if bed.endswith('.gz'):
        if not os.path.isfile(bed + '.tbi'):  # no index
            pysam.tabix_index(bed, preset='bed')
        return pysam.TabixFile(bed)
    else:
        if not os.path.isfile(bed + '.gz'):  # no compress
            pybedtools.BedTool(bed).bgzip()
        if not os.path.isfile(bed + '.gz.tbi'):  # no index
            pysam.tabix_index(bed + '.gz', preset='bed')
        return pysam.TabixFile(bed + '.gz')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
