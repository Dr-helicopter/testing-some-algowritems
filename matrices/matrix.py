from argparse import ArgumentTypeError
from copy import deepcopy
from types import GeneratorType


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
    def get_line(self, i: int): return deepcopy(self.args[i])

    def get_colum(self, i: int): return deepcopy([a[i] for a in self.args])

    __getitem__ = get_line




    # print
    def print(self):
        for i in self.args:
            for j in i:
                print(f'{j : 6}', end='')
            print('')

    def __str__(self):
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
        a = []
        for i in self.args:
            a.append([j * n for j in i])
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



    def __mul__(self, other):
        if type(other) is int: other = float(other)
        if type(other) is float: return self.multiply_by_number(other)
        if type(other) is Matrix: return self.multiply_by_matrix(other)



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

    def swap_colum_with(self, index : int, new_col : list[float]):
        if index > self.col: raise IndexError("out of bounds")
        if len(new_col) > self.line: raise IndexError("out of bounds")
        a = deepcopy(self.args)
        for i in range(len(self.args)):
            a[i][index] = new_col[i]
        return Matrix.make_from_list(a)
    # line and colum operators  ----end-----




    # determinant
    def determinant(self) -> float:
        if not self.is_squer(): return 0
        line_one = self.get_line(0)
        if len(line_one) == 1: return line_one[0]

        a = 0
        for i in range(0, self.col):
            c = line_one[i] * ((-1) ** (i % 2))
            m = self.delete_line(0).delete_colum(i)
            a += m.determinant() * c
        return a




    @staticmethod
    def make_from_list(l: list):
        return Matrix(a for a in l)




def solve_gaussian_linear_system(multis : Matrix, vars: list, answers: list):
    # checking
    if len(vars) != len(answers):
        raise ValueError('too many ' +'variables' if len(vars) > len(answers) else 'answers')
    if not multis.is_squer():
        raise ValueError('coefficient is not squer')
    if multis.col != len(vars):
        raise ValueError('not enough' if multis.col < len(vars) else 'too many' + ' coefficient')


    a = eliminate_system(multis.add_colum(answers).add_colum(vars))

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

# gaussian linear system utils (with spaghetti flavor )
def extract_from_eliminated(m :Matrix):
    r = {}
    for _ in range(len(m.args)):
        t = m.args[-1][-2]/m.args[-1][-3]
        r[m.args[-1][-1]] = t
        m = m.delete_line(m.line - 1)
        for i in m.args:
            i[-2] -= i[-3] * t
        if m.col == 0: break
        m = m.delete_colum(m.col - 3)
    return r

def eliminate_system(m : Matrix):
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
        eliminate_row(m.args[i], line_one)

    t = eliminate_system(m.delete_line(0).delete_colum(0))

    return add_zeros(t, line_one)

def eliminate_row(l : list, ro : list):
    p = float(l[0]) / ro[0]
    for i in range(len(l)):
        if type(l[i]) is str: continue

        l[i] -= ro[i] * p

def add_zeros(m : Matrix, lo : list):
    a = [lo]
    for i in m.args:
        a.append([0] + i)
    return Matrix.make_from_list(a)
# gaussian linear system utils end


# general utils
def remove_from_list(l: list, i: int) -> list:
    r = deepcopy(l)
    r.pop(i)
    return r

def row_to_column_mapping(r : list, c : list) -> float:
    t = 0
    for a, b in zip(r, c): t += a * b
    return t
 # general utils end