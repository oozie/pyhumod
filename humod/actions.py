"""Action functions to be taken in response to events."""

import re

# pylint: disable-msg=W0613
def call_notification(modem, message):
    """Execute when someone is calling."""
    print('Someone is calling')

def null_action(modem, message):
    """Take no action."""
    pass

def rssi_update(modem, message):
    """Handle RSSI level change."""
    modem.status.rssi = modem.get_rssi()

def flow_report_update(modem, message):
    """Update connection report."""
    hex2dec = lambda h: int(h, 16)
    flow_rpt = message[11:].rstrip()
    values = [hex2dec(item) for item in flow_rpt.split(',', 7)]
    sts = modem.status
    (sts.link_uptime, sts.uplink, sts.downlink, sts.byte_tx, 
     sts.byte_rx) = values[0:5]

def mode_update(modem, message):
    """Update connection mode."""
    # Source info is no longer available, taken from:
    # https://forge.betavine.net/pipermail/vodafonemobilec-devel/
    # 2007-November/000044.html
    mode_dict = {'0': 'No service', '1': 'AMPS', '2': 'CDMA', '3': 'GSM/GPRS',
                 '4': 'HDR', '5': 'WCDMA', '6': 'GPS'}
    submode_dict = {'0': 'None', '1': 'GSM', '2': 'GPRS', '3': 'EDEG', 
                    '4': 'WCDMA', '5': 'HSDPA', '6': 'HSUPA', '7': 'HSDPA'}
    mode, submode = message[6:].strip().split(',', 1)
    modem.status.mode = '%s/%s' % (mode_dict[mode], submode_dict[submode])

def new_message(modem, message):
    """New message action."""
    print('New message arrived.')

PATTERN = {'incoming call': re.compile(r'^RING\r\n'),
           'new sms': re.compile(r'^\+CMTI:.*'),
	   'rssi update': re.compile(r'^\^RSSI:.*'),
	   'flow report': re.compile(r'^\^DSFLOWRPT:'),
	   'mode update': re.compile(r'^\^MODE:.*'),
	   'boot update': re.compile(r'^\^BOOT:.*$'),
	   'new line': re.compile(r'^\r\n$'),
	   'empty line': re.compile(r'^$')}

STANDARD_ACTIONS = [(PATTERN['incoming call'], call_notification),
                    (PATTERN['new line'], null_action),
                    (PATTERN['empty line'], null_action),
                    (PATTERN['boot update'], null_action),
                    (PATTERN['new sms'], new_message),
                    (PATTERN['mode update'], mode_update),
                    (PATTERN['rssi update'], rssi_update),
		    (PATTERN['flow report'], flow_report_update)]
