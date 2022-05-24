
from abc import ABC, abstractmethod
import re

class Expression(ABC):
    
    @abstractmethod
    def __init__(self, *args) -> None:
        pass

    @abstractmethod
    def eval(self, *args) -> bool:
        pass


class NotExpr(Expression):
    def __init__(self, expr) -> None:
        self.expr = expr

    def eval(self, x):
        return not self.expr.eval(x)


class AndExpr(Expression):
    
    def __init__(self, expr1, expr2) -> None:
        self.expr1 = expr1
        self.expr2 = expr2

    def eval(self, x):
        return self.expr1.eval(x) and self.expr2.eval(x)


class OrExpr(Expression):
    def __init__(self, expr1, expr2) -> None:
        self.expr1 = expr1
        self.expr2 = expr2

    def eval(self, x):
        return self.expr1.eval(x) or self.expr2.eval(x)


class IntExpr(Expression):
    
    def __init__(self, min: int =None, max: int =None) -> None:
        if min is None and max is None:
            raise Exception("'min' and 'max' cannot both be None at the same time")
        self.min = min
        self.max = max
    
    def eval(self, x: int) -> bool:
        if self.min is None:
            return x <= self.max
        if self.max is None:
            return x >= self.min

        return self.min <= x <= self.max


class StrExpr(Expression):
    
    def __init__(self, p: str, method: str ='') -> None:
        self.p = p
        self.method = method

    def eval(self, s: str) -> bool:
        if self.method:
            #return self.func_dict.get(self.func)(self.s, x)
            return StrMagic.call(self.method, s, self.p)
        else:
            return s == self.p


class StrMagic:
    '''
    Class to define checks on strings.
    Example:
        @staticmethod
        def foo(s, p):
            return # Some boolean expression

    To use the method, do:
        StrMagic.call(name_of_method, s, p)
    '''
    @staticmethod
    def contains(s, p):
        return p in s
    
    @staticmethod
    def search(s, p):
        return bool(re.search(p, s))

    @staticmethod
    def fullmatch(s, p):
        return bool(re.fullmatch(p, s))

    @classmethod
    def call(cls, name, s, p):
        if name.startwith('__'):
            raise Exception
        return getattr(cls, name)(s, p) 

