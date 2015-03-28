"""pyhumod provides user friendly interface to advanced features of 3g modems.

Modules:
    at_commands - classes and methods for handling AT commands,
    errors - exceptions and error-handling methods,
    actions - action functions to be taken in response to events,
    detect - methods helpful by detecting modems,
    humodem - the Modem() class and it's dependencies.
"""

__version__ = '0.4'

import humod.at_commands
import humod.errors
import humod.actions
import humod.defaults
from humod.humodem import Modem
