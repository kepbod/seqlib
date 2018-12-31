import sys
import os

try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest as zip_longest

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['dna_to_rna', 'codon', 'load_codon_table']


def dna_to_rna(fa, strand='+', tou=False):
    '''
    Convert DNA to RNA.
    1. convert all the characters to uppercase
    2. reverse complement for minus strand RNAs
    3. convert T to U if tou is True
    >>> dna_to_rna('AAttcgGTA')
    'AATTCGGTA'
    >>> dna_to_rna('AAttcgGTA', tou=True)
    'AAUUCGGUA'
    >>> dna_to_rna('AAttcgGTA', strand='-')
    'TACCGAATT'
    >>> dna_to_rna('AAttcgGTA', strand='-', tou=True)
    'UACCGAAUU'
    '''
    if strand == '+':
        if tou:
            table = maketrans('ATCGatcg', 'AUCGaucg')
            return fa.translate(table).upper()
        else:
            return fa.upper()
    elif strand == '-':
        if tou:
            table = maketrans('ATCGatcg', 'UAGCuagc')
            return fa.translate(table).upper()[::-1]
        else:
            table = maketrans('ATCGatcg', 'TAGCtagc')
            return fa.translate(table).upper()[::-1]
    else:
        sys.exit('Strand should be "+" or "-"!')


def load_codon_table(seq_type):
    import msgpack
    dir_path = os.path.dirname(os.path.abspath(__file__))
    table_f = os.path.join(dir_path, 'data/%s_codon.msg' % seq_type)
    with open(table_f, 'rb') as f:
        table = msgpack.unpackb(f.read(), encoding='utf-8')
    return table


def codon(seq, seq_type='dna', frame=0, table=None):
    '''
    Convert sequence to codon
    >>> codon('ATGTTAGCTATC')
    ('MLAI', None)
    >>> codon('ATGTTAGCTATC', frame=1)
    ('C*L', 'TC')
    >>> codon('AUGUUAGCUAUC', seq_type='rna')
    ('MLAI', None)
    '''
    # check codon table
    if not table:
        table = load_codon_table(seq_type)
    # convert sequence
    aa = ''
    remain = None
    for i in map(''.join, zip_longest(*([iter(seq[frame:])] * 3),
                                      fillvalue='')):
        if len(i) == 3:
            aa += table[i]
        else:
            remain = i
    return str(aa), remain


if __name__ == '__main__':
    import doctest
    doctest.testmod()
