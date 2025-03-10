from .base_state import BaseState

class BarrierDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: BarrierDetected")

        decision = True

        if decision:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))