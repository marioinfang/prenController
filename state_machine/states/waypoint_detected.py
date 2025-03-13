from communication.car_service import CarService
from communication.types.detection_type import StopTypes
from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision

logger = get_logger(__name__)


class WaypointDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.car_service = CarService()

    def context(self):
        logger.info("Entered State: WaypointDetected")
        self.car_service.stop(state=Decision.WAYPOINT_DETECTED, reason=StopTypes.WAYPOINT)

        decision = self.get_decision()

        if decision == Decision.WAYPOINT_REACHED:
            from .waypoint_reached import WaypointReached
            self.machine.set_state(WaypointReached(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        Replace this with actual sensor input, AI processing, or UART responses.
        """
        return Decision.WAYPOINT_REACHED
