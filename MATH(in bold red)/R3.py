from Vectors import Vector3


class Line:
    def __init__(self, direct : Vector3 , dispos ):
        self.direction : Vector3 = direct.normalize()
        self.disposition = _closest_point_to_origin(dispos, self.direction)


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

    def is_parallel_to_line(self, other) -> bool:
        if type(other) != Line: raise ValueError
        return self.direction.is_linear_dependent_to(other.direction)

    def is_coplanar_with_line(self, other):
        if type(other) != Line: raise ValueError

        return (self.disposition - other.disposition).dot_product(self.direction.x_product(other.direction)) == 0

    def status_to_line(self, other):
        if type(other) != Line: raise ValueError

        if self.is_parallel_to_line(other):
            if self.disposition == other.disposition:
                return 'overlapping'
            return 'parallel'
        else:
            if self.is_coplanar_with_line(other):
                return "crossing"
            return "unrelated"




# I have not a clue what this does.
def _closest_point_to_origin(disp : Vector3, dir : Vector3) -> Vector3:
    t = -(disp.x * dir.x + disp.y * dir.y + disp.z * dir.z) / (dir.x ** 2 + dir.y ** 2 + dir.z ** 2)

    closest_x = disp.x + t * dir.x
    closest_y = disp.y + t * dir.y
    closest_z = disp.z + t * dir.z

    return Vector3(closest_x, closest_y, closest_z)





