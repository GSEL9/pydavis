# -*- coding: utf-8 -*-
#
# to_database.py
#
# The module is part of pydavis.
#

"""
Illustrates how to used DataLogger for streaming data to a MySQL database.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


from pydavis.data_logging import DataLogger


def gen_sample_url():
    """An URL referencing the target Davis WeatherLink report."""

    base = 'http://www.weatherlink.com/user/'
    location = 'vneza/index.php?view=summary&headers=0'

    return ('').join((base, location))


def logging_to_database(url, user, password, database, table):
    """Creates a DataLogger instance and writes Davis weather station
    parameters to a MySQL database."""

    logger = DataLogger(url)

    logger.initiate_logging(to_table=True,
                            user=user,
                            password=password,
                            database=database,
                            table=table)


if __name__ == '__main__':
    # Demo run

    # NOTE: Abort script with CTRL + C.

    user = 'davis'
    password = 'davis'
    database = 'pydavis'
    table = 'weather_data'

    # Drop the parameters `Dew_Point` and `Year` from the target parameters.
    DataLogger.drop_parameters(['Dew_Point', 'Year'])

    # Increase the interval between web scraping sessions.
    DataLogger.update_slumber_interval(30)

    logging_to_database(
        gen_sample_url(), user, password, database, table
    )
