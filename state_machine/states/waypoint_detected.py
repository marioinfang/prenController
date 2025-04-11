import random

from state_machine.types.decision_state import Decision
from utils.log_config import get_logger
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.vehicle_control_service import VehicleControlService
from detection.angle_detector import AngleDetector
from .base_state import BaseState
from .error import Error
from utils.raspberry_checker import is_raspberry_pi

logger = get_logger(__name__)


class WaypointDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.angle_detecor = AngleDetector()

    def context(self):
        logger.info("Entered State: WaypointDetected")
        try:
            decision, angles = self.get_decision()

            self.vehicle_control_service.drive_to_waypoint(state=Decision.WAYPOINT_DETECTED)

            if decision == Decision.WAYPOINT_REACHED:
                from .waypoint_reached import WaypointReached
                self.machine.set_state(WaypointReached(self.machine, angles))
        except CommandExecutionError:
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        If not overridden in tests, use random decision.
        """
        if is_raspberry_pi():
            from camera.pi_camera import PiCamera
            img = PiCamera().take_picture()
        else:
            import cv2
            img = cv2.imread("state_machine/input/images/testKreis30.png")
        
        angles = self.angle_detecor.get_angles(img)
        self.machine.set_data(angles)

        return Decision.WAYPOINT_REACHED, angles
