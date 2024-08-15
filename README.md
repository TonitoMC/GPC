# Laboratorio 2: Shaders
## Autor: José Mérida | 14 de Agosto 2024

## Ubicación de Archivos:
- **Models:** Los archivos de los modelos utilizados dentro del programa
- **Textures:** Los archivos BMP utilizados como textura para los modelos dentro del programa
- **Renders:** El output BMP del programa y cualquier otro render requerido para la entrega
## Instrucciones
El objetivo de este laboratorio, es que practiquen crear shaders interesantes utilizando los parámetros que tienen ya a su disposición.

Para éste lab, tienen que crear tres shaders diferentes y mostrar sus resultados usando su Rasterizador. La nota de los criterios subjetivos dependera de qué tan complejo e interesante sea el shader que implementen. Usen su creatividad y habilidades matemáticas/artísticas para crear sus shaders. Pueden agregar o implementar el uso de diferentes tipos de iluminación, texturas múltiples, argumentos del shader, etc.

## Resultados
El output de la aplicación de los 3 shaders hechos para el Lab, el tercero está animado :)

![Render](/renders/output.bmp)

## Shaders
### Pixel Shader:
Toma un parámetro pixelSize, encuentra las coordenadas y luego fuerza un intervalo de valores a uno en específico.
```python
    pixelSize = 0.02
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    vtP[0] = (vtP[0] // pixelSize) * pixelSize
    vtP[1] = (vtP[1] // pixelSize) * pixelSize
```
Esto fuerza a que todos los pixeles en cierto rango de coordenadas tomen el mismo color de la textura

### Noise Shader:


### Blanco y Negro + Toon + Estática (Animado)
Primero utiliza un Toon Shader y lo pasa a blanco y negro
``` Python
    intensity = np.dot(normal, -np.array(dirLight) )
    intensity = max(0, intensity)
    
    if intensity < 0.33:
        intensity = 0.3
    elif intensity < 0.66:
        intensity = 0.6
    else:
        intensity = 1.0

    r *= intensity
    g *= intensity
    b *= intensity

    grayscale = (r + g + b) / 3
```
Luego genera la estática
``` Python
    staticStrength = 0.05
    noise = (random.random() - 0.5) * staticStrength
    dotProbability = 0.05 
    if random.random() < dotProbability:
        grayscale = 0.2 
    grayscale += noise
    grayscale = np.clip(grayscale, 0, 1) 
```
Al utilizar valores aleatorios para la estática se crea un efecto animado.
