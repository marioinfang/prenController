import serial
import time
from utils.log_config import get_logger

logger = get_logger(__name__)

class UARTHandler:
    _instance = None
    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout: float = 2):
        if UARTHandler._instance is not None:
            raise Exception("Use get_instance() to access UARTHandler.")
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UARTHandler()
        return cls._instance

    def connect(self):
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to connect to UART: {e}")

    def send(self, data: str):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("UART connection is not open!")
        try:
            logger.info(f"Sending: {data}")
            self.serial_conn.write(data.encode('utf-8'))
            self.serial_conn.flush()
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to send data: {e}")

    def receive(self) -> str:
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("UART connection is not open!")
        try:
            received_data = self.serial_conn.readline().decode('utf-8').strip()
            logger.info(f"Received: {received_data}")
            return received_data
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to receive data: {e}")

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
            except serial.SerialException as e:
                raise ConnectionError(f"Failed to close UART connection: {e}")
