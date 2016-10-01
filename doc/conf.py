#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#
import os
import sys

# update path to the sources
source_path = os.path.abspath(__file__)
source_path = os.path.dirname(source_path)
source_path = os.path.join(source_path, '../addressbook')
source_path = os.path.abspath(source_path)

sys.path.append(source_path)

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
