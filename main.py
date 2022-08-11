from FileParser import Parser
from GeneralInstruction import WaitInstruction
from KeyboardManager import KeyboardManager, KeyPress
from MouseManager import MouseManager, MouseInstruction

keyboard = KeyboardManager()
mouse = MouseManager()

with open('test.key', 'r') as file:
    file_content = file.read()

file_parser = Parser(file_content)

tree = file_parser.get_return()

#print(tree)
#print([str(k) for k in tree])



def call_tree(root):
    for instruction in root:
        if isinstance(instruction, MouseInstruction):
            mouse.call_mouse_instruction(instruction)
        elif isinstance(instruction, KeyPress):
            keyboard.call_key(instruction)
        elif isinstance(instruction, WaitInstruction):
            instruction.call()

print(tree)
call_tree(tree)

