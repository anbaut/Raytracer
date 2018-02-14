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

    '''def __add__(self,other):
        x = self.x+other.x
        y = self.y+other.y
        z = self.z+other.z
        return Point(x,y,z)'''
