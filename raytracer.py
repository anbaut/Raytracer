"""
    Ce projet est réalisé dans le cadre des partiels de l'ESGI
    Il permet de faire un lancer de rayon
     et de créer une image
     en fonction des éléments crées sur une scène
"""
from math import sqrt
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

    def dot(self, other):
        """
            Produit Scalaire de 2 vecteurs
        """
        return self.vecteur_x * other.vecteur_x + self.vecteur_y * \
            other.vecteur_y + self.vecteur_z * other.vecteur_z

    def cross(self, other):
        """
            Donne le produit vectoriel des deux vecteurs passés en paramètre
        """
        return (
            self.vecteur_y *
            other.vecteur_z -
            self.vecteur_z *
            other.vecteur_y,
            self.vecteur_z *
            other.vecteur_x -
            self.vecteur_x *
            other.vecteur_z,
            self.vecteur_x *
            other.vecteur_y -
            self.vecteur_y *
            other.vecteur_x)

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

    def __add__(self, other):
        """
            Redéfinit la fonction "+" pour additionner 2 vecteurs
        """
        return Vecteur(
            self.vecteur_x +
            other.vecteur_x,
            self.vecteur_y +
            other.vecteur_y,
            self.vecteur_z +
            other.vecteur_z)

    def __sub__(self, other):
        """
            Redéfinit la fonction "-" pour soustraire 2 vecteurs
        """
        return Vecteur(
            self.vecteur_x -
            other.vecteur_x,
            self.vecteur_y -
            other.vecteur_y,
            self.vecteur_z -
            other.vecteur_z)

    def __mul__(self, other):
        """
            Redéfinit la fonction "*" pour multiplier 2 vecteurs
        """
        assert isinstance(other, float) or isinstance(other, int)
        return Vecteur(
            self.vecteur_x * other,
            self.vecteur_y * other,
            self.vecteur_z * other)


class Couleur(Vecteur):
    """
        Classe qui gère les couleurs des éléments
    """

    def __init__(self, vecteur_x, vecteur_y, vecteur_z):
        self.vecteur_x = int(vecteur_x)
        self.vecteur_y = int(vecteur_y)
        self.vecteur_z = int(vecteur_z)

    def _set_vecteur_x(self, vecteur_x):
        if vecteur_x < 0:
            self.vecteur_x = 0
        elif vecteur_x > 255:
            self.vecteur_x = 255

    def _set_vecteur_y(self, vecteur_y):
        if vecteur_y < 0:
            self.vecteur_y = 0
        elif vecteur_y > 255:
            self.vecteur_y = 255

    def _set_vecteur_z(self, vecteur_z):
        if vecteur_z < 0:
            self.vecteur_z = 0
        elif vecteur_z > 255:
            self.vecteur_z = 255


class Sphere(object):
    """
        Permet la création de Sphère dans la scène
    """

    def __init__(self, centre, rayon, couleur):
        self.centre = centre
        self.rayon = rayon
        self.couleur = couleur

    def intersection(self, other):
        """
            Calcule les intersections
        """
        other.origin -= self.centre
        coef_a = other.dir.dot(other.dir)
        coef_b = 2 * (other.dir.dot(other.origin))
        coef_c = other.origin.dot(other.origin) - self.rayon**2
        discriminant = coef_b**2 - 4 * coef_a * coef_c
        if(discriminant < 0):
            return Intersection(Vecteur(0, 0, 0), -1, Vecteur(0, 0, 0), self)
        valeur_a = (-coef_b - sqrt(discriminant)) / (2 * coef_a)
        valeur_b = (-coef_b + sqrt(discriminant)) / (2 * coef_a)
        if valeur_a > 0 and (valeur_a < valeur_b or valeur_b < 0):
            return Intersection(
                other.origin + other.dir * valeur_a,
                valeur_a,
                self.normal(
                    other.origin + other.dir * valeur_a),
                self)
        if valeur_b > 0 and (valeur_b < valeur_a or valeur_a < 0):
            return Intersection(
                other.origin + other.dir * valeur_b,
                valeur_b,
                self.normal(
                    other.origin + other.dir * valeur_b),
                self)

        return Intersection(Vecteur(0, 0, 0), -1, Vecteur(0, 0, 0), self)

    def normal(self, b):
        return (b - self.centre).normal()


