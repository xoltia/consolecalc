from .expressions import Grouping, Operator, Precedence
from importlib import import_module

@Operator.new('+', Precedence.Addition)
def add(x, y):
    return x.evaluate() + y.evaluate()

@Operator.new('-', Precedence.Addition)
def sub(x, y):
    return x.evaluate() - y.evaluate()

@Operator.new('*', Precedence.Multiplication)
def mul(x, y):
    return x.evaluate() * y.evaluate()

@Operator.new('/', Precedence.Multiplication)
def div(x, y):
    return x.evaluate() / y.evaluate()

@Operator.new('%', Precedence.Multiplication)
def mod(x, y):
    return x.evaluate() % y.evaluate()

@Operator.new('^', Precedence.Exponentiation)
def exp(x, y):
    return x.evaluate() ** y.evaluate()

@Operator.new('-', Precedence.Unary)
def negate(x):
    return -x.evaluate()

@Operator.new('!', Precedence.UnaryPostfix)
def factorial(x):
    n = x.evaluate()
    assert n.is_integer() and n >= 0, "factorial only supports positive integral values"
    if n == 0:
        return 1
    for i in range(1, int(n) + 1):
        n *= i
    return n

@Grouping.new('(', ')')
def group(x):
    return x.evaluate()

@Grouping.new('|')
def absolute(x):
    return abs(x.evaluate())

def number_func_to_expression_func(num_func):
    '''
    Wraps functions that take numeric values as arguments to accept instances of the Expression class
    by evaluating all expressions before passing them as arguments
    '''
    def expression_func(*args):
        return num_func(*map(lambda x: x.evaluate(), args))
    setattr(expression_func, '__doc__', getattr(num_func, '__doc__'))
    return expression_func

def load_defaults(parser):
    parser.add_operator(add)
    parser.add_operator(sub)
    parser.add_operator(mul)
    parser.add_operator(div)
    parser.add_operator(mod)
    parser.add_operator(exp)
    parser.add_operator(group)
    parser.add_operator(absolute)
    parser.add_operator(negate)
    parser.add_operator(factorial)
    
    math = import_module("math")
    for k in dir(math):
        if k.startswith('__'):
            continue
        attr = getattr(math, k)
        if callable(attr):
            parser.set_func(k, number_func_to_expression_func(attr))
        elif type(attr) in [float, int]:
            parser.set_var(k, attr)