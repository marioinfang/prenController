import random

from state_machine.types.decision_state import Decision
from utils.log_config import get_logger
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.vehicle_control_service import VehicleControlService
from .base_state import BaseState
from .error import Error
from ..input.button_service import ButtonService
from ..input.character_recognition_service import scan_node

logger = get_logger(__name__)


class WaypointDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.button_service = ButtonService.get_instance()


    def context(self):
        logger.info("Entered State: WaypointDetected")
        try:
            self.vehicle_control_service.drive_to_waypoint(state=Decision.WAYPOINT_DETECTED)

            decision = self.get_decision()

            if decision == Decision.WAYPOINT_REACHED:
                from .waypoint_reached import WaypointReached
                self.machine.set_state(WaypointReached(self.machine))
        except CommandExecutionError:
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        if self._is_destination_waypoint():
            return Decision.FINISH_LINE_REACHED
        else:
            return Decision.WAYPOINT_REACHED

    def _is_destination_waypoint(self):
        logger.info("Checking whether the waypoint is our destination state")
        destination = self.button_service.get_selected_destination()
        logger.info(f"Our destination is {destination}")

        logger.info("Processing Image")
        result = scan_node("../../tests/images/letter_A/A_3.jpeg");
        logger.info(f"Image result: {result}")
        if destination == result:
            return True
        else:
            return False
