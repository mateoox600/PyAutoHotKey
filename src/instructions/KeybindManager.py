from __future__ import annotations
from functools import partial
from threading import Thread
from abc import ABC, abstractmethod
from pynput import keyboard
from pynput.keyboard import Key
from Types import Instruction
from instructions.KeyboardManager import KeyboardManager, KeyTap, KeyHold

class Keybind(ABC):
    @abstractmethod
    def __init__(self):
        self.keybind = None
        self.keys = None

    @abstractmethod
    def call(self, instance):
        pass

class KeybindTap(Keybind):

    def __init__(self, keybind: Instruction, keys: list[Instruction]):
        self.keybind = keybind
        self.keys = keys

    def call(self, instance):
        print('tap')
        instance.call_tree(self.keys, False)

    def __str__(self):
        return f'KeybindTap[keybind={str(self.keybind)},keys={(str(key) for key in self.keys)}]'

class KeybindToggle(Keybind):

    def __init__(self, keybind: Instruction, keys: list[Instruction]):
        self.instance = None
        self.keybind = keybind
        self.keys = keys
        self.toggled = False

    def call(self, instance):
        self.toggled = not self.toggled
        print(self.toggled)

    def __str__(self):
        return f'KeybindToggle[keybind={str(self.keybind)},keys={(str(key) for key in self.keys)}]'

class KeybindManager:

    hotkeys_keybinds_list: list[tuple[keyboard.HotKey, Keybind]]

    pressed_keys = []
    released_keys = []

    def __init__(self, instance, keyboard_manager: KeyboardManager):
        self.instance = instance
        self.keyboard = keyboard_manager
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.hotkey_thread = Thread(target=self.hotkey_thread_call, args=())
        self.toggle_thread = Thread(target=self.call_toggleable_hotkey, args=())

    def hotkey_thread_call(self):
        while True:
            for hotkey_keybind in self.hotkeys_keybinds_list:
                hotkey = hotkey_keybind[0]
                for key_press in self.pressed_keys:
                    hotkey.press(key_press)
                for key_release in self.released_keys:
                    hotkey.release(key_release)
            self.pressed_keys.clear()
            self.released_keys.clear()
            self.toggle_thread.run()

    def call_toggleable_hotkey(self):
        for hotkey_keybind in self.hotkeys_keybinds_list:
            keybind = hotkey_keybind[1]
            if isinstance(keybind, KeybindToggle) and keybind.toggled:
                self.instance.call_tree(keybind.keys, False)

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

    def on_press(self, key):
        key = self.listener.canonical(key)
        self.pressed_keys.append(key)

    def on_release(self, key):
        key = self.listener.canonical(key)
        self.released_keys.append(key)

    def add_keybinds(self, keybinds: list[Keybind]):
        hotkeys: list[tuple[keyboard.HotKey, Keybind]] = []

        for keybind in keybinds:
            key = self.map_instruction_name(keybind.keybind)
            hotkeys.append((
                keyboard.HotKey(
                    keyboard.HotKey.parse(key),
                    partial(keybind.call, self.instance)
                ),
                keybind
            ))

        self.hotkeys_keybinds_list = hotkeys

        self.toggle_thread.start()
        self.listener.start()
        self.hotkey_thread.start()