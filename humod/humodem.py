"""This module defines the base Modem() class."""

import serial
import threading
try:
    import Queue as queue
except ImportError:
    import queue
import time
import os
from humod import errors
from humod import actions
from humod import defaults
from humod import at_commands as atc


class Interpreter(threading.Thread):
    """Interpreter thread."""
    def __init__(self, modem, queue, patterns):
        self.active = True
        self.queue = queue
        self.patterns = patterns
        self.modem = modem
        threading.Thread.__init__(self)

    def run(self):
        """Keep interpreting messages while active attribute is set."""
        while self.active:
            self.interpret(self.queue.get().decode())

    def interpret(self, message):
        """Match message pattern with an action to take.

        Arguments:
            message -- string received from the modem.
        """
        for pattern_action in self.patterns:
            pattern, action = pattern_action
            if pattern.search(message):
                action(self.modem, message)
                break
        else:
            actions.null_action(self.modem, message)


class QueueFeeder(threading.Thread):
    """Queue feeder thread."""
    def __init__(self, queue, ctrl_port, ctrl_lock):
        self.active = True
        self.queue = queue
        self.ctrl_port = ctrl_port
        self.ctrl_lock = ctrl_lock
        threading.Thread.__init__(self)

    def run(self):
        """Start the feeder thread."""
        while self.active:
            self.ctrl_lock.acquire()
            try:
                # set timeout
                input_line = self.ctrl_port.readline() 
                self.queue.put(input_line)
            finally:
                self.ctrl_lock.release()
                # Putting the thread on idle between releasing
                # and acquiring the lock for 100ms
                time.sleep(.1)

    def stop(self):
        """Stop the queue feeder thread."""
        self.active = False
        self.ctrl_port.write(b'\r\n')


class Prober(object):
    """Class responsible for reading in and queueing of control data."""

    def __init__(self, modem):
        self.queue = queue.Queue()
        self._interpreter = None
        self._feeder = None
        self.modem = modem
        self.patterns = None

    def _stop_interpreter(self):
        """Stop the interpreter."""
        self._interpreter.active = False
        self._interpreter.queue.put('')

    def _start_interpreter(self):
        """Instanciate and start a new interpreter."""
        self._interpreter = Interpreter(self.modem, self.queue, self.patterns)
        self._interpreter.start()

    def start(self, patterns=None):
        """Start the prober.

        Starts two threads, an instance of QueueFeeder and Interpreter.
        """
        self.patterns = patterns
        if not patterns:
            self.patterns = actions.STANDARD_ACTIONS
        if self._feeder:
            raise errors.HumodUsageError('Prober already started.')
        else:
            self._feeder = QueueFeeder(self.queue, self.modem.ctrl_port, 
                                       self.modem.ctrl_lock)
            self._feeder.start()
            self._start_interpreter()

    def stop(self):
        """Stop the prober."""
        if self._feeder:
            self._stop_interpreter()
            self._feeder.stop()
            self._feeder = None
        else:
            raise errors.HumodUsageError('Prober not started.')


# pylint: disable-msg=R0904
# pylint: disable-msg=R0903
# pylint: disable-msg=R0902
# pylint: disable-msg=R0901
class ModemPort(serial.Serial):
    """Class extending serial.Serial by humod specific methods."""

    def send_at(self, cmd, suffix, prefixed=True):
        """Send serial text to the modem.

        Arguments:
            self -- serial port to send to,
            text -- text value to send,
            prefixed -- boolean determining weather to strip the AT
                        command prefix from each output line.

        Returns:
            List of strings.
        """
        self.write(('AT%s%s\r' % (cmd, suffix)).encode())
        # Read in the echoed text.
        # Check for errors and raise exception with specific error code.
        input_line = self.readline().decode()
        errors.check_for_errors(input_line)
        # Return the result.
        if prefixed:
            # If the text being sent is an AT command, only relevant context
            # answer (starting with '+command:' value) will be returned by 
            #return_data(). Otherwise any string will be returned.
            return self.return_data(cmd)
        else:
            return self.return_data()

    def read_waiting(self):
        """Clear the serial port by reading all data waiting in it."""
        return self.read(self.inWaiting())

    def return_data(self, command=None):
        """Read until exit status is returned.

        Returns:
            data: List of right-stripped strings containing output
            of the command.

        Raises:
            AtCommandError: If an error is returned by the modem.
        """
        data = []
        while 1:
            # Read in one line of input.
            try:
                input_line = self.readline().decode().rstrip()
            except serial.serialutil.SerialException:
                time.sleep(.2)
                continue
                
            # Check for errors and raise exception with specific error code.
            errors.check_for_errors(input_line)
            if input_line == 'OK':
                return data
            # Append only related data (starting with "command" contents).
            if command:
                if input_line.startswith(command):
                    prefix_length = len(command)+2
                    data.append(input_line[prefix_length:])
            else:
                # Append only non-empty data.
                if input_line:
                    data.append(input_line)


