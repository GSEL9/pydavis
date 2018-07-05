# -*- coding: utf-8 -*-
#
# setup.py
#
# This module is part of pydavis.
#

"""
Setup script for pydavis.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


from setuptools import setup, find_packages

MAIN_PACKAGE = 'pydavis'
DESCRIPTION = 'Tools to stream weather data from Davis weather stations.'
LICENSE = "MIT"
URL = 'https://github.com/GSEL9/pydavis'
AUTHOR = 'Severin Langberg'
EMAIL = 'langberg91@gmail.com'
VERSION = '0.1.1'

TESTS_REQUIRE = ['pytest', 'pytest_mock', 'nose']

KEYWORDS = ['data science', 'data analytics', 'web scraping', 'database',
            'weather data', 'data collection', 'davis']

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Environment :: Console',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Programming Language :: Python :: 3']


def readme():
    """Return the contents of the README.rst file."""

    with open('README.rst') as freadme:
        return freadme.read()


def requirements():
    """Return the contents of the REQUIREMENTS.txt file."""

    with open('REQUIREMENTS.txt', 'r') as freq:
        return freq.read().splitlines()


def license():
    """Return the contents of the LICENSE.txt file."""

    with open('LICENSE.txt') as flicense:
        return flicense.read()


def package_setup():

    setup(name=MAIN_PACKAGE,
          version=VERSION,
          url=URL,
          description=DESCRIPTION,
          author=AUTHOR,
          author_email=EMAIL,
          include_package_data=True,
          install_requires=requirements(),
          keywords=KEYWORDS,
          license=LICENSE,
          long_description=readme(),
          classifiers=CLASSIFIERS,
          packages=find_packages(exclude=['tests', 'tests.*']),
          setup_requires=['pytest-runner'],
          tests_require=TESTS_REQUIRE,
          )

if __name__ == '__main__':

    package_setup()
