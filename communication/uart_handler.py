import serial
import time

class UARTHandler:
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

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
            self.serial_conn.write(data.encode('utf-8'))
            self.serial_conn.flush()
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to send data: {e}")

    def receive(self) -> str:
        if not self.serial_conn or not self.serial_conn.is_open:
            raise ConnectionError("UART connection is not open!")
        try:
            received_data = self.serial_conn.readline().decode('utf-8').strip()
            return received_data
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to receive data: {e}")

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
            except serial.SerialException as e:
                raise ConnectionError(f"Failed to close UART connection: {e}")
