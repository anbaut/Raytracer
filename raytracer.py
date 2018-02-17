"""
    Ce projet est réalisé dans le cadre des partiels de l'ESGI
    Il permet de faire un lancer de rayon
     et de créer une image
     en fonction des éléments crées sur une scène
"""
from math import sqrt, pi
from PIL import Image


class Point:
    """
        Classe qui définit les points du raytracer
    """

    def __init__(self, point_x, point_y, point_z):
        self._point_x = point_x
        self._point_y = point_y
        self._point_z = point_z

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
        point_x = self._point_x + other.point_x
        point_y = self._point_y + other.point_y
        point_z = self._point_z + other.point_z
        return Point(point_x, point_y, point_z)


class Vecteur:
    """
        Classe qui gère les vecteurs du raytracer
    """

    def __init__(self, vecteur_x, vecteur_y, vecteur_z):
        self.vecteur_x = vecteur_x
        self.vecteur_y = vecteur_y
        self.vecteur_z = vecteur_z

    def dot(self, b):
        return self.vecteur_x * b.vecteur_x + self.vecteur_y * \
            b.vecteur_y + self.vecteur_z * b.vecteur_z

    def cross(self, b):
        """
            Donne le produit vectoriel des deux vecteurs passés en paramètre
        """
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
        """
            Donne la magnitude du vecteur
        """
        return sqrt(self.vecteur_x**2 + self.vecteur_y**2 + self.vecteur_z**2)

    def normal(self):
        """
            Donne la normale du vecteur
        """
        mag = self.magnitude()
        return Vecteur(
            self.vecteur_x / mag,
            self.vecteur_y / mag,
            self.vecteur_z / mag)

    def __add__(self, b):
        """
            Redéfinit la fonction "+" pour additionner 2 vecteurs
        """
        return Vecteur(
            self.vecteur_x +
            b.vecteur_x,
            self.vecteur_y +
            b.vecteur_y,
            self.vecteur_z +
            b.vecteur_z)

    def __sub__(self, b):
        """
            Redéfinit la fonction "-" pour soustraire 2 vecteurs
        """
        return Vecteur(
            self.vecteur_x -
            b.vecteur_x,
            self.vecteur_y -
            b.vecteur_y,
            self.vecteur_z -
            b.vecteur_z)

    def __mul__(self, b):
        """
            Redéfinit la fonction "*" pour multiplier 2 vecteurs
        """
        assert isinstance(b, float) or isinstance(b, int)
        return Vecteur(
            self.vecteur_x * b,
            self.vecteur_y * b,
            self.vecteur_z * b)


class Couleur:
    """
        Classe qui gère les couleurs des éléments
    """

    def __init__(self, couleur_r, couleur_g, couleur_b):
        self._couleur_r = couleur_r
        self._couleur_g = couleur_g
        self._couleur_b = couleur_b

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


class Sphere(object):
    """
        Permet la création de Sphère dans la scène
    """

    def __init__(self, centre, rayon, couleur):
        self.centre = centre
        self.rayon = rayon
        self.couleur = couleur

    def intersection(self, l):
        q = l.d.dot(l.o - self.centre)**2 - \
            (l.o - self.centre).dot(l.o - self.centre) + self.rayon**2
        if q < 0:
            return Intersection(Vecteur(0, 0, 0), -1, Vecteur(0, 0, 0), self)

        d = -l.d.dot(l.o - self.centre)
        d1 = d - sqrt(q)
        d2 = d + sqrt(q)
        if 0 < d1 and (d1 < d2 or d2 < 0):
            return Intersection(
                l.o + l.d * d1,
                d1,
                self.normal(
                    l.o + l.d * d1),
                self)
        if 0 < d2 and (d2 < d1 or d1 < 0):
            return Intersection(
                l.o + l.d * d2,
                d2,
                self.normal(
                    l.o + l.d * d2),
                self)

        return Intersection(Vecteur(0, 0, 0), -1,
                            Vecteur(0, 0, 0), self)

    def normal(self, b):
        return (b - self.centre).normal()


