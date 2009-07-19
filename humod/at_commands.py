#
# Copyright 2009 by Slawek Ligus <root@ooz.ie>
#
# Please refer to the LICENSE file for conditions 
#  under which this software may be distributed.
#
#   Visit http://pyhumod.ooz.ie/ for more info.
#

"""Classes and methods for handling AT commands."""

import re
import humod.errors as errors

__author__ = 'Slawek Ligus <root@ooz.ie>'

class Command(object):
    """Class defining generic perations performed on AT commands."""

    def __init__(self, modem, cmd):
        """Constructor for Command class."""
        self.cmd = cmd
        self.modem = modem

    def run(self, should_wait=True):
        r"""Send the AT command followed by the '\r' character to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        self.modem.ctrl_port.read_waiting()
        return self.modem.ctrl_port.send(self.cmd, should_wait, at_cmd=self.cmd)

    def get(self, should_wait=True):
        r"""Send the AT command followed by the '?\r' characters to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        self.modem.ctrl_port.read_waiting()
        return self.modem.ctrl_port.send('%s?' % self.cmd, 
                               should_wait, at_cmd=self.cmd)

    def set(self, value, should_wait=True):
        r"""Send the 'AT<+CMD>=<value>\r' string to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        self.modem.ctrl_port.read_waiting()
        return self.modem.ctrl_port.send('%s=%s' % (self.cmd,
                               value), should_wait, at_cmd=self.cmd)

    def dsc(self, should_wait=True):
        r"""Send the AT command followed by the '=?\r' characters to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        self.modem.ctrl_port.read_waiting()
        data = self.modem.ctrl_port.send('%s=?' % self.cmd, 
                               should_wait, at_cmd=self.cmd)
        return data


def _common_run_unprefixed(modem, at_cmd):
    """Boilerplate for most methods based on Command.run()."""
    info_cmd = Command(modem, at_cmd)
    modem.ctrl_lock.acquire()
    try:
        info_cmd.run(should_wait=False)
        info = modem.ctrl_port.return_data()
        return info
    finally:
        modem.ctrl_lock.release()

def _common_get_prefixed(modem, at_cmd):
    """Boilerplate for most methods based on Command.get()."""
    data_cmd = Command(modem, at_cmd)
    modem.ctrl_lock.acquire()
    try:
        data = data_cmd.get()
        return data
    finally:
        modem.ctrl_lock.release()

def _common_run_prefixed(modem, at_cmd):
    """Boilerplate for most methods based on Command.run()."""
    data_cmd = Command(modem, at_cmd)
    modem.ctrl_lock.acquire()
    try:
        data = data_cmd.run()
        return data
    finally:
        modem.ctrl_lock.release()

def _common_dsc_prefixed(modem, at_cmd):
    """Boilerplate for most methods based on Command.dsc()."""
    data_cmd = Command(modem, at_cmd)
    modem.ctrl_lock.acquire()
    try:
        data = data_cmd.dsc()
        return data
    finally:
        modem.ctrl_lock.release()

def _common_set(modem, at_cmd, value):
    """Boilerplate for most methods based on Command.set()."""
    modem.ctrl_lock.acquire()
    try:
        Command(modem, at_cmd).set(value)
    finally:
        modem.ctrl_lock.release()


class InteractiveCommands(object):
    """SIM interactive commands."""
    ctrl_lock = None
    ctrl_port = None
    def send_text(self, number, contents):
        """Send a text message from the modem.
        
        Arguments:
            number -- string with reciepent number,
            contents -- text message body.
        
        Returns:
            Sent text message number since last counter reset.
        """
        self.ctrl_lock.acquire()
        try:
            textsend = Command(self, '+CMGS')
            # Perform a SIM test first.
            textsend.dsc()
            textsend.set('"%s"' % number, should_wait=False)
            result = self.ctrl_port.send(contents+chr(26))
            # A text number is an integer number, returned in the
            # last returned entry of the result, just after the ": " part.
            text_number = int(result[-1].split(': ')[1])
            return text_number
        finally:
            self.ctrl_lock.release()

    def list_messages(self, message_type='ALL'):
        """List messages by type.
        
        Arguments:
            message_type -- one of the following strings:
                'ALL' -- all messages,
                'REC READ' -- read messages,
                'REC UNREAD' -- unread messages,
                'STO SENT' -- stored sent messages,
                'STO UNSENT' -- stored unsent messages.
        Returns:
            list of string lists representing message headers.
        """
        self.ctrl_lock.acquire()
        try:
            message_lister = Command(self, '+CMGL')
            messages_data = message_lister.set('"%s"' % message_type)
            return messages_data
        finally:
            self.ctrl_lock.release()

    def read_message(self, message_num):
        """Read one message from the SIM.
        
        Arguments:
            message_num -- number of a message to read.
        Returns:
            message body (string) or None if the message isn't found.
        """
        self.ctrl_lock.acquire()
        try:
            message_reader = Command(self, '+CMGR')
            message_reader.set(message_num, should_wait=False)
            message = self.ctrl_port.return_data()
            # Slicing out the header.
            return '\n'.join(message[1:])
        finally:
            self.ctrl_lock.release()

    def del_message(self, message_num):
        """Delete message from the SIM."""
        msg_num_str = '%d' % message_num
        _common_set(self, '+CMGD', msg_num_str)

    def hangup(self):
        """Hang up."""
        hup = Command(self, '+CHUP')
        self.ctrl_lock.acquire()
        try:
            hup.run()
        finally:
            self.ctrl_lock.release()


