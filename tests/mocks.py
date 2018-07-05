# -*- coding: utf-8 -*-
#
# mocks.py
#
# The module is part of pydavis.
#

"""
Mocks for test purposes.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


class MockCreateDB:
    """Mocking a create database MySQL query."""

    def __init__(self, name):

        self.query = 'CREATE DATABASE IF NOT EXISTS {};'.format(name)

    def __call__(self):

        return self.query


class MockUseDB:
    """Mocking a use database MySQL query."""

    def __init__(self, name):

        self.query = 'USE {}'.format(name)

    def __call__(self):

        return self.query


class MockDropDB:
    """Mocking a drop database MySQL query."""

    def __init__(self, name):

        self.query = 'DROP DATABASE IF EXISTS {};'.format(name)

    def __call__(self):

        return self.query


class MockCreateTable:
    """Mocking a create table MySQL query."""

    def __init__(self, table_name, labels, dtypes):

        self.table_name = table_name
        self.labels = labels
        self.dtypes = dtypes

    def __call__(self):

        return self._construct_query()

    def _construct_query(self):
        # Generates create table MySQL query.

        _columns = ''
        for label, dtype in zip(self.labels[:-1], self.dtypes[:-1]):
            _columns += ' {} {},'.format(label, dtype)

        _columns += ' {} {}'.format(self.labels[-1], self.dtypes[-1])

        return """CREATE TABLE IF NOT EXISTS {} ({});
               """.format(self.table_name, _columns)


class MockDropTable:
    """Mocking a drop table MySQL query."""

    def __init__(self, name):

        self.query = 'DROP TABLE IF EXISTS {};'.format(name)

    def __call__(self):

        return self.query


class MockDescribeTable:
    """Mocking a describe table MySQL query."""

    def __init__(self, name):

        self.query = 'DESCRIBE {};'.format(name)

    def __call__(self):

        return self.query


class MockInsertValues:
    """Mocking a insert into table MySQL query."""

    def __init__(self, table_name, labels, values):

        self.table_name = table_name
        self.labels = labels
        self.values = values

    def __call__(self):

        return self._construct_query()

    def _construct_query(self):
        # Generates insert into table MySQL query.

        _columns, _values = '', ''
        for label, value in zip(self.labels[:-1], self.values[:-1]):

            _columns += "{}, ".format(str(label))
            _values += "'{}', ".format(str(value))

        _columns += "{}".format(str(self.labels[-1]))
        _values += "'{}'".format(str(self.values[-1]))

        return """INSERT INTO {} ({}) VALUES ({});
               """.format(self.table_name, _columns, _values)


class MockWebScraper:
    """Mocking a WeatherLinkScraper instance."""

    _keys = ['KeyA', 'KeyB', 'KeyC']
    _values = [1, 2, 3]

    def __init__(self, keys=None, values=None):

        if keys is None:
            self.keys = self._keys
        else:
            self.keys = keys

        if values is None:
            self.values = self._values
        else:
            self.values = values

    @property
    def parameters(self):
        """Returns a dict of parameters."""

        return dict(zip(self.keys, self.values))

    def __call__(self):

        return self.collect_parameters()

    def collect_parameters(self):
        """Returns a dict of parameters."""

        return self.parameters
