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

## Salida del Programa
![Render](/renders/output.bmp)

## Figuras Elegidas
### Triángulo
Se define por sus 3 vertices y utiliza el algoritmo Moller-Trumbore.
```python
# Triángulo Definido por sus 3 Vértices
class Triangle(Shape):
    def __init__(self, v0, v1, v2, material, epsilon=1e-6):
        super().__init__(v0, material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.type = "Triangle"
        self.epsilon = epsilon 

        # Cálculo de normal por producto cruz de 2 vectores
        # sobre la superficie del triángulo, afecta el orden de los
        # vértices para la normal
        self.edge1 = vec_sub(self.v1, self.v0)
        self.edge2 = vec_sub(self.v2, self.v0)
        self.normal = cross_product(self.edge1, self.edge2)
        self.normal = [x / vec_norm(self.normal) for x in self.normal]
```
### Cilindro
Se define por coordenadas de posición, radio y altura. Se compone de una curva infinita y dos "caps" representados con planos
```python
class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"

        # Crear dos objetos Disk para las tapas superior e inferior
        self.bottom_cap = Disk(
            position=[position[0], position[1], position[2]],
            normal=[0, -1, 0],  # Normal apuntando hacia abajo
            radius=radius,
            material=material
        )

        self.top_cap = Disk(
            position=[position[0], position[1] + height, position[2]],
            normal=[0, 1, 0],  # Normal apuntando hacia arriba
            radius=radius,
            material=material
        )
```

