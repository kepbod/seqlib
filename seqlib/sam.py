'''
Functions and classes related to SAM/BAM file
'''

import re
from itertools import groupby

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['convert_cigar_digit', 'parse_MD_iter', 'parse_MD',
           'parse_CIGAR_iter', 'parse_CIGAR', 'convert_CIGAR']


CIGAR_DIGIT = {0: 'M', 1: 'I', 2: 'D', 3: 'N', 4: 'S', 5: 'H', 6: 'P', 7: '=',
               8: 'X', 9: 'B'}


def convert_cigar_digit(digit):
    return CIGAR_DIGIT[digit]


def parse_MD_iter(md_str, return_base=False):
    '''
    parse MD tag literally
    '''
    for s in re.split(r'([\\^]*[ACGT]+)[0]*', md_str):
        if s.isnumeric():
            yield (int(s), 'M', '') if return_base else (int(s), 'M')
        elif s.startswith('^'):
            base = s[1:]
            length = len(base)
            yield (length, 'D', base) if return_base else (length, 'D')
        else:
            length = len(s)
            if length == 0:
                continue
            yield (length, 'U', s) if return_base else (length, 'U')


def parse_MD(md_str, return_base=False):
    '''
    parse MD tag
    >>> parse_MD('272^A2G1G257')
    [(272, 'M'), (1, 'D'), (2, 'M'), (1, 'U'), (1, 'M'), (1, 'U'), (257, 'M')]
    >>> parse_MD('92T1^CA0C380')
    [(92, 'M'), (1, 'U'), (1, 'M'), (2, 'D'), (1, 'U'), (380, 'M')]
    '''
    return list(parse_MD_iter(md_str, return_base))


def parse_CIGAR_iter(cigar_str):
    '''
    parse CIGAR literally
    '''
    cigar_iter = groupby(cigar_str, lambda c: c.isdigit())
    for g, n in cigar_iter:
        counts, tag = int("".join(n)), "".join(next(cigar_iter)[1])
        yield (counts, tag)


def parse_CIGAR(cigar_str):
    '''
    parse CIGAR
    >>> parse_CIGAR('11S23M1D35M6S')
    [(11, 'S'), (23, 'M'), (1, 'D'), (35, 'M'), (6, 'S')]
    '''
    return list(parse_CIGAR_iter(cigar_str))


def convert_CIGAR(cigar_str, md_str):
    '''
    conver CIGAR with mismatches
    >>> aln = convert_CIGAR('6S271M1I4M2D253M8S', '273T1^CA0C252')
    >>> ''.join('{}{}'.format(x[0], x[1]) for x in aln)
    '6S271M1I2M1U1M2D1U252M8S'
    '''
    cigar = parse_CIGAR(cigar_str)
    md = parse_MD(md_str)
    aln = []
    i, j = 0, 0
    tag, base = None, None
    query_base, reference_base = 0, 0
    while i < len(cigar) and j < len(md):
        cigar_base = cigar[i][0] + query_base
        cigar_tag = cigar[i][1]
        md_base = md[j][0] + reference_base
        md_tag = md[j][1]
        if cigar_tag in ['S', 'H', 'I']:
            aln.append((cigar_base, cigar_tag))
            i += 1
            continue
        if cigar_base < md_base:
            tag = cigar_tag
            base = cigar_base
            reference_base -= base
            query_base = 0
            i += 1
        elif cigar_base > md_base:
            tag = md_tag
            base = md_base
            query_base -= base
            reference_base = 0
            j += 1
        else:
            tag = cigar_tag
            base = cigar_base
            query_base, reference_base = 0, 0
            i += 1
            j += 1
        aln.append((base, tag))
    if i == len(cigar) - 1:
        cigar_base = cigar[i][0]
        cigar_tag = cigar[i][1]
        aln.append((cigar_base, cigar_tag))
    return aln


if __name__ == '__main__':
    import doctest
    doctest.testmod()
