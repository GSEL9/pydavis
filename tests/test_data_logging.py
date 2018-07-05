# -*- coding: utf-8 -*-
#
# test_data_logging.py
#
# The module is part of pydavis.
#

"""
Testing of DataLogger.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import os
import mocks
import pytest

import nose.tools as ntools

from pytest_mock import mocker
from pydavis import DataLogger


class TestDataLogger:
    """Testing the DataLogger."""

    testing_class = DataLogger

    logger = None
    orig_parameters = None

    def setup(self):
        """Executed before each test."""

        logger = self.testing_class('')

        self.orig_parameters = {
            'separator': logger.separator,
            'newline': logger.newline,
            'slumber_interval': logger.slumber_interval,
            'target_labels': logger.target_parameters,
            'target_values': logger.target_value_locations
        }

        self.logger = logger

    def teardown(self):
        """Executed after each test."""

        self.testing_class.update_separator(
            self.orig_parameters['separator']
        )
        self.testing_class.update_newline(
            self.orig_parameters['newline']
        )
        self.testing_class.update_slumber_interval(
            self.orig_parameters['slumber_interval']
        )

        keys = self.orig_parameters['target_labels']
        values = self.orig_parameters['target_values']

        self.testing_class.drop_parameters(self.logger.target_parameters)

        self.testing_class.add_parameters(dict(zip(keys, values)))

        for (key, value) in zip(keys, values):
            self.testing_class.update_target_value(key, value)

        self.logger, self.orig_parameters = None, None

    def _logger_ref(self, add_on):
        # Creates a reference to the DataLogger class for patching.

        base = 'pydavis.data_logging.DataLogger'

        return ('.').join((base, add_on))

    def test_add_parameters(self):
        """Test including additional target parameters."""

        test_param, test_value = 'Snow_Depth', 10

        assert test_param not in self.logger.target_parameters
        assert test_value not in self.logger.target_value_locations

        self.testing_class.add_parameters({test_param: test_value})

        assert test_param in self.logger.target_parameters
        assert test_value in self.logger.target_value_locations

    def test_drop_parameters(self):
        """Test removing target parameters."""

        test_param = 'Outside_Temp'

        assert test_param in self.logger.target_parameters

        self.testing_class.drop_parameters([test_param])

        assert test_param not in self.logger.target_parameters

    def test_update_target_value(self):
        """Test selecting a different logging value for any given parameter."""

        target_param = 'Outside_Temp'
        orig_target, new_target = 1, 10

        ntools.eq_(self.logger.target_params[target_param], orig_target)

        self.testing_class.update_target_value(target_param, new_target)

        ntools.eq_(self.logger.target_params[target_param], new_target)

    def test_update_slumber_interval(self):
        """Test defining the slumber interval."""

        orig_interval, new_interval = 20, 30

        ntools.eq_(self.logger.slumber_interval, orig_interval)

        self.testing_class.update_slumber_interval(new_interval)

        ntools.eq_(self.logger.slumber_interval, new_interval)

    def test_separator(self):
        """test altering the separator symbol."""

        ntools.eq_(self.logger.separator, ';')

        self.testing_class.update_separator(',')

        ntools.eq_(self.logger.separator, ',')

    def test_newline(self):
        """Test altering the newline character."""

        # Check default setting.
        ntools.eq_(self.logger.newline, '\n')

        self.testing_class.update_newline('\\')

        ntools.eq_(self.logger.newline, '\\')

    def test_init_status(self):
        """Tests initial status of attributes."""

        attributes = [
            self.logger.last_logging, self.logger.web_scraper,
            self.logger.db_manager, self.logger.current_db,
            self.logger.path_to_file
        ]

        assert (attribute is None for attribute in attributes)

    def test_no_web_scraper(self):
        """Test error is raised if trying to update data without a web scraper
        instance."""

        with pytest.raises(RuntimeError):
            self.logger.update_data()

    def test_update_data(self, mocker):
        """Test parameter collection."""

        # Mocking a web scraper instance.
        mocker.patch(self._logger_ref('web_scraper'), mocks.MockWebScraper())

        self.logger.update_data()

    def test_write_to_file(self, mocker):
        """Creates a test file, writes mocked data and deletes the file."""

        test_path = './test.csv'

        # Mocking a path to file.
        mocker.patch(self._logger_ref('path_to_file'), test_path)

        # Mocking a web scraper instance.
        mocker.patch(self._logger_ref('web_scraper'), mocks.MockWebScraper())

        self.logger.update_data()
        self.logger.write_to_file()

        # Clean up
        os.remove(test_path)
