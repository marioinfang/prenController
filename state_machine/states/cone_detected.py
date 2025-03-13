from communication.car_service import CarService
from communication.types.detection_type import StopTypes
from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision

logger = get_logger(__name__)


class ConeDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.car_service = CarService()


    def context(self):
        logger.info("State: ConeDetected")
        self.car_service.stop(state=Decision.CONE_DETECTED, reason=StopTypes.CONE)

        decision = self.get_decision()

        if decision == Decision.FOLLOW_LINE:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        Replace this with actual sensor input, AI processing, or UART responses.
        """
        return Decision.FOLLOW_LINE