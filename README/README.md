# pydavis

A Python package intended the logging of weather data parameters monitored by
Davis weather stations. The parameters are obtained through the reports
generated at Davis WeatherLink websites, and can be streamed to a *MySQL*
database or a specified file.

## Installation

The package can be installed with `pip`

```
pip install pydavis [--user]
```

or through `setuptools` by cloning the repository and running

```
python setup.py install [--user]
```

## Usage

Through the `data_logging.py` module, the weather parameters are streamed
from [WeatherLink](https://www.weatherlink.com/). By instantiating the
`DataLogger` with an URL, the logging sequence can be initiated. To abort the
logging sequence, type `CTRL + C` in the command line.

**Storing data in a *MySQL* database:**

```
logger = DataLogger(url)
logger.initiate_logging(to_table=True,
                        user='user',
                        password='password',
                        database='pydavis',
                        table='weather_data')
```

The necessary arguments are *MySQL* login credentials, and the name of the
database and the table. The `logger` will create the database and the table if
necessary.

**Storing data in a file:**

```
logger = DataLogger(url)
logger.initiate_logging(to_file=True,
                        path_to_file='./weather_data.csv')
```

The location including the name of the file must be passed as argument. The
`logger` will create a new file if necessary.

## Features

Various logging parameters can be specified through the `DataLogger` such as:
* The target parameters among the available weather station parameters.
* The target parameter values such as *Current* or *Today's Highs*.
* The time interval between conducting each web scraping.
* The value separator and new line characters in the case of writing to file.

The `DatabaseManager` located in the `db_manager.py` module can be use to
interact with a *MySQL* database. The user can maintain a database through
various methods without having to explicitly state the *MySQL* queries while
working in a Python environment.
