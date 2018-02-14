#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: fetch_geoinfo.py [options] <GSE_NUM>

Options:
    -h --help         Show help message.
    --version         Show version.
    -o output_file    Output file name [default: stdout].
    --add-url         Add URL information.
'''

import sys
import re
import tarfile
from future.moves.urllib.request import urlretrieve, urlopen
from docopt import docopt
from bs4 import BeautifulSoup
from seqlib.path import smart_write
from seqlib.version import __version__

__author__ = 'Xiao-Ou Zhang <kepbod@gmail.com>'


def main():
    # parse options
    options = docopt(__doc__, version=__version__)
    if options['--add-url']:
        url_flag = True
        url_prefix = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='
    else:
        url_flag = False
    # get GSE NUMBER
    gse_num = options['<GSE_NUM>']
    # check GSE NUMBER
    gse_pattern = re.compile('GSE\d{3,}')
    if not gse_pattern.match(gse_num):
        sys.exit('Error: <GSE_NUM> should be in correct format!')
    # set up MINiML url
    info_xml_name = gse_num + '_family.xml'
    info_xml_url = 'ftp.ncbi.nlm.nih.gov/geo/series/'
    info_xml_url += gse_num[:-3] + 'nnn/' + gse_num + '/miniml/'
    info_xml_url += info_xml_name + '.tgz'
    # store xml file
    try:  # try using ftp
        zipped_xml, _ = urlretrieve('ftp://' + info_xml_url)
    except:  # ftp connection failed, using http
        zipped_xml, _ = urlretrieve('http://' + info_xml_url)
    # parse xml
    xml_file = tarfile.open(zipped_xml).extractfile(info_xml_name)
    info_xml = BeautifulSoup(xml_file, 'xml')
    # write infomation
    with smart_write(options['-o']) as f:
        # write GSE infomation
        f.write(gse_num + '\t')
        if url_flag:
            f.write(url_prefix + gse_num + '\t')
        f.write(info_xml.Series.Title.string + '\n')
        # write GSM information
        for sample in info_xml.find_all('Sample'):
            gsm_num = sample['iid']
            f.write(gsm_num + '\t')
            if url_flag:
                f.write(url_prefix + gsm_num + '\t')
            f.write(sample.Title.string + '\t')
            sra_page = sample.find('Relation', type='SRA')['target']
            f.write(fetch_sra(sra_page, url_flag=url_flag))
            f.write('\n')


def fetch_sra(sra_page, url_flag=False):
    sra_info = []
    if url_flag:
        sra_url_template = 'ftp://ftp-trace.ncbi.nih.gov/'
        sra_url_template += 'sra/sra-instant/reads/ByRun/sra/SRR/'
        sra_url_template += '%s/%s/%s.sra'
    sra_html = BeautifulSoup(urlopen(sra_page).read(), 'html.parser')
    for table in sra_html.find_all('tbody'):
        for row in table.find_all('tr'):
            try:
                sra_num_info, read_info = row.find_all('td')[:2]
                sra_num = sra_num_info.string
                if url_flag:
                    sra_url = sra_url_template % (sra_num[:6], sra_num, sra_num)
                    sra_info.append('\t'.join([sra_num, read_info.string, sra_url]))
                else:
                    sra_info.append('\t'.join([sra_num, read_info.string]))
            except:
                continue
    return '\t'.join(sra_info)


if __name__ == '__main__':
    main()
