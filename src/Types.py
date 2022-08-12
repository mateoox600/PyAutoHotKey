from typing import TypeAlias
from instructions.KeyboardManager import KeyPress
from instructions.MouseManager import MouseInstruction
from instructions.GeneralInstruction import GeneralInstruction

Instruction: TypeAlias = KeyPress | MouseInstruction | GeneralInstruction