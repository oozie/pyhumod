"""Exceptions and error-handling methods."""

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
        raise AtCommandError(input_line)
