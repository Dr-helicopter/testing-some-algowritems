from argparse import ArgumentTypeError
from copy import deepcopy
from types import GeneratorType
import chatGPTs_help


class Matrix:
    def __init__(self, *args):
        # for generator
        if isinstance(args[0], GeneratorType): args = list(args[0])

        self.args = []
        self.col = 0
        self.line = len(args)

        # initial checking
        for i in args:
            if not type(i) is list: raise TypeError(f"Matrices only takes lists entered type :" + str(type(i)))
            if len(i) > self.col: self.col = len(i)

        self.args = list(i + [0] * (self.col - len(i)) for i in args)



    # getters
    def get_line(self, i: int) -> list: return deepcopy(self.args[i])

    def get_colum(self, i: int) -> list: return deepcopy([a[i] for a in self.args])

    def get_diagonal(self) -> list: return list(self[i][i] for i in range(min(self.line,self.col)))

    __getitem__ = get_line



    # print
    def print(self) -> None:
        for i in self.args:
            for j in i:
                print(f'{j : 6}', end='')
            print('')

    def __str__(self) -> str:
        r = ''
        for i in self.args:
            for j in i:
                r += f'{j : 6} ,' if type(j) != str else j
            r += '\n'
        return r



    # bool
    def is_squer(self) -> bool:
        return self.col == self.line



    # oppor
    def multiply_by_number(self, n: float):
        a = [[j * n for j in i]for i in self.args]
        return Matrix.make_from_list(a)

    def multiply_by_matrix(self, m):
        if type(m) != Matrix: raise ArgumentTypeError("can only take matrix entered type : " + str(type(m)))
        if self.col != m.line: raise ValueError("the RHS's columns must be equal to  LHS's rows")

        r = []
        for i in range(self.line):
            a = []
            for j in range(m.col):
                a.append(row_to_column_mapping(self.get_line(i), m.get_colum(j)))
            r.append(a)
        return Matrix.make_from_list(r)

    def multiply_by_list(self, l : list[int, float]):
        a = [[i] for i in l]
        return self.multiply_by_matrix(Matrix.make_from_list(a)).get_colum(0)

    def add(self, m):
        if not type(m) is Matrix: raise ArgumentTypeError(f"matrix can only be added with other matrix. type of argument given:{str(type(m))}" )
        if not m.line == self.line: raise ValueError("the number of lines must be equal")
        if not m.col == self.col: raise ValueError("the number of columns must be equal")

        a = [[self[i][j] + m[i][j] for j in range(self.col)] for i in range(self.line)]
        return Matrix.make_from_list(a)

    def sub(self, m): return self.add(m * -1)

    def T(self):
        a = [self.get_colum(i) for i in range(self.col)]
        return Matrix.make_from_list(a)

    def __mul__(self, other):
        if type(other) is int: other = float(other)
        if type(other) is float: return self.multiply_by_number(other)
        if type(other) is list: return self.multiply_by_list(other)
        if type(other) is Matrix: return self.multiply_by_matrix(other)

    __add__ = add
    __sub__ = sub


    # line and colum operators  ----start----
    def delete_line(self, i):
        if i < 0 or i > self.line: raise IndexError("out of bounds")
        return Matrix.make_from_list(remove_from_list(self.args, i))

    def delete_colum(self, i):
        if i < 0 or i > self.col: raise IndexError("out of bounds")
        return Matrix(remove_from_list(a, i) for a in self.args)

    def add_line(self, l : list):
        return Matrix.make_from_list(self.args + [l])

    def add_colum(self, r : list):
        a = deepcopy(self.args)

        for i in range(len(r)):
            if i >= len(a): a.append([0] * self.col + [r[i]])
            else: a[i].append(r[i])
        return Matrix.make_from_list(a)

    def swap_line(self,a : int,b: int):
        t = deepcopy(self.args)
        t[a] , t[b] = t[b] , t[a]
        return Matrix.make_from_list(t)

    def swap_colum_with(self, index : int, new_col : list):
        if not is_vector(new_col): raise ArgumentTypeError("can only teke lists containing floats")
        if index > self.col: raise IndexError("out of bounds")
        if len(new_col) > self.line: raise IndexError("out of bounds")

        a = deepcopy(self.args)
        for i in range(len(self.args)):
            a[i][index] = new_col[i]
        return Matrix.make_from_list(a)

    def minor(self, i, j): return self.delete_line(i).delete_colum(j)
    # line and colum operators  ----end-----




    # determinant
    def determinant(self) -> float:
        if not self.is_squer(): return 0
        line_one = self.get_line(0)
        if len(line_one) == 1: return line_one[0]

        a = 0
        for i in range(0, self.col):
            c = line_one[i] * ((-1) ** (i % 2))
            m = self.minor(0, i)
            a += m.determinant() * c
        return a

    # rank
    def rank(self) -> int:
        a = row_esioln(self)
        b = 0
        for i in a.args:
            if not is_zero(i): b += 1
        return b



    # Adjugate
    def cofactor(self, i, j) -> float:
        return self.minor(i,j).determinant() * (-1)**((i+j)%2)

    def adjugate(self):
        a = [[self.cofactor(i , j) for j in range(self.col)]for i in range(self.line)]
        return Matrix.make_from_list(a).T()


    # Inverse
    def inverse(self):
        return self.adjugate() * (1 / self.determinant())

    @staticmethod
    def make_from_list(l: list):
        return Matrix(a for a in l)

    @staticmethod
    def I(i : int):
        a = [[0] * i + [1] for i in range(i)]
        return Matrix.make_from_list(a)








