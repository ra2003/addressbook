#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# addressbook
# https://github.com/tgorka/addressbook
#
# Copyright (C) 2016 Tomasz Gorka <http://tomasz.gorka.org.pl>
#
import uuid

import datetime
from addressbook import exception, trie


class AddressBook:
    """
    Address Book structure contains groups and persons.
    """

    def __init__(self):
        """
        Initialize address book with all the needed structures
        """
        # initialize groups and persons
        self.groups = set()
        self.persons = set()
        # hash maps for searching over first and the last person name
        self.first_names = {}
        self.last_names = {}
        # hash maps for searching over email and trie with emails
        self.emails = {}
        self.emailsTrie = trie.Trie()

    def add_person(self, person):
        """
        Add a person to the address book.

        :param person: to add
        :raises AlreadyPresentException: person is already added
        """
        if person in self.persons:
            raise exception.AlreadyPresentException(
                'Person %s has been already added.' % person.name)

        self.persons.add(person)
        # add index for first and the last name for searching
        self.first_names.setdefault(person.first_name.lower(), set()).add(person)
        self.last_names.setdefault(person.last_name.lower(), set()).add(person)
        # add index for email for searching
        for email in person.emails:
            self.emails.setdefault(email.lower(), set()).add(person)
            self.emailsTrie.add(email.lower())

    def add_group(self, group):
        """
        Add a group to the address book.

        :param group: to add
        :raises AlreadyPresentException: group is already added
        """
        if group in self.groups:
            raise exception.AlreadyPresentException(
                'Group %s has been already added.' % group.name)

        self.groups.add(group)
        for person in group.persons:
            # double check if group is set for the person
            if group not in person.groups:
                person.groups.add(group)
            if person not in self.persons:
                self.add_person(person)

    def find_persons_by_group(self, group):
        """
        Given a group we want to easily find its members.

        :param group: to filter
        :return: set of persons
        """
        return group.persons

    def find_groups_by_person(self, person):
        """
        Given a person we want to easily find the groups the person belongs to.

        :param person: to filter
        :return: set of groups
        """
        return person.groups

    def find_persons_by_name(self, first_name=None, last_name=None):
        """
        Find person by name (can supply either first name, last name, or both).

        :param first_name: first name of the person
        :param last_name: last name of the person
        :return: set of persons
        """
        # get the sets of persons by first name and last name
        persons_by_first_name = self.first_names.get(first_name.lower(), set()) \
            if first_name is not None else self.persons
        persons_by_last_name = self.last_names.get(last_name.lower(), set()) \
            if last_name is not None else self.persons

        # return the common part of this 2 sets
        return persons_by_first_name & persons_by_last_name

    def find_persons_by_email(self, email_prefix):
        """
        Find person by email address (can supply either the exact string or
        a prefix string, ie. both "alexander@company.com" and "alex").

        :param email_prefix: to find the person
        :return: set of persons
        """
        persons = set()
        for email in self.emailsTrie.get(email_prefix.lower()):
            persons |= self.emails.get(email, set())

        return persons


class Person:
    """
    Person structure:
    - A person has a first name and a last name.
    - A person has one or more street addresses.
    - A person has one or more email addresses.
    - A person has one or more phone numbers.
    - A person can be a member of one or more groups.
    """

    def __init__(self, first_name, last_name, id=None):
        """
        Initialize Person with all needed structures.
        If id is None the default one will be generated using UUID algorithm.
        IMPORTANT: recognize person by id not by name because sometimes
        a few people has the same name (the first and the last one)

        :param first_name: of the person.
        :param last_name: of the person.
        :param id: identifier of the person. None by default.
        """
        self.__id = id if id is not None else uuid.uuid4()
        self.creation_date = datetime.datetime.now()

        self.first_name = first_name
        self.last_name = last_name

        self.emails = set()
        self.phones = set()
        self.addresses = set()

        self.groups = set()

    @property
    def name(self):
        """
        Get simplified name based of first name and second name

        :return: full name
        """
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        raise Exception("Can't change the ID, once it has ben set in "
                        + "the constructor.")

    def __eq__(self, other):
        """
        Equal method
        Use id to equal 2 persons by id.
        So it will work even if person has changed the name and only one object
        will represent current state.

        :param other: object to compare
        :return: is the same
        """
        if isinstance(other, self.__class__):
            return self.id is other.id

        return False

    def __ne__(self, other):
        """
        Not equal method
        Use id to equal 2 persons by id.
        So it will work even if person has changed the name and only one object
        will represent current state.

        :param other: object to compare
        :return: is different
        """
        if isinstance(other, self.__class__):
            return self.id is not other.id

        return True

    def __hash__(self):
        """
        Hash method
        Use hash of the id property.

        :return: hash code
        """
        return hash(self.id)


class Address:
    """
    Address structure.
    """

    def __init__(self, *street_address_lines):
        """
        Initialize Address with all needed structures.

        :param street_address_lines: all the lines needed to be in the envelope.
        """
        self.street_address_lines = street_address_lines
        self.creation_date = datetime.datetime.now()


class Group:
    """
    Group structure.
    """

    def __init__(self, name):
        """
        Initialize Group with all needed structures.
        The persons connected to th group will be empty at the beginning.

        :param name: of the group.
        """
        self.name = name
        self.creation_date = datetime.datetime.now()

        self.persons = set()
