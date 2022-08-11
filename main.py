from KeyboardManager import KeyboardManager
from FileParser import Parser

keyboard = KeyboardManager()

with open('test.key', 'r') as file:
    file_content = file.read()

file_parser = Parser(file_content)

tree = file_parser.get_return()

#print(tree)ttestTESTMA
#print([str(k) for k in tree])

keyboard.callTree(tree)

