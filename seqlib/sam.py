'''
Functions and classes related to SAM/BAM file
'''

import re

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['convert_cigar_digit', 'parse_MD_iter', 'parse_MD']


CIGAR_DIGIT = {0: 'M', 1: 'I', 2: 'D', 3: 'N', 4: 'S', 5: 'H', 6: 'P', 7: '=',
               8: 'X', 9: 'B'}


def convert_cigar_digit(digit):
    return CIGAR_DIGIT[digit]


def parse_MD_iter(md_tag, return_base=False):
    '''
    parse MD tag literally
    '''
    for s in re.split(r'([\\^]*[ACGT]+)[0]*', md_tag):
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


def parse_MD(md_tag, return_base=False):
    '''
    parse MD tag
    >>> parse_MD('272^A2G1G257')
    [(272, 'M'), (1, 'D'), (2, 'M'), (1, 'U'), (1, 'M'), (1, 'U'), (257, 'M')]
    >>> parse_MD('92T1^CA0C380')
    [(92, 'M'), (1, 'U'), (1, 'M'), (2, 'D'), (1, 'U'), (380, 'M')]
    '''
    return list(parse_MD_iter(md_tag, return_base))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
