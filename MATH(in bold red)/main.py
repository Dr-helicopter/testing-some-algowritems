from matrices.Vectors import Vector3
from matrix import Matrix , multi_is_linear_dependent
from R3 import Line


a = Line(Vector3(1 ,-2 ,1), Vector3(1 ,2 ,3))
b = Line(Vector3(2 ,-4 ,2 ),Vector3(4 , 5, 6))

print(a.is_coplanar_with_line(b))