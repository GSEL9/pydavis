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
DESCRIPTION = "Tools to stream weather data from Davis weather stations."
VERSION = '0.1.3'
KEYWORDS = 'web scraping, database, weather data'
EXCLUDE = ['tests', 'docs', 'build']
TESTS_REQUIRE = ['pytest', 'pytest_mock', 'nose']


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
        author="Severin Langberg",
        author_email="Langberg91@gmail.com",
        description=DESCRIPTION,
        url='https://github.com/GSEL9/pydavis',
        install_requires=requirements(),
        long_description=readme(),
        license=license(),
        name=MAIN_PACKAGE,
        version=VERSION,
        packages=find_packages(exclude=EXCLUDE),
        setup_requires=['pytest-runner'],
        tests_require=TESTS_REQUIRE,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ]
    )


if __name__ == '__main__':

    package_setup()
