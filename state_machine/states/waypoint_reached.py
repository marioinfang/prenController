from .base_state import BaseState

class WaypointReached(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: WaypointReached")

        decision = 1

        if decision == 1:
            from .finish_line_reached import FinishLineReached
            self.machine.set_state(FinishLineReached(self.machine))
        elif decision == 2:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))