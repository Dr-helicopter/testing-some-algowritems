from copy import deepcopy
from types import GeneratorType

class matrix:
    def __init__(self, *args):
        #for generator
        if isinstance(args[0], GeneratorType): args = list(args[0])


        self.args = []
        self.col = 0
        self.line = len(args)

        # initial checking
        for i in args:
            if not type(i) is list: raise TypeError(f"Matrices only takes lists entered type :" + str(type(i)))
            if len(i) > self.col: self.col = len(i)



        self.args = list(i + [0] * (self.col - len(i)) for i in args)



    #getters
    def get_line(self, i : int):return deepcopy(self.args[i])
    def get_colum(self, i : int): return deepcopy([a[i] for a in self.args])
    __getitem__ = get_line



    #print
    def print(self):
        for i in self.args:
            for j in i:
                print(f'{j : 6}', end='')
            print('')
    def __str__(self):
        r = ''
        for i in self.args:
            for j in i:
                r += f'{j : 6} ,'
            r += '\n'
        return r


    # bool
    def is_squer(self) -> bool: return self.col == self.line


    #oppor
    def multiply_by_number(self,n : float):
        a = []
        for i in self.args:
            a.append([j * n for j in i])
        return matrix.make_from_list(a)


    def __mul__(self, other):
        if type(other) is int: other = float(other)
        if type(other) is float: return self.multiply_by_number(other)




    #deleters
    def delete_line(self,i):
        if i < 0 or i > self.line: raise IndexError("out of bounds")
        return matrix.make_from_list(remove_from_list(self.args, i))

    def delete_colum(self,i):
        if i < 0 or i > self.col: raise IndexError("out of bounds")
        return matrix(remove_from_list(a, i) for a in self.args)


    #determinant
    def determinant(self) -> float:
        if not self.is_squer(): return 0
        line_one = self.get_line(0)
        if len(line_one) == 1: return line_one[0]

        a = 0
        for i in range(0, self.col):
            c = line_one[i]*((-1)**(i % 2))
            m = self.delete_line(0).delete_colum(i)
            a += m.determinant() * c
        return a

    @staticmethod
    def make_from_list(l : list):
        return matrix(a for a in l)




def remove_from_list(l: list, i: int) -> list:
    r = deepcopy(l)
    r.pop(i)
    return r