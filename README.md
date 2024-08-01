# R2: Cameras
## Autor: José Mérida

## Ubicación de Archivos:
- **Src:** Los archivos principales .py
- **Data:** Los archivos de input / output
- **Tests:** Pruebas unitarias (No hice)
- **Renders:** Los 4 BMP de los renders, aqui en el readme se detallan las configuraciones para cada uno
## Instrucciones
El objetivo de este ejercicio es que puedan renderizar un modelo OBJ y visualizarlo desde diferentes ángulos con una cámara con perspectiva.

Para obtener la nota completa de ésta tarea deben entregar lo siguiente:

Código fuente capaz de cargar un archivo .obj y renderizarlo ya sea con puntos o líneas.
Archivo obj de su elección.
Su código debe implementar las siguientes transformaciones utilizando matrices:
- Model
- View
- Projection
- Viewport
  
Photoshoot! Deben renderizar 4 tomas de su modelo:
- Medium shot
- Low angle
- High angle
- Dutch angle
El modelo debe ser cargado en el centro de la pantalla y debe ser completamente visible para cada una de las cuatro tomas. Recuerden incluir instrucciones sobre como hacer las cuatros tomas de su modelo y los cuatro FrameBuffers finales.

## Resultados
Nota: Utilice uno de los renders de clase, el que había utilizado en la entrega anterior estaba raro porque lo había convertido a un archivo obj desde otro formato y no se podría apreciar bien a perspectiva. No especificaba en las instrucciones si se podía utilizar alguno de clase así que decidí hacerlo.

### Medium Shot
Shot donde la cámara se encuentra directamente al frente del objeto
```
modelo1.translate[1] -= 4.5
modelo1.translate[2] = -20
modelo1.scale[0] = 0.3
modelo1.scale[1] = 0.3
modelo1.scale[2] = 0.3
```

### Low Angle
Shot donde la cámara se encuentra más abajo del objeto viendo hacia arriba
```
modelo1.translate[1] -= 2
modelo1.translate[2] = -20
modelo1.scale[0] = 0.3
modelo1.scale[1] = 0.3
modelo1.scale[2] = 0.3
rend.camera.translate[1] -= 15
rend.camera.rotate[0] += 45
```

### High Angle
Shot donde la cámara se encuentra más arriba del objeto viendo hacia abajo
```
modelo1.translate[1] -= 2
modelo1.translate[2] = -20
modelo1.scale[0] = 0.3
modelo1.scale[1] = 0.3
modelo1.scale[2] = 0.3
rend.camera.translate[1] += 15
rend.camera.rotate[0] -= 45
```

### Dutch Angle
Shot dónde la cámara rota.
```
modelo1.translate[1] += 5
modelo1.translate[2] = -20
modelo1.scale[0] = 0.3
modelo1.scale[1] = 0.3
modelo1.scale[2] = 0.3
rend.camera.translate[1] += 15
rend.camera.rotate[0] -= 20
rend.camera.rotate[2] += 45
```
