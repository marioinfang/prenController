import random

from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.types.detection_type import StopTypes
from vehicle_control.types.direction_type import DirectionType
from vehicle_control.vehicle_control_service import VehicleControlService
from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision
from .error import Error
from ..input.button_service import ButtonService
from ..input.character_recognition_service import process_image
logger = get_logger(__name__)


class WaypointReached(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.button_service = ButtonService.get_instance()

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
        if self._is_destination_waypoint():
            return Decision.FINISH_LINE_REACHED
        else:
            return Decision.FOLLOW_LINE

    def _is_destination_waypoint(self):
        logger.info("Checking whether the waypoint is our destination state")
        destination = self.button_service.get_selected_destination()
        logger.info(f"Our destination is {destination}")

        logger.info("Processing Image")
        result = process_image("../../images/test_image_c_flipped.jpeg")
        logger.info(f"Image result: {result}")
        if destination == result:
            return True
        else:
            return False