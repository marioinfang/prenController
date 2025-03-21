import time

from .base_state import BaseState
from .start import Start
from utils.log_config import get_logger
from ..input.button_service import ButtonService

logger = get_logger(__name__)

class Idle(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.running = True
        self.button_service = ButtonService(self.button_pressed)

    def context(self):
        logger.info("State: Idle - Waiting for button press")
        while self.running:
            time.sleep(0.1)

    def button_pressed(self, button_name: str):
        logger.info(f"Button {button_name} pressed! Transitioning to Start state.")
        self.running = False
        self.machine.set_state(Start(self.machine))

    def exit(self):
        self.button_service.stop()