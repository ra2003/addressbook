#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#

class AlreadyPresentException(Exception):
    """
    Exception to raise when an element is already added in the structure.
    """