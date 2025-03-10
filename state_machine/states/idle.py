from .base_state import BaseState

class Idle(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: Idle")

        decision = True

        if decision:
            from .start import Start
            self.machine.set_state(Start(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