def solve_gaussian_linear_system(multis : Matrix, vars: list, answers: list):
    # checking
    if len(vars) != len(answers):
        raise ValueError('too many ' +'variables' if len(vars) > len(answers) else 'answers')
    if not multis.is_squer():
        raise ValueError('coefficient is not squer')
    if multis.col != len(vars):
        raise ValueError('not enough' if multis.col < len(vars) else 'too many' + ' coefficient')

    a = row_esioln(multis.add_colum(answers).add_colum(vars))

    return extract_from_eliminated(a)

def solve_cramer_linear_system(multis : Matrix, vars: list, answers: list):
    # checking
    if len(vars) != len(answers):
        raise ValueError('too many ' + 'variables' if len(vars) > len(answers) else 'answers')
    if not multis.is_squer():
        raise ValueError('coefficient is not squer')

    a = {}
    for i in range(len(answers)):
        b = multis.swap_colum_with(i, answers).determinant() /multis.determinant()
        a[vars[i]] = b
    return a






# eigenvalues & eigenvectors
def calculate_eigenvalues(m : Matrix) -> list:
    return chatGPTs_help.calculate_eigenvalues(m.args)


def eigen_v(m : Matrix):
    if not m.is_squer(): raise ValueError("the matrix must be squere")

    r = {}
    values = calculate_eigenvalues(m)
    for v in values:
        a = m - Matrix.I(m.line) * v
        x = [str(i)for i in range(m.line)]
        b = [0] * m.line

        t = solve_gaussian_linear_system(a, x, b)
        t = {k: v for k, v in sorted(t.items(), key=lambda item: int(item[0]), reverse=True)}
        r[v] = [t[i] for i in t]
    return r


    # gaussian linear system utils (with spaghetti flavor )
def extract_from_eliminated(m :Matrix):
    r = {}
    for _ in range(len(m.args)):
        try:
            t = m.args[-1][-2]/m.args[-1][-3]
        except ZeroDivisionError:
            t = 1
        r[m.args[-1][-1]] = t
        m = m.delete_line(m.line - 1)
        for i in m.args:
            i[-2] -= i[-3] * t
        if m.col == 0: break
        m = m.delete_colum(m.col - 3)
    return r
# gaussian linear system utils end





# general utils
def row_esioln(m : Matrix):
    if len(m.args) == 1: return m

    #format check
    line_one = None
    for i in range(len(m.args)):
        if m.args[i][0] != 0:
            line_one = m.args[i]
            m = m.swap_line(0 ,i)
            break
    if line_one is None: raise ValueError('unsolvable with Gaussian Elimination')

    for i in range(1, len(m.args)):
        eliminate_line(m.args[i], line_one)

    t = row_esioln(m.delete_line(0).delete_colum(0))

    return add_zeros(t, line_one)

def add_zeros(m : Matrix, lo : list):
    a = [lo]
    for i in m.args:
        a.append([0] + i)
    return Matrix.make_from_list(a)

def eliminate_line(l : list, ro : list):
    p = float(l[0]) / ro[0]
    for i in range(len(l)):
        if type(l[i]) is str: continue

        l[i] -= ro[i] * p

def remove_from_list(l: list, i: int) -> list:
    r = deepcopy(l)
    r.pop(i)
    return r

def row_to_column_mapping(r : list, c : list) -> float:
    t = 0
    for a, b in zip(r, c): t += a * b
    return t

def is_vector(l : list) -> bool:
    for i in l:
        if not((type(i) is int)or(type(i) is float)): return False
    return True

def is_zero(l : list) -> bool:
    for i in l:
        if i != 0: return False
    return True
 # general utils end