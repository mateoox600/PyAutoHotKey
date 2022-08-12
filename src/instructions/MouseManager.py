from __future__ import annotations
from pynput.mouse import Controller
from abc import ABC, abstractmethod

class MouseInstruction(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def call(self, mouse: MouseManager):
        raise NotImplementedError()

class MouseClick(MouseInstruction):
    def __init__(self, button: int):
        self.button = button

    def call(self, mouse: MouseManager):
        mouse.controller.press(self.button)
        mouse.controller.release(self.button)

    def __str__(self):
        return f'MouseClick[button={self.button}]'

class MouseMove(MouseInstruction):
    def __init__(self, position: tuple[int, int]):
        self.position = position

    def call(self, mouse: MouseManager):
        mouse.controller.position = self.position

    def __str__(self):
        return f'MouseMove[position=({self.position[0]},{self.position[1]})]'

class MouseManager:

    def __init__(self):
        self.controller = Controller()

    def call_mouse_instruction(self, mouse_instruction: MouseInstruction):
        mouse_instruction.call(self)
