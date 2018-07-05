# -*- coding: utf-8 -*-
#
# web_scraping.py
#
# The module is part of pydavis.
#

"""
Collect weather data parameters from Davis weather stations through the
reports generated at Davis WeatherLink websites.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import time

import urllib.request

from bs4 import BeautifulSoup
from collections import OrderedDict

from dateutil.parser import parse
from pydavis.utils import _check_parameter


class WeatherLinkScraper:
    """Scraper, parser and extractor collecting Davis weather station
    parameters through Davis WeatherLink HTML data.

    Args:
        url (str): The URL reference for the Davis WeatherLink website
            displaying the weather report with target parameters.

        target_parameters (dict): The target parameter labels and corresponding
            column numbers of target parameter values as key-value pairs. The
            parameter labels should be given as they appear in the Davis
            WeatherLink report. The column number referes to the report column
            number beginning at one and counting along each row.

    """

    # In seconds.
    _SLUMBER_INTERVAL = 5

    _TIME_STAMP_ID = 'idtime'

    # Parameter units to filter from the collected parameter values.
    _REMOVABLE_UNITS = [
        '%',
        'mm',
        'mb',
        'mm/Hour',
        '/Hour',
        'km/h',
        'mb',
        'Index',
        'W/m2',
        'hPa'
    ]

    # Parameter values to be replaced by `NULL`.
    _INVALID_PARAMETER_VALUES = [
        'n/a',
        'na',
        'nan'
    ]

    @classmethod
    def add_unit(cls, unit):
        """Adds a parameter unit that will be filtered from the collected raw
        parameter values.

        Args:
            unit (str): The unit symbol that will be removed from the
                collected raw parameters.

        """

        _check_parameter('Unit', str, unit)

        cls._REMOVABLE_UNITS.append(unit)

    @classmethod
    def drop_unit(cls, unit):
        """Removes a parameter unit such that it will not be filtered from the
        collected raw parameter values.

        Args:
            unit (str): The unit symbol that will no longer be removed from the
                collected raw parameters.

        """

        _check_parameter('Unit', str, unit)

        del cls._REMOVABLE_UNITS[cls._REMOVABLE_UNITS.index(unit)]

    def __init__(self, url, target_parameters):

        self.url = url
        self.target_params = target_parameters

        # NOTE: Variables set during instance
        self._data = None
        self._stamp = None
        self._dtypes = None
        self._params = None

    @property
    def parameters(self):
        """Returns the collected weather parameters."""

        return self._params

    @property
    def data_types(self):
        """Returns the evaluated data type of each parameter."""

        return self._dtypes

    @property
    def last_logging(self):
        """Returns the time of last logging."""

        return self._stamp

    @property
    def removeable_units(self):
        """Returns units """

        return self._REMOVABLE_UNITS

    @property
    def invalid_parameter_values(self):
        """Returns parameter values that are converted to `NULL`."""

        return self._INVALID_PARAMETER_VALUES

    def fetch_html(self):
        """Collects the raw HTML data."""

        _check_parameter('url', str, self.url)

        # Request HTML file.
        try:
            html = urllib.request.urlopen(self.url).read()

        except:
            print('No connection. Retrying in {} seconds'
                  ''.format(float(self._SLUMBER_INTERVAL)))

            time.sleep(float(self._SLUMBER_INTERVAL))

            html = urllib.request.urlopen(self.url).read()

        return html

    def process_html(self, data):
        """Extract the contents from raw HTML data, in addition to removing
        whitespace and joining text line elements by underscore.

        Args:
            data (bytes): The raw HTML data.

        """

        _check_parameter('data', bytes, data)

        # Extracts contents from raw HTML.
        soup = BeautifulSoup(data, 'lxml')
        for script in soup(['script', 'style']):
            script.extract()

        contents = soup.get_text().splitlines()

        # Strips whitespace and joins line elements.
        self._data = []
        for line in contents:
            elements = line.split()

            if elements:
                self._data.append('_'.join(elements))

        return self

    def _update_timestamp(self, key=r'Current_Conditions', split_key='of'):
        # Updates the last logging time stamp reference.

        result = [element for element in self._data if key in element]

        raw_stamp_data = result[0].split(split_key)[1].replace('_', '')

        # Attempts converting raw stamp data to time stamp format.
        try:
            self._stamp = parse(raw_stamp_data)
        except:
            self._stamp = str(raw_stamp_data)

        return self

    def collect_parameters(self, html=None):
        """Extracts parameter values and data types from HTML data according to
        specified target parameter labels."""

        if not html:
            html = self.fetch_html()

        # Append elements to _data.
        self.process_html(html)

        # Assign to _stamp.
        self._update_timestamp()

        # Insert into _params and _dtypes.
        self._extract_parameters()

    def _extract_parameters(self):
        # Collects parameter values and dtypes from HTML data.

        self._params, self._dtypes = OrderedDict(), OrderedDict()

        target_parameters = list(self.target_params.keys())

        # Add time of parameter collection as key.
        self._params[self._TIME_STAMP_ID] = self._stamp
        self._dtypes[self._TIME_STAMP_ID] = type(self._stamp)

        for loc, element in enumerate(self._data):

            if element in target_parameters:
                self._include_element(loc, element)

        return self

    def _include_element(self, loc, parameter):
        # Add parameter value and dtype to _params and _dtypes.

        item = self._data[loc + self.target_params[parameter]]

        value_label = item.split('_')[0]

        if value_label in self._INVALID_PARAMETER_VALUES:
            value_label = 'NULL'
        else:
            for unit_label in self._REMOVABLE_UNITS:
                value_label = value_label.replace(str(unit_label), '')

        try:
            param_value = eval(value_label)
        except:
            param_value = str(value_label)

        self._params[parameter] = param_value
        self._dtypes[parameter] = type(param_value)

        return self