class ShowCommands(object):
    """Show methods extract static read-only data."""

    def show_imei(self):
        """Show IMEI serial number."""
        return _common_run_unprefixed(self, '+GSN')[0]

    def show_sn(self):
        """Show serial number."""
        return _common_run_prefixed(self, '^SN')[0]

    def show_manufacturer(self):
        """Show manufacturer name."""
        return _common_run_unprefixed(self, '+GMI')[0]

    def show_model(self):
        """Show device model name."""
        return _common_run_unprefixed(self, '+GMM')[0]
        
    def show_revision(self):
        """Show device revision."""
        return _common_run_unprefixed(self, '+GMR')[0]

    def show_hardcoded_operators(self):
        """List operators hardcoded on the device."""
        hard_ops_list = _common_run_prefixed(self, '+COPN')
        data = dict()
        for entry in hard_ops_list:
            num, op_name = [item[1:-1] for item in entry.split(',', 1)] 
            data[num] = op_name
        return data

    def show_who_locked(self):
        """Show what network operator has locked the device."""
        locker_info = _common_dsc_prefixed(self, '^CARDLOCK')
        if locker_info:
            # Slice brackets off.
            locker_info = locker_info[0][1:-1].split(',')
        return locker_info

class SetCommands(object):
    """Set methods write user settings that are kept permanently."""

    # pylint: disable-msg=R0913
    def set_pdp_context(self, num, proto='IP', apn='', ip_addr='', d_comp=0,
                        h_comp=0):
        """Set Packet Data Protocol context."""
        pdp_context_str = '%d,"%s","%s","%s",%d,%d' % (num, proto, apn, 
                                                       ip_addr, d_comp, h_comp)
        _common_set(self, '+CGDCONT', pdp_context_str)

    def set_service_center(self, sca, tosca=145):
        """Set Service Center address and type.
        
        Args:
          sca -- String with service center address,
          tosca -- Integer with SC type.
        Raises:
          AtCommandError -- if tosca contains an unknown value for SC type,
          TypeError -- if SC type is not an integer.
        """
        # Possible type of SC values:
        #  128: unknown
        #  129: national
        #  145: international
        #  161: national 
        if tosca not in (128, 129, 145, 161):
            raise errors.AtCommandError('Unknown SC type: %i.' % tosca)
        sca_str = '"%s",%i' % (sca, tosca)
        _common_set(self, '+CSCA', sca_str)

class EnterCommands(object):
    """Enter methods write user settings that are kept until modem restarts."""

    def enter_text_mode(self):
        """Enter text mode."""
        _common_set(self, '+CMGF', '1')

    def enter_pdu_mode(self):
        """Enter PDU mode."""
        _common_set(self, '+CMGF', '0')

    def enter_pin(self, pin, new_pin=None):
        """Enter or set new PIN."""
        if new_pin:
            set_arg = '"%d","%d"' % (pin, new_pin)
        else:
            set_arg = '"%d"' % pin
        
        return _common_set(self, '+CPIN', set_arg)

    def enable_nmi(self, status=None):
        """Enable, disable or check status on new message indications."""
        inactive = '0,0,0,0,0' 
        active = '2,1,0,2,1'
        if status is None:
            result = _common_get_prefixed(self, '+CNMI')[0]
            return result == active
        if status is True:
            return _common_set(self, '+CNMI', active)
        else:
            return _common_set(self, '+CNMI', inactive)
 
class GetCommands(object):
    """Get methods read dynamic or user-set data."""

    def get_networks(self):
        """Scan for networks."""
        active_ops = _common_dsc_prefixed(self, '+COPS')
        bracket_group = re.compile('\(.+?\)')
        if active_ops:
            data = list()
            network_data_list = bracket_group.findall(active_ops[0])
            for network_data_set in network_data_list:
                unbracketed_set = network_data_set[1:-1]
                items = unbracketed_set.split(',')
                if len(items) == 5:
                    transformed_set = [_transform(ni) for ni in items]
                    data.append(transformed_set)
            return data
            
    def get_mode(self):
        """Get current mode.
        
        Returns:
            0 -- PDU mode,
            1 -- Text mode.
        """
        current_mode = _common_get_prefixed(self, '+CMGF')[0]
        return int(current_mode)

    def get_clock(self):
        """Return internal modem clock."""
        return _common_get_prefixed(self, '+CCLK')[0]

    def get_service_center(self):
        """Show service center number."""
        sc_data = _common_get_prefixed(self, '+CSCA')[0].split(',', 1)
        service_center, sc_type_num = [_transform(item) for item in sc_data]
        return service_center, sc_type_num

    def get_detailed_error(self):
        """Print detailed error message."""
        return _common_run_prefixed(self, '+CEER')[0]

    def get_rssi(self):
        """Show RSSI level."""
        rssi_info = _common_run_prefixed(self, '+CSQ')[0]
        rssi = rssi_info.split(',', 1)
        return int(rssi[0])

    def get_pin_status(self):
        """Inform about PIN status.
        
        Returns:
            'READY' -- sim card ready to use,
            'SIM PIN' -- PIN required,
            'SIM PUK' -- PUK required.
        """
        pin_info = _common_get_prefixed(self, '+CPIN')[0]
        return pin_info

    def get_pdp_context(self):
        """Read PDP context entries."""
        pdp_context_data = _common_get_prefixed(self, '+CGDCONT')
        data = list()
        for pdp_context in pdp_context_data:
            pdp_set = [_transform(item) for item in pdp_context.split(',')]
            data.append(pdp_set)
        return data


def _transform(pdp_item):
    """Return a string if pdp_item starts with quotes or integer otherwise."""
    if pdp_item:
        if pdp_item.startswith('"'):
            return pdp_item[1:-1]
        else:
            return int(pdp_item)
    else:
        return ''

