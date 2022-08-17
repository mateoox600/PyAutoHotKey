import re
from enum import Enum
from pynput.keyboard import Key
from pynput.mouse import Button
from Types import Instruction
from instructions.GeneralInstruction import WaitInstruction
from instructions.KeyboardManager import KeyTap, KeyHold
from instructions.MouseManager import MouseClick, MouseMove
from instructions.KeybindManager import KeybindTap, KeybindToggle

class TokenType(Enum):
    NO_TOKEN = 0
    SINGLE_CHAR_KEY_TOKEN = 1
    MULTIPLE_CHAR_KEY_TOKEN = 2
    KEY_LIST_TOKEN = 3
    MOUSE_INSTRUCTION_TOKEN = 4
    TIME_WAIT_TOKEN = 5
    KEYBIND_TOKEN = 6
    TOGGLE_KEYBIND_TOKEN = 7

class Parser:

    def __init__(self, string: str):
        self.string = string

        self.tokens = []
        self.current_token = ''
        self.current_token_type = TokenType.NO_TOKEN
        self.opened = {
            '(': 0,
            '[': 0,
            '{': 0
        }

        self.parse_string()
        self.combine_keys()
        self.transform_tokens_to_instructions()

    def finish_token(self):
        if self.current_token_type in (TokenType.KEY_LIST_TOKEN, TokenType.KEYBIND_TOKEN):
            self.current_token = self.current_token[1:-1]
            self.parse_key_list_from_current()
        elif self.current_token_type in (
                TokenType.MULTIPLE_CHAR_KEY_TOKEN,
                TokenType.MOUSE_INSTRUCTION_TOKEN,
                TokenType.TIME_WAIT_TOKEN):
            self.current_token = self.current_token[2:-1]
        elif self.current_token_type == TokenType.TOGGLE_KEYBIND_TOKEN:
            self.current_token = self.current_token[2:-1]
            self.parse_key_list_from_current()
        self.tokens.append((self.current_token_type, self.current_token))
        self.current_token = ''
        self.current_token_type = TokenType.NO_TOKEN

    def parse_key_list_from_current(self):
        parser = Parser(self.current_token)
        self.current_token = parser.get_return()

    def any_opened(self):
        return self.opened['('] == 0 and self.opened['['] == 0 and self.opened['{'] == 0

    def parse_string(self):
        for char in [*self.string]:
            if re.match(r'\s', char) and self.current_token_type != TokenType.KEY_LIST_TOKEN:
                continue
            if self.current_token_type == TokenType.SINGLE_CHAR_KEY_TOKEN:
                if char == '(':
                    self.current_token += char
                    self.opened['('] += 1
                    if self.current_token.startswith('k'):
                        self.current_token_type = TokenType.MULTIPLE_CHAR_KEY_TOKEN
                        continue
                    elif self.current_token.startswith('m'):
                        self.current_token_type = TokenType.MOUSE_INSTRUCTION_TOKEN
                        continue
                    elif self.current_token.startswith('t'):
                        self.current_token_type = TokenType.TIME_WAIT_TOKEN
                        continue
                elif char == '{' and self.current_token.startswith(':'):
                    self.current_token += char
                    self.opened['{'] += 1
                    self.current_token_type = TokenType.TOGGLE_KEYBIND_TOKEN
                    continue
                else:
                    self.finish_token()
            self.current_token += char
            if self.current_token_type != TokenType.NO_TOKEN:
                if char == '(':
                    self.opened['('] += 1
                elif char == '[':
                    self.opened['['] += 1
                elif char == '{':
                    self.opened['{'] += 1
                elif char == ')':
                    self.opened['('] -= 1
                elif char == ']':
                    self.opened['['] -= 1
                elif char == '}':
                    self.opened['{'] -= 1
            if self.current_token_type == TokenType.NO_TOKEN:
                if char == '[':
                    self.opened['['] += 1
                    self.current_token_type = TokenType.KEY_LIST_TOKEN
                elif char == '{':
                    self.opened['{'] += 1
                    self.current_token_type = TokenType.KEYBIND_TOKEN
                else:
                    self.current_token_type = TokenType.SINGLE_CHAR_KEY_TOKEN
            elif self.current_token_type in (
                    TokenType.MULTIPLE_CHAR_KEY_TOKEN,
                    TokenType.MOUSE_INSTRUCTION_TOKEN,
                    TokenType.TIME_WAIT_TOKEN):
                if char == ')' and self.any_opened():
                    self.finish_token()
            elif self.current_token_type == TokenType.KEY_LIST_TOKEN:
                if char == ']' and self.any_opened():
                    self.finish_token()
            elif self.current_token_type in (TokenType.KEYBIND_TOKEN, TokenType.TOGGLE_KEYBIND_TOKEN):
                if char == '}' and self.any_opened():
                    self.finish_token()

        if self.current_token_type != TokenType.NO_TOKEN:
            self.finish_token()

    def combine_keys(self):
        new_tokens = []
        last_token = None
        for token in self.tokens:
            if last_token is None:
                last_token = token
                continue
            if token[0] in (TokenType.KEY_LIST_TOKEN, TokenType.KEYBIND_TOKEN, TokenType.TOGGLE_KEYBIND_TOKEN):
                last_token = (
                    token[0],
                    last_token,
                    token[1]
                )
            else:
                new_tokens.append(last_token)
                last_token = token
        if last_token is not None:
            new_tokens.append(last_token)
        self.tokens = new_tokens

    def transform_token_to_instruction(self, token):
        if not isinstance(token, tuple):
            return token
        elif token[0] == TokenType.SINGLE_CHAR_KEY_TOKEN:
            return KeyTap(token[1])
        elif token[0] == TokenType.MULTIPLE_CHAR_KEY_TOKEN:
            return KeyTap(Key[token[1]])
        elif token[0] == TokenType.KEY_LIST_TOKEN:
            hold_key = self.transform_token_to_instruction(token[1])
            return KeyHold(hold_key.key, token[2])
        elif token[0] == TokenType.KEYBIND_TOKEN:
            activate_key = self.transform_token_to_instruction(token[1])
            return KeybindTap(activate_key, token[2])
        elif token[0] == TokenType.TOGGLE_KEYBIND_TOKEN:
            toggle_key = self.transform_token_to_instruction(token[1])
            return KeybindToggle(toggle_key, token[2])
        elif token[0] == TokenType.MOUSE_INSTRUCTION_TOKEN:
            if re.match(r'\D+', token[1]):
                return MouseClick(Button[token[1]])
            elif result := re.match(r'(\d+)\s*,\s*(\d+)', token[1]):
                position = result.groups()
                return MouseMove(position)
        elif token[0] == TokenType.TIME_WAIT_TOKEN:
            return WaitInstruction(int(token[1]))
        else:
            return token

    def transform_tokens_to_instructions(self):
        instructions = []
        for token in self.tokens:
            instructions.append(self.transform_token_to_instruction(token))
        self.tokens = instructions

    def get_return(self) -> list[Instruction]:
        return self.tokens