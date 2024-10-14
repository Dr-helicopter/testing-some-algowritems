from matrix import Matrix , solve_cramer_linear_system, solve_gaussian_linear_system


m = Matrix(
    [4, 0],
          [0, 8],
          [9, 5],
           )
a = Matrix(
    [3, 5, 7],
          [1, 2, 3],
          [-1, 3, 5])

print(a.rank())