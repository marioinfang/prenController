from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision

logger = get_logger(__name__)


class Start(BaseState):

    def __init__(self, machine):
        self.machine = machine

    def context(self):
        logger.info("Entered State: Start")
        #TODO add logic when destination selected and start button pressed

        decision = Decision.FOLLOW_LINE

        if decision == Decision.FOLLOW_LINE:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
