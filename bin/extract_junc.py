#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: extract_junc.py [options] <bam>

Options:
    -h --help         Show help message.
    --version         Show version.
    -o output_dir     Output file name [default: ./].
    --url             Extract from remote url.
    --bb              Convert to BigWig.
'''

import sys
import os
import os.path
import tempfile
import pysam
from docopt import docopt
from seqlib.ngs import fetch_juncfile
from seqlib.path import which
from seqlib.version import __version__

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


def main():
    # parse options
    options = docopt(__doc__, version=__version__)
    # check output_dir
    if options['-o'] == './':
        dir = os.getcwd()
    else:
        if os.path.isdir(options['-o']):
            dir = options['-o']
        else:
            sys.exit('No such dir: %s' % options['-o'])
    # fetch junction bed file
    junc_f = fetch_juncfile(options['<bam>'], url=options['--url'], dir=dir)
    # create junction bigbed file in case
    if options['--bb'] and which('bedToBigBed') is not None:
        prefix = os.path.splitext(os.path.split(options['<bam>'])[-1])[0]
        bamf = pysam.AlignmentFile(options['<bam>'], 'rb')
        with tempfile.NamedTemporaryFile() as chrom_size:
            for seq in bamf.header['SQ']:
                chrom_size.write('%s\t%s\n' % (seq['SN'], seq['LN']))
            chrom_size.seek(0)
            bb_path = os.path.join(dir, prefix + '_junc.bb')
            return_code = os.system('bedToBigBed -type=bed12 %s %s %s' %
                                    (junc_f, chrom_size.name, bb_path)) >> 8
            if return_code:
                sys.exit('Error: cannot convert bed to BigBed!')
        bamf.close()


if __name__ == '__main__':
    main()
