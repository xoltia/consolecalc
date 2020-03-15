from typing import Callable
from enum import IntEnum

class Precedence(IntEnum):
    Addition = 0
    Multiplication = 1
    Exponentiation = 2
    Grouping = 3
    Unary = 4,
    UnaryPostfix = 5

class Expression:
    def __init__(self, operands: list, solver: Callable):
        self.operands = operands
        self.solver = solver

    @classmethod
    def from_number(cls, num):
        return cls([num], lambda x: x)

    def evaluate(self):
        return self.solver(*self.operands)

class Operator:
    def __init__(self, char: str, precedence: Precedence, solver: Callable):
        self.char = char
        self.solver = solver
        self.precedence = precedence

    @classmethod
    def new(cls, char: str, precedence: Precedence):
        def create_new(solver):
            return cls(char, precedence, solver)
        return create_new

class Grouping():
    def __init__(self, char: str, end_char: str, solver: Callable):
        self.char = char
        self.end_char = end_char
        self.solver = solver
        self.precedence = Precedence.Grouping

    @classmethod
    def new(cls, char, end_char=None):
        def create_new(solver):
            return cls(char, end_char if end_char != None else char, solver)
        return create_new

