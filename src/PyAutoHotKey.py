from __future__ import annotations
from pathlib import Path
from Types import Instruction
from instructions.KeyboardManager import KeyboardManager, KeyPress
from instructions.MouseManager import MouseManager, MouseInstruction
from instructions.KeybindManager import KeybindManager, Keybind
from instructions.GeneralInstruction import GeneralInstruction
from Parser import Parser

class PyAutoHotKey:

    def __init__(self):
        self.keyboard = KeyboardManager()
        self.mouse = MouseManager()
        self.keybind = KeybindManager(self, self.keyboard)

    def execute_string(self, string: str):
        parser = Parser(string)
        instruction_tree = parser.get_return()
        self.call_tree(instruction_tree)

    def execute_file(self, file_name: Path):
        with open(file_name, 'r') as file:
            file_content = file.read()
            self.execute_string(file_content)

    def call_tree(self, tree: list[Instruction], keybind=True):
        keybinds = []
        for instruction in tree:
            if isinstance(instruction, MouseInstruction):
                self.mouse.call_mouse_instruction(instruction)
            elif isinstance(instruction, KeyPress):
                self.keyboard.call_key(instruction)
            elif isinstance(instruction, GeneralInstruction):
                instruction.call()
            elif isinstance(instruction, Keybind):
                keybinds.append(instruction)
        if keybind:
            self.keybind.add_keybinds(keybinds)