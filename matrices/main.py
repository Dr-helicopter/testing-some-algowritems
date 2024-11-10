from matrix import Matrix , multi_is_linear_dependent


a = Matrix(
    [1, 2, 3 , 4],
        [0, 4, 0, 5],
        [0, 0, 6, 6],
        [0 ,0 ,0 ,7]
)
a = [1,1,1]
b = [1,1,-1]
c = [2,2,2]



multi_is_linear_dependent(a,b,c)