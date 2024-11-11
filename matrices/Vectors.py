import math
from matrices.matrix import is_linear_dependent, Matrix


class Vector3:
    def __init__(self, x , y , z):
        if type(x) != float and type(x) != int: raise ValueError('x can only be float or int')
        if type(y) != float and type(y) != int: raise ValueError('y can only be float or int')
        if type(z) != float and type(z) != int: raise ValueError('z can only be float or int')

        self.x , self.y , self.z = x ,y ,z


    def __str__(self) -> str: return f'Vector3({self.x}, {self.y}, {self.z})'


    # -----operators start-----
    def is_equal_to_vector(self, other) -> bool:
        if type(other) != Vector3: raise ValueError
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def is_equal_to_list(self, other : list) -> bool:
        if len(other) != 3: raise ValueError
        return (self.x == other[0]) and (self.y == other[1]) and (self.z == other[2])

    def is_equal_to_tuple(self, other : tuple) -> bool:
        if len(other) != 3: raise ValueError
        return (self.x == other[0]) and (self.y == other[1]) and (self.z == other[2])

    def eq(self, other) -> bool:
        if type(other) == Vector3: return self.is_equal_to_vector(other)
        if type(other) == list: return self.is_equal_to_list(other)
        if type(other) == tuple: return self.is_equal_to_tuple(other)


    def multiply_by_number(self, n):
        if type(n) != int and type(n) != float: raise ValueError
        x, y, z= self.x * n, self.y * n, self.z * n
        return Vector3(x ,y ,z)

    def mul(self, other):
        if type(other) == int: return self.multiply_by_number(other)
        if type(other) == float: return self.multiply_by_number(other)

    def neg(self):
        return self.multiply_by_number(-1)

    def divide_by_number(self, n):
        if type(n) != int and type(n) != float: raise ValueError
        x, y, z = self.x * n, self.y * n, self.z * n
        return Vector3(x, y, z)

    def div(self, other):
        if type(other) == int: return self.divide_by_number(other)
        if type(other) == float: return self.divide_by_number(other)


    def add_to_vector(self, other):
        if type(other) != Vector3: raise ValueError
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def add_to_list(self, other : list):
        if len(other) != 3: raise ValueError
        return Vector3(self.x + other[0], self.y + other[1], self.z + other[2])

    def add_to_tuple(self, other : tuple):
        if len(other) != 3: raise ValueError
        return Vector3(self.x + other[0], self.y + other[1], self.z + other[2])

    def add(self, other):
        if type(other) == Vector3: return self.add_to_vector(other)
        if type(other) == list: return self.add_to_list(other)
        if type(other) == tuple: return self.add_to_tuple(other)

    def sub(self, other):
        return -(-self).add(other)


    def size(self): return math.sqrt(self.x **2 +self.y **2 + self.z **2)

    __eq__ = eq
    __mul__ = mul
    __neg__ = neg
    __add__ = add
    __sub__ = sub
    __truediv__ = div
    __abs__ = size
    # -----operators end-----


    # -----casting start-----
    def to_list(self) -> list: return [self.x, self.y, self.z]
    def to_tuple(self) -> tuple: return self.x, self.y, self.z
    # -----casting end -----



    def normalize(self): return self.divide_by_number(self.size())


    def is_linear_dependent_to(self, other) -> bool:
        if type(other) != Vector3: raise ValueError
        return is_linear_dependent(self.to_list() , other.to_list())

    def x_product(self, other):
        if type(other) != Vector3: raise ValueError
        x = Matrix([self.y, self.z],[other.y, other.z])
        y = -Matrix([self.x, self.z],[other.x, other.z])
        z = Matrix([self.x, self.y],[other.x, other.y])

        return Vector3(x.determinant(), y.determinant(), z.determinant())

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z