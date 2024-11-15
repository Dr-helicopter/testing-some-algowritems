from abc import ABC, abstractmethod


class expression(ABC):
    @abstractmethod
    def represent(self) -> str: pass

    @abstractmethod
    def simplify(self) -> None: pass

    def __str__(self):return self.represent()



class const(expression):
    def __init__(self,value):
        assert type(value) == int or type(value) == float
        self.value = value



    # boolean ops -----start-----
    def eq(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if type(other) != const: return False
        return self.value == other.value
    def lt(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if type(other) != const: raise ValueError("Only constants.")
        return self.value < other.value
    def gt(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if type(other) != const: raise ValueError("Only constants.")
        return self.value > other.value
    def le(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if type(other) != const: raise ValueError("Only constants.")
        return self.value <= other.value
    def ge(self, other) -> bool:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if type(other) != const: raise ValueError("Only constants.")
        return self.value >= other.value
    __eq__ = eq
    __lt__ = lt
    __gt__ = gt
    __le__ = le
    # boolean ops -----end-----


    def add(self, other) -> expression:
        if not isinstance(other, expression): other = turn_to_expression(other)
        if type(other) == const: return const(other.value + self.value)
        return addition(other, self)

    __add__ = add
    __radd__ = add

    def represent(self) -> str:
        return  str(self.value)

    def simplify(self) -> None: pass


class variable(expression):
    def __init__(self, name : str):
        self.name : str = name

    def represent(self) -> str:
        return self.name

    def simplify(self) -> None: pass


def turn_to_expression(a) -> expression:
    if type(a) == int: return const(a)
    if type(a) == float: return const(a)
    if type(a) == str: return variable(a)



class addition(expression):
    def __init__(self, a, b, *args):
        if len(args):
            args += (a, b,)
            c = []
            e = []
            for i in args: pass

        print(args)
        self.a : expression = a if isinstance(a, expression) else turn_to_expression(a)
        self.b : expression = b if isinstance(b ,expression) else turn_to_expression(b)
        self.simplify()

    def _flatten(self):
        res = []
        if type(self.a) == addition: res += self.a._flatten()
        else: res.append(self.a)
        if type(self.b) == addition: res += self.b._flatten()
        else: res.append(self.b)
        return res

    def simplify(self):  # !! danger zone !! careful with recursion here
        # Recursively simplify nested expressions
        if isinstance(self.a, addition):
            self.a.simplify()
        if isinstance(self.b, addition):
            self.b.simplify()

        # Check if both parts are constants after simplification
        if isinstance(self.a, const) and isinstance(self.b, const):
            # Perform the simplification by changing `self` into a `const`
            a = self.a.value
            b = self.b.value
            self.__class__ = const
            const.__init__(self, a + b)
            return

        # Flatten out terms like 7 + (x + 8) into (7 + 8) + x if possible
        if isinstance(self.a, const) and isinstance(self.b, addition) and isinstance(self.b.a, const):
            # Combine self.a and self.b.a into one const
            new_value = self.a.value + self.b.a.value
            self.a = const(new_value)
            self.b = self.b.b  # Simplify to the remaining part
            self.simplify()  # Re-run to simplify further if needed

        elif isinstance(self.b, const) and isinstance(self.a, addition) and isinstance(self.a.a, const):
            # Combine self.b and self.a.a into one const (symmetric case)
            new_value = self.b.value + self.a.a.value
            self.b = const(new_value)
            self.a = self.a.b  # Simplify to the remaining part
            self.simplify()  # Re-run to simplify further if needed


    def represent(self) -> str:
        print(type(self.a))
        a = self.a.represent() if type(self.a) == addition else f'({self.a.represent()})'
        b = self.b.represent() if type(self.b) == addition else f'({self.b.represent()})'
        return f'{a} +{b}'



a = const(4)
b = const(4.0)
c = const(6.0)
x = variable('x')
print( a == 4)
print( 4 == a)
print( a != 4)
print( a != 4)
print( a == b)
print( b == a)
print( a != b)
print( a != b)