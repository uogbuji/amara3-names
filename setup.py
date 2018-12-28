#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Note: careful not to conflate install_requires with requirements.txt

https://packaging.python.org/discussions/install-requires-vs-requirements/

Reluctantly use setuptools to get install_requires & long_description_content_type
'''

import sys
#from setuptools import setup
from distutils.core import setup

PROJECT_NAME = 'amara3.names'
PROJECT_DESCRIPTION = 'Tools to handle human names (and organization names). Credit to https://www.github.com/rliebz/whoswho by Robert Liebowitz <rliebz@gmail.com> (MIT License)',
PROJECT_LICENSE = 'License :: OSI Approved :: Apache Software License'
PROJECT_AUTHOR = 'Uche Ogbuji'
PROJECT_AUTHOR_EMAIL = 'uche@ogbuji.net'
PROJECT_MAINTAINER = 'Zepheira'
PROJECT_MAINTAINER_EMAIL = 'uche@zepheira.com'
PROJECT_URL = 'http://zepheira.com/'
PACKAGE_DIR = {'amara3.names': 'pylib'}
PACKAGES = [
    'amara3.names',
    'amara3.names.config',
]
SCRIPTS = [
#    'exec/marc2bf',
]

CORE_REQUIREMENTS = [
    'amara3-iri',
    'nameparser',
    'pytest',
]

# From http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Intended Audience :: Developers',
    "Intended Audience :: Information Technology",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing :: Linguistic',
    "Topic :: Text Processing :: Indexing",
    #"Development Status :: 5 - Production/Stable",
]

KEYWORDS=['naturallanguage', 'name', 'match', 'parser']

version_file = 'pylib/version.py'
exec(compile(open(version_file, "rb").read(), version_file, 'exec'), globals(), locals())
__version__ = '.'.join(version_info)

LONGDESC = '''amara3.names

Tools to parse human (and eventually organization) names, compare them, etc.

Requires Python 3.5+. To install:

    python setup.py install


# Acknowledgments

The seeds of the code was from [whoswho 0.1.2](https://pypi.org/project/whoswho/)
Also incorporates refactored code from [nameparser 1.0.2](https://pypi.org/project/nameparser/)

See also:

* https://github.com/gwu-libraries/namesparser


'''

LONGDESC_CTYPE = 'text/markdown',

setup(
    name=PROJECT_NAME,
    version=__version__,
    description=PROJECT_DESCRIPTION,
    license=PROJECT_LICENSE,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_AUTHOR_EMAIL,
    maintainer=PROJECT_MAINTAINER,
    maintainer_email=PROJECT_MAINTAINER_EMAIL,
    url=PROJECT_URL,
    package_dir=PACKAGE_DIR,
    packages=PACKAGES,
    scripts=SCRIPTS,
    install_requires=CORE_REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=LONGDESC,
    long_description_content_type=LONGDESC_CTYPE,
    keywords=KEYWORDS,
)
