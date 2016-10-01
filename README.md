# addressbook
Simple address book library in Python.

## Description
The source code that will :
- A person has a first name and a last name.
- A person has one or more street addresses.
- A person has one or more email addresses.
- A person has one or more phone numbers.
- A person can be a member of one or more groups.
- An address book is a collection of persons and groups.

## Requirements

- Python 3.x (tested on 3.4)
- Tested on MacOS X

## Installation

### Application
To install application with all dependencies:

```
pip install git+git://github.com/tgorka/addressbook.git
```

To install in develop mode from the sources you should clone the sources and
install in in develop mode:

```
pip install -e /path/to/sources --no-binary :all: pytest
```

To check if the application was installed:

```
python -c "import sys; import addressbook; print('addressbook' in sys.modules)"
```

It should print True or throw an ImportError.

To uninstall application:

```
pip uninstall addressbook
```

HINT: It's always save to use VirtualEnv
(https://virtualenv.readthedocs.org/en/latest/) and virtualenvwrapper.

## Run

### API

There is an API functions to use the library. The documentation can be
generated from the comments using reStructuredText.

```
python setup.py build_sphinx
```

There is generated html version of the documentation in `doc/html` folder.

The simpe use of API:

```
import addressbook

ab = addressbook.AddressBook()

p = addressbook.Person('John', 'Smith')
p.emails.add('john@smith.us')
g = addressbook.Group()
g.persons.add(p)

ab.add_person(p)
ab.add_group(g)

### will return set that contain g:
groups = ab.find_groups_by_person(p)

### will return set that contain p:
persons = ab.find_persons_by_group(g)
persons = ab.find_persons_by_name(first_name='john')
persons = ab.find_persons_by_name(last_name='smith')
persons = ab.find_persons_by_name(first_name='john', last_name='smith')
persons = ab.find_persons_by_email('john@smith.us')
persons = ab.find_persons_by_email('john')
persons = ab.find_persons_by_email('jo')
```

## Design ideas

find_persons_by_email work only with email prefix not with any part of the email
or mistaken like:

```
### will return empty set
persons = ab.find_persons_by_email('smith')
persons = ab.find_persons_by_email('john@smoth.us')
```

to makes this more it working I would use map/reruce technique with
tools like Spark, or hadoop. We would:
- map to emails
- filter by email that contains part of the text, or checking
levenshtein distance (https://en.wikipedia.org/wiki/Levenshtein_distance) for mistakes
- maping email to person by getting the person from email
- collect by getting the answers

## Tests

tests suits are in test folder to run it

```
python setup.py test
```


## Release History
+ 1.0.0 - initial final version of the application

## Author
Tomasz Górka <http://tomasz.gorka.org.pl>

## License
&copy; 2016 Tomasz Górka

MIT licensed.
