'''
NGS relevant functions and classes
'''

import sys
import os
import os.path
import re
from collections import defaultdict
import tempfile
import pysam
import pybedtools

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['check_fasta', 'check_bam', 'check_bed', 'fetch_juncfile',
           'bam_to_bedgraph']


def check_fasta(fa, return_handle=True):
    '''
    Check fasta files.
    http://pysam.readthedocs.io/en/latest/api.html?highlight=faidx#fasta-files
    '''
    if not os.path.isfile(fa):
        sys.exit('No such file: %s!' % fa)
    if not os.path.isfile(fa + '.fai'):
        pysam.faidx(fa)
    if return_handle:
        return pysam.FastaFile(fa)
    else:
        return fa


def check_bam(bam, return_handle=True):
    '''
    Check bam files.
    http://pysam.readthedocs.io/en/latest/api.html?highlight=faidx#sam-bam-files
    '''
    if not os.path.isfile(bam):
        sys.exit('No such file: %s!' % bam)
    if not os.path.isfile(bam + '.bai'):
        pysam.index(bam)
    if return_handle:
        return pysam.AlignmentFile(bam, 'rb')
    else:
        return bam


def check_bed(bed, return_handle=True):
    '''
    Check bed files.
    http://pysam.readthedocs.io/en/latest/api.html?highlight=faidx#tabix-files
    '''
    if not os.path.isfile(bed):
        sys.exit('No such file: %s!' % bed)
    if bed.endswith('.gz'):
        if not os.path.isfile(bed + '.tbi'):  # no index
            pysam.tabix_index(bed, preset='bed')
        bedf = bed
    else:
        if not os.path.isfile(bed + '.gz'):  # no compress
            pybedtools.BedTool(bed).bgzip()
        if not os.path.isfile(bed + '.gz.tbi'):  # no index
            pysam.tabix_index(bed + '.gz', preset='bed')
        bedf = bed + '.gz'
    if return_handle:
        return pysam.TabixFile(bedf)
    else:
        return bedf


def fetch_juncfile(bam, url=False, dir=None, uniq=False, stranded=False,
                   min=0):
    '''
    Fetch junction reads to create a junc file
    '''
    bamf = pysam.AlignmentFile(bam, 'rb')
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
        if uniq and read.get_tag('NH') != 1:
            continue
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
    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        for junc in junc_lst:
            if junc_lst[junc] < min:
                continue
            chrom, pos1, pos2, strand = junc.split()
            pos1 = int(pos1)
            pos2 = int(pos2)
            start = pos1 - 10
            end = pos2 + 10
            offset = pos2 - start
            junc_info = '%s\t%d\t%d\tjunc/%d\t0\t%s'
            junc_info += '\t%d\t%d\t0,0,0\t2\t10,10\t0,%d\n'
            tmp.write(junc_info % (chrom, start, end, junc_lst[junc],
                                   strand, start, end, offset))
        tmp.seek(0)
        sorted_junc_bed = pybedtools.BedTool(tmp.name).sort()
        sorted_junc_bed.saveas(junc_path)
    return junc_path


def bam_to_bedgraph(bam, url=False, dir=None, stranded=False, scale=False):
    '''
    Convert bam file to bedgraph file
    Note: `scale` only supports local files
    '''
    if url:  # from remote server
        bamf = pybedtools.BedTool(bam, remote=True)
    else:  # from local file
        bamf = pybedtools.BedTool(bam, remote=False)
        bam_head = check_bam(bam)
    prefix = os.path.splitext(os.path.split(bam)[-1])[0]
    if not dir:
        if url:
            dir = os.getcwd()
        else:
            dir = os.path.dirname(os.path.abspath(bam))
    else:
        if not os.path.isdir(dir):
            sys.exit('Your directory is wrong: %s' % dir)
    chrom_size_f = tempfile.NamedTemporaryFile('w+')
    for seq in bam_head.header['SQ']:
        chrom_size_f.write('%s\t%s\n' % (seq['SN'], seq['LN']))
    chrom_size_f.seek(0)
    chrom_size_fn = chrom_size_f.name
    if scale and not url:
        mapped_reads = bam_head.mapped
        for read in bam_head:
            read_length = read.query_length
            break
        s = 1000000000.0 / mapped_reads / read_length
    else:
        s = 1
    if stranded:
        bedgraph_pfn = os.path.join(dir, prefix + '_plusS.bg')
        bedgraph_mfn = os.path.join(dir, prefix + '_minusS.bg')
        _cal_cov(bedgraph_pfn, bamf, chrom_size_fn, s, strand='+')
        _cal_cov(bedgraph_mfn, bamf, chrom_size_fn, s, strand='-')
    else:
        bedgraph_fn = os.path.join(dir, prefix + '.bg')
        _cal_cov(bedgraph_fn, bamf, chrom_size_fn, s)
    chrom_size_f.close()
    if stranded:
        return (bedgraph_pfn, bedgraph_mfn)
    else:
        return bedgraph_fn


def _cal_cov(bedgraph_fn, bamf, chrom_size_fn, scale, strand=None):
    opt = {'bg': True, 'g': chrom_size_fn, 'split': True, 'scale': scale}
    if strand == '+':
        opt['strand'] = '-'  # for TruSeq kit
    elif strand == '-':
        opt['strand'] = '+'  # for TruSeq kit
        opt['scale'] *= -1
    with open(bedgraph_fn, 'w') as bedgraph_f:
        for line in bamf.genome_coverage(**opt):
            value = str(int(float(line[3]) + 0.5))
            bedgraph_f.write('\t'.join(line[:3]) + '\t%s\n' % value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
