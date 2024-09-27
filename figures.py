from intercept import Intercept
from MathLib import *
from math import atan2, acos, pi
class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"
    
    def ray_intersect(self, orig, dir):
        return None
    
class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        # Vector substraction
        L = vec_sub(self.position, orig)
        # Producto punto
        tca = dot_product(L, dir)
        d = (vec_norm(L) ** 2 - tca ** 2) ** 0.5
        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        
        if t0 < 0:
            return None
        
        P = vec_sum(orig, [x * t0 for x in dir ])
        normal = vec_sub(P, self.position)
        normal = [x / vec_norm(normal) for x in normal]

        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi

        return Intercept(point = P,
                         normal = normal,
                         distance = t0,
                         obj = self,
                         texCoords = [u,v],
                         rayDirection = dir
                         )