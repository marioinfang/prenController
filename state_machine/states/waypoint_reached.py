from .base_state import BaseState
from .decision_state import Decision

class WaypointReached(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: WaypointReached")

        "missing logic"

        decision = Decision.FINISH_LINE_REACHED

        if decision == Decision.FINISH_LINE_REACHED:
            from .finish_line_reached import FinishLineReached
            self.machine.set_state(FinishLineReached(self.machine))
        elif decision == Decision.SEARCH_PATH:
            from .search_path import SearchPath
            self.machine.set_state(SearchPath(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))