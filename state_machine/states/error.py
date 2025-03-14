from .base_state import BaseState

class Error(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: Error")

        "missing logic"