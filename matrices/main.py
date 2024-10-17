from matrix import Matrix , solve_cramer_linear_system, solve_gaussian_linear_system, row_esioln, eigen_v

a = Matrix(
    [3, 1],
          [0, 2]
)


print(eigen_v(a))

print(a * [-1, 1])