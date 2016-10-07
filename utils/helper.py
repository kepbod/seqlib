import os
import os.path
import sys
import contextlib
import pysam
import pybedtools


def which(program):
    '''
    Check the path of external programs, and source codes are modified from
    https://github.com/infphilo/tophat/blob/master/src/tophat.py.
    '''
    def is_executable(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        progpath = os.path.join(path, program)
        if is_executable(progpath):
            return progpath
    return None


@contextlib.contextmanager
def smart_write(filename=None):
    '''
    Smart open output file.
    '''
    if filename and filename != '-' and filename != 'stdout':
        fn = open(filename, 'w')
    else:
        fn = sys.stdout
    try:
        yield fn
    finally:
        if fn is not sys.stdout:
            fn.close()


@contextlib.contextmanager
def smart_open(filename=None):
    '''
    Smart open input file.
    '''
    if filename and filename != '-' and filename != 'stdin':
        fn = open(filename, 'r')
    else:
        fn = sys.stdin
    try:
        yield fn
    finally:
        if fn is not sys.stdin:
            fn.close()


def check_option(n, msg):
    '''
    Check the number of options.
    '''
    if len(sys.argv) != n:
        sys.exit(msg)


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
