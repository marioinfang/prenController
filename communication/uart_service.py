import time
from utils.log_config import get_logger
from .mock_uart_handler import MockUARTHandler
from .uart_handler import UARTHandler

logger = get_logger(__name__)

#TODO MAYBE use env var instead of this nasty workaround
def is_raspberry_pi():
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read()
        return "Raspberry Pi" in cpuinfo
    except FileNotFoundError:
        return False


class UARTService:
    def __init__(self):
        if is_raspberry_pi():
            self.uart = UARTHandler()
        else:
            self.uart = MockUARTHandler.get_instance()
        self.uart.connect()

    def send(self, command: str, max_retries=3, ack_timeout=2.0):
        for attempt in range(max_retries):
            logger.info(f"Sending command (Attempt {attempt+1}): {command}")
            self.uart.send(command)

            start_time = time.time()
            while time.time() - start_time < ack_timeout:
                response = self.uart.receive()

                if response:
                    logger.info(f"Received: {response}")
                    return response

            logger.warning(f"No ACK received for {command}, retrying...")

        logger.error(f"Command {command} failed after {max_retries} retries.")
        return "ERR"