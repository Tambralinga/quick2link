import unittest
from quick2link.serialtransport import *

__author__ = 'romilly'


class SerialHalfDuplexTransportTest(unittest.TestCase):
    def testSerial_transport_asks_for_result(self):
        with closing(SerialHalfDuplexTransport()) as transport:
            self.assertIn("arduino", transport.ask('?'))

BAD_REQUEST='`'
class ArduinoTest(unittest.TestCase):
    def setUp(self): self.arduino = Arduino()
    def tearDown(self):
        if self.arduino is not None: self.arduino.close()

    def testRespondsWithIdentifier(self):
        self.assertEqual("arduino", self.arduino.ask(whois()))

    def testFailsWithUnknownCommand(self):
        with self.assertRaises(SerialTransportException) as cm:
            self.arduino.ask(BAD_REQUEST)
        exception_message = str(cm.exception)
        self.assertIn(BAD_REQUEST, exception_message)
        self.assertIn('1', exception_message)

    def testEchoesProcessedCharacters(self):
        self.assertEqual("arduino>e?", self.arduino.ask("e", whois()))

    def testWritesAndReadsDigitalPin(self):
        # connect digital pins 11 <-> 12
        self.assertEqual("1>e12d1o11dip",
            self.arduino.ask(
                echo(),
                on_pin(12), digital_write(HIGH),
                on_pin(11), digital_read(), print_value()))
        self.assertEqual("0>e12d0o11dip",
            self.arduino.ask(
                echo(),
                on_pin(12), digital_write(LOW),
                on_pin(11), digital_read(), print_value()))

if __name__ == '__main__':
    unittest.main()
