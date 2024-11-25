# Proyecto 3: OpenGL
## Autor: Jose Merida | 24 de Noviembre 2024
Los alumnos deben entregar un Diorama creado en base al renderer de OpenGL que se trabajó en clase. Un diorama es "un tipo de maqueta que muestra figuras humanas, vehículos, animales o incluso seres imaginarios como punto focal de su composición, presentados dentro de un entorno y con el propósito de representar una escena". En otras palabras, es una simple presentación de una escena 3D.

## Video Demostrativo
[Link](https://youtu.be/3bnXfLrfhv0)

Se muestran la mayoría de los shaders y funcionalidades que se implementaron a detalle.

## Ubicacion de Archivos
- Models: Los modelos utilizados en el programa
- Textures: Los archivos BMP utilizados como textura para los modelos dentro del programa
- Audio: Archivos .ogg y .mp3 de sonido

## Descripción de Input
### Movimiento de Cámara
Teclado:
- 'a' -> Orbitar Izquierda
- 'd' -> Orbitar Derecha
- 'w' -> Camara Hacia Arriba
  's' -> Camara Hacia Abajo
- '↑' -> Acercarse
- '↓' -> Alejarse
  
Mouse:
- Click + Drag Izq. -> Orbitar Izquierda
- Click + Drag Der. -> Orbitar Derecha
- Click + Drag Up -> Camara Hacia Arriba
- Click + Drag Down -> Camara Hacia Abajo

### Seleccion de Objeto a Orbitar
Teclado
- '0' -> Piso + un Offset, el centro / overview de la escena
- '1' -> Torreta de Killjoy + Efecto de Sonido
- '2' -> Dizzy / Flash de Gekko + Efecto de Sonido
- '3' -> Granada de Razes + Efecto de Sonido

## Objetos y Shaders:

### Torreta de Killjoy (Spring + Mouse Light)
El objeto rebota con un efecto de resorte, deformándose y desplazándose. Basado en el input del mouse se ilumina una sección.

![image](https://github.com/user-attachments/assets/2fe6351c-b22c-4e85-b3a6-2af0a7d23938)

### Dizzy (Energy)
El objeto tiene efectos de "energía" azules animados

![image](https://github.com/user-attachments/assets/8e4c6f29-efad-4f7f-a00b-f4f74985a79d)

### Nade (Bubble + Aberration)
Nota: Creo que se implemento para alguna de las versiones en clase, pero este ya lo habia hecho para mi Lab de Shaders

El objeto se distorsiona con 'burbujas' y tiene un efecto de aberración RGB

![image](https://github.com/user-attachments/assets/03eb7dd8-f27c-4e12-995c-cda0780c6dbb)

### Create (Grayscale)
El efecto cambia los colores a blanco y negro y agrega estática animada

![image](https://github.com/user-attachments/assets/ded0e0ec-d397-4d74-b47d-8c87dce61359)

### Piso y Pared
Figuras planas, las texturas fueron tomadas utilizando screenshots de Valorant
![image](https://github.com/user-attachments/assets/fb655d64-93f8-4d6e-9740-8764666d884f)

## Herramientas de IA
### Generacion Piso + Caja
https://chatgpt.com/share/67440a92-3c7c-8007-8db2-15f2af05f906

Aqui simplemente le pedi a ChatGPT que generara unos .obj

### Model Offset + Sonidos + Debug Texturas
https://chatgpt.com/share/67440ab6-b320-8007-8bd8-6e91269035af

Aquí quería verificar cómo agregarle un Offset a los modelos, ya que algunos estaban como "elevados" y el centro de su translation matrix estaba abajo de ellos. Solo apliqué un Offset de tipo glm.vec3 y cada vez que se llama el orbitar, orbita el translation + offset. También pregunté sobre sonidos en Pygame e hice un debug de por qué las texturas no estaban funcionando. Tuve que modificar el tamaño de las imágenes y los comandos de Pygame son bastante simples.
