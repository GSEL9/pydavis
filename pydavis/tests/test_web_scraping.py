# -*- coding: utf-8 -*-
#
# test_web_scraping.py
#
# The module is part of pydavis.
#

"""
Testing of WeatherLinkScraper.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


import pytest

import nose.tools as ntools

from datetime import datetime
from pydavis.web_scraping import WeatherLinkScraper


class TestWeatherLinkScraper:
    """Testing the WeatherLinkScraper."""

    testing_class = WeatherLinkScraper

    test_params = {
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
    }

    target_params = {
        'idtime': datetime(2018, 7, 4, 13, 13),
        'Outside_Temp': 23.6,
        'Inside_Temp': 27.2,
        'Outside_Humidity': 43,
        'Inside_Humidity': 37,
        'Wind_Gust_Speed': 12.9,
        'Wind_Speed': 16,
        'Wind_Chill': 23.3,
        'Heat_Index': 23.3,
        'Dew_Point': 10.0,
        'Year': 0.0,
    }

    @pytest.fixture
    def scraper(self):
        """Returns a weather link scraper instance for test purposes."""

        return self.testing_class('', self.test_params)

    @pytest.fixture
    def html(self):
        """Returns HTML test data."""

        # NOTE: Context manager `rb` signifies "read <bytes>".
        with open('./test_html.txt', 'rb') as infile:
            html = infile.read()

        return html

    def test_unit_atlering(self, scraper):
        """Test adding and dropping removeable units."""

        test_unit = 'test_unit'

        assert not test_unit in scraper.removeable_units

        scraper.add_unit(test_unit)

        assert test_unit in scraper.removeable_units

        scraper.drop_unit(test_unit)

        assert not test_unit in scraper.removeable_units

    def test_init_status(self, scraper):
        """Tests initial status of attributes."""

        attributes = [
            scraper.parameters, scraper.data_types, scraper.last_logging
        ]

        assert all(attribute is None for attribute in attributes)

    def test_invalid_args(self, scraper):
        """Tests if error is raised as invalid arguments are passed."""

        invalid_args = [1, 1.0, {}, [], (), None, False, True]

        for invalid_arg in invalid_args:
            with pytest.raises(TypeError):
                scraper.add_unit(invalid_arg)
                scraper.drop_unit(invalid_arg)
                scraper.fetch_html(invalid_arg)
                scraper.process_html(invalid_arg)

    def test_timestamp(self, scraper, html, time_format='%Y-%m-%d %H:%M:%S'):
        """Test assigning of time stamp value."""

        target_stamp = datetime.strptime('2018-07-04 13:13:00', time_format)

        ntools.eq_(scraper.last_logging, None)

        scraper.collect_parameters(html=html)

        ntools.eq_(scraper.last_logging, target_stamp)

    def test_parameters(self, scraper, html):
        """Test collection of parameters."""

        scraper.collect_parameters(html=html)

        assert all(item in self.target_params for item in scraper.parameters)
