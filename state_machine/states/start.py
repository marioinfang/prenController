from .base_state import BaseState

class Start(BaseState):

    def __init__(self, machine):
            self.machine = machine

    def context(self):
        print("State: Start")

        decision = True

        if decision == True:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))
