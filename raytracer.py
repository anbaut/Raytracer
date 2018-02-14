import math
from math import sqrt

class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    def _get_y(self):
        return self._y

    def _set_y(self, y):
        self._y = y

    def _get_z(self):
        return self._z

    def _set_z(self, z):
        self._z = z

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    z = property(_get_z, _set_z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)


class Vecteur:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, b):
        return self.x * b.x + self.y * b.y + self.z * b.z

    def cross(self, b):
        return (
            self.y *
            b.z -
            self.z *
            b.y,
            self.z *
            b.x -
            self.x *
            b.z,
            self.x *
            b.y -
            self.y *
            b.x)

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normal(self):
        mag = self.magnitude()
        return Vecteur(self.x / mag, self.y / mag, self.z / mag)

    def __add__(self, b):
        return Vecteur(self.x + b.x, self.y + b.y, self.z + b.z)

    def __sub__(self, b):
        return Vecteur(self.x - b.x, self.y - b.y, self.z - b.z)

    def __mul__(self, b):
        assert isinstance(b, float) or isinstance(b, int)
        return Vecteur(self.x * b, self.y * b, self.z * b)


class Couleur:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def _get_r(self):
        return self._r

    def _set_r(self, r):
        self._r = r

    def _get_g(self):
        return self._g

    def _set_g(self, g):
        self._g = g

    def _get_b(self):
        return self._b

    def _set_b(self, b):
        self._b = b

    r = property(_get_r, _set_r)
    g = property(_get_g, _set_g)
    b = property(_get_b, _set_b)
