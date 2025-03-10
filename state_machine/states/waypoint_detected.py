from .base_state import BaseState

class WaypointDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: WaypointDetected")

        decision = True

        if decision == True:
            from .waypoint_reached import WaypointReached
            self.machine.set_state(WaypointReached(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))