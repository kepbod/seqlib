#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: extract_region.py [options] -r region <annotation>

Options:
    -h --help         Show help message.
    --version         Show version.
    -r region         Fetched region (TSS, TES, exon, intron, 5UTR, CDS, \
3UTR, gene).
    -t type           Type of annotation file. [default: ref]
    --extend=dis      Extended distance (for TSS, TES or gene). [default: 0]
    --direction=type  Extended direction (both, upstream, downstream).
                      [default: both]
    --split-strand    Whether split according to strand.
    --no-merge        Do not merge regions
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
    if region not in ['TSS', 'TES', 'exon', 'intron', '5UTR', 'CDS', '3UTR',
                      'gene']:
        sys.exit('Error: incorrect region!')
    anno_type = options['-t']
    if anno_type not in ['ref', 'bed']:
        sys.exit('Error: incorrect annotation file format!')
    anno = options['<annotation>']
    if os.path.isfile(anno):
        anno = Annotation(anno, ftype=anno_type)
    else:
        sys.exit('Error: No annotation file!')
    dis = int(options['--extend'])
    direction = options['--direction']
    if direction not in ['both', 'upstream', 'downstream']:
        sys.exit('Error: incorrect extended direction!')
    split_flag = options['--split-strand']
    if split_flag:
        region_plus_lst = defaultdict(list)
        region_minus_lst = defaultdict(list)
    else:
        region_lst = defaultdict(list)
    no_merge_flag = options['--no-merge']
    for info in anno:
        if info.strand == '+':
            tss_site = info.tx_start
            tes_site = info.tx_end
            ref_lst = region_plus_lst if split_flag else region_lst
            left_dis = 0 if direction == 'downstream' else dis
            right_dis = 0 if direction == 'upstream' else dis
        else:
            tss_site = info.tx_end
            tes_site = info.tx_start
            ref_lst = region_minus_lst if split_flag else region_lst
            left_dis = 0 if direction == 'upstream' else dis
            right_dis = 0 if direction == 'downstream' else dis
        chrom = info.chrom
        if region == 'TSS':  # TSS
            ref_lst[chrom].append([max(tss_site - left_dis, 0),
                                   tss_site + right_dis])
        elif region == 'TES':  # TES
            ref_lst[chrom].append([max(tes_site - left_dis, 0),
                                   tes_site + right_dis])
        elif region == 'exon':  # exon
            for s, e in zip(info.exon_starts, info.exon_ends):
                ref_lst[chrom].append([s, e])
        elif region == 'intron':  # intron
            for s, e in zip(info.intron_starts, info.intron_ends):
                ref_lst[chrom].append([s, e])
        elif region == '5UTR':  # 5utr
            ref_lst[chrom].extend(info.utr5_regions)
        elif region == '3UTR':  # 3utr
            ref_lst[chrom].extend(info.utr3_regions)
        elif region == 'CDS':  # cds
            ref_lst[chrom].extend(info.cds_regions)
        else:  # gene
            ref_lst[chrom].append([max(info.tx_start - left_dis, 0),
                                   info.tx_end + right_dis])
    if split_flag:
        for chrom in region_plus_lst:
            if no_merge_flag:
                region_interval = region_plus_lst[chrom]
            else:
                region_interval = Interval(region_plus_lst[chrom])
            for itl in region_interval:
                print('%s\t%d\t%d\t%s\t0\t+' % (chrom, itl[0], itl[1], region))
        for chrom in region_minus_lst:
            if no_merge_flag:
                region_interval = region_minus_lst[chrom]
            else:
                region_interval = Interval(region_minus_lst[chrom])
            for itl in region_interval:
                print('%s\t%d\t%d\t%s\t0\t-' % (chrom, itl[0], itl[1], region))
    else:
        for chrom in region_lst:
            if no_merge_flag:
                region_interval = region_lst[chrom]
            else:
                region_interval = Interval(region_lst[chrom])
            for itl in region_interval:
                print('%s\t%d\t%d\t%s' % (chrom, itl[0], itl[1], region))


if __name__ == '__main__':
    main()
