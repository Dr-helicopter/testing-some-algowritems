from matrix import Matrix


a = Matrix(
    [1, 2, 3 , 4],
        [0, 4, 0, 5],
        [0, 0, 6, 6],
        [0 ,0 ,0 ,7]
)

print(a.is_upper_triangular())
