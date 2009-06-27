#
# Copyright 2009 by Slawek Ligus <root@ooz.ie>
#
# Please refer to the LICENSE file for conditions 
#  under which this software may be distributed.
#
#   Visit http://huawei.ooz.ie/ for more info.
#

"""Action functions to be taken in response to events."""

import re

def call_notification(modem, message):
    """Execute when someone is calling."""
    print 'Someone is calling'

def no_match(modem, message):
    """Handle a message non-matching any pattern."""
    print 'No match for %r' % message

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
    s = modem.status
    x = None
    (s.link_uptime, s.uplink, s.downlink, s.byte_tx, s.byte_rx, 
     s.x, s.y) = values

def mode_update(modem, message):
    """Update connection mode."""
    # Info taken from:
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
    print 'New message arrived.'

STANDARD_PATTERNS = [(re.compile(r'^RING\r\n'), call_notification),
                     (re.compile(r'^$'), null_action),
                     (re.compile(r'^\+CMTI:.*'), new_message),
                     (re.compile(r'^\r\n$'), null_action),
                     (re.compile(r'^\^BOOT:.*$'), null_action),
                     (re.compile(r'^\^MODE:.*'), mode_update),
                     (re.compile(r'^\^RSSI:.*'), rssi_update),
		     (re.compile(r'^\^DSFLOWRPT:'), flow_report_update)]

