import time
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from detection.detection_service import DetectionService
from vehicle_control.vehicle_control_service import VehicleControlService
from .base_state import BaseState
from .barrier_detected import BarrierDetected
from .cone_detected import ConeDetected
from .waypoint_detected import WaypointDetected
from state_machine.types.decision_state import Decision
from vehicle_control.types.detection_type import StopTypes
from .error import Error
from utils.log_config import get_logger

logger = get_logger(__name__)

class FollowLine(BaseState):
    UPDATE_INTERVAL = 0.1
    DEFAULT_DRIVE_DISTANCE = 100
    SAFE_DISTANCE = 100

    SAFE_DISTANCES = {
        "cone": 100,
        "barrier": 30,
        "waypoint": 30
    }

    OBJECT_STATES = {
        "cone": ConeDetected,
        "barrier": BarrierDetected,
        "waypoint": WaypointDetected
    }

    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.detection_service = DetectionService()
        self.current_distance = self.DEFAULT_DRIVE_DISTANCE

    def context(self):
        logger.info("Entered State: FollowLine")

        try:
            while self.machine.current_state == self:
                time.sleep(self.UPDATE_INTERVAL)
                self._drive_vehicle()

                # Detect only the object directly in front of the vehicle
                front_obj = self.detection_service.get_object_in_path()

                if front_obj:
                    logger.info(f"Object detected directly in front of the vehicle: {front_obj}")
                    distance = front_obj["distance_from_bottom"]
                    object_type = front_obj["name"]

                    if isinstance(distance, (int, float)) and isinstance(object_type, str):
                        self._handle_obstacle(distance, object_type)

        except Exception as e:
            logger.error(f"Error in FollowLine state: {e}")
            self.machine.set_state(Error(self.machine))

    def _drive_vehicle(self):
        try:
            self.vehicle_control_service.drive(
                state=Decision.FOLLOW_LINE,
                blocked=False,
                distance=self.current_distance
            )
        except CommandExecutionError as e:
            logger.error(f"Error while sending drive command: {e}")
            self.machine.set_state(Error(self.machine))

    def _handle_obstacle(self, distance, object_type):
        safe_distance = self.SAFE_DISTANCES.get(object_type, self.SAFE_DISTANCE)

        if distance <= safe_distance:
            logger.info(f"Stopping vehicle due to {object_type} at distance {distance}px")
            try:
                self.vehicle_control_service.stop(
                    state=Decision.FOLLOW_LINE,
                    reason=StopTypes.OBSTACLE
                )
            except CommandExecutionError as e:
                logger.error(f"Error while stopping the vehicle: {e}")
                self.machine.set_state(Error(self.machine))

            next_state_class = self.OBJECT_STATES.get(object_type)
            if next_state_class:
                self.machine.set_state(next_state_class(self.machine))
