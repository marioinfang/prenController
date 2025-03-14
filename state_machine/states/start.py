from .base_state import BaseState
from .decision_state import Decision

class Start(BaseState):

    def __init__(self, machine):
            self.machine = machine

    def context(self):
        print("State: Start")

        "missing logic"

        decision = Decision.FOLLOW_LINE

        if decision == Decision.FOLLOW_LINE:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
