from matrix import Matrix , solve_cramer_linear_system


m = Matrix(
    [4, 0],
          [0, 8],
          [9, 5],
           )
a = Matrix(
    [4, 4, 5],
          [7, 4, 5],
          [3, 8, 1])

print(a)

print(solve_cramer_linear_system(a,['x','y','z'],[3, 5 ,6]))