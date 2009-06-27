#
# Copyright 2009 by Slawek Ligus <root@ooz.ie>
#
# Please refer to the LICENSE file for conditions 
#  under which this software may be distributed.
#
#   Visit http://huawei.ooz.ie/ for more info.
#

"""Exceptions and error-handling methods."""

__author__ = 'Slawek Ligus <root@ooz.ie>'

ERROR_CODES = ['COMMAND NOT SUPPORT', 'ERR', 'NO CARRIER', 'BUSY']

class Error(Exception):
    """Generic Exception."""
    pass

class AtCommandError(Error):
    """AT Command exception."""
    pass

class PppdError(Error):
    """PPPD fork-exec exception."""
    pass

class HumodUsageError(Error):
    """Humod usage error exception."""
    pass

def check_for_errors(input_line):
    """Check if input line contains error code."""
    if ('ERROR' in input_line) or (input_line in ERROR_CODES):
        raise AtCommandError, input_line


