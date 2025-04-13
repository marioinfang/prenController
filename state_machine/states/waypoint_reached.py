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
from utils.raspberry_checker import is_raspberry_pi

logger = get_logger(__name__)


class WaypointReached(BaseState):
    def __init__(self, machine, angles):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.line_analyzer = PathAnalyzer("detection/model/best.onnx")
        self.angles = angles

    def context(self):
        logger.info("Entered State: WaypointReached")

        try:
            decision = self.get_decision()

            if decision == Decision.FOLLOW_LINE:
                from .follow_line import FollowLine
                self.machine.set_state(FollowLine(self.machine))
        except CommandExecutionError:
            self.machine.set_state(Error(self.machine))


    def get_decision(self):
            self._find_line()
            return Decision.FOLLOW_LINE
        
    def _find_line(self):
        sorted_angles = sorted(self.angles)

        for angle in sorted_angles[1:]:
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
            is_cone_on_line,_,_ = self.line_analyzer.analyze_path(img)
            return not is_cone_on_line

        return random.choice([True, False])

