from Vectors import Vector3
from R3 import Line
from plot import Plot3D as plt
from matrix import Matrix , multi_is_linear_dependent, row_echelon

a = Matrix([1,2,4], [3,2,1], [1,-2,-5])
print(row_echelon(a))

multi_is_linear_dependent([0,1,1], [1,0,1], [1,1,2])