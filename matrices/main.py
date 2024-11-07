from matrix import Matrix


a = Matrix(
    [1, 2, 3],
          [5, 4, 0],
          [1, 0, 6]
)

print(a.adjugate())
print( a.inverse())

print(a * a.inverse())