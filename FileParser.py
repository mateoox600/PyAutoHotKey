import re
from enum import Enum
from pynput.keyboard import Key
from pynput.mouse import Button
from GeneralInstruction import WaitInstruction
from KeyboardManager import KeyTap, KeyHold
from MouseManager import MouseClick, MouseMove

class TokenType(Enum):
    NO_TOKEN = 0
    SINGLE_CHAR_KEY_TOKEN = 1
    MULTIPLE_CHAR_KEY_TOKEN = 2
    KEY_LIST_TOKEN = 3
    MOUSE_INSTRUCTION_TOKEN = 4
    TIME_WAIT_TOKEN = 5

class Parser:

    def __init__(self, string: str):
        self.string = string

        self.tokens = []
        self.current_token = ''
        self.current_token_type = TokenType.NO_TOKEN

        self.parse_string()
        self.combine_hold_key()
        self.transform_tokens_to_instructions()

    def finish_token(self):
        if self.current_token_type == TokenType.KEY_LIST_TOKEN:
            self.parse_key_list_from_current()
        elif self.current_token_type in (
                TokenType.MULTIPLE_CHAR_KEY_TOKEN,
                TokenType.MOUSE_INSTRUCTION_TOKEN,
                TokenType.TIME_WAIT_TOKEN):
            self.current_token = self.current_token[2:-1]
        self.tokens.append((self.current_token_type, self.current_token))
        self.current_token = ''
        self.current_token_type = TokenType.NO_TOKEN

    def parse_key_list_from_current(self):
        current_token_value = self.current_token \
            .removeprefix('[') \
            .removesuffix(']')
        parser = Parser(current_token_value)
        self.current_token = parser.get_return()

    def parse_string(self):
        for char in [*self.string]:
            if re.match(r'\s', char) and self.current_token_type != TokenType.KEY_LIST_TOKEN:
                continue
            if self.current_token_type == TokenType.SINGLE_CHAR_KEY_TOKEN:
                if char == '(':
                    self.current_token += char
                    if self.current_token.startswith('k'):
                        self.current_token_type = TokenType.MULTIPLE_CHAR_KEY_TOKEN
                        continue
                    elif self.current_token.startswith('m'):
                        self.current_token_type = TokenType.MOUSE_INSTRUCTION_TOKEN
                        continue
                    elif self.current_token.startswith('t'):
                        self.current_token_type = TokenType.TIME_WAIT_TOKEN
                        continue
                else:
                    self.finish_token()
            if self.current_token_type == TokenType.NO_TOKEN:
                self.current_token += char
                if char == '[':
                    self.current_token_type = TokenType.KEY_LIST_TOKEN
                else:
                    self.current_token_type = TokenType.SINGLE_CHAR_KEY_TOKEN
            elif self.current_token_type in (
                    TokenType.MULTIPLE_CHAR_KEY_TOKEN,
                    TokenType.MOUSE_INSTRUCTION_TOKEN,
                    TokenType.TIME_WAIT_TOKEN):
                self.current_token += char
                if char == ')':
                    self.finish_token()
            elif self.current_token_type == TokenType.KEY_LIST_TOKEN:
                self.current_token += char
                if char == ']':
                    self.finish_token()

        if self.current_token_type != TokenType.NO_TOKEN:
            self.finish_token()

    def combine_hold_key(self):
        new_tokens = []
        last_token = None
        for token in self.tokens:
            if last_token is None:
                last_token = token
                continue
            if token[0] == TokenType.KEY_LIST_TOKEN:
                new_tokens.append((
                    token[0],
                    last_token,
                    token[1]
                ))
                last_token = None
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

    def get_return(self):
        return self.tokens