class Plane(object):
    """
        Permet la création d'un Plane dans la scène
    """

    def __init__(self, point, normal, couleur):
        self.normal = normal
        self.point = point
        self.couleur = couleur

    def intersection(self, other):
        """
            Calcule les intersections
        """
        valeur = other.dir.dot(self.normal)
        if valeur == 0:
            return Intersection(Vecteur(0, 0, 0), -1, Vecteur(0, 0, 0), self)
        valeur = (self.point - other.origin).dot(self.normal) / valeur
        return Intersection(other.origin + other.dir * valeur, valeur, self.normal, self)


class Ray(object):
    """
        Classe qui définit les rayons
    """

    def __init__(self, origin, direction):
        self.origin = origin
        self.dir = direction


class Intersection(object):
    """
        Classe qui définit les intersections entre les rayons et objets
    """

    def __init__(self, point, distance, normal, obj):
        self.p = point
        self.d = distance
        self.n = normal
        self.obj = obj


def test_ray(ray, objects, ignore=None):
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
    intersect = test_ray(ray, objects)
    if intersect.d == -1:
        col = Couleur(AMBIENT, AMBIENT, AMBIENT)
    else:
        col = intersect.obj.couleur * AMBIENT
    return col


def gamme_correction(color, factor):
    return (int(pow(color.vecteur_x / 255.0, factor) * 255),
            int(pow(color.vecteur_y / 255.0, factor) * 255),
            int(pow(color.vecteur_z / 255.0, factor) * 255))


AMBIENT = 0.1
GAMMA_CORRECTION = 1 / 2.2  # Valeur de la correction Gamma

OBJS = []  # Dictionnaire contenant tout les éléments de la scène

# Place des éléments sur la scène
OBJS.append(Sphere(Vecteur(-3.5, 1, -5), 1, Couleur(120, 255, 0)))
OBJS.append(Sphere(Vecteur(2, 1, -5), 2, Couleur(340.5, 0, 0)))
OBJS.append(Sphere(Vecteur(-0.5, -4, -5), 1.8, Couleur(0, 200, 255)))
OBJS.append(Sphere(Vecteur(-4, -2, -5), 1.8, Couleur(85, 0, 255)))
OBJS.append(Sphere(Vecteur(3.8, -3.5, -5), 2.4, Couleur(120, 120.1, 120)))
OBJS.append(Plane(Vecteur(-2, 4, -12), Couleur(0, 0, 1),
                  Couleur(30, 30, 30)))

LIGHTSOURCE = Vecteur(0, 10, -3)  # Emplacement de la lumière


# Dimensions de l'image avec son format couleur
IMG = Image.new("RGB", (500, 500))
CAMERAPOS = Vecteur(0, 0, 20)  # Emplacement de la caméra
for x in range(500):
    print(x, "/500")  # Donne l'avancement de l'éxécution du programme
    for y in range(500):
        ray = Ray(
            CAMERAPOS,
            (Vecteur(
                x / 50.0 - 5,
                y / 50.0 - 5,
                0) - CAMERAPOS).normal())
        # Récupère la couleur transmise par le rayon
        col = trace(ray, OBJS, LIGHTSOURCE, 0)
        # Place un pixel de couleur et applique la correction Gamma
        IMG.putpixel((x, 499 - y), gamme_correction(col, GAMMA_CORRECTION))

IMG.save("raytracer.png", "PNG")  # Sauvegarde l'image au format PNG
print("Traitement terminé")
