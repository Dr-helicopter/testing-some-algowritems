from matrix import Matrix


m = Matrix(
    [4, 0],
          [0, 8],
          [9, 5],
           )
a = Matrix(
    [3, 4, 5],
          [2, 4, 5])

print(a * m)

print(m * a)
