'''
Functions and classes related to SAM/BAM file
'''

import sys
import re
from itertools import groupby

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['convert_cigar_digit', 'parse_MD_iter', 'parse_MD',
           'parse_CIGAR_iter', 'parse_CIGAR', 'convert_CIGAR',
           'count_alignment_length', 'index_alignment', 'sub_alignment']


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


def parse_CIGAR(cigar_str, reverse=False):
    '''
    parse CIGAR
    >>> parse_CIGAR('11S23M1D35M6S')
    [(11, 'S'), (23, 'M'), (1, 'D'), (35, 'M'), (6, 'S')]
    >>> parse_CIGAR('11S23M1D35M6S', reverse=True)
    [(6, 'S'), (35, 'M'), (1, 'D'), (23, 'M'), (11, 'S')]
    '''
    if reverse:
        return list(parse_CIGAR_iter(cigar_str))[::-1]
    else:
        return list(parse_CIGAR_iter(cigar_str))


def convert_CIGAR(cigar_str, md_str, reverse=False):
    '''
    conver CIGAR with mismatches
    >>> aln = convert_CIGAR('6S271M1I4M2D253M8S', '273T1^CA0C252')
    >>> ''.join('{}{}'.format(x[0], x[1]) for x in aln)
    '6S271M1I2M1U1M2D1U252M8S'
    >>> aln = convert_CIGAR('6S271M1I4M2D253M8S', '273T1^CA0C252',
    ...                     reverse=True)
    >>> ''.join('{}{}'.format(x[0], x[1]) for x in aln)
    '8S252M1U2D1M1U2M1I271M6S'
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
        if cigar_tag in ('S', 'H', 'I'):
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
    if reverse:
        return aln[::-1]
    else:
        return aln


def count_alignment_length(cigar_str, read_length=False):
    '''
    Count reference covered length for reads
    >>> count_alignment_length('63M1D308M1U1M1U2M1U1U1U285M648S')
    665
    >>> count_alignment_length('666H540M106H')
    540
    >>> count_alignment_length('66S54M3I5U5D2M106H')
    66
    >>> count_alignment_length('66S54M3I5U5D2M106H', read_length=True)
    236
    '''
    total_length = 0
    for counts, tag in parse_CIGAR_iter(cigar_str):
        if tag in ('M', 'U'):
            total_length += counts
        if not read_length and tag in ('D', 'N'):
            total_length += counts
        if read_length and tag in ('I', 'S', 'H'):
            total_length += counts
    return total_length


def index_alignment(cigar_str):
    '''
    Find index of alignment in the read
    >>> index_alignment('404M843S')
    (0, 404)
    >>> index_alignment('879H368M')
    (879, 1247)
    >>> index_alignment('365S144M1I3M1I27M1I291M1D1U8M405S')
    (365, 842)
    '''
    start_index, end_index = 0, 0
    for n, (counts, tag) in enumerate(parse_CIGAR_iter(cigar_str)):
        if tag in ('S', 'H') and n == 0:
            start_index += counts
            end_index += counts
        if tag in ('M', 'U', 'I'):
            end_index += counts
    return (start_index, end_index)


def sub_alignment(cigar_str, start, total=None):
    '''
    Substract alignments according to position
    >>> sub_alignment('15S34M1I2M3U5D3M1I5M5H', 38, 9)
    '1U5D3M1I'
    >>> sub_alignment('15S34M1I2M3U5D3M1I5M5H', 0, 37)
    '15S34M1I2M1U'
    >>> sub_alignment('15S34M1I2M3U5D3M1I5M5H', 38)
    '1U5D3M1I5M5H'
    >>> sub_alignment('15S34M1I2M3U5D3M1I5M5H', 34)
    '1I2M3U5D3M1I5M5H'
    '''
    sub_cigar = ''
    index_start, index_end = 0, 0
    move_flag = False
    if total is None:
        end = sys.maxsize
    else:
        end = start + total
    for counts, tag in parse_CIGAR_iter(cigar_str):
        if tag in ('M', 'U', 'D', 'N'):
            index_start = index_end
            index_end += counts
            move_flag = True
        if start <= index_end <= end:
            if move_flag:
                move_flag = False
                if index_start < start:
                    n = counts - (start - index_start)
                elif start <= index_start:
                    n = counts
            else:
                n = counts
            sub_cigar += '{}{}'.format(n, tag) if n else ''
        elif index_start < end < index_end:
            if index_start < start:
                n = end - start
            elif start <= index_start:
                n = counts - (index_end - end)
            sub_cigar += '{}{}'.format(n, tag) if n else ''
            break
    return sub_cigar


if __name__ == '__main__':
    import doctest
    doctest.testmod()
