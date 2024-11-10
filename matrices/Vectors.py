import math

from typing_extensions import Tuple

from matrices.matrix import is_linear_dependent, Matrix


class Vector3:
    def __init__(self, x , y , z):
        if type(x) != float and type(x) != int: raise ValueError('x can only be float or int')
        if type(y) != float and type(y) != int: raise ValueError('y can only be float or int')
        if type(z) != float and type(z) != int: raise ValueError('z can only be float or int')

        self.x , self.y , self.z = x ,y ,z


    def __str__(self) -> str: return f'Vector3({self.x}, {self.y}, {self.z})'

    def __eq__(self, other): return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __add__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self + (-other)

    def multiply_by_number(self, n):
        if type(n) != int and type(n) != float: raise ValueError
        x, y, z= self.x * n, self.y * n, self.z * n
        return Vector3(x ,y ,z)

    def __mul__(self, other):
        if type(other) == int:return self.multiply_by_number(other)
        if type(other) == float:return self.multiply_by_number(other)

    def __neg__(self): return self.multiply_by_number(-1)

    def divide_by_number(self, n):
        if type(n) != int and type(n) != float: raise ValueError
        x, y, z = self.x * n, self.y * n, self.z * n
        return Vector3(x, y, z)


    def size(self): return math.sqrt(self.x **2 +self.y **2 + self.z **2)

    def to_list(self) -> list: return [self.x, self.y, self.z]
    def to_tuple(self) -> Tuple: return self.x, self.y, self.z



    __truediv__ = divide_by_number
    __abs__ = size



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