from matrix import Matrix , solve_gaussian_linear_system


m = Matrix(
    [4, 0],
          [0, 8],
          [9, 5],
           )
a = Matrix(
    [4, 4, 5],
          [7, 4, 5],
          [3, 8, 1])



print(solve_gaussian_linear_system(a, ['x', 'y', 'z'], [2, 4, 7]))