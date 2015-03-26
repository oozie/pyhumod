#!/usr/bin/env python

"""Setup file for PyHumod package."""

import os
from distutils.core import setup
from humod import __version__

__author__ = 'Slawek Ligus <root@ooz.ie>'

CONFIG_FILES = [('/etc/ppp/peers', ['conf/humod'])]
try:
    os.stat('/etc/ppp/options')
except OSError:
    CONFIG_FILES = [('/etc/ppp/peers', ['conf/humod']),
                    ('/etc/ppp/options', ['conf/options'])]

setup(name='pyhumod',
      version=__version__,
      packages=['humod'],
      description='Python interface to Huawei modems.',
      long_description='A Python package that talks to Huawei'
                       ' (and compatible) modems.',
      author='Slawek Ligus',
      author_email='root@ooz.ie',
      url='https://github.com/oozie/pyhumod',
      license='BSD',
      platforms=['Linux'],
      data_files=CONFIG_FILES,
      classifiers=['License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: POSIX',  
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: MacOS :: MacOS X',
                   'Intended Audience :: Developers',
                   'Topic :: Communications',
                   'Topic :: Software Development :: Libraries'])
