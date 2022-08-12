from __future__ import annotations
from Types import Instruction
from instructions.KeyboardManager import KeyboardManager, KeyPress
from instructions.MouseManager import MouseManager, MouseInstruction
from instructions.GeneralInstruction import GeneralInstruction
from Parser import Parser

class PyAutoHotKey:

    def __init__(self):
        self.keyboard = KeyboardManager()
        self.mouse = MouseManager()

    def execute_string(self, string: str):
        parser = Parser(string)
        instruction_tree = parser.get_return()
        self.call_tree(instruction_tree)

    def execute_file(self, file_name: str):
        with open(file_name, 'r') as file:
            file_content = file.read()
            self.execute_string(file_content)

    def call_tree(self, tree: list[Instruction]):
        for instruction in tree:
            if isinstance(instruction, MouseInstruction):
                self.mouse.call_mouse_instruction(instruction)
            elif isinstance(instruction, KeyPress):
                self.keyboard.call_key(instruction)
            elif isinstance(instruction, GeneralInstruction):
                instruction.call()