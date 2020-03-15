from typing import Callable
from .expressions import Precedence, Operator, Expression, Grouping
from .defaults import load_defaults

class ExpressionParser:
    def __init__(self, expression_str):
        self.expression = expression_str
        self.pos = 0
        self.operators = [[] for _ in range(len(Precedence))]
        self.vars = {}
        self.funcs = {}

    def load_defaults(self):
        load_defaults(self)

    def add_operator(self, operator):
        if operator.precedence == Precedence.Grouping and type(operator) != Grouping:
            raise Exception('Must provide a grouping class to use a precedence level of grouping')
        self.operators[operator.precedence].append(operator)
        return self

    def set_func(self, name: str, func: Callable):
        assert callable(func)
        self.funcs[name] = func

    def set_var(self, name: str, value: float):
        self.vars[name] = value

    def parse(self):
        return self.expr()

    def reset(self, new: str):
        self.expression = new
        self.pos = 0

    def match_precedence(self, precedence: Precedence):
        for operator in self.operators[precedence]:
            if self.match(operator.char):
                self.pos += 1
                return operator
        return None

    def next_precedence(self, current: Precedence, next_func: Callable):
        expr = next_func()
        operator = self.match_precedence(current)
        while operator != None:
            expr = Expression([expr, next_func()], operator.solver)
            operator = self.match_precedence(current)
        return expr

    def expr(self):
        return self.next_precedence(Precedence.Addition, self.term)

    def term(self):
        return self.next_precedence(Precedence.Multiplication, self.exponent)

    def exponent(self):
        return self.next_precedence(Precedence.Exponentiation, self.factor)

    def factor(self):
        unary_operator = self.match_precedence(Precedence.Unary)
        expr = None

        if self.current().isdigit() or self.current() == '.':
            expr = self.number()
        elif self.current().isalpha():
            identifier = self.current()
            self.pos += 1
            while self.can_continue() and self.current().isalpha():
                identifier += self.current()
                self.pos += 1
            if self.consume('('):
                args = [self.expr()]
                while self.consume(','):
                    args.append(self.expr())
                expr = Expression.from_number(self.funcs[identifier](*args))
                assert self.consume(')')
            else:
                expr = Expression.from_number(self.vars[identifier])
        else:
            for grouping in self.operators[Precedence.Grouping]:
                if self.consume(grouping.char):
                    expr = Expression([self.expr()], grouping.solver)
                    assert self.consume(grouping.end_char)
                    break

        assert expr != None
        unary_postfix_operator = self.match_precedence(Precedence.UnaryPostfix)
        if unary_postfix_operator != None:
            expr = Expression([expr], unary_postfix_operator.solver)
        if unary_operator != None:
            expr = Expression([expr], unary_operator.solver)
        return expr

    def number(self):
        start = self.pos
        hit_decimal = False
        while self.can_continue() and (self.expression[self.pos].isdigit() or (self.expression[self.pos] == '.' and not hit_decimal)):
            if (self.expression[self.pos] == '.'):
                hit_decimal = True
            self.pos += 1
        return Expression.from_number(float(self.expression[start:self.pos]))
    
    def can_continue(self) -> bool:
        return self.pos < len(self.expression)

    def consume(self, char: str) -> bool:
        if self.match(char):
            self.pos += 1
            return True
        return False

    def current(self) -> str:
        while self.can_continue() and self.expression[self.pos] in [' ', '\t']:
            self.pos += 1
        return self.expression[self.pos]

    def match(self, match: str) -> bool:
        return self.can_continue() and match == self.current()