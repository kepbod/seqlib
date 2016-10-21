#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: fetch_geoinfo [options] <GSE_NUM>

Options:
    -h --help         Show help message.
    --version         Show version.
    -o output_file    Output file name (default: stdout).
    --add-url         Add URL information.
'''


import sys
import re
import urllib
import tarfile
from docopt import docopt
from bs4 import BeautifulSoup
from helper import smart_write


__author__ = 'Xiao-Ou Zhang (Xiaoou.Zhang@umassmed.edu)'
__version__ = 0.1


def main():
    # parse options
    options = docopt(__doc__, version=__version__)
    if options['--add-url']:
        url_flag = True
        url_prefix = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='
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
    info_xml_url = 'ftp://ftp.ncbi.nlm.nih.gov/geo/series/'
    info_xml_url += gse_num[:-3] + 'nnn/' + gse_num + '/miniml/'
    info_xml_url += info_xml_name + '.tgz'
    # store xml file
    zipped_xml, _ = urllib.urlretrieve(info_xml_url)
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
            sra_url = sample.find('Relation', type='SRA')['target']
            if url_flag:
                f.write(sra_url + '\t')
            f.write(fetch_sra(sra_url))
            f.write('\n')


def fetch_sra(sra_url):
    sra_info = []
    sra_html = BeautifulSoup(urllib.urlopen(sra_url).read(), 'html.parser')
    for row in sra_html.tbody.find_all('tr'):
        sra_num_info, read_info = row.find_all('td')[:2]
        sra_info.append('\t'.join([sra_num_info.string, read_info.string]))
    return '\t' .join(sra_info)


if __name__ == '__main__':
    main()
