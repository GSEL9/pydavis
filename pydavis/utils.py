# -*- coding: utf-8 -*-
#
# utils.py
#
# The module is part of pydavis.
#

"""
The pydavis utilities module.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'
__status__ = 'Operational'


def _check_parameter(parameter, dtype, value):
    # Parameter value type checking.

    if not isinstance(value, dtype):
        raise TypeError('`{}` must be {}, and not {}'
                        ''.format(parameter, dtype, type(value)))


class DatabaseConnectionError(Exception):
    """Error raised if not connected to database."""

    def __init__(self, message):
        super().__init__(message)


class DatabaseExecutionError(Exception):
    """Error raised if unable to execute database command."""

    def __init__(self, message):
        super().__init__(message)


class DatabaseCommitError(Exception):
    """Error raised if unable to commit changes to database."""

    def __init__(self, message):
        super().__init__(message)


class MissingDatabaseError(Exception):
    """Error raise if not working database is specified."""

    def __init__(self, message):
        super().__init__(message)
