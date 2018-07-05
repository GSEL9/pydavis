# -*- coding: utf-8 -*-
#
# data_logging.py
#
# The module is part of pydavis.
#

"""
The DataLogger collects and stores weather data from Davis weather stations
through Davis WeatherLink.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import os
import time

from pydavis.utils import _check_parameter
from pydavis.db_manager import DatabaseManager
from pydavis.web_scraping import WeatherLinkScraper


class DataLogger:
    """Logg weather data parameters monitored by Davis weather stations. The
    parameters are obtained through the reports generated at Davis WeatherLink
    websites, and can be streamed to a MySQL database or a file.

    Args:
        url (str): The URL reference for the Davis WeatherLink website
            displaying the weather report with target parameters.

        target_parameters (dict): The target parameter labels and
            corresponding column numbers of target parameter values as
            key-value pairs. The parameter labels should be given as they
            appear in the Davis WeatherLink report. The column number referes
            to the report column number beginning at one and counting  along
            each row.

    """

    # Default target parameters with corresponding column index specifying
    # target value.
    _TARGET_PARAMETERS = {
        'Outside_Temp': 1,
        'Inside_Temp': 1,
        'Outside_Humidity': 1,
        'Inside_Humidity': 1,
        'Wind_Gust_Speed': 1,
        'Wind_Speed': 2,
        'Wind_Chill': 1,
        'Heat_Index': 1,
        'Dew_Point': 1,
        'Year': 2,
        'UV_Radiation': 1,
        'Solar_Radiation': 1,
        'Barometer': 1,
        'Bar_Trend': 1
    }

    # In seconds.
    _SLUMBER_INTERVAL = 20

    # Default items separator and new line character when writing to file.
    _SEPARATOR = ';'
    _NEWLINE = '\n'

    @classmethod
    def add_parameters(cls, target_parameters):
        """Include additional target parameters.

        Args:
            target_parameters (dict): The target parameter labels and
                corresponding column numbers of target parameter values as
                key-value pairs. The parameter labels should be given as they
                appear in the Davis WeatherLink report. The column number
                referes to the report column number beginning at one and
                counting along each row.

        Example:

            Collecting the amount of rain for the last hour. The parameter
            label is given as `Last_Hour_rain`, and the target value is
            located at column number one as `Rate` (mm/hour). Thus,

            >>> DataLogger.add_parameters({'Last_Hour_rain': 1})

        """

        _check_parameter('target_parameters', dict, target_parameters)

        for (key, value) in target_parameters.items():

            _check_parameter('key', str, key)
            _check_parameter('value', int, value)

            cls._TARGET_PARAMETERS[key] = value

    @classmethod
    def drop_parameters(cls, parameter_labels):
        """Remove target parameters.

        Args:
            parameter_labels (iterable of str): The labels of each parameter
                that will be excluded from the target parameters.

        Example:

            Dropping the default target parameter `Year`:

            >>> DataLogger.drop_parameters(['Year'])

        """

        _check_parameter('parameter_labels', (list, tuple),
                             parameter_labels)

        for parameter_label in parameter_labels:
            _check_parameter('parameter_label', str, parameter_label)

            del cls._TARGET_PARAMETERS[parameter_label]

    @classmethod
    def update_target_value(cls, parameter, column_number):
        """Select a different logging value for any given parameter.

        Args:
            parameter (str): The target parameter label.

            column_number (int): The new reference to the target value.

        Example:

            Collecting `Today's Highs` values rather than `Current` values of
            the outside temperature requires changing the target value column
            number fron 1 to 2. Thus,

            >>> DataLogger.update_target_value('Outside_Temp', 2)

        """

        _check_parameter('parameter', str, parameter)
        _check_parameter('column_number', int, column_number)

        cls._TARGET_PARAMETERS[parameter] = column_number

    @classmethod
    def update_slumber_interval(cls, slumber_interval):
        """Define the amount of time (in seconds) that is passed between each
        attempt to collect parameters from the Davis WeatherLink website.

        Args:
            slumber_interval (int): The slumber interval time in seconds.

        """

        _check_parameter('slumber_interval', int, slumber_interval)

        cls._SLUMBER_INTERVAL = slumber_interval

    @classmethod
    def update_separator(cls, separator):
        """Define the symbol used to seraprate items when writing to file.

        Args:
            separator (str): The symbol used to separate items when writing to
                file.

        """

        _check_parameter('separator', str, separator)

        cls._SEPARATOR = separator

    @classmethod
    def update_newline(cls, newline):
        """Define the symbol used as newline character when writing to file.

        Args:
            newline (str): The symbol used as newline character when writing to
                file.

        """

        _check_parameter('newline', str, newline)

        cls._NEWLINE = newline

    def __init__(self, url, target_parameters=None):

        self.url = str(url)

        if target_parameters:
            self.target_params = target_parameters
        else:
            self.target_params = self._TARGET_PARAMETERS

        # NOTE: Variables set from instance.
        self._stamp = None
        self._web_scraper = None
        self._param_labels = None
        self._param_values = None

        self._path_to_file = None

        self._db_manager = None
        self._current_db = None
        self._table = None

    @property
    def last_logging(self):
        """Returns time of last logging parameters."""

        return self._stamp

    @property
    def web_scraper(self):
        """Returns the web scraper."""

        return self._web_scraper

    @property
    def db_manager(self):
        """Returns the database manager."""

        return self._db_manager

    @property
    def current_db(self):
        """Returns the working database label."""

        return self._current_db

    @property
    def separator(self):
        """Returns the symbol used as value separator when writing to file."""

        return self._SEPARATOR

    @property
    def newline(self):
        """Returns the symbol used as newline character when writing to file."""

        return self._NEWLINE

    @property
    def slumber_interval(self):
        """Returns the slumber interval."""

        return self._SLUMBER_INTERVAL

    @property
    def path_to_file(self):
        """Returns path to file in case of writing to file."""

        return self._path_to_file

    @property
    def target_parameters(self):
        """Returns target parameter labels."""

        return list(self.target_params.keys())

    @property
    def target_value_locations(self):
        """Returns the column indices of target parameter values."""

        return list(self.target_params.values())

    def initiate_logging(self, to_table=False, to_file=False, **kwargs):
        """Stream weather data parameters monitored by Davis weather stations
        to a MySQL database or a file.

        NOTE: Abort logging with CTRL + C.

        Kwargs:
            to_table (bool): Stores in a MySQL database table if True.

            user (str): The MySQL username credential.

            password (str): The MySQL password credential.

            host (str): Specifies the host where the server is running. Uses
                localhost by default.

            port (int): Specifies port number. Uses port 3306 by default.

            database (str): The name the database where data is stored. Creates
                new database if not already existing.

            table (str): The name of database table where data is stored.
                Creates new table if not already existing.

            to_file (bool): Writes data to file if True.

            path_to_file (str): Location of existing file, or where a new file
                will be created.

        Example:

            Logging default parameters to MySQL table:

            >>> logger = DataLogger(url)
            >>> logger.initiate_logging(to_table=True,
                                        user='user',
                                        password='password',
                                        database='davis',
                                        table='station_wsid')

            Initiate logging to CSV file:

            >>> logger.initiate_logging(to_file=True,
                                   file_path='./weather_data.csv')

        """

        if self.web_scraper is None:
            self._web_scraper = WeatherLinkScraper(self.url, self.target_params)

        if to_table:
            self._inspect_db_setup(**kwargs)

        if to_file:
            self._inspect_file_setup(**kwargs)

        while True:
            self.update_data()

            print('Collected data at {}'.format(self.web_scraper.last_logging))

            if self.last_logging != self.web_scraper.last_logging:

                if to_file:
                    self.write_to_file()

                if to_table:
                    self.write_to_table()

                self._stamp = self.web_scraper.last_logging

            time.sleep(float(self.slumber_interval))

    def update_data(self):

        if self.web_scraper is None:
            raise RuntimeError('No web scraper instantiated')

        self.web_scraper.collect_parameters()

        self._param_labels = list(self.web_scraper.parameters.keys())
        self._param_values = list(self.web_scraper.parameters.values())

        return self

    def _inspect_db_setup(self, **kwargs):
        # Connects to MySQL server and sets working database.

        self._table = str(kwargs['table'])
        self._current_db = str(kwargs['database'])

        try:
            host, port = str(kwargs['host']), int(kwargs['port'])
        except:
            host, port = 'localhost', 3306

        if self.db_manager is None:
            self._db_manager = DatabaseManager(str(kwargs['user']),
                                               str(kwargs['password']),
                                               host, port)
            self.db_manager.connect()

        try:
            self.db_manager.use_database(self.current_db).execute()

        except:
            self.db_manager.create_database(self.current_db).execute()
            self.db_manager.use_database(self.current_db).execute()

            print('Created database: `{}`'.format(self._current_db))

    def _inspect_file_setup(self, **kwargs):
        # Check for existing file.

        self._path_to_file = str(kwargs['path_to_file'])

        if os.path.isfile(self.path_to_file):

            return

        else:
            # Collect initial parameters.
            self.update_data()

            file_header = self.separator.join(self._param_labels)

            with open(self.path_to_file, 'w') as outfile:
                outfile.write(file_header)
                outfile.write(self.newline)
                outfile.flush()

            print('Created file: `{}`'.format(self.path_to_file))

            time.sleep(1)

            return

    def write_to_table(self):
        # Writes data to table.

        try:
            self.db_manager.insert_values(
                self._table, self.web_scraper.parameters
            )
            self.db_manager.execute()

        except:
            self.db_manager.create_table(
                self._table, self.web_scraper.data_types
            )
            self.db_manager.execute()

            print('Created table: `{}`'.format(self._table))

            self.db_manager.insert_values(
                self._table, self.web_scraper.parameters
            )
            self.db_manager.execute()

        print('Writing to table: `{}`'.format(self._table))

        return self

    def write_to_file(self):
        # Writes data to file.

        file_data = self.separator.join(str(value)
                                        for value in self._param_values)

        # NOTE: Context manager `a` appends to file.
        with open(self.path_to_file, 'a') as outfile:
            outfile.write(file_data)
            outfile.write(self.newline)
            outfile.flush()

        print('Writing to file: `{}`'.format(self.path_to_file))

        time.sleep(1)

        return self
