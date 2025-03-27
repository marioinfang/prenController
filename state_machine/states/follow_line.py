import time
import random
from detection.DetectionService import DetectionService
from vehicle_control.vehicle_control_service import VehicleControlService
from .base_state import BaseState
from .barrier_detected import BarrierDetected
from .cone_detected import ConeDetected
from .waypoint_detected import WaypointDetected
from state_machine.types.decision_state import Decision

class FollowLine(BaseState):
    SAFE_DISTANCE = 100
    UPDATE_INTERVAL = 0.1

    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()
        self.detection_service = DetectionService()

    def context(self):
        print("State: FollowLine - Continuously driving and checking for obstacles")
        
        last_check_time = time.time()

        while True:
            self.vehicle_control_service.drive(state=Decision.FOLLOW_LINE, blocked=False, distance=100)
            
            if time.time() - last_check_time >= self.UPDATE_INTERVAL:
                last_check_time = time.time()  # Reset the timer
                
                self.detection_service.capture_and_detect()
                distance, object_type = self.detection_service.get_distance_to_nearest_object()
                
                if distance != -1 and distance < self.SAFE_DISTANCE:
                    print(f"Object '{object_type}' detected at {distance} pixels! Stopping and taking action...")
                    self.vehicle_control_service.stop()
                    decision = self.get_decision(object_type)

                    if decision == Decision.CONE_DETECTED:
                        print("Cone detected - transitioning to ConeDetected state.")
                        self.machine.set_state(ConeDetected(self.machine))
                    elif decision == Decision.BARRIER_DETECTED:
                        print("Barrier detected - transitioning to BarrierDetected state.")
                        self.machine.set_state(BarrierDetected(self.machine))
                    elif decision == Decision.WAYPOINT_DETECTED:
                        print("Waypoint detected - transitioning to WaypointDetected state.")
                        self.machine.set_state(WaypointDetected(self.machine))
                    return

    def get_decision(self, object_type):
        decision_mapping = {
            "cone": Decision.CONE_DETECTED,
            "barrier": Decision.BARRIER_DETECTED,
            "waypoint": Decision.WAYPOINT_DETECTED,
        }
        return decision_mapping.get(object_type, Decision.FOLLOW_LINE)  # Default to FOLLOW_LINE
