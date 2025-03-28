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
        print("Entered State: FollowLine")

        try:
            while self.machine.current_state == self:
                time.sleep(self.UPDATE_INTERVAL)  
                self._drive_vehicle()
                
                detections = self.detection_service.capture_and_detect()
                if detections:
                    print(f"Detections: {detections}")
                
                distance_data = self.detection_service.get_distance_to_nearest_object()
                
                if isinstance(distance_data, tuple) and len(distance_data) == 2:
                    distance, object_type = distance_data
                    if isinstance(distance, (int, float)) and isinstance(object_type, str):
                        self._handle_detected_object(distance, object_type)

        except CommandExecutionError as e:
            print(f"Error: {e}")
            self.machine.set_state(Error(self.machine))

    def _drive_vehicle(self):
        self.vehicle_control_service.drive(state=Decision.FOLLOW_LINE, blocked=False, distance=self.current_distance)

    def _handle_detected_object(self, distance, object_type):
        object_safe_distance = self.SAFE_DISTANCES.get(object_type, self.SAFE_DISTANCE)

        if distance == -1 or distance >= object_safe_distance:
            self.current_distance = self.DEFAULT_DRIVE_DISTANCE
            return

        print(f"Object '{object_type}' detected at {distance}, adjusting distance.")
        self.current_distance = max(20, int((distance / object_safe_distance) * self.DEFAULT_DRIVE_DISTANCE))

        if distance < object_safe_distance // 2:  
            print(f"Stopping due to '{object_type}' detected at {distance}.")
            self.vehicle_control_service.stop(state=Decision.FOLLOW_LINE, reason=StopTypes.OBSTACLE_DETECTED)

            next_state = self.OBJECT_STATES.get(object_type)
            if next_state:
                print(f"Switching to state: {next_state.__name__}")
                self.machine.set_state(next_state(self.machine))
            else:
                print("Unknown object detected. Continuing to follow the line.")
