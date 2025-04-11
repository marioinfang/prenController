from state_machine.types.decision_state import Decision
from utils.log_config import get_logger
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.types.detection_type import StopTypes
from vehicle_control.types.direction_type import DirectionType
from vehicle_control.vehicle_control_service import VehicleControlService
from .base_state import BaseState
from .error import Error

logger = get_logger(__name__)


class WaypointReached(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()

    def context(self):
        logger.info("Entered State: WaypointReached")

        try:
            "missing logic"

            decision = self.get_decision()

            if decision == Decision.FINISH_LINE_REACHED:
                from .finish_line_reached import FinishLineReached
                self.vehicle_control_service.stop(Decision.FINISH_LINE_REACHED, StopTypes.WAYPOINT)
                self.machine.set_state(FinishLineReached(self.machine))
            elif decision == Decision.FOLLOW_LINE:
                self.vehicle_control_service.rotate(Decision.WAYPOINT_REACHED, DirectionType.LEFT, 65)
                from .follow_line import FollowLine
                self.machine.set_state(FollowLine(self.machine))
        except CommandExecutionError:
            self.machine.set_state(Error(self.machine))


    def get_decision(self):
        return Decision.FOLLOW_LINE

