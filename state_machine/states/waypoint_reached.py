import random

from vehicle_control.types.direction_type import DirectionType
from vehicle_control.vehicle_control_service import VehicleControlService
from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision

logger = get_logger(__name__)


class WaypointReached(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
    def context(self):
        logger.info("Entered State: WaypointReached")

        "missing logic"

        decision = self.get_decision()

        if decision == Decision.FINISH_LINE_REACHED:
            from .finish_line_reached import FinishLineReached
            self.machine.set_state(FinishLineReached(self.machine))
        elif decision == Decision.FOLLOW_LINE:
            self.vehicle_control_service.rotate(Decision.WAYPOINT_REACHED, DirectionType.LEFT, 65)
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))


    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        If not overridden in tests, use random decision.
        """
        return random.choice([
            Decision.FINISH_LINE_REACHED,
            Decision.FOLLOW_LINE
        ])

    def get_direction(self):
        """
        Placeholder for real decision-making logic.
        If not overridden in tests, use random decision.
        """
        return random.choice([
            DirectionType.LEFT,
            DirectionType.RIGHT
        ])
