import pygame
from pygame.locals import *
from gl import Renderer, LINES, POINTS
from src.model import Model
from src.shaders import vertexShader

# Variables de dimensiones de la pantalla
width = 960
height = 540
# Inicializa la pantalla de Pygame
screen = pygame.display.set_mode((width, height))

# Refresh rate / FPS
clock = pygame.time.Clock()

# Loop donde todo va a estar corriendo
isRunning = True

rend = Renderer(screen)
rend.vertexShader = vertexShader

modelo1 = Model("../data/chamber.obj")
modelo1.translate[0] = width / 2 - 200
modelo1.translate[1] = (height / 2) - 50

modelo1.scale[0] = 1500
modelo1.scale[1] = 1500
modelo1.scale[2] = 1500
modelo1.rotate[0] = -90

rend.models.append(modelo1)

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 10
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 10
            elif event.key == pygame.K_UP:
                modelo1.rotate[0] += 10
            elif event.key == pygame.K_DOWN:
                modelo1.rotate[0] -= 10
            elif event.key == pygame.K_l:
                modelo1.rotate[2] += 10
            elif event.key == pygame.K_k:
                modelo1.rotate[2] -= 10
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES

    rend.glClear()

    rend.glRender()

    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("../data/bitmap.bmp")

pygame.quit()
