import re
from enum import Enum
from pynput.keyboard import Key
from KeyboardManager import KeyTap, KeyHold

class TokenType(Enum):
    NO_TOKEN = 0
    SINGLE_CHAR_KEY_TOKEN = 1
    MULTIPLE_CHAR_KEY_TOKEN = 2
    KEY_LIST_TOKEN = 3

class Parser:

    def __init__(self, string: str):
        self.string = string

        self.tokens = []
        self.current_token = ''
        self.current_token_type = TokenType.NO_TOKEN

        self.parse_string()
        self.combine_hold_key()
        self.transform_tokens_to_key_press()

    def finish_token(self):
        if self.current_token_type == TokenType.KEY_LIST_TOKEN:
            self.parse_key_list_from_current()
        elif self.current_token_type == TokenType.MULTIPLE_CHAR_KEY_TOKEN:
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
                else:
                    self.finish_token()
            if self.current_token_type == TokenType.NO_TOKEN:
                self.current_token += char
                if char == '[':
                    self.current_token_type = TokenType.KEY_LIST_TOKEN
                else:
                    self.current_token_type = TokenType.SINGLE_CHAR_KEY_TOKEN
            elif self.current_token_type == TokenType.MULTIPLE_CHAR_KEY_TOKEN:
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

    def transform_to_key_press(self, token):
        if token[0] == TokenType.SINGLE_CHAR_KEY_TOKEN:
            return KeyTap(token[1])
        elif token[0] == TokenType.MULTIPLE_CHAR_KEY_TOKEN:
            return KeyTap(Key[token[1]])
        elif token[0] == TokenType.KEY_LIST_TOKEN:
            hold_key = self.transform_to_key_press(token[1])
            return KeyHold(hold_key.key, token[2])

    def transform_tokens_to_key_press(self):
        key_presses = []
        for token in self.tokens:
            key_presses.append(self.transform_to_key_press(token))
        self.tokens = key_presses

    def get_return(self):
        return self.tokens