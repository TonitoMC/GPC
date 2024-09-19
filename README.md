# RT1: Spheres, Materials & Phong Shading
## Autor: José Mérida | Septiembre 2024

## Ubicación de Archivos:
- **Renders:** El output BMP del programa y cualquier otro render requerido para la entrega
## Instrucciones
Para obtener la nota completa de ésta tarea deben entregar lo siguiente:

- Código fuente capaz de renderizar esferas por medio de un Ray Intersect Algorithm.
  
- Usar un modelo de iluminación Phong
  
- El programa principal debe mostrar la siguiente figura (o lo más cercano posible) en pantalla o en un BMP:

![image](https://github.com/user-attachments/assets/8897aac4-3e79-4f5c-8b3e-b072e9ed4854)

## Resultados
El output / render final del proyecto

![Render](/renders/output.bmp)

### Materiales Utilizados
```
# Nieve, no refleja mucha luz
snow = Material(diffuse = [1,1,1], spec = 16, Ks = 0.08)

# Zanahoria, refleja mucha luz por motivos demostrativos
carrot = Material(diffuse = [1,0.5,0], spec = 64, Ks = 0.1)

# Botones de carbon, poco especular
charcoal = Material(diffuse = [0.2,0.2,0.2], spec = 16, Ks = 0.1)

# Botones (de plastico? no he hecho un muñeco de nieve) reflejan bastante luz
button = Material(diffuse = [0.2,0.2,0.2], spec = 128, Ks = 0.2)

# Ojos que reflejan bastante
eyewhite = Material(diffuse = [1,1,1], spec = 64, Ks = 0.2)
eyeblack = Material(diffuse = [0.2,0.2,0.2], spec = 64, Ks = 0.2)
```