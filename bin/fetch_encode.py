#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: fetch_encode.py [options] <EXP_NUM>

Options:
    -h --help         Show help message.
    --version         Show version.
    -o output_file    Output file name [default: stdout].
    -a assembly       Version of assembly [default: hg19].
'''

import re
from docopt import docopt
from seqlib.path import smart_write
from seqlib.encode import Exp
from seqlib.version import __version__

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


def main():
    # parse options
    options = docopt(__doc__, version=__version__)
    accession = options['<EXP_NUM>']
    assembly = options['-a']
    # fetch info
    exp = Exp(accession)
    info = '\t'.join([exp.accession, exp.description])
    info += '\n'
    for f in exp.fetch_file(process_type='processed'):
        if f.assembly != assembly:
            continue
        if f.status != 'released':
            continue
        file_type = re.subn(r'\s', '_', f.file_type)[0]
        output_type = re.subn(r'\s', '_', f.output_type)[0]
        biorep = str(f.biological_replicate)
        tchrep = str(f.technical_replicate)
        info += '\t'.join([f.accession, file_type, biorep, tchrep, f.assembly,
                           output_type, f.file_url, f.file_md5])
        info += '\n'
    # write info
    with smart_write(options['-o']) as out:
        out.write(info)


if __name__ == '__main__':
    main()
