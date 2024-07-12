import pygame
from pygame.locals import *
from gl import Renderer

#Variables de dimensiones de la pantalla
width = 960
height = 540
#Inicializa la pantalla de Pygame
screen = pygame.display.set_mode((width,height))

#Refresh rate / FPS
clock = pygame.time.Clock()

#Loop donde todo va a estar corriendo
isRunning = True

rend = Renderer(screen)

rend.glColor(1,0,1)
rend.glClearColor(0,0,0)

def poligono(listaPuntos):
    for i in range(len(listaPuntos)):
        rend.glLine(listaPuntos[i],listaPuntos[(i + 1)%len(listaPuntos)], (1,1,1))

pol1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360),
        (250, 380), (220, 385), (205, 410), (193, 383)]

pol2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

pol3 = [(377, 249), (411, 197), (436, 249)]

pol4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192),
        (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rend.glGenerateFrameBuffer('bitmap.bmp')
                isRunning = False
    pygame.display.flip()
    clock.tick(60)
    rend.glClear()
    #rend.glFill(pol1, (1,1,1))
    rend.glFill(pol2, (1,1,1))
    rend.glFill(pol3, (1,1,1))
    #rend.glFill(pol4, (1,1,1))
    #poligono(pol1)
    #poligono(pol2)
    #poligono(pol3)
    #poligono(pol4)

    #for x in range(0, width, 10):
    #   rend.glLine(punto0,(x, height), (0,0,0))
    #for x in range(0, width, 10):
    #    rend.glLine(punto0, (x, 0), (0,0,0))
    #for x in range (0, height, 10):
    #    rend.glLine(punto0, (0,x), (0,0,0))
    #for x in range (0, height, 10):
    #    rend.glLine(punto0, (width, x), (0, 0, 0))
pygame.quit()