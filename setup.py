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

AUTHOR = 'Severin Langberg'
EMAIL = 'Langberg91@gmail.com'

MAIN_PACKAGE = 'pydavis'
VERSION = '0.2.0'
DESCRIPTION = "Tools to stream weather data from Davis weather stations."
URL = 'https://github.com/GSEL9/pydavis'

TESTS_REQUIRE = ['pytest', 'pytest_mock', 'nose']

KEYWORDS = ['data science', 'data analytics', 'web scraping', 'database',
            'weather data', 'data collection']

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Environment :: Console',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Programming Language :: Python :: 3',
               'Topic :: Scientific/Engineering :: Chemistry',
               'Topic :: Scientific/Engineering :: Physics']


def readme():
    """Return the contents of the README.rst file."""

    with open('./README.rst') as freadme:
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

    setup(
        author=AUTHOR,
        author_email=EMAIL,
        description=DESCRIPTION,
        url=URL,
        install_requires=requirements(),
        long_description=readme(),
        license=license(),
        name=MAIN_PACKAGE,
        keywords=KEYWORDS,
        version=VERSION,
        packages=find_packages(exclude=['tests', 'tests.*']),
        setup_requires=['pytest-runner'],
        tests_require=TESTS_REQUIRE,
        classifiers=CLASSIFIERS
    )


if __name__ == '__main__':

    package_setup()
