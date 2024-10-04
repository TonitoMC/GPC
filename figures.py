from intercept import Intercept
from MathLib import *
from math import atan2, acos, pi, isclose
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
    
class Plane(Shape):
    def __init__(self, position, normal, material, texture_scale=(0.2, 0.2)):
        super().__init__(position, material)
        self.normal = [x / vec_norm(normal) for x in  normal]
        self.type = "Plane"
        self.u_dir, self.v_dir = compute_uv_axes(self.normal)
        self.texture_scale = texture_scale

    def ray_intersect(self, orig, dir):
        denom = dot_product(dir, self.normal)
        if isclose(0, denom):
            return None
        
        num = dot_product(vec_sub(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None
        
        P = vec_sum(orig, [x * t for x in dir])
        
        local_p = vec_sub(P, self.position)
        u = dot_product(local_p, self.u_dir) * self.texture_scale[0]
        v = dot_product(local_p, self.v_dir) * self.texture_scale[1]

        u = u % 1.0
        v = v % 1.0

        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self,
        )


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None
        
        contact = vec_sub(planeIntercept.point, self.position)

        contact = vec_norm(contact)

        if contact > self.radius:
            return None
        
        return planeIntercept
    
class AABB(Shape):
    # Axis Aligned Bounding Box
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        self.planes = []

        rightPlane = Plane([position[0] + sizes[0]/2, position[1], position[2]], [1,0,0], material)
        leftPlane = Plane([position[0] - sizes[0]/2, position[1], position[2]], [-1,0,0], material)

        upPlane = Plane([position[0], position[1] + sizes[1]/2, position[2]], [0,1,0], material)
        downPlane = Plane([position[0], position[1] - sizes[1]/2, position[2]], [0,-1,0], material)

        frontPlane = Plane([position[0], position[1], position[2] + sizes[2]/2], [0,0,1], material)
        backPlane = Plane([position[0], position[1], position[2] - sizes[2]/2], [0,0,-1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        # Bounds

        self.boundsMin = [0,0,0]

        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i] / 2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i] / 2)
    
    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")
        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept
        
        if intercept == None:
            return None
        
        u, v = 0, 0

        if abs(intercept.normal[0]) > 0:
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]


        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
        
        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))


        return Intercept(point = intercept.point,
                         normal = intercept.normal,
                         distance = t,
                         texCoords = [u,v],
                         rayDirection = dir,
                         obj = self)
    
# Triángulo Definido por sus 3 Vértices
class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(v0, material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.type = "Triangle"

        # Cálculo de normal por producto cruz de 2 vectores
        # sobre la superficie del triángulo
        self.edge1 = vec_sub(self.v1, self.v0)
        self.edge2 = vec_sub(self.v2, self.v0)
        self.normal = cross_product(self.edge1, self.edge2)
        self.normal = [x / vec_norm(self.normal) for x in self.normal]

    # Ray intersect para el triángulo
    def ray_intersect(self, orig, dir):
        # Möller–Trumbore
        h = cross_product(dir, self.edge2)
        a = dot_product(self.edge1, h)
        
        # Determina si el rayo es paralelo al triangulo
        # en este caso es imposible que intercepte
        if isclose(a, 0):
            return None
        
        # Calcula si la intercepcion cae dentro del triangulo,
        # similar a como funcionan las caras de un cubo con planos

        # Revisa coordenada u
        f = 1.0 / a
        s = vec_sub(orig, self.v0)
        u = f * dot_product(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        # Revisa coordenada v
        q = cross_product(s, self.edge1)
        v = f * dot_product(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None
        
        # Calculo de distancia al punto de intercepcion
        t = f * dot_product(self.edge2, q)
        
        if t < 0:
            return None
        
        P = vec_sum(orig, [x * t for x in dir])

        w = 1 - u - v
        texCoords = [u, v, w]
        
        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=texCoords[:2],
            rayDirection=dir,
            obj=self
        )

# Pirámide definida por coordenada de centro de base, altura, y ancho
class Pyramid(Shape):
    def __init__(self, base_center, base_size, height, material):
        super().__init__(base_center, material)
        self.type = "Pyramid"
        self.triangles = []

        # Vertices de la base
        half_size = base_size / 2
        v0 = [base_center[0] - half_size, base_center[1], base_center[2] - half_size]
        v1 = [base_center[0] + half_size, base_center[1], base_center[2] - half_size]
        v2 = [base_center[0] + half_size, base_center[1], base_center[2] + half_size]
        v3 = [base_center[0] - half_size, base_center[1], base_center[2] + half_size]

        # Calculo del apice
        apex = [base_center[0], base_center[1] + height, base_center[2]]

        # Creacion de caras triangulares
        self.triangles.append(Triangle(v0, v1, apex, material))
        self.triangles.append(Triangle(v1, v2, apex, material))
        self.triangles.append(Triangle(v2, v3, apex, material))
        self.triangles.append(Triangle(v3, v0, apex, material))

        # Base solida
        self.triangles.append(Triangle(v0, v1, v2, material))
        self.triangles.append(Triangle(v0, v2, v3, material))

    def ray_intersect(self, orig, dir):
        # Buffer para el intercepto más cercano
        closest_intercept = None
        min_distance = float("inf")

        for triangle in self.triangles:
            intercept = triangle.ray_intersect(orig, dir)
            if intercept is not None and intercept.distance < min_distance:
                min_distance = intercept.distance
                closest_intercept = intercept

        return closest_intercept
