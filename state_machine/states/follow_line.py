from .base_state import BaseState
from .decision_state import Decision

class FollowLine(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: FollowLine")

        "missing logic"

        decision = Decision.WAYPOINT_DETECTED

        if decision == Decision.BARRIER_DETECTED:
            from .waypoint_detected import WaypointDetected
            self.machine.set_state(WaypointDetected(self.machine))
        elif decision == Decision.BARRIER_DETECTED:
            from .barrier_detected import BarrierDetected
            self.machine.set_state(BarrierDetected(self.machine))
        elif decision == Decision.CONE_DETECTED:
            from .cone_detected import ConeDetected
            self.machine.set_state(ConeDetected(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
