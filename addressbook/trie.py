#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#


class Trie:
    """
    Data structure based on tree to get the set of sentences based
    on their prefix.
    """

    def __init__(self):
        """
        Initialize trie with empty hash map of the characters.
        """
        self.letters = {}

    def add(self, text):
        """
        Add a text into trie recursievly.

        :param text: prefix to add
        """
        if len(text) > 0:
            self.letters.setdefault(text[0], Trie()).add(text[1:])
        else:
            self.letters[''] = None # terminate text by \n

    def get(self, prefix):
        """
        Generator to get the names based on the prefix.

        :param prefix: to get the list (can be full name)
        :return: generator of the texts
        """
        if len(prefix) > 0:
            if prefix[0] in self.letters:
                # return only if prefix is in the trie
                for text in self.letters.get(prefix[0]).get(prefix[1:]):
                    yield ''.join((prefix[0], text))
        else:
            # end of the prefix: get all the elements
            for text in self:
                yield text

    def __iter__(self):
        """
        Generator of all the texts in the trie.

        :return: all the texts
        """
        for letter,trie in self.letters.items():
            if trie is None:
                # terminated text yield letter == ''
                yield letter
            else:
                for text in trie:
                    # yield all children texts
                    yield ''.join((letter, text))
