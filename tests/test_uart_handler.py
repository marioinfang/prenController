from unittest import TestCase
from unittest.mock import patch
from communication.uart_handler import UARTHandler
import serial


class TestUARTHandler(TestCase):
    @patch("serial.Serial")
    def test_connect(self, mock_serial):
        uart = UARTHandler("/dev/serial0")
        uart.connect()
        mock_serial.assert_called_with(port="/dev/serial0", baudrate=115200, timeout=1)

    @patch("serial.Serial")
    def test_connect_failure(self, mock_serial):
        mock_serial.side_effect = serial.SerialException("Connection failed")
        uart = UARTHandler("/dev/serial0")
        with self.assertRaises(ConnectionError) as context:
            uart.connect()
        self.assertIn("Failed to connect to UART", str(context.exception))

    @patch("serial.Serial")
    def test_send_data(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = True

        uart = UARTHandler("/dev/serial0")
        uart.connect()
        uart.send("Test Message")

        mock_serial_instance.write.assert_called_with(b"Test Message")

    @patch("serial.Serial")
    def test_send_data_failure(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = False

        uart = UARTHandler("/dev/serial0")
        uart.connect()
        with self.assertRaises(ConnectionError) as context:
            uart.send("Test Message")
        self.assertIn("UART connection is not open!", str(context.exception))

    @patch("serial.Serial")
    def test_receive_data(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = True
        mock_serial_instance.readline.return_value = b"Received Data\n"

        uart = UARTHandler("/dev/serial0")
        uart.connect()
        data = uart.receive()

        self.assertEqual(data, "Received Data")

    @patch("serial.Serial")
    def test_receive_data_failure(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = False

        uart = UARTHandler("/dev/serial0")
        uart.connect()
        with self.assertRaises(ConnectionError) as context:
            uart.receive()
        self.assertIn("UART connection is not open!", str(context.exception))

    @patch("serial.Serial")
    def test_close(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = True

        uart = UARTHandler("/dev/serial0")
        uart.connect()
        uart.close()

        mock_serial_instance.close.assert_called()

    @patch("serial.Serial")
    def test_close_failure(self, mock_serial):
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.is_open = True
        mock_serial_instance.close.side_effect = serial.SerialException("Close failed")

        uart = UARTHandler("/dev/serial0")
        uart.connect()
        with self.assertRaises(ConnectionError) as context:
            uart.close()
        self.assertIn("Failed to close UART connection", str(context.exception))