# -*- coding: utf-8 -*-
#
# db_manager.py
#
# The module is part of pydavis.
#

"""
Interacting with MySQL databases through the DatabaseManager.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import pymysql

from pydavis import utils
from datetime import datetime


class DatabaseManager:
    """Handles interaction with MySQL database.

    Args:
         user (str): Follows from writing data to table. The MySQL username
             credential. Necessary for connecting to database.

         password (str): Follows from writing data to table. The MySQL
             password credential. Necessary for connecting to database.

         host (str): Specifies the host where the server is running. Uses
             localhost by default.

         port (int): Specifies port number. Uses 3306 by default.

         database (str): Follows from writing data to table. Name of an
             existing database, or the name of a database that will be created.

    """

    _CHARS_LIMIT = 20

    @classmethod
    def update_limit_varchars(cls, new_limit):
        """Defines the maximum number of characters assigned to string
        attributes in the created database tables.

        Args:
            new_limit (int): The maximum number of characters assigned to
                string attributes.

        """

        utils._check_parameter('new_limit', int, new_limit)

        cls._CHARS_LIMIT = new_limit

    def __init__(self, user, password, host='localhost', port=3306):

        self.user = str(user)
        self.password = str(password)
        self.host = str(host)
        self.port = int(port)

        # NOTE: Variables set during instance.
        self._con = None
        self._cur = None
        self._query = None
        self._current_db = None

    @property
    def connection(self):
        """Returns database connection."""

        return self._con

    @property
    def current_db(self):
        """Returns name of working database."""

        return self._current_db

    @property
    def query(self):
        """Returns the latest MySQL query ready to be executed."""

        return self._query

    @property
    def results(self):
        """Returns the result from a database query."""

        return self._cur.fetchall()

    @property
    def limit_varchars(self):
        """Returns the current limit to number of characters in varchar
        variables."""

        return self._CHARS_LIMIT

    def connect(self):
        """Connects to a MySQL server."""

        if self.connection:
            print('Already connected to `{}`'.format(self.host))

            return

        try:
            con = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.password)

            print('Connecting to: `{}`'.format(self.host))

            self._con = con
            self._cur = self._con.cursor()

        except:
            raise utils.DatabaseConnectionError('Unable to connect to: `{}`'
                                                ''.format(self.host))

        return self

    def _check_connection(self):
        # Checks if connected to a MySQL server.

        if self.connection:
            return
        else:
            raise utils.DatabaseConnectionError('Disconnected from {}'
                                                ''.format(self.host))

    def _check_database(self):

        if self.current_db:
            return
        else:
            raise utils.MissingDatabaseError('Must specify working database')

    def execute(self):
        """Execute a MySQL command and commit changes to the database."""

        self._check_connection()

        try:
            self._cur.execute(self._query)
        except:
            raise utils.DatabaseExecutionError('Unable to execute query:\n'
                                               '`{}`'.format(self._query))

        # Commit changes to database.
        try:
            self._con.commit()
        except:
            raise utils.DatabaseCommitError('Unable to commit changes: `{}`'
                                            ''.format(self._db_name))

        return self

    def create_database(self, database):
        """Creates a new database. Only enabled if connected to a MySQL server.

        Args:
            database (str): Name of the database to create.

        """

        utils._check_parameter('database', str, database)

        self._current_db = database

        self._query = 'CREATE DATABASE IF NOT EXISTS {};'.format(database)

        return self

    def use_database(self, database):
        """Selects an existent database as working database. Only enabled if
        connected to a MySQL server and the database exists.

        Args:
            database (str): Name of the new working database.

        """

        utils._check_parameter('database', str, database)

        self._current_db = database

        self._query = 'USE {}'.format(database)

        return self

    def drop_database(self, database):
        """Deletes a database. Only enabled if connected to a MySQL server.

        Args:
            database (str): Name of the database to delete.

        """

        utils._check_parameter('database', str, database)

        # Resetting working DB variable.
        self._current_db = None

        self._query = 'DROP DATABASE IF EXISTS {};'.format(database)

        return self

    def create_table(self, table_name, table_columns):
        """Creates a table if connected to a MySQL server and a working
        database is set.

        Args:
            table_name (str): Name of the new table.

            table_columns (dict): The column labels and corresponding column
                data types as key-value pairs. The data types are given in
                Python format.

        """

        self._check_database()
        utils._check_parameter('table_name', str, table_name)
        utils._check_parameter('table_columns', dict, table_columns)

        col_labels, col_dtypes = list(zip(*table_columns.items()))

        mysql_dtypes = self.convert_dtypes(col_dtypes)

        _columns = ''
        for label, dtype in zip(col_labels[:-1], mysql_dtypes[:-1]):
            _columns += ' {} {},'.format(label, dtype)

        _columns += ' {} {}'.format(col_labels[-1], mysql_dtypes[-1])

        self._query = """CREATE TABLE IF NOT EXISTS {} ({});
                      """.format(table_name, _columns)

        return self

    def convert_dtypes(self, data_types):
        """Converts from Python to MySQL data types.

        Args:
            data_types (iterable): A container of Python data types that will
                be converted to MySQL data types.

        Returns:
            list: The corresponding MySQL data types.

        """

        mysql_dtypes = []
        for data_type in data_types:

            if data_type is datetime:
                mysql_dtypes.append('DATETIME')

            elif data_type is float:
                mysql_dtypes.append('FLOAT')

            elif data_type is int:
                mysql_dtypes.append('INT')

            elif data_type is str:
                mysql_dtypes.append('VARCHAR({})'.format(self._CHARS_LIMIT))

            else:
                raise TypeError('Unable to recognize {} as data type'
                                ''.format(data_type))

        return mysql_dtypes

    def drop_table(self, table_name):
        """Deletes specified table from database. Only enabled if connected to
        a MySQL server and a working database is set.

        Args:
            table_name (str): Name of the table.

        """

        self._check_database()
        utils._check_parameter('table_name', str, table_name)

        self._query = 'DROP TABLE IF EXISTS {};'.format(table_name)

        return self

    def describe_table(self, table_name):
        """Returns description of table content. Only enabled if connected to a
        MySQL server and a working database is set.

        Args:
            table_name (str): Name of the table.

        """

        self._check_database()
        utils._check_parameter('table_name', str, table_name)

        self._query = 'DESCRIBE {};'.format(table_name)

        return self

    def insert_values(self, table_name, table_values):
        """Inserts entities into a table.

        Args:
            table_name (str): The name of the table.

            table_values (dict): The column labels and corresponding values as
                key-value pairs.

        """

        self._check_database()
        utils._check_parameter('table_name', str, table_name)
        utils._check_parameter('table_values', dict, table_values)

        labels, values = list(zip(*table_values.items()))

        _columns, _values = '', ''
        for label, value in zip(labels[:-1], values[:-1]):

            _columns += "{}, ".format(str(label))
            _values += "'{}', ".format(str(value))

        _columns += "{}".format(str(labels[-1]))
        _values += "'{}'".format(str(values[-1]))

        self._query = """INSERT INTO {} ({}) VALUES ({});
                      """.format(table_name, _columns, _values)

        return self

    def add_constraints(self, table_name, constraints):

        raise NotImplementedError('Method currently not implemented.')

    def terminate_connection(self):
        """Shuts down connection to MySQL server."""

        self._con.close()
        self._cur.close()

        print('Shutting down connection to: `{}`'.format(self.host))

        # NOTE: Resetting connection variables.
        self._con = None
        self._cur = None

        return self
