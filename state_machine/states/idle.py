import random

from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision

logger = get_logger(__name__)


class Idle(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        logger.info("Entered: Idle State")

        "missing logic"

        decision = self.get_decision()

        if decision == Decision.START:
            from .start import Start
            self.machine.set_state(Start(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        If not overridden in tests, use random decision.
        """
        return random.choice([
            Decision.START
        ])