from .parser import ExpressionParser
from .expressions import Operator, Precedence, Grouping
from .defaults import load_defaults
from .commands import ls, details
import importlib.util
import os
import sys

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
        COMMANDS[cmd][0](parser, args)
        return

    parser.reset(line)
    try:
        ans = parser.parse().evaluate()
        parser.set_var('ans', ans)
        print(ans)
    except Exception as e:
        print(f'Error' + (f': {e}' if str(e) != '' else ''))

def main():
    ans = 0
    parser = ExpressionParser(None)
    parser.load_defaults()

    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'import_from'), 'r+') as f:
            spec = importlib.util.spec_from_file_location('imported', f.read())
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
    except:
        pass

    if len(sys.argv) > 1:
        handle_input(''.join(sys.argv[1:]), parser)
        return
    while True:
        handle_input(input('> '), parser)
