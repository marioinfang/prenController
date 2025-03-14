from state_machine.states.idle import Idle
from utils.log_config import get_logger

logger = get_logger(__name__)


class StateMachine:
    def __init__(self):
        self.state = Idle(self)
        logger.info(f"Initialized with state: {self.state.__class__.__name__}")

    def change(self):
        self.state.context()

    def set_state(self, new_state):
        logger.info(f"Transitioning from {self.state.__class__.__name__} to {new_state.__class__.__name__}")
        self.state = new_state
