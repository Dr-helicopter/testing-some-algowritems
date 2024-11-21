from abc import ABC, abstractmethod
from copy import deepcopy
from math import e



class expression(ABC):
    @abstractmethod
    def eq(self, other) -> bool: pass
    def __eq__(self, other) -> bool: return self.eq(other)

    @abstractmethod
    def represent(self) -> str: pass

    @abstractmethod
    def simplify(self):pass

    @abstractmethod
    def copy(self): pass

    def __str__(self): return self.represent()

    def add(self, other):
        if isinstance(other, const): return other.add(self)
        return addition(self, other)

    def mul(self, other):
        if isinstance(other, const): return other.add(self)
        return multiplication(self, other)

    def pow(self, other):
        return power(self, other)

    __add__ = add
    __radd__ = add
    __mul__ = mul
    __rmul__ = mul

    def mutate(self, other):
        if not isinstance(other, expression): other = turn_to_expression(other)
        self.__class__ = other.__class__
        self.__dict__ = deepcopy(other.__dict__)

class const(expression):
    def __init__(self, value):
        assert type(value) == int or type(value) == float
        self.value = value

    # boolean ops -----start-----
    def eq(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if not isinstance(other, const): return False
        return self.value == other.value
    def lt(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if not isinstance(other, const): raise ValueError("Only constants.")
        return self.value < other.value
    def gt(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if not isinstance(other, const): raise ValueError("Only constants.")
        return self.value > other.value
    def le(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if not isinstance(other, const): raise ValueError("Only constants.")
        return self.value <= other.value
    def ge(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if not isinstance(other, const): raise ValueError("Only constants.")
        return self.value >= other.value

    __lt__ = lt
    __gt__ = gt
    __le__ = le
    # boolean ops -----end-----

    #  casting ---start---
    def bool(self) -> bool: return bool(self.value)
    def int(self) -> int: return int(self.value)
    def float(self) -> float: return float(self.value)
    __bool__ = bool
    __int__ = int
    __float__ = float
    #  casting ---end ---



    # operations --- start ----
    def add(self, other) -> expression:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if isinstance(other, const): return const(other.value + self.value)
        return addition(other, self)

    def mul(self, other) -> expression:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if isinstance(other, const): return const(self.value * other.value)
        return multiplication(self, other)

    def neg(self): return const(-self.value)

    def pow(self, other) -> expression:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if isinstance(other, const): return const(self.value ** other.value)
        return power(self, other)


    __add__ = add
    __radd__ = add
    __mul__ = mul
    __rmul__ = mul
    __neg__ = neg
    __pow__ = pow
    # operations ----end -----


    def is_negative(self): return self.value < 0
    def represent(self) -> str: return str(self.value)
    def copy(self): return self
    def simplify(self) -> None: pass
c0 = const(0)


class variable(expression):
    def __init__(self, name: str):
        self.name: str = name

    def eq(self, other) -> bool:
        if type(other) == str: return self.name == other
        if type(other) == variable: return self.name == other.name
        return False

    def copy(self): return self
    def represent(self) -> str: return self.name
    def simplify(self) -> None: pass


def turn_to_expression(a) -> expression:
    if type(a) == int: return const(a)
    if type(a) == float: return const(a)
    if type(a) == str: return variable(a)


class addition(expression):
    def __init__(self, a, b, *args, restructure=True):
        if len(args):
            args += (a, b,)
            c, e = [], []
            for i in args:
                if not isinstance(i, expression): i = turn_to_expression(i)
                (c if type(i) == const else e).append(i)
            c = sum(c)
            r = c
            for i in e: r = addition(i, r, restructure=False)
            self.a, self.b = 0, r
            self.simplify()
            return

        self.a: expression = a if isinstance(a, expression) else turn_to_expression(a)
        self.b: expression = b if isinstance(b, expression) else turn_to_expression(b)
        self.simplify()

    def eq(self, other) -> bool:
        if not isinstance(other, addition): return False
        s = self._flatten()
        o = other._flatten()
        if len(o) != len(s): return False
        for i in s:
            if not all(j != i for j in o): continue
            return False
        return True

    def _flatten(self):
        res = []
        if isinstance(self.a, addition):
            res += self.a._flatten()
        else:
            res.append(self.a)
        if isinstance(self.b, addition):
            res += self.b._flatten()
        else:
            res.append(self.b)
        return res

    def simplify(self): # !! danger zone !! careful with recursion here
        if self.a == c0:
            self.mutate(self.b)
        elif self.b == c0:
            self.mutate(self.a)
        elif isinstance(self.a, const) and isinstance(self.b, const):
            self.mutate(const(self.a.value + self.b.value))




    def represent(self) -> str:
        a = self.a.represent() if type(self.a) == addition else f'({self.a.represent()})'
        b = self.b.represent() if type(self.b) == addition else f'({self.b.represent()})'
        return f'{a} +{b}'

    def copy(self): return addition(self.a, self.b, restructure=False)


class multiplication(expression):
    def __init__(self, a, b, restructure=True):
        self.a: expression = a if isinstance(a, expression) else turn_to_expression(a)
        self.b: expression = b if isinstance(b, expression) else turn_to_expression(b)
        self.simplify()

    def eq(self, other) -> bool:
        if not isinstance(other, multiplication): return False
        s = self._flatten()
        if len(s) != 2: #we got multiple
            o = other._flatten()
            if len(o) != len(s): return False
            for i in s:
                if not all(j != i for j in o):continue
                return False
            return True



    def _flatten(self):
        res = []
        if isinstance(self.a, multiplication):
            res += self.a._flatten()
        else:
            res.append(self.a)
        if isinstance(self.b, multiplication):
            res += self.b._flatten()
        else:
            res.append(self.b)
        return res

    def get_const(self) -> const:
        f, c = self._flatten(), const(1)
        for i in f:
            if isinstance(i , const):
                print(c, i)
                c *= i if isinstance(i, const) else 1
                print(c, i)
        return c

    def simplify(self):
        if self.a == c0 or self.b == c0:
            self.mutate(c0)
        elif isinstance(self.a, const) and isinstance(self.a, const):
            self.mutate(const(self.a.value * self.a.value))
        else:
            f = self._flatten()
    def represent(self) -> str:
        return f'({self.a})({self.b})'

    def copy(self): return multiplication(self.a, self.b, restructure=False)

class division(multiplication):
    pass


class power(expression):
    def get_component(self) -> expression: return self.b
    def get_exponent(self) -> expression: return self.a
    

    def __init__(self, a, b):
        self.a: expression = a if isinstance(a, expression) else turn_to_expression(a)
        self.b: expression = b if isinstance(b, expression) else turn_to_expression(b)
        self.simplify()

    def eq(self, other) -> bool:
        if not isinstance(other, power): return False
        if self.get_component() != other.get_component(): return False
        if self.get_exponent() != other.get_exponent(): return False
        return True

    def simplify(self):
        if self.a == c0:
            if self.b == c0: raise ValueError("0^0 is undefined.")
            return self.mutate(c0)

        if isinstance(self.a, power):
            self.mutate(power(self.a.a, self.a.b * self.b))


        if isinstance(self.b, const):
            if self.b == c0: self.mutate(const(1))
            elif self.b == 1: self.mutate(self.a)
            elif isinstance(self.a, const): self.mutate(const(self.a.value ** self.b.value))
            elif self.b.is_negative(): self.mutate(power(division(1, self.a), -self.b))
            return


        if isinstance(self.b, multiplication):
            if isinstance(self.a, const):
                self.a = const(self.a.value ** self.b.get_const().value)
                self.b = division(self.b, self.b.get_const())


    def represent(self) -> str:
        return f'({self.a})^({self.b})'

    def copy(self): return power(self.a, self.b)