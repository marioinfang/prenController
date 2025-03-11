from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def context(self):
        "Implementation of the logic of the state"
        pass