class ConnectionStatus(object):
    """Data structure representing current state of the modem."""

    def __init__(self):
        """Constructor for ConnectionStatus class."""
        self.rssi = 0
        self.uplink = 0
        self.downlink = 0
        self.bytes_tx = 0
        self.bytes_rx = 0
        self.link_uptime = 0
        self.mode = None
 
    def report(self):
        """Print connection status report."""
        format = '%20s : %5s'
        mapping = (('Signal Strength', self.rssi),
                   ('Bytes rx', self.bytes_rx),
                   ('Bytes tx', self.bytes_tx),
                   ('Uplink (B/s)', self.uplink),
                   ('Downlink (B/s)', self.downlink),
                   ('Seconds uptime', self.link_uptime),
                   ('Mode', self.mode))
        print()
        for item in mapping:
            print(format % item)


class Modem(atc.SetCommands, atc.GetCommands, atc.ShowCommands,
            atc.InteractiveCommands, atc.EnterCommands):
    """Class representing a modem."""

    # pylint: disable-msg=R0901
    # pylint: disable-msg=R0904
    status = ConnectionStatus()
    baudrate = defaults.BAUDRATE
    pppd_params = defaults.PPPD_PARAMS
    _pppd_pid = None
    _dial_num = defaults.DIALNUM

    def __init__(self, data=defaults.DATA_PORT,
                 ctrl=defaults.CONTROL_PORT):
        """Open a serial connection to the modem."""
        self.data_port = ModemPort(data, defaults.BAUDRATE,
                timeout=defaults.PROBER_TIMEOUT)
        self.ctrl_port = ModemPort(ctrl, 9600,
                timeout=defaults.PROBER_TIMEOUT)
        self.ctrl_lock = threading.Lock()
        self.prober = Prober(self)
        atc.SetCommands.__init__(self)
        atc.GetCommands.__init__(self)
        atc.EnterCommands.__init__(self)
        atc.InteractiveCommands.__init__(self)
        atc.ShowCommands.__init__(self)

    def connect(self, dialtone_check=True):
        """Use pppd to connect to the network."""
        # Modem is not connected if _pppd_pid is set to None.
        if not self._pppd_pid:
            data_port = self.data_port
            data_port.open()
            data_port.write(b'ATZ\r\n')
            data_port.return_data()
            if not dialtone_check:
                data_port.write(b'ATX3\r\n')
                data_port.return_data()
            data_port.write(('ATDT%s\r\n' % self._dial_num).encode())
            data_port.readline()
            status = data_port.readline()
            if status.startswith('CONNECT'):
                pppd_args = [defaults.PPPD_PATH, self.baudrate,
                             self.data_port.port] + self.pppd_params
                pid = os.fork()
                if pid:
                    self._pppd_pid = pid
                else:
                    try:
                        os.execv(defaults.PPPD_PATH, pppd_args)
                    except:
                        raise errors.PppdError('An error while starting pppd.')
        else:
            last_pppd_result = os.waitpid(self._pppd_pid, os.WNOHANG)
            if last_pppd_result != (0, 0):
                # Reconnect.
                self._pppd_pid = None
                self.connect(dialtone_check)
            else:
                # Modem already connected.   
                raise errors.HumodUsageError('Modem already connected.')

    def disconnect(self):
        """Disconnect the modem."""
        if self._pppd_pid:
            os.kill(self._pppd_pid, 15)
            os.waitpid(self._pppd_pid, 0)
            self._pppd_pid = None
        else:
            raise errors.HumodUsageError('Not connected.')
