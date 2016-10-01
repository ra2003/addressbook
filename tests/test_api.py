#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#
import unittest

import addressbook
from addressbook import exception
import tests


class ApiTestCase(unittest.TestCase):
    """
    Test case of the library API.
    """

    def setUp(self):
        """
        initialize structure to be tested.
        self.address_book - structure to be tested
        self.persons, self.groups - helper sets to test if the person, group
                has been added using address_book API
        """
        self.address_book = addressbook.AddressBook()
        self.persons = set()
        self.groups = set()
        # prepare persons structure to test adding new persons
        # and already existing one
        self.all_persons = [tests.create_person(i) for i in
                            range(tests.TEST_COUNT)]

    def tearDown(self):
        """
        Dispose structure and helper objects.
        """
        self.address_book = None
        self.persons = None
        self.groups = None
        self.all_persons = None

    def _create_group(self, count):
        """
        Create group and adding all the created persons for the group in
        the helper set (self.persons).
        Created group will be added in the helper set(self.groups).
        Created group will be added to the address book structure

        :param count: parameter to get the data from the list.
        :return: created group object
        """
        group = tests.create_group(count)
        self.groups.add(group)
        for person in group.persons:
            self.persons.add(person)
        # add to address book
        self.address_book.add_group(group)
        return group

    def _get_persons_by_name(self, first_name, last_name):
        """
        Get persons from helper structure by the selected parameters.

        :param first_name: nullable first name
        :param last_name: nullable last name
        :return: set of the values
        """
        persons = set()
        for person in self.persons:
            doAdding = True
            if first_name is not None:
                doAdding &= first_name == person.first_name
            if last_name is not None:
                doAdding &= last_name == person.last_name

            if doAdding:
                persons.add(person)

        return persons

    def _get_persons_by_email_prefix(self, email_prefix):
        """
        Get persons from helper structure by the selected parameters.

        :param email_prefix: prefix of the email
        :return: set of the values
        """
        persons = set()
        for person in self.persons:
            for email in person.emails:
                if email.startswith(email_prefix):
                    persons.add(person)

        return persons

    def test_add_person(self):
        """
        Test adding persons.
        1. Testing empty structure if it's empty
        2. Testing adding various persons in the structure
        3. For each person testing by adding the second time the same object
                if it's raising an exception.
        4. For each person testing by adding new person with the same id
                if it's raising an exception.
        """
        assert len(self.persons ^ self.address_book.persons) == 0, \
            'Initial number of the persons should be empty.'

        for i in range(tests.TEST_COUNT):
            # create testing person object
            person = tests.create_person(i)
            # add to testing set
            self.persons.add(person)
            # add to address book
            self.address_book.add_person(person)
            # add the same person second time to test if it's not duplicate
            self.assertRaises(exception.AlreadyPresentException,
                self.address_book.add_person, person)
            # add next person with the same ID - check if created person with
            # the same information raise an exception
            same_person = tests.create_person(i, person.id)
            self.assertRaises(exception.AlreadyPresentException,
                self.address_book.add_person, same_person)

            assert len(self.persons ^ self.address_book.persons) == 0, \
                'Persons has not been added in the strcuture with sucess.'

    def test_add_group(self):
        """
        Test adding groups.
        1. Testing empty structure if it's empty
        2. Testing adding various groups in the structure
        3. For each group testing by adding the second time the same object
                if it's raising an exception.
        4. Check if new persons added with the group are present
                in the address book.
        """
        assert len(self.groups ^ self.address_book.groups) == 0, \
            'Initial number of the groups should be empty.'

        for i in range(tests.TEST_COUNT):
            # create testing group object
            group = self._create_group(i)

            # add the same group second time to test if it's not duplicate
            self.assertRaises(exception.AlreadyPresentException,
                self.address_book.add_group, group)

            assert len(self.groups ^ self.address_book.groups) == 0, \
                'Groups has not been added in the strcuture with sucess'
            assert len(self.persons ^ self.address_book.persons) == 0, \
                'Persons has not been added in the strcuture with sucess.'

    def test_find_persons_by_group(self):
        """
        Test finding persons by group.
        1. Create group, adding it into address book, find persons by
                this group and check if it's correct.
        """
        for i in range(tests.TEST_COUNT):
            # create testing group object
            group = self._create_group(i)
            persons = self.address_book.find_persons_by_group(group)

            assert len(group.persons ^ persons) == 0, \
                'Find by groups is not giving good results'

    def test_find_groups_by_person(self):
        """
        Test finding groups by person.
        1. Create group, adding it into address book, find persons by
                this group and check if returned values represent groups where
                person is present.
        """
        for i in range(tests.TEST_COUNT):
            # create testing group object
            group = self._create_group(i)

            for person in group.persons:
                # all groups where the person exists in helper structures
                groups_by_person = set([group for group
                                        in self.groups if
                                        person in group.persons])

                groups = self.address_book.find_groups_by_person(person)

                # compare helper structures with method result
                assert len(groups_by_person ^ groups) == 0, \
                    'Find by persons is not giving good results'

    def test_find_persons_by_name(self):
        """
        Test finding person by first name, last name, both or none.
        1. Checking finding in empty structure.
        2. Create group, adding it into address book, find persons by
                this first/last/both/none names and check if returned values
                represent persons where parameters are equal with the one
                from helper structure
        """
        assert len(set() ^ self.address_book.find_persons_by_name()) == 0, \
            'No first and last name checking.'

        for i in range(tests.TEST_COUNT):
            # create testing group object
            group= self._create_group(i)

            for person in group.persons:
                # create parameters to chek for the first/last name only,
                # both or none of them
                # None - should not chcek first/last name
                params = {
                    'first_name': person.first_name
                        if len(person.first_name) > 0 else None,
                    'last_name': person.last_name
                        if len(person.last_name) > 0 else None
                }

                # check by he parameters
                persons = self.address_book.find_persons_by_name(**params)
                # check values from helper structures
                persons_by_name = self._get_persons_by_name(**params)

                # check if it's the same
                assert len(persons_by_name ^ persons) == 0, \
                    'Find by name is not giving good results'

    def test_find_persons_by_email(self):
        """
        Test finding person by either the exact string or a prefix string, ie.
        both "alexander@company.com" and "alex" should work.
        1. Create group, adding it into address book, check all persons with
                all email addresses, all prefixes of the emails  and check if
                returned values represent persons where parameters are
                equal with the one from helper structure.
        """
        for i in range(len(tests.EMAILS)): # only email addresses needed to check
            # create testing group object
            group = self._create_group(i)

            for person in group.persons:
                for email in person.emails:
                    for j in range(0, len(email), 4):
                        email_prefix = email[:j]
                        # check by prefix
                        persons = self.address_book.find_persons_by_email(email_prefix)
                        # check values from helper structures
                        persons_by_email_prefix = self._get_persons_by_email_prefix(email_prefix)

                        # check if it's the same
                        assert len(persons_by_email_prefix ^ persons) == 0, \
                            'Find by email prefix is not giving good results'


if __name__ == '__main__':
    unittest.main()
