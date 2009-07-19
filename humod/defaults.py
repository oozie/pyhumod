#
# Copyright 2009 by Slawek Ligus <root@ooz.ie>
#
# Please refer to the LICENSE file for conditions 
#  under which this software may be distributed.
#
#   Visit http://pyhumod.ooz.ie/ for more info.
#

"""This module provides default values for different OS types."""

__author__ = 'Slawek Ligus <root@ooz.ie>'

import os

DATA_PORT = '/dev/ttyUSB0'
CONTROL_PORT = '/dev/ttyUSB1'
PPPD_PATH = '/usr/sbin/pppd'
PROBER_TIMEOUT = 0.5
BAUDRATE = '115200'
DIALNUM = '*99#'
PPPD_PARAMS = ['modem', 'crtscts', 'defaultroute', 'usehostname', '-detach',
               'noipdefault', 'call', 'humod', 'user', 'ppp', 'usepeerdns',
               'idle', '0', 'logfd', '8']
if os.name == 'posix':
    # Posix systems.
    if 'linux' in os.sys.platform:
        # Linux systems. Already set.
        pass
    elif 'freebsd' in os.sys.platform:
        # FreeBSD systems.
        DATA_PORT = '/dev/ugen0'
        CONTROL_PORT = '/dev/ugen1'
    elif os.sys.platform == 'darwin':
        # Darwin (MacOS X) systems.
        DATA_PORT = '/dev/cu.HUAWEIMobile-Modem'
        CONTROL_PORT = '/dev/cu.HUAWEIMobile-Pcui'
