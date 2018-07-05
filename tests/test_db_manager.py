# -*- coding: utf-8 -*-
#
# test_db_manager.py
#
# The module is part of pydavis.
#

"""
Testing of DatabaseManager.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import pytest

import nose.tools as ntools

import mocks
from datetime import datetime
from pytest_mock import mocker

from pydavis import utils
from pydavis import DatabaseManager


class TestDatabaseManager:
    """Testing the DatabaseManager."""

    testing_class = DatabaseManager

    @pytest.fixture
    def manager(self):
        """Returns a database manager instance for test purposes."""

        return self.testing_class('test', 'test')

    def test_update_limit_varchars(self, manager):
        """Test changing the character limit of carchar variables."""

        test_limit = 30

        with pytest.raises(AssertionError):
            ntools.eq_(manager.limit_varchars, test_limit)

        manager.update_limit_varchars(test_limit)

        ntools.eq_(manager.limit_varchars, test_limit)

    def test_init_status(self, manager):
        """Tests initial status of attributes."""

        attributes = [manager.connection, manager.current_db, manager.query]

        assert all(attribute is None for attribute in attributes)

    def test_connection(self, manager, mocker):
        """Test no error is raised if existing connetion."""

        # Mocking a connection.
        mocker.patch('pydavis.db_manager.DatabaseManager.connection',
                     'test_connection')

        manager.connect()

    def test_no_connection(self, manager):
        """Tests if error is raised should if no connection exists."""

        with pytest.raises(utils.DatabaseConnectionError):
            manager.connect()

        with pytest.raises(utils.DatabaseConnectionError):
            manager.execute()

    def test_no_database(self, manager):
        """Tests if error is raised should no working database be set."""

        with pytest.raises(utils.MissingDatabaseError):
            manager.create_table('test', 'test')

        with pytest.raises(utils.MissingDatabaseError):
            manager.drop_table('test')

        with pytest.raises(utils.MissingDatabaseError):
            manager.describe_table('test')

        with pytest.raises(utils.MissingDatabaseError):
            manager.insert_values('test', 'test')

    def test_invalid_args(self, manager, mocker):
        """Tests if error is raised as invalid arguments are passed."""

        # Mocking a working database
        mocker.patch('pydavis.db_manager.DatabaseManager.current_db', 'test')

        invalid_args = [1, 1.0, {}, [], (), None, False, True]

        for invalid_arg in invalid_args:

            with pytest.raises(TypeError):

                manager.create_database(invalid_arg)
                manager.use_database(invalid_arg)
                manager.drop_database(invalid_arg)

                manager.create_table(invalid_arg, invalid_arg)
                manager.insert_values(invalid_arg, invalid_arg)
                manager.create_table('', invalid_arg)
                manager.insert_values('', invalid_arg)

                manager.drop_table(invalid_arg)
                manager.describe_table(invalid_arg)

    def test_create_database(self, manager):
        """Test database creation query."""

        # Mocking query.
        target_query = mocks.MockCreateDB('test')

        manager.create_database('test')

        ntools.eq_(manager.query, target_query())

    def test_use_database(self, manager):
        """Test use database query."""

        # Mocking query.
        target_query = mocks.MockUseDB('test')

        manager.use_database('test')

        ntools.eq_(manager.query, target_query())

    def test_drop_database(self, manager):
        """Test drop database query."""

        # Mocking query.
        target_query = mocks.MockDropDB('test')

        manager.drop_database('test')

        ntools.eq_(manager.query, target_query())

    def test_create_table(self, manager, mocker):
        """Test table creation query."""

        # Mocking a working database
        mocker.patch('pydavis.db_manager.DatabaseManager.current_db', 'test')

        # Mocking query.
        target_query = mocks.MockCreateTable(
            'test', ['ColA', 'ColB', 'ColC'],
            ['INT', 'FLOAT', 'VARCHAR({})'.format(manager.limit_varchars)]
        )

        manager.create_table('test', {'ColA': int, 'ColB': float, 'ColC': str})

        ntools.eq_(manager.query.strip(), target_query().strip())

    def test_convert_dtypes(self, manager):
        """Test conversion of Python data types to MySQL data types."""

        target_dtypes = [
            'INT', 'FLOAT', 'DATETIME',
            'VARCHAR({})'.format(manager.limit_varchars)
        ]

        valid_dtypes = [int, float, datetime, str]

        transformed_dtypes = manager.convert_dtypes(valid_dtypes)

        for target, transformed in zip(target_dtypes, transformed_dtypes):
            ntools.eq_(target, transformed)

        with pytest.raises(TypeError):
            manager.convert_dtypes[()]
            manager.convert_dtypes[[]]

    def test_drop_table(self, manager, mocker):
        """Test drop table query."""

        # Mocking a working database
        mocker.patch('pydavis.db_manager.DatabaseManager.current_db', 'test')

        # Mocking query.
        target_query = mocks.MockDropTable('test')

        manager.drop_table('test')

        ntools.eq_(manager.query, target_query())

    def test_describe_table(self, manager, mocker):
        """Test describe table query."""

        # Mocking a working database
        mocker.patch('pydavis.db_manager.DatabaseManager.current_db', 'test')

        # Mocking query.
        target_query = mocks.MockDescribeTable('test')

        manager.describe_table('test')

        ntools.eq_(manager.query, target_query())

    def test_insert_values(self, manager, mocker):
        """Test insertin into table query."""

        # Mocking a working database
        mocker.patch('pydavis.db_manager.DatabaseManager.current_db', 'test')

        # Mocking query.
        target_query = mocks.MockInsertValues(
            'test', ['ColA', 'ColB', 'ColC'], ['1', '2', '3']
        )

        manager.insert_values('test', {'ColA': 1, 'ColB': 2, 'ColC': 3})

        ntools.eq_(manager.query.strip(), target_query().strip())
