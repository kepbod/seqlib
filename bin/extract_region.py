#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: extract_region.py [options] -r region <annotation>

Options:
    -h --help         Show help message.
    --version         Show version.
    -r region         Fetched region (promoter, exon, intron, gene).
    -t type           Type of annotation file. [default: ref]
    --extend=extend   Entended region. [default: 1000]
    --split-strand    Whether split according to strand.
'''

import sys
import os.path
from collections import defaultdict
from docopt import docopt
from seqlib.parse import Annotation
from seqlib.interval import Interval
from seqlib.version import __version__

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


def main():
    # parse options
    options = docopt(__doc__, version=__version__)
    region = options['-r']
    if region not in ['promoter', 'exon', 'intron', 'gene']:
        sys.exit('Error: incorrect region!')
    anno_type = options['-t']
    if anno_type not in ['ref', 'bed']:
        sys.exit('Error: incorrect annotation file format!')
    anno = options['<annotation>']
    if os.path.isfile(anno):
        anno = Annotation(anno, type=anno_type)
    else:
        sys.exit('Error: No annotation file!')
    dis = int(options['--extend'])
    split_flag = options['--split-strand']
    if split_flag:
        region_plus_lst = defaultdict(list)
        region_minus_lst = defaultdict(list)
    else:
        region_lst = defaultdict(list)
    for info in anno:
        if info.strand == '+':
            site = info.tx_start
            ref_lst = region_plus_lst if split_flag else region_lst
        else:
            site = info.tx_end
            ref_lst = region_minus_lst if split_flag else region_lst
        chrom = info.chrom
        if region == 'promoter':
            ref_lst[chrom].append([site - dis, site + dis])
        elif region == 'exon':
            for s, e in zip(info.exon_starts, info.exon_ends):
                ref_lst[chrom].append([s - dis, e + dis])
        elif region == 'intron':
            for s, e in zip(info.intron_starts, info.intron_ends):
                ref_lst[chrom].append([s - dis, e + dis])
        else:
            ref_lst[chrom].append([info.tx_start - dis, info.tx_end + dis])
    if split_flag:
        for chrom in region_plus_lst:
            for itl in Interval(region_plus_lst[chrom]):
                print('%s\t%d\t%d\t%s\t0\t+' % (chrom, itl[0], itl[1], region))
        for chrom in region_minus_lst:
            for itl in Interval(region_minus_lst[chrom]):
                print('%s\t%d\t%d\t%s\t0\t-' % (chrom, itl[0], itl[1], region))
    else:
        for chrom in region_lst:
            for itl in Interval(region_lst[chrom]):
                print('%s\t%d\t%d\t%s\t0\t+' % (chrom, itl[0], itl[1], region))


if __name__ == '__main__':
    main()
