from .base_state import BaseState
from .decision_state import Decision

class Idle(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: Idle")

        "missing logic"

        decision = Decision.START

        if decision == Decision.START:
            from .start import Start
            self.machine.set_state(Start(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
