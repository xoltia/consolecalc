from .parser import ExpressionParser
from .expressions import Operator, Precedence, Grouping
from .defaults import load_defaults
from .commands import ls, details
import importlib.util
import os
import sys
import argparse

FUNC_TAG = '_func'
VAR_TAG = '_var'
CMD_PREFIX = '?'

COMMANDS = {
    'ls': [ls, 'List vars and/or funcs'],
    'details': [details, 'Get details about a specific function or variable']
}

def handle_input(line, parser):
    if line.startswith(CMD_PREFIX):
        args = [arg.lower() for arg in line[len(CMD_PREFIX):].split()]
        if len(args) == 0:
            for name, info in COMMANDS.items():
                print(f'{name}: {info[1]}')
            return
        cmd = args.pop(0)
        if not cmd in COMMANDS:
            print(f"Invalid command: '{cmd}'")
            return
        COMMANDS[cmd][0](parser, args)
        return

    parser.reset(line)
    try:
        ans = parser.parse().evaluate()
        parser.set_var('ans', ans)
        print(ans)
    except Exception as e:
        print(f'Error' + (f': {e}' if str(e) != '' else ''))

def load_custom_file(file_path, parser):
    try:
        spec = importlib.util.spec_from_file_location('imported', file_path)
        imported = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported)
        for k in dir(imported):
            attr = getattr(imported, k)
            if type(attr) in [Operator, Grouping]:
                parser.add_operator(attr)
            elif k.endswith(FUNC_TAG) and callable(attr):
                parser.set_func(k[:-len(FUNC_TAG)], attr)
            elif k.endswith(VAR_TAG) and type(attr) in [float, int]:
                parser.set_var(k[:-len(VAR_TAG)], attr)
    except Exception as e:
        print(f'Failed to load {file_path}')
        

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--eval', '-e', nargs='*', help='Evaluate expression (MUST COME LAST)')
    arg_parser.add_argument('--bare', '-b', action='store_true', default=False, help="Don't load default operators, functions, and vars")
    arg_parser.add_argument('--set-custom', '-s', help='Set permanent import file')
    arg_parser.add_argument('--reset-custom', '-r', action='store_true', default=False, help='Reset permanent import file')
    arg_parser.add_argument('--load-custom', '-l', help='Import file for current session')
    arg_parser.add_argument('--terminate', '-t', action='store_true', default=False, help='Terminate after completing argument commands')
    args = arg_parser.parse_args()

    ans = 0
    parser = ExpressionParser(None)

    import_config = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'import_from')

    if not args.bare:
        parser.load_defaults()
    if args.reset_custom:
        os.remove(import_config)
    if args.set_custom:
        with open(import_config, 'w+') as f:
            f.write(args.set_custom)
    if args.load_custom:
        load_custom_file(args.load_custom, parser)

    # TODO: multiple imports
    if os.path.exists(import_config):
        with open(import_config, 'r+') as f:
            load_custom_file(f.read(), parser)

    if args.eval:
        handle_input(''.join(args.eval), parser)
    if args.terminate:
        return
    while True:
        handle_input(input('> '), parser)