class Plane(object):
    """
        Permet la création d'un Plane dans la scène
    """

    def __init__(self, point, normal, couleur):
        self.n = normal
        self.p = point
        self.couleur = couleur

    def intersection(self, l):
        d = l.d.dot(self.n)
        if d == 0:
            return Intersection(Vecteur(0, 0, 0), -1, Vecteur(0, 0, 0), self)
        d = (self.p - l.o).dot(self.n) / d
        return Intersection(l.o + l.d * d, d, self.n, self)


class Ray(object):
    """
        Classe qui définit les rayons
    """

    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction


class Intersection(object):
    """
        Classe qui définit les intersections entre les rayons et objets
    """

    def __init__(self, point, distance, normal, obj):
        self.p = point
        self.d = distance
        self.n = normal
        self.obj = obj


def testRay(ray, objects, ignore=None):
    intersect = Intersection(Vecteur(0, 0, 0), -1, Vecteur(0, 0, 0), None)

    for obj in objects:
        if obj is not ignore:
            current_intersect = obj.intersection(ray)
            if current_intersect.d > 0 and intersect.d < 0:
                intersect = current_intersect
            elif 0 < current_intersect.d < intersect.d:
                intersect = current_intersect
    return intersect


def trace(ray, objects, light, max_recur):
    if max_recur < 0:
        return (0, 0, 0)
    intersect = testRay(ray, objects)
    if intersect.d == -1:
        col = Vecteur(AMBIENT, AMBIENT, AMBIENT)
    elif intersect.n.dot(light - intersect.p) < 0:
        col = intersect.obj.couleur * AMBIENT
    else:
        light_ray = Ray(intersect.p, (light - intersect.p).normal())
        if testRay(light_ray, objects, intersect.obj).d == -1:
            light_intensity = 1000.0 / \
                (4 * pi * (light - intersect.p).magnitude()**2)
            col = intersect.obj.couleur * \
                max(intersect.n.normal().dot((light - intersect.p).normal() *
                                             light_intensity), AMBIENT)
        else:
            col = intersect.obj.couleur * AMBIENT
    return col


def gamme_correction(color, factor):
    return (int(pow(color.vecteur_x / 255.0, factor) * 255),
            int(pow(color.vecteur_y / 255.0, factor) * 255),
            int(pow(color.vecteur_z / 255.0, factor) * 255))


AMBIENT = 0.1
GAMMA_CORRECTION = 1 / 2.2

OBJS = []   # create an empty Python "list"
# Put 4 objects into the list: 3 spheres and a plane (rf. class __init__
# methods for parameters)
# center, radius, color(=RGB)
OBJS.append(Sphere(Vecteur(-2, 0, -10), 2.0, Vecteur(0, 255, 0)))
OBJS.append(Sphere(Vecteur(2, 0, -10), 3.5, Vecteur(255, 0, 0)))
OBJS.append(Sphere(Vecteur(0, -4, -10), 3.0, Vecteur(0, 0, 255)))
OBJS.append(Plane(Vecteur(0, 0, -12), Vecteur(0, 0, 1),
                  Vecteur(255, 255, 255)))  # normal, point, color

# experiment with a different (x,y,z) light position
LIGHTSOURCE = Vecteur(-10, 0, 0)

IMG = Image.new("RGB", (500, 500))
CAMERAPOS = Vecteur(0, 0, 20)
for x in range(500):  # loop over all x values for our image
    print(x)   # provide some feedback to the user about our progress
    for y in range(500):  # loop over all y values
        ray = Ray(
            CAMERAPOS,
            (Vecteur(
                x / 50.0 - 5,
                y / 50.0 - 5,
                0) - CAMERAPOS).normal())
        col = trace(ray, OBJS, LIGHTSOURCE, 10)
        IMG.putpixel((x, 499 - y), gamme_correction(col, GAMMA_CORRECTION))
# save the image as a .png (or "BMP", but it produces a much larger file)
IMG.save("trace.png", "PNG")
