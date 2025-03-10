from .base_state import BaseState

class FinishLineReached(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: FinishLineReached")

        decision = True

        if decision:
            from .error import Error
            self.machine.set_state(Error(self.machine))