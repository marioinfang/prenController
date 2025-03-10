from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self, machine):
        self.machine = machine

    @abstractmethod
    def context(self):
        pass
