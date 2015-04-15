import sys
import unittest
try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock
    from imp import reload
import serial
import humod

class MockSerial(serial.serialutil.SerialBase):
    payload = None
    def __init__(self, port, baudrate, **kwargs):
        serial.serialutil.SerialBase.__init__(self, None, baudrate, **kwargs)
        self.read = Mock()
        self.write = Mock()
        self.payload = []

    def inWaiting(self):
        return sum(len(s) for s in self.payload)

    def readline(self):
        line = self.payload.pop(0)
        if sys.version_info >= (3, 0):
            line = bytes(line, 'utf-8')
        return line


class TestHumod(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        humod.humodem.serial.Serial = MockSerial
        reload(humod.humodem)

    def setUp(self):
        self.modem = humod.Modem()

    def test_handle_content_ok(self):
        self.set_payload([
            u'CMDOK',
            u'+CMGL: 0,"REC READ","999222",,"12/05/10,10:05:41+08"\r\n',
            u'Za Data, Internet Vam bylo odecteno 30.00 Kc.\r\n',
            u'+CMGL: 1,"REC READ","999222",,"12/05/10,10:05:41+08"\r\n',
            u'OK\r\n',
            u'+CMGL: 2,"REC READ","123456",,"12/05/10,09:50:51+08"\r\n',
            u'Whatever\r\n',
            u'OK\r\n',
        ])
        texts = self.modem.sms_list()
        self.assertEqual(3, len(texts))

    def set_payload(self, payload):
        self.modem.ctrl_port.payload = payload

if __name__ == "__main__":
    unittest.main()
