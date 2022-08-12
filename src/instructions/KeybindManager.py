from __future__ import annotations
from functools import partial
from pynput import keyboard
from pynput.keyboard import Key
from Types import Instruction
from instructions.KeyboardManager import KeyboardManager, KeyTap, KeyHold

class Keybind:

    def __init__(self, keybind: Instruction, keys: list[Instruction]):
        self.keybind = keybind
        self.keys = keys

    def call(self, instance):
        instance.call_tree(self.keys, False)

    def __str__(self):
        return f'Keybind[keybind={str(self.keybind)},keys={(str(key) for key in self.keys)}]'

class KeybindManager:

    def __init__(self, instance, keyboard_manager: KeyboardManager):
        self.instance = instance
        self.keyboard = keyboard_manager

    def compile_key_name(self, key_name: Key | str):
        if isinstance(key_name, Key):
            return f'<{key_name.name}>'
        return key_name if len(key_name) < 2 else f'<{key_name}>'

    def map_instruction_name(self, instruction: Instruction):
        output = ''
        if isinstance(instruction, KeyHold):
            output = f'{self.compile_key_name(instruction.key)}+{self.map_instruction_name(instruction.sub_keys[0])}'
        elif isinstance(instruction, KeyTap):
            output = f'{self.compile_key_name(instruction.key)}'
        return output

    def add_keybinds(self, keybinds: list[Keybind]):
        hotkeys = {}
        for keybind in keybinds:
            key = self.map_instruction_name(keybind.keybind)
            hotkeys[key] = partial(keybind.call, self.instance)

        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()
