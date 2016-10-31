import sys
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
