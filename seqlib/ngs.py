'''
NGS relevant functions and classes
'''

import sys
import os
import os.path
import re
from collections import defaultdict
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


def fetch_juncfile(bam, url=False, dir=None, stranded=False):
    '''
    fetch junction reads to create a junc file
    '''
    if url:  # from remote server
        bamf = pysam.AlignmentFile(bam, 'rb')
    else:  # from local file
        bamf = check_bam(bam)
    prefix = os.path.splitext(os.path.split(bam)[-1])[0]
    if not dir:
        if url:
            dir = os.getcwd()
        else:
            dir = os.path.dirname(os.path.abspath(bam))
    else:
        if not os.path.isdir(dir):
            sys.exit('Your directory is wrong: %s' % dir)
    junc_lst = defaultdict(int)
    for read in bamf:
        if read.cigartuples and any(filter(lambda x: x[0] == 3,
                                           read.cigartuples)):
            npos = re.findall(r'N|D|I', read.cigarstring).index('N')
            pos1 = read.get_blocks()[npos][1]
            pos2 = read.get_blocks()[npos + 1][0]
            if stranded:
                strand = '+' if read.is_reverse else '-'
            else:
                strand = '+'
            junc_id = '%s\t%d\t%d\t%s' % (read.reference_name, pos1, pos2,
                                          strand)
            junc_lst[junc_id] += 1
    junc_path = os.path.join(dir, prefix + '_junc.bed')
    with open(junc_path, 'w') as junc_f:
        for junc in junc_lst:
            chrom, pos1, pos2, strand = junc.split()
            pos1 = int(pos1)
            pos2 = int(pos2)
            start = pos1 - 10
            end = pos2 + 10
            offset = pos2 - start
            junc_info = '%s\t%d\t%d\tjunc/%d\t0\t%s'
            junc_info += '\t%d\t%d\t0,0,0\t2\t10,10\t0,%d\n'
            junc_f.write(junc_info % (chrom, start, end, junc_lst[junc],
                                      strand, start, end, offset))
    return junc_path


if __name__ == '__main__':
    import doctest
    doctest.testmod()
