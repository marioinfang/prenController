from .base_state import BaseState

class ConeDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: ConeDetected")

        decision = True

        if decision:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))