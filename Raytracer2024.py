

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import *
width = 800
height = 450

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/lot.bmp")
rt.glClearColor(0.5,0.0,0.0)
rt.glClear()


brick = Material(diffuse = [1.0,0.2,0.2], spec = 128, Ks = 0.25)
grass = Material(diffuse = [0.2,1.0,0.2], spec = 64, Ks = 0.2)

mirror = Material(diffuse = [0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse = [0.5, 0.5, 1.0], spec = 128, Ks = 0.2, matType = REFLECTIVE)
paint = Material(texture = Texture("textures/eee.bmp"))
glass = Material(spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT)

rt.lights.append( DirectionalLight(direction = [-1,-1,-1], intensity = 0.8))
rt.lights.append( AmbientLight(intensity = 0.1))

# Opacas - Izquierda
rt.scene.append( Sphere(position = [-2.5, -1.25, -5], radius = 1, material = paint))
rt.scene.append( Sphere(position = [-2.5, 1.25, -5], radius = 1, material = paint))

# Reflectivas - Centro
rt.scene.append( Sphere(position = [0, -1.25, -5], radius = 1, material = mirror))
rt.scene.append( Sphere(position = [0, 1.25, -5], radius = 1, material = mirror))

# Refractivas - Derecha
rt.scene.append( Sphere(position = [2.5, -1.25, -5], radius = 1, material = glass))
rt.scene.append( Sphere(position = [2.5, 1.25, -5], radius = 1, material = glass))

# Dos adicionales para mostrar Refraccion / Refleccion
rt.scene.append( Sphere(position = [2.5, 0, -7.5], radius = 0.5, material = paint))
rt.scene.append( Sphere(position = [0, 0, -2.5], radius = 0.25, material = paint))


rt.glRender()


isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				rt.glGenerateFrameBuffer('renders/output.bmp')
				
	pygame.display.flip()
	clock.tick(60)
	
pygame.quit()