import math


class Vector3:
    def __init__(self, x , y , z):
        if type(x) != float and type(x) != int: raise ValueError('x can only be float or int')
        if type(y) != float and type(y) != int: raise ValueError('y can only be float or int')
        if type(z) != float and type(z) != int: raise ValueError('z can only be float or int')

        self.x , self.y , self.z = x ,y ,z


    def __str__(self) -> str:
        return f'Vector3({self.x}, {self.y}, {self.z})'

    def __eq__(self, other): return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __add__(self, other):
        if type(other) == Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def multiply_by_number(self, n):
        if type(n) != int and type(n) != float: raise ValueError
        x, y, z= self.x * n, self.y * n, self.z * n
        return Vector3(x ,y ,z)

    def multiply(self, other):
        if type(other) == int:return self.multiply_by_number(other)
        if type(other) == float:return self.multiply_by_number(other)
    __mul__ = multiply

    def divide_by_number(self, n):
        if type(n) != int and type(n) != float: raise ValueError
        x, y, z = self.x * n, self.y * n, self.z * n
        return Vector3(x, y, z)
    __truediv__ = divide_by_number

    def __neg__(self): return  self.multiply_by_number(-1)

    def size(self): return math.sqrt(self.x **2 +self.y **2 + self.z **2)
    __abs__ = size



    def normalize(self): return self.divide_by_number(self.size)