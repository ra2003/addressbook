#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'sphinx', # for generatng documentation

]

test_requires = [ require for require in requires ]
test_requires.extend([

])

setup(name='addressbook',
    version='0.0.1',
    description='Super Simple Stocs',
    long_description=README,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Address book :: Library :: Application',
        'Intended Audience :: Developers',
        'License :: MIT',
    ],
    author='Tomasz Gorka',
    author_email='tomasz@gorka.org.pl',
    url='http://tomasz.gorka.org.pl',
    keywords='python address library',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = requires,
    tests_require = test_requires,
    test_suite='tests',
    license='MIT',
)