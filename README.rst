Installation_ | Usage_ | License_


##################
pydavis
##################

A package intended the logging of weather data parameters monitored by
Davis weather stations. The parameters are obtained through the reports
generated at Davis WeatherLink websites, and can be streamed to a *MySQL*
database or a specified file.


************
Installation
************

The package can be installed with `pip <https://pypi.python.org/pypi/pip>`_

.. code-block:: bash

   pip install pydavis


*****
Usage
*****

Through the ``data_logging.py`` module, the weather parameters are
streamed from `WeatherLink <https://www.weatherlink.com/>`__ websites::

   >>> from data_logging import DataLogger

By instantiating the ``DataLogger`` with an URL, the logging sequence can then
be initiated and data stored according to specified format. Any logging
sequence is aborted with ``CTRL + C``.

**Storing data in a MySQL database**

.. code-block:: python

    >>> logger = DataLogger(url)
    >>> logger.initiate_logging(to_table=True,
                                user='user',
                                password='password',
                                database='pydavis',
                                table='weather_data')

The necessary arguments are *MySQL* login credentials, the name of the database
and the table. The ``logger`` will create the database and the table if
necessary.

**Storing data in a file**

.. code-block:: python

    >>> logger = DataLogger(url)
    >>> logger.initiate_logging(to_file=True,
                                path_to_file='./weather_data.csv')

The location including the name of the file must be passed as argument.
The ``logger`` will create a new file if necessary.

*******
License
*******

MIT, see `MIT license <https://opensource.org/licenses/MIT>`_.
