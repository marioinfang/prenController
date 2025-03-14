from states.idle import Idle

class StateMachine:
    def __init__(self):
        self.state = Idle(self)

    def change(self):
        self.state.context()

    def set_state(self, new_state):
        self.state = new_state