# Proyecto 2: Raytracer
## Autor: José Mérida | 23 de Octubre 2024

## Ubicación de Archivos:
- **Textures:** Los archivos BMP utilizados como textura para las diferentes figuras dentro del programa
- **Renders:** El output BMP del programa
## Instrucciones
El objetivo de éste proyecto es demostrar los conocimientos adquiridos durante la segunda parte del curso.

Los alumnos deben entregar un Ray Tracer simple que trate de recrear una escena/imagen escogida por el alumno por medio de figuras simples.

## Resultados
Imagen de Inspiración: Master of Puppets de Metallica

La escena creada utilizando el Raytracer (Algunos elementos adicionales agregados a la escena utilizando formas simples)

![Render](/renders/output.bmp)

## Materiales Utilizados
Mirror: Material reflectivo sin textura.
``` Python
# Mirror, material reflectivo simple
mirror = Material(diffuse=[0.9, 0.9, 0.9], spec=128, Ks=0.2, matType=REFLECTIVE)
```
Brick: Material opaco con textura de ladrillo
``` Python
# Ladrillos para la piramide
brick = Material(spec=16, Ks=0.08, matType=OPAQUE, texture=Texture("textures/brick2.bmp"))
```
Military: Material 
``` Python
# Material para el casco militar
military = Material(diffuse=[0.9, 0.9, 0.9], spec=128, Ks=0.2, matType=OPAQUE, texture =Texture("textures/military.bmp"))
```
Pavement: Material del que están hechas las cruces
Grass: Material utilizado en el suelo de la escena

## Figuras Implementadas

Cross: Compuesta de 6 AABB's para darle la forma deseada, se llama utilizando la posición del centro de su base y el tamaño de cada bloque que la compone.
``` Python
rt.scene.append( Cross(position = [-6, -3.5, -8.5], block_size = 0.75, material = whiteSolid))
```
Pyramid: Compuesta por triangulos, se llama utilizando el centro de la pirámide, las dimensinoes de su base y su altura.
``` Python
rt.scene.append( Pyramid(base_center = [0, -3.5, -100], base_size = 30, height = 20, material = brick))
```
Cylinder: Compuesto por una curva infinita y dos planos como "caps", se llama utilizando coordenadas de posición, radio y altura.
``` Python
rt.scene.append(Cylinder(position=[0, -3.5, -8.5], radius=1.25, height = 1.5, material=mirror))
```
Hollow Sphere: Compuesta por una esfera ligeramente modificada para que únicamente tome en cuenta los hits que suceden de una mitad, al igual que los hits que suceden "atrás". Se llama utilizando coordendas de posición y radio.
``` Python
rt.scene.append(HalfSphere(position = [-3.75, -1.625, -8.5], radius = 0.7, material = military)) # Casco colgando de la primera cruz
```

## Iluminacion

Directional Lights: Se implementaron dos luces direccionales para darle un poco de dinamicidad a la escena, cada una va en diagonal hacia al frente y abajo pero una hacia la izquierda y otra hacia la derecha.

Spotlights: Se implementaron dos spotlights diferentes para mostrar un poco la reflectividad del cilindro
