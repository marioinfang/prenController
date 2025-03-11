from .base_state import BaseState
from .decision_state import Decision

class WaypointDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: WaypointDetected")

        "missing logic"

        decision = Decision.WAYPOINT_REACHED

        if decision == Decision.WAYPOINT_REACHED:
            from .waypoint_reached import WaypointReached
            self.machine.set_state(WaypointReached(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))