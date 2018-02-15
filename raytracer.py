import math
from math import sqrt


class Point:
""" Classe qui définit les points de la scène """
    def __init__(self, point_x, point_y, point_z):
        self.point_x = point_x
        self.point_y = point_y
        self.point_z = point_z

    def _get_point_x(self):
        return self._point_x

    def _set_point_x(self, point_x):
        self._point_x = point_x

    def _get_point_y(self):
        return self._point_y

    def _set_point_y(self, point_y):
        self._point_y = point_y

    def _get_point_z(self):
        return self._point_z

    def _set_point_z(self, point_z):
        self._point_z = point_z

    x = property(_get_point_x, _set_point_x)
    y = property(_get_point_y, _set_point_y)
    z = property(_get_point_z, _set_point_z)

    def __add__(self, other):
        point_x = self.point_x + other.point_x
        point_y = self.point_y + other.point_y
        point_z = self.point_z + other.point_z
        return Point(point_x, point_y, point_z)


class Vecteur:
    def __init__(self, vecteur_x, vecteur_y, vecteur_z):
        self.vecteur_x = vecteur_x
        self.vecteur_y = vecteur_y
        self.vecteur_z = vecteur_z

    def dot(self, b):
        return self.vecteur_x * b.vecteur_x + self.vecteur_y * \
            b.vecteur_y + self.vecteur_z * b.vecteur_z

    def cross(self, b):
        return (
            self.vecteur_y *
            b.vecteur_z -
            self.vecteur_z *
            b.vecteur_y,
            self.vecteur_z *
            b.vecteur_x -
            self.vecteur_x *
            b.vecteur_z,
            self.vecteur_x *
            b.vecteur_y -
            self.vecteur_y *
            b.vecteur_x)

    def magnitude(self):
        return sqrt(self.vecteur_x**2 + self.vecteur_y**2 + self.vecteur_z**2)

    def normal(self):
        mag = self.magnitude()
        return Vecteur(
            self.vecteur_x / mag,
            self.vecteur_y / mag,
            self.vecteur_z / mag)

    def __add__(self, b):
        return Vecteur(
            self.vecteur_x +
            b.vecteur_x,
            self.vecteur_y +
            b.vecteur_y,
            self.vecteur_z +
            b.vecteur_z)

    def __sub__(self, b):
        return Vecteur(
            self.vecteur_x -
            b.vecteur_x,
            self.vecteur_y -
            b.vecteur_y,
            self.vecteur_z -
            b.vecteur_z)

    def __mul__(self, b):
        assert isinstance(b, float) or isinstance(b, int)
        return Vecteur(
            self.vecteur_x * b,
            self.vecteur_y * b,
            self.vecteur_z * b)


class Couleur:

    def __init__(self, couleur_r, couleur_g, couleur_b):
        self.couleur_r = couleur_r
        self.couleur_g = couleur_g
        self.couleur_b = couleur_b

    def _get_couleur_r(self):
        return self._couleur_r

    def _set_couleur_r(self, couleur_r):
        self._couleur_r = couleur_r

    def _get_couleur_g(self):
        return self._couleur_g

    def _set_couleur_g(self, couleur_g):
        self._couleur_g = couleur_g

    def _get_couleur_b(self):
        return self._couleur_b

    def _set_couleur_b(self, couleur_b):
        self._couleur_b = couleur_b

    couleur_r = property(_get_couleur_r, _set_couleur_r)
    couleur_g = property(_get_couleur_g, _set_couleur_g)
    couleur_b = property(_get_couleur_b, _set_couleur_b)
