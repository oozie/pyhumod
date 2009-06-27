#
# Copyright 2009 by Slawek Ligus <root@ooz.ie>
#
# Please refer to the LICENSE file for conditions 
#  under which this software may be distributed.
#
#   Visit http://huawei.ooz.ie/ for more info.
#

"""Classes and methods for handling AT commands."""

import re

__author__ = 'Slawek Ligus <root@ooz.ie>'

class Command(object):
    """Class defining generic perations performed on AT commands."""
    def __init__(self, modem, cmd):
        self.cmd = cmd
        self.modem = modem

    def run(self, should_wait=True):
        r"""Send the AT command followed by the '\r' character to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        return self.modem.ctrl_port.send(self.cmd, should_wait, at_cmd=self.cmd)

    def get(self, should_wait=True):
        r"""Send the AT command followed by the '?\r' characters to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        return self.modem.ctrl_port.send('%s?' % self.cmd, 
                               should_wait, at_cmd=self.cmd)

    def set(self, value, should_wait=True):
        r"""Send the 'AT<+CMD>=<value>\r' string to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        return self.modem.ctrl_port.send('%s=%s' % (self.cmd,
                               value), should_wait, at_cmd=self.cmd)

    def dsc(self, should_wait=True):
        r"""Send the AT command followed by the '=?\r' characters to the modem.
        
        Returns:
            List of strings or None if should_wait is set to True.
        """
        data = self.modem.ctrl_port.send('%s=?' % self.cmd, 
                               should_wait, at_cmd=self.cmd)
        return data


class CommonActions(object):
    """Common boilerplate for most Modem methods."""

    ctrl_lock = None
    ctrl_port = None
    send = lambda:None
    def _common_run_unprefixed(self, at_cmd):
        """Boilerplate for most methods based on Command.run()."""
        info_cmd = Command(self, at_cmd)
        self.ctrl_lock.acquire()
        try:
            # clear the buffer if something is in it
            self.ctrl_port.read(self.ctrl_port.inWaiting())
            info_cmd.run(should_wait=False)
            info = self.ctrl_port.return_data()
            return info
        finally:
            self.ctrl_lock.release()

    def _common_get_prefixed(self, at_cmd):
        """Boilerplate for most methods based on Command.get()."""
        data_cmd = Command(self, at_cmd)
        self.ctrl_lock.acquire()
        try:
            data = data_cmd.get()
            return data
        finally:
            self.ctrl_lock.release()

    def _common_run_prefixed(self, at_cmd):
        """Boilerplate for most methods based on Command.run()."""
        data_cmd = Command(self, at_cmd)
        self.ctrl_lock.acquire()
        try:
            data = data_cmd.run()
            return data
        finally:
            self.ctrl_lock.release()

    def _common_dsc_prefixed(self, at_cmd):
        """Boilerplate for most methods based on Command.dsc()."""
        data_cmd = Command(self, at_cmd)
        self.ctrl_lock.acquire()
        try:
            data = data_cmd.dsc()
            return data
        finally:
            self.ctrl_lock.release()

    def _common_set(self, at_cmd, value):
        """Boilerplate for most methods based on Command.set()."""
        self.ctrl_lock.acquire()
        try:
            Command(self, at_cmd).set(value)
        finally:
            self.ctrl_lock.release()


class InteractiveCommands(CommonActions):
    """SIM interactive commands."""
   
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
           message body (string) or None if no message is found.
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
        self._common_set('+CMGD', msg_num_str)

    def hangup(self):
        """Hang up."""
        hup = Command(self, '+CHUP')
        self.ctrl_lock.acquire()
        try:
            hup.run()
        finally:
            self.ctrl_lock.release()


class ShowCommands(CommonActions):
    """Show methods extract static read-only data."""

    def show_imei(self):
        """Show IMEI serial number."""
        return self._common_run_unprefixed('+GSN')[0]

    def show_sn(self):
        """Show serial number."""
        return self._common_run_prefixed('^SN')[0]

    def show_manufacturer(self):
        """Show manufacturer name."""
        return self._common_run_unprefixed('+GMI')[0]

    def show_model(self):
        """Show device model name."""
        return self._common_run_unprefixed('+GMM')[0]
        
    def show_revision(self):
        """Show device revision."""
        return self._common_run_unprefixed('+GMR')[0]

    def show_hardcoded_operators(self):
        """List operators hardcoded on the device."""
        hard_ops_list = self._common_run_prefixed('+COPN')
        data = dict()
        for entry in hard_ops_list:
            num, op_name = [item[1:-1] for item in entry.split(',', 1)] 
            data[num] = op_name
        return data

    def show_who_locked(self):
        """Show what network operator has locked the device."""
        locker_info = self._common_dsc_prefixed('^CARDLOCK')
        if locker_info:
            # Slice brackets away.
            locker_info = locker_info[0][1:-1].split(',')
        return locker_info

class SetCommands(CommonActions):
    """Set methods write user settings that are kept permanently."""

    def set_pdp_context(self, num, proto='IP', apn='', ip_addr='', d_comp=0,
                        h_comp=0):
        """Set Packet Data Protocol context."""
        pdp_context_str = '%d,"%s","%s","%s",%d,%d' % (num, proto, apn, 
                                                       ip_addr, d_comp, h_comp)
        self._common_set('+CGDCONT', pdp_context_str)


class EnterCommands(CommonActions):
    """Enter methods write user settings that are kept until modem restarts."""

    def enter_text_mode(self):
        """Enter text mode."""
        self._common_set('+CMGF', '1')

    def enter_pdu_mode(self):
        """Enter PDU mode."""
        self._common_set('+CMGF', '0')

    def enter_pin(self, pin, new_pin=None):
        """Enter or set new PIN."""
        if new_pin:
            set_arg = '"%d","%d"' % (pin, new_pin)
        else:
            set_arg = '"%d"' % pin
        
        return self._common_set('+CPIN', set_arg)

    def enable_nmi(self, status=None):
        """Enable, disable or check status on new message indications."""
        inactive = '0,0,0,0,0' 
        active = '2,1,0,2,1'
        if status is None:
            result = self._common_get_prefixed('+CNMI')[0]
            return result == active

        if status is True:
            return self._common_set('+CNMI', active)
        else:
            return self._common_set('+CNMI', inactive)
 
class GetCommands(CommonActions):
    """Get methods read dynamic or user-set data."""

    def get_networks(self):
        """Scan for networks."""
        active_ops = self._common_dsc_prefixed('+COPS')
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
         0 - PDU mode,
         1 - Text mode."""
        current_mode = self._common_get_prefixed('+CMGF')[0]
        return int(current_mode)

    def get_clock(self):
        """Return internal modem clock."""
        return self._common_get_prefixed('+CCLK')[0]

    def get_service_center(self):
        """Show service center number."""
        sc_data = self._common_get_prefixed('+CSCA')[0].split(',', 1)
        service_center, sc_type_num = [_transform(item) for item in sc_data]
        return service_center, sc_type_num

    def get_detailed_error(self):
        """Print detailed error message."""
        return self._common_run_prefixed('+CEER')[0]

    def get_rssi(self):
        """Show RSSI level."""
        rssi_info = self._common_run_prefixed('+CSQ')[0]
        rssi = rssi_info.split(',', 1)
        return int(rssi[0])

    def get_pin_status(self):
        """Inform about PIN status.
        
        Returns:
            'READY' -- sim card ready to use,
            'SIM PIN' -- PIN required,
            'SIM PUK' -- PUK required.
        """
        pin_info = self._common_get_prefixed('+CPIN')[0]
        return pin_info

    def get_pdp_context(self):
        """Read PDP context entries."""

        pdp_context_data = self._common_get_prefixed('+CGDCONT')
        data = list()
        for pdp_context in pdp_context_data:
            pdp_set = [_transform(item) for item in pdp_context.split(',')]
            data.append(pdp_set)
        return data


class CommandSet(GetCommands, SetCommands, EnterCommands,  InteractiveCommands,
                 ShowCommands):
    """Command set for a modem."""
    pass

def _transform(pdp_item):
    """Return string if pdp_item contains quotes, integer otherwise."""
    if pdp_item:
        if pdp_item.startswith('"'):
            return pdp_item[1:-1]
        else:
            return int(pdp_item)
    else:
        return ''

