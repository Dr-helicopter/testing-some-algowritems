from matrices.Vectors import Vector3


class Line:
    def __init__(self, direct : Vector3 , dispos ):


        self.direction : Vector3 = direct.normalize()
        self.disposition = dispos


    def sym_equ(self) -> str:
        x = f'(x - {self.disposition.x})/({self.direction.x})'
        y = f'(y - {self.disposition.y})/({self.direction.y})'
        z = f'(z - {self.disposition.z})/({self.direction.z})'
        return f'{x}\n||\n{y}\n||\n{z}'

    def pram_eq(self) -> str:
        x = f'x = {self.direction.x}t + {self.disposition.x}'
        y = f'y = {self.direction.y}t + {self.disposition.y}'
        z = f'z = {self.direction.z}t + {self.disposition.z}'
        return f'|{x}\n|{y}\n|{z}'

    def is_parallel_to_line(self, other):
            if type(other) != Line: raise ValueError
            return self.direction == other.direction
