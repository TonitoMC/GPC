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
## Ubicaciones de los Elementos

```python
# Opaque Triangle
rt.scene.append(Triangle( v0 = [-4.5, 0, -5],v1 = [-4.5, -2, -5], v2 = [-2.5, 0, -5], material = brick))

# Reflective Triangle
rt.scene.append(Triangle( v0 = [-1, 0, -5],v1 = [-1, -2, -5], v2 = [1, 0, -5], material = mirror))

# Refractive Triangle
rt.scene.append(Triangle( v0 = [2.5, 0, -5],v1 = [2.5, -2, -5], v2 = [4.5, 0, -5], material = glass))

# Opaque Cylinder
rt.scene.append(Cylinder(position=[-2.5, 1.25, -5], radius=1, height = 0.5, material=brick))

# Reflective Cylinder
rt.scene.append(Cylinder(position=[0, 1.25, -5], radius=1, height = 0.5, material=mirror))

# Behind Refractive Cylinder for Demonstration
rt.scene.append(Cylinder(position=[2.5, 1.25, -7.5], radius=1, height = 1, material=brick))


# Refractive Cylinder
rt.scene.append(Cylinder(position=[2.5, 1, -5], radius=1, height = 1.5, material=glass))
```

## ChatGPT
Tuve una conversación corta para que me explicara algunos de los algoritmos que se utilizan, para el cilindro sabía que iba a utilizar discos para las tapas.
```
¿Qué algoritmos puedo utilizar para calcular la intersección con un triángulo en un raytracer simple?
¿Y en la parte circular de un cilindro?
```
### Resumen
- Para el triángulo, utiliza el algoritmo de Möller–Trumbore.

- Para la parte circular del cilindro, utiliza un método cuadrático para resolver la intersección con la superficie lateral del cilindro, y luego verifica los límites si el cilindro es finito. Si el discriminante es positivo, el rayo intersecta la superficie lateral del cilindro. Si el discriminante es negativo, no hay intersección.

Incorporé estos algoritmos y algunos conceptos utilizados en otras formas, por ejemplo los discos para el cilindro y el concepto de un "buffer" para los interceptos en el cilindro.

