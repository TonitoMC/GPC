import numpy as np
from intercept import Intercept
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

# TODO numpy
    def ray_intersect(self, orig, dir):
        # Vector substraction
        L = np.subtract(self.position, orig)
        # Producto punto
        tca = np.dot(L, dir)
        # np.linalg.norm = magnitud,
        d = (np.linalg.norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        
        if t0 < 0:
            return None
        
        P = np.add(orig, np.multiply(dir, t0))
        normal = np.subtract(P, self.position)
        normal /= np.linalg.norm(normal)
        return Intercept(point = P,
                         normal = normal,
                         distance = t0,
                         obj = self
                         )