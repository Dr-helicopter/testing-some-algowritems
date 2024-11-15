from abc import ABC, abstractmethod


class expression(ABC):
    @abstractmethod
    def represent(self) -> str: pass

    @abstractmethod
    def copy(self): pass

    def __str__(self): return self.represent()

    def add(self, other):
        if isinstance(other, const): return other.add(self)
        return addition(self, other)
    __add__ = add
    __radd__ = add

class const(expression):
    def __init__(self,value):
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
    __eq__ = eq
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


    def add(self, other) -> expression:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if isinstance(other, const): return const(other.value + self.value)
        return addition(other, self)



    def pow(self, other) -> expression:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if isinstance(other, const): return const(self.value ** other.value)
        return power(self, other)

    __add__ = add
    __radd__ = add
    __pow__ = pow



    def represent(self) -> str: return str(self.value)

    def copy(self):return self

    def simplify(self) -> None: pass


class variable(expression):


    def copy(self):return self

    def __init__(self, name : str):
        self.name : str = name

    def eq(self, other) -> bool:
        if type(other) == str: return self.name == other
        if type(other) == variable: return self.name == other.name
        return False
    __eq__ = eq

    def represent(self) -> str:
        return self.name

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
            for i in e: r = addition(i , r, restructure=False)
            self.a, self.b = 0, r
            self.simplify()
            return

        self.a : expression = a if isinstance(a, expression) else turn_to_expression(a)
        self.b : expression = b if isinstance(b ,expression) else turn_to_expression(b)
        self.simplify()

    def _flatten(self):
        res = []
        if isinstance(self.a, addition): res += self.a._flatten()
        else: res.append(self.a)
        if isinstance(self.b, addition): res += self.b._flatten()
        else: res.append(self.b)
        return res

    def simplify(self): # !! danger zone !! careful with recursion here
        if self.a == 0:
            self.__class__ = type(self.b)
            self.__dict__ = self.b.__dict__
            return
        if self.b == 0:
            self.__class__ = type(self.a)
            self.__dict__ = self.a.__dict__
            return


        if isinstance(self.a, const) and isinstance(self.b, const):
            self.__class__ = const
            const.__init__(self, self.a.value + self.b.value)
            return


    def represent(self) -> str:
        a = self.a.represent() if type(self.a) == addition else f'({self.a.represent()})'
        b = self.b.represent() if type(self.b) == addition else f'({self.b.represent()})'
        return f'{a} +{b}'


    def copy(self):return addition(self.a, self.b, restructure=False)


class multiplication(expression):
    def __init__(self):pass

    def represent(self) -> str:
        pass

    def copy(self):pass

class power(expression):
    def __init__(self,a , b):
        self.a : expression = a if isinstance(a, expression) else turn_to_expression(a)
        self.b : expression = b if isinstance(b ,expression) else turn_to_expression(b)
        self.simplify()


    def simplify(self):
        if isinstance(self.b, const):
            if self.b == 0:
                t = const(1)
                self.__class__ = const
                self.__dict__ = t.__dict__
                return
            if self.b == 1:
                self.__class__ = type(self.a)
                self.__dict__ = self.a.__dict__
                return
            if isinstance(self.a, const):
                self.__class__ = const
                const.__init__(self, self.a.value ** self.b.value)
    def represent(self) -> str:
        return f'({self.a})^({self.b})'

    def copy(self): return power(self.a, self.b)