'''
Functions and classes to fetch information
'''

import sys
from future.utils import implements_iterator

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'
__all__ = ['Annotation', 'Junc']


class Info(object):

    def __init__(self, info, type='ref'):
        if type == 'ref':
            assert len(info) == 11, 'REF format should have 11 columns'
        elif type == 'bed':
            assert len(info) == 12, 'BED format should have 12 columns'
        else:
            sys.exit('Wrong format!')
        self._info = info
        self._type = type

    @property
    def gene(self):
        '''
        Return gene symbol.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.gene
        'DDX11L1'
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.gene
        'uc010nxq.1'
        '''
        if self._type == 'ref':
            return self._info[0]
        else:
            return self._info[3]

    @property
    def isoform(self):
        '''
        Return isoform symbol.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.isoform
        'uc010nxq.1'
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.isoform
        'uc010nxq.1'
        '''
        if self._type == 'ref':
            return self._info[1]
        else:
            return self._info[3]

    @property
    def name(self):
        '''
        Return name.
        >>> info = Info(['chr1', '14819', '15805', 'junc/1', '0', '+', '14819',
        ...              '15805', '0,0,0', '2', '10,10', '0,976'], type='bed')
        >>> info.name
        'junc/1'
        '''
        if self._type == 'ref':
            sys.exit('ERROR: Ref does not have name entry!')
        else:
            return self._info[3]

    @property
    def chrom(self):
        '''
        Return chromosome.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.chrom
        'chr1'
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.chrom
        'chr1'
        '''
        if self._type == 'ref':
            return self._info[2]
        else:
            return self._info[0]

    @property
    def strand(self):
        '''
        Return strand.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.strand
        '+'
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.strand
        '+'
        '''
        if self._type == 'ref':
            return self._info[3]
        else:
            return self._info[5]

    @property
    def tx_start(self):
        '''
        Return transcript start.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.tx_start
        11873
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.tx_start
        11873
        '''
        if self._type == 'ref':
            return int(self._info[4])
        else:
            return int(self._info[1])

    @property
    def tx_end(self):
        '''
        Return transcript end.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.tx_end
        14409
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.tx_end
        14409
        '''
        if self._type == 'ref':
            return int(self._info[5])
        else:
            return int(self._info[2])

    @property
    def total_length(self):
        '''
        Return total length (including exons and introns).
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.total_length
        2536
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.total_length
        2536
        '''
        return self.tx_end - self.tx_start

    @property
    def cds_start(self):
        '''
        Return cds start.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.cds_start
        12189
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.cds_start
        12189
        '''
        return int(self._info[6])

    @property
    def cds_end(self):
        '''
        Return cds end.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.cds_end
        13639
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.cds_end
        13639
        '''
        return int(self._info[7])

    @property
    def exon_num(self):
        '''
        Return exon number.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.exon_num
        3
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.exon_num
        3
        '''
        if self._type == 'ref':
            return int(self._info[8])
        else:
            return int(self._info[9])

    @property
    def intron_num(self):
        '''
        Return intron number.
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.intron_num
        2
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.intron_num
        2
        '''
        return self.exon_num - 1

    @property
    def exon_starts(self):
        '''
        Return exon starts
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.exon_starts
        [11873, 12594, 13402]
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.exon_starts
        [11873, 12594, 13402]
        '''
        if self._type == 'ref':
            return [int(x) for x in self._info[9].split(',')[:-1]]
        else:
            offsets = [int(x) for x in self._info[11].split(',')]
            return [self.tx_start + x for x in offsets]

    @property
    def exon_ends(self):
        '''
        Return exon ends
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.exon_ends
        [12227, 12721, 14409]
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.exon_ends
        [12227, 12721, 14409]
        '''
        if self._type == 'ref':
            return [int(x) for x in self._info[10].split(',')[:-1]]
        else:
            sizes = [int(x) for x in self._info[10].split(',')]
            return [start + size for start, size in zip(self.exon_starts,
                                                        sizes)]

    @property
    def exon_lengths(self):
        '''
        Return exon lengths
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.exon_lengths
        [354, 127, 1007]
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.exon_lengths
        [354, 127, 1007]
        '''
        if self._type == 'ref':
            return [end - start for start, end in zip(self.exon_starts,
                                                      self.exon_ends)]
        else:
            return [int(x) for x in self._info[10].split(',')]

    @property
    def intron_starts(self):
        '''
        Return intron starts
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.intron_starts
        [12227, 12721]
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.intron_starts
        [12227, 12721]
        '''
        return self.exon_ends[:-1]

    @property
    def intron_ends(self):
        '''
        Return intron ends
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.intron_ends
        [12594, 13402]
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.intron_ends
        [12594, 13402]
        '''
        return self.exon_starts[1:]

    @property
    def intron_lengths(self):
        '''
        Return intron lengths
        >>> info = Info(['DDX11L1', 'uc010nxq.1', 'chr1', '+', '11873',
        ...              '14409', '12189', '13639', '3', '11873,12594,13402,',
        ...              '12227,12721,14409,'])
        >>> info.intron_lengths
        [367, 681]
        >>> info = Info(['chr1', '11873', '14409', 'uc010nxq.1', '0', '+',
        ...              '12189', '13639', '0,0,0', '3', '354,127,1007',
        ...              '0,721,1529'], type='bed')
        >>> info.intron_lengths
        [367, 681]
        '''
        return [end - start for start, end in zip(self.intron_starts,
                                                  self.intron_ends)]


@implements_iterator
class Annotation(object):

    def __init__(self, fname, type='ref'):
        self.fh = open(fname, 'r')
        self.type = type

    def __iter__(self):
        return self

    def __next__(self):
        info = self.fh.readline()
        if info:
            return Info(info.split(), type=self.type)
        else:
            raise StopIteration()

    def close(self):
        self.fh.close()


@implements_iterator
class Junc(object):

    def __init__(self, fname):
        self.fh = open(fname, 'r')

    def __iter__(self):
        return self

    def __next__(self):
        info = self.fh.readline()
        if info:
            junc_info = Info(info.split(), type='bed')
            if junc_info.exon_num != 2:
                sys.exit('Error: exon number is not 2!')
            junc_read = int(junc_info.name.split('/')[1])
            junc_start = junc_info.intron_starts[0]
            junc_end = junc_info.intron_ends[0]
            return (junc_info.chrom, junc_start, junc_end, junc_info.strand,
                    junc_read)
        else:
            raise StopIteration()

    def close(self):
        self.fh.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
