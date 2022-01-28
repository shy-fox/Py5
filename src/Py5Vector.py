from typing import Union
from Py5 import Py5

class Py5Vector(object):

    """ A point-like object which can be moved. """

    x: float
    y: float
    z: float
    w: float

    def __init__(self, x: float, y: float, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def add(self, other: 'Py5Vector') -> 'Py5Vector':
        new_x = self.x + other.x
        new_y = self.y + other.y
        new_z = self.z + other.z
        new_w = self.w + other.w

        return Py5Vector(new_x, new_y, new_z, new_w)

    def sub(self, other: 'Py5Vector') -> 'Py5Vector':
        new_x = self.x - other.x
        new_y = self.y - other.y
        new_z = self.z - other.z
        new_w = self.w - other.w

        return Py5Vector(new_x, new_y, new_z, new_w)

    def mult(self, other: 'Py5Vector') -> 'Py5Vector':
        new_x = self.x * other.x
        new_y = self.y * other.y
        new_z = self.z * other.z
        new_w = self.w * other.w

        return Py5Vector(new_x, new_y, new_z, new_w)

    def div(self, other: 'Py5Vector') -> 'Py5Vector':
        new_x = self.x / other.x
        new_y = self.y / other.y
        new_z = self.z / other.z
        new_w = self.w / other.w

        return Py5Vector(new_x, new_y, new_z, new_w)

    def scale(self, amount: float) -> 'Py5Vector':
        return Py5Vector(self.x * amount, self.y * amount, self.z * amount, self.w * amount)

    @staticmethod
    def random2d(bound: Union[int, float] = 1.0) -> 'Py5Vector':
        return Py5Vector(Py5.random(0, bound), Py5.random(0, bound))

    @staticmethod
    def random3d(bound: Union[int, float] = 1.0) -> 'Py5Vector':
        return Py5Vector(Py5.random(0, bound), Py5.random(0, bound), Py5.random(0, bound))

    @staticmethod
    def random(bound: Union[int, float] = 1.0) -> 'Py5Vector':
        return Py5Vector(Py5.random(0, bound), Py5.random(0, bound), Py5.random(0, bound), Py5.random(0, bound))

    def get(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z, "w": self.w} \
            if self.w != 0 \
            else {"x": self.x, "y": self.y, "z": self.z} \
            if self.z != 0 else {"x": self.x, "y": self.y}
