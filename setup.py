#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from seqlib.version import __version__

setup(name='seqlib',
      version=__version__,
      description='NGS analysis toolkits',
      author='Xiao-Ou Zhang',
      author_email='kepbod@gmail.com',
      url='https://github.com/kepbod/seqlib',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='NGS',
      packages=find_packages(),
      install_requires=[
          'future',
          'requests',
          'pysam>=0.8.4',
          'pybedtools>=0.7.8',
          'docopt',
          'beautifulsoup4'
      ],
      scripts=[
          'bin/fetch_geoinfo.py',
          'bin/extract_junc.py'
      ]
      )
