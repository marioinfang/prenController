from .base_state import BaseState

class FollowLine(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: FollowLine")

        decision = 1

        if decision == 1:
            from .waypoint_detected import WaypointDetected
            self.machine.set_state(WaypointDetected(self.machine))
        elif decision == 2:
            from .barrier_detected import BarrierDetected
            self.machine.set_state(BarrierDetected(self.machine))
        elif decision == 3:
            from .cone_detected import ConeDetected
            self.machine.set_state(ConeDetected(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
