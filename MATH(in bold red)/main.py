from Vectors import Vector3
from R3 import Line
from plot import Plot3D as plt

a = Line(Vector3(1 ,-2 ,1), Vector3(1 ,2 ,3))
b = Line(Vector3(2 ,-4 ,2 ),Vector3(4 , 5, 6))
c = Vector3(3, 2, 1)

plt.plot_point(c)


print(a.is_coplanar_with_line(b))