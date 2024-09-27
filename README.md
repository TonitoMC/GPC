# RT2: Opaque, Reflective & Refractive Materials
## Autor: José Mérida | Septiembre 2024

## Ubicación de Archivos:
- **Renders:** El output BMP del programa y cualquier otro render requerido para la entrega
- **Textures:** Las texturas aplicadas a l as esferas
## Instrucciones
Para obtener la nota completa de ésta tarea deben entregar lo siguiente:

- Código fuente capaz de renderizar esferas con distintos tipos de materiales.
  
- Cargar una textura que sirva de Environment Map en la escena (diferente al usado en clase).
  
- El programa principal debe cargar y mostrar seis esferas diferentes de distintos colores y propiedades: 2 opacas, 2 reflectivas y 2 transparentes.

## Resultados
El output / render final de la entrega

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
