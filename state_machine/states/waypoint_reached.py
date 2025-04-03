import random

from state_machine.types.decision_state import Decision
from utils.log_config import get_logger
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.types.detection_type import StopTypes
from vehicle_control.types.direction_type import DirectionType
from vehicle_control.vehicle_control_service import VehicleControlService
from detection.path_analyzer import PathAnalyzer
from .base_state import BaseState
from .error import Error
from ..input.button_service import ButtonService
from utils.raspberry_checker import is_raspberry_pi

logger = get_logger(__name__)


class WaypointReached(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.button_service = ButtonService.get_instance()
        self.line_analyzer = PathAnalyzer()

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
            self._find_line()
            return Decision.FOLLOW_LINE

    def _is_destination_waypoint(self):
        logger.info("Checking whether the waypoint is our destination state")
        destination = self.button_service.get_selected_destination()
        logger.info(f"Our destination is {destination}")

        logger.info("Processing Image")
        #result = process_image("../input/images/test_image_c_flipped.jpeg")
        result = True
        logger.info(f"Image result: {result}")
        if destination == result:
            return True
        else:
            return False
        
    def _find_line(self):
        sorted_angles = sorted(self.machine.data)

        for angle in sorted_angles[:-1]:
            self.vehicle_control_service.rotate(Decision.WAYPOINT_REACHED, DirectionType.RIGHT, angle)

            if self._is_driveable_line():
                logger.info("Drivable line was found!")
                return

        logger.info("No drivable line was found! Rotade to initial line.")
        self.vehicle_control_service.rotate(Decision.WAYPOINT_REACHED, DirectionType.RIGHT, sorted_angles[-1])


    def _is_driveable_line(self):
        if is_raspberry_pi():
            from camera.pi_camera import PiCamera
            img = PiCamera.take_picture()
            self.line_analyzer.analyze_path(img)

        return random.choice([True, False])
