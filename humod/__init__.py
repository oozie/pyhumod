#
# Copyright 2009 by Slawek Ligus <root@ooz.ie>
#
# Please refer to the LICENSE file for conditions 
#  under which this software may be distributed.
#
#   Visit http://huawei.ooz.ie/ for more info.
#

"""pyhumod provides user friendly interface to advanced features of 3g modems.

Modules:
    at_commands - classes and methods for handling AT commands,
    errors - exceptions and error-handling methods,
    actions - action functions to be taken in response to events,
    detect - methods helpful by detecting modems,
    humodem - the Modem() class and it's dependencies.
"""

__author__ = 'Slawek Ligus <root@ooz.ie>'

import humod.at_commands
import humod.errors
import humod.actions 
from humod.humodem import Modem
