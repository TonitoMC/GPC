# Lab 3: Ray-Intersect Algorithm, New Shapes
## Autor: José Mérida | Septiembre 2024
## Ubicación de Archivos:
- **Renders:** El output BMP del programa y cualquier otro render requerido para la entrega
- **Textures:** Texturas aplicadas a los diferentes objetos
## Instrucciones
El objetivo de este laboratorio es que los alumnos rendericen nuevas figuras a través del RayTracer simple que hemos estado trabajando.

Para éste lab, tienen que investigar e implementar el Ray Intersect Algorithm de DOS figuras diferentes a las aprendidas en clase. Las figuras pueden ser cualquiera de las siguientes opciones:

- Triángulo (puede ser usado después para dibujar modelos)
- OBBs (oriented bounding boxes)
- Cilindro o capsula
- Toroide/dona
- Elipsoide/Esfera ovalada
- Cualquier otra figura que se les ocurra

## Primera Entrega
### No funciona la reflexión, creo que es por la implementación de los triángulos y el cálculo de la normal (Están reflejando lo de adentro). Pendiente revisar, las texturas funcionan bien.
![Render](/renders/output.bmp)

## Figuras Elegidas
### Triángulo
Se define por sus 3 vertices y utiliza el algoritmo Moller-Trumbore.
```python
# Triángulo Definido por sus 3 Vértices
class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(material)
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
```
### Piramide
Se define por coordenadas de base, altura y ancho. Utiliza 4 triangulos para las caras y una base cuadrada.
```python
# Pirámide definida por coordenada de centro de base, altura, y ancho
class Pyramid(Shape):
    def __init__(self, base_center, base_size, height, material):
        super().__init__(material)
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
```

