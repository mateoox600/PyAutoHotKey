from time import sleep
from abc import ABC, abstractmethod

class GeneralInstruction(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def call(self):
        pass

class WaitInstruction(GeneralInstruction):
    def __init__(self, time: int):
        self.time = time

    def call(self):
        sleep(self.time / 1000)