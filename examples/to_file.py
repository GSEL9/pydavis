# -*- coding: utf-8 -*-
#
# to_file.py
#
# The module is part of pydavis.
#

"""
Illustrates how to used DataLogger for streaming data to file.
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


def logging_to_file(url, path_to_file):
    """Creates a DataLogger instance and writes Davis weather station
    parameters to a CSV file."""

    logger = DataLogger(url)

    logger.initiate_logging(to_file=True,
                            path_to_file=path_to_file)


if __name__ == '__main__':
    # Demo run

    # NOTE: Abort script with CTRL + C.

    # The path to the file that will be created.
    path_to_file = './weather_data.csv'

    # Change the parameter value separator symbol and newline character.
    DataLogger.update_separator(',')

    logging_to_file(gen_sample_url(), path_to_file)
