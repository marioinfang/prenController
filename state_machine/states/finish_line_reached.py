from .base_state import BaseState
from .decision_state import Decision

class FinishLineReached(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: FinishLineReached")

        "missing logic"

        decision = Decision.ERROR

        if decision == Decision.ERROR:
            from .error import Error
            self.machine.set_state(Error(self.machine))