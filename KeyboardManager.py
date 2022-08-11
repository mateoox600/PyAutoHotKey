from __future__ import annotations
from abc import ABC, abstractmethod

from pynput.keyboard import Controller

class KeyPress(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def call(self, keyboard: KeyboardManager):
        pass

class KeyTap(KeyPress):
    def __init__(self, key):
        self.key = key

    def call(self, keyboard: KeyboardManager):
        keyboard.controller.press(self.key)
        keyboard.controller.release(self.key)

    def __str__(self):
        return f'KeyTap[key={self.key}]'

class KeyHold(KeyPress):
    def __init__(self, key, sub_keys: KeyPress | list[KeyPress] = None):
        if sub_keys is None:
            sub_keys = list()
        self.key = key
        self.sub_keys = sub_keys

    def call(self, keyboard: KeyboardManager):
        keyboard.controller.press(self.key)
        if isinstance(self.sub_keys, list):
            [key.call(keyboard) for key in self.sub_keys]
        else:
            self.sub_keys.call(keyboard)
        keyboard.controller.release(self.key)

    def __str__(self):
        return f'KeyHold[key={self.key}, sub_keys={[str(k) for k in self.sub_keys]}]'

class KeyboardManager:

    def __init__(self):
        self.controller = Controller()

    def callTree(self, root: KeyPress | list[KeyPress]):
        if isinstance(root, list):
            [key.call(self) for key in root]
        else:
            root.call(self)
