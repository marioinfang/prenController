import random

from communication.vehicle_control_service import VehicleControlService
from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision

logger = get_logger(__name__)


class FollowLine(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()

    def context(self):
        logger.info("Entered State: FollowLine")

        self.vehicle_control_service.drive(state=Decision.FOLLOW_LINE, blocked=False, distance=100)

        decision = self.get_decision()

        if decision == Decision.WAYPOINT_DETECTED:
            from .waypoint_detected import WaypointDetected
            self.machine.set_state(WaypointDetected(self.machine))
        elif decision == Decision.BARRIER_DETECTED:
            from .barrier_detected import BarrierDetected
            self.machine.set_state(BarrierDetected(self.machine))
        elif decision == Decision.CONE_DETECTED:
            from .cone_detected import ConeDetected
            self.machine.set_state(ConeDetected(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        If not overridden in tests, use random decision.
        """
        return random.choice([
            Decision.WAYPOINT_DETECTED,
            Decision.BARRIER_DETECTED,
            Decision.CONE_DETECTED
        ])