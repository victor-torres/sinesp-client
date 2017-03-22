#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='sinesp_client',
    version='1.7',
    license='Copyright',
    description='SINESP Cidadão database client.',
    author='Victor Torres',
    author_email='vpaivatorres@gmail.com',
    url='https://github.com/victor-torres/sinesp-client',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'sinesp_client': ['body.xml']},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests==2.8.1',
    ]
)
