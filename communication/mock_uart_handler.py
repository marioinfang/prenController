import queue
import re

from utils.log_config import get_logger

logger = get_logger(__name__)

class MockUARTHandler:
    _instance = None

    def __init__(self):
        logger.warning("Running in MOCK mode. No real UART connection is being used.")
        self.mock_queue = queue.Queue()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MockUARTHandler()
        return cls._instance

    def connect(self):
        self.is_open = True

    def send(self, data: str):
        logger.info(f"[MOCK] Sending: {data}")
        self.mock_queue.put(f"ACK: {data}")

    def receive(self) -> str:
        try:
            received_data = self.mock_queue.get(timeout=1)
            logger.info(f"[MOCK] Received: {received_data}")
            return "ACK"
        except queue.Empty:
            return ""

    def close(self):
        self.is_open = False
        logger.info("[MOCK] UART connection closed.")