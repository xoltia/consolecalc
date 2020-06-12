from .parser import ExpressionParser
from typing import List
from sys import exit

def close(*_):
    exit(0)

def ls(parser: ExpressionParser, args: List[str]):
    # TODO: OPERATORS
    if len(args) < 1:
        print('VARS:')
        for k, v in parser.vars.items():
            print(f'{k}: {v}')
        print('\nFUNCS:')
        for k, v in parser.funcs.items():
            print(f'{k}')
    elif args[0] == 'vars':
        for k, v in parser.vars.items():
            print(f'{k}: {v}')
    elif args[0] == 'funcs':
        for k, v in parser.funcs.items():
            print(f'{k}')
    else:
        print('Invalid usage')

def details(parser: ExpressionParser, args: List[str]):
    if len(args) < 1:
        return print('Invalid usage')
    all_items = {**parser.funcs, **parser.vars}
    print(all_items[args[0]].__doc__)