#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#

# Constant data and functions for example data for tests

import addressbook


# Count of the test cases. In case of using all variation of the example datas.
TEST_COUNT = 100

# Test data for person objects
FIRST_NAMES = ['Jan', 'Tomasz', 'Marta', 'Georges', 'Nirina', '']
LAST_NAMES = ['Kowalski', 'Nowak', 'Müller', 'Lefèvre', 'Papadopoulos', 'Nagy', '']
EMAILS = ['test1@test.co', 'test1@test.com', 'test2@test.co', '1test@test.co']

# Test data for group objects
GROUP_NAMES = ['', 'default', 'family', 'friends']


def create_person(count, id=None):
    """
    Function to create person object based on actual count number
    from tests data.

    :param count: parameter to get the data from the list.
    :return: created person object
    """
    first_name = FIRST_NAMES[count % len(FIRST_NAMES)]
    last_name = LAST_NAMES[count % len(LAST_NAMES)]
    person = addressbook.Person(first_name=first_name, last_name=last_name, id=id)
    for i in range(0, count):
        email = EMAILS[i % len(EMAILS)]
        person.emails.add(email)

    return person


def create_group(count):
    """
    Create testing group object based on actual count number
    from tests data.

    :param count: of the persons in the group
    :return: created group object with persons
    """
    # create testing group object
    group_name = GROUP_NAMES[count % len(GROUP_NAMES)]
    group = addressbook.Group(name=group_name)
    # create testing person object
    for i in range(0, count):
        person = create_person(i)
        group.persons.add(person)

    return group