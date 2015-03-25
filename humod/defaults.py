"""This module provides default values for different OS types."""

import os

DATA_PORT = '/dev/ttyUSB0'
CONTROL_PORT = '/dev/ttyUSB1'
# Point-to-Point Protocol - The pppd daemon works together with the kernel
# PPP driver to establish and maintain a PPP link with another system
# (called the peer) and to negotiate...
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
