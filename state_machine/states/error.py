from utils.log_config import get_logger
from .base_state import BaseState
logger = get_logger(__name__)

class Error(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        logger.error("Entered State: Error")

        "missing logic"