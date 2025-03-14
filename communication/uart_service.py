import time
import threading
import queue
from utils.log_config import get_logger
from .mock_uart_handler import MockUARTHandler
from .uart_handler import UARTHandler

logger = get_logger(__name__)

# TODO: Use an environment variable instead of this workaround
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
        self.running = False
        self.listen_thread = None
        self.message_queue = queue.Queue()

    def send(self, command: str, max_retries=3, ack_timeout=2.0) -> str:
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

    def start_listening(self):
        if self.running:
            logger.warning("Listening is already running.")
            return

        self.running = True
        self.listen_thread = threading.Thread(target=self._listen, daemon=True)
        self.listen_thread.start()
        logger.info("Started UART listening.")

    def stop_listening(self):
        if not self.running:
            logger.warning("Listening is already stopped.")
            return

        self.running = False
        logger.info("Stopped UART listening.")

    def _listen(self):
        while self.running:
            response = self.uart.receive()
            if response:
                logger.info(f"Received (Listening Mode): {response}")
                self.message_queue.put(response)

    def get_received_message(self, timeout: float = 1.0) -> str:
        try:
            return self.message_queue.get(timeout=timeout)
        except queue.Empty:
            return ""