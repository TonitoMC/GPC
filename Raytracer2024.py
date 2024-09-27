

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import *
width = 400
height = 225

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/lot.bmp")
rt.glClearColor(0.5,0.0,0.0)
rt.glClear()

# brick = Material(diffuse = [1.0,0.2,0.2], spec = 128, Ks = 0.25)
# grass = Material(diffuse = [0.2,1.0,0.2], spec = 64, Ks = 0.2)

mirror = Material(diffuse = [0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse = [0.5, 0.5, 1.0], spec = 128, Ks = 0.2, matType = REFLECTIVE)
paint = Material(texture = Texture("textures/eee.bmp"))
glass = Material(spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT)

rt.lights.append( DirectionalLight(direction = [-1,-1,-1], intensity = 0.8))
rt.lights.append( AmbientLight(intensity = 0.1))

brick = Material(spec = 128, Ks = 0.25, matType = OPAQUE, texture = Texture("textures/brick2.bmp"))
pavement = Material(spec = 128, Ks = 0.25, matType = OPAQUE, texture = Texture("textures/pavement.bmp"))

ice = Material(spec = 128, Ks = 0.2, matType = REFLECTIVE, texture = Texture("textures/ice.bmp"))
marble = Material(spec = 128, Ks = 0.2, matType = REFLECTIVE, texture = Texture("textures/marble.bmp"))

water = Material(spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT, texture = Texture("textures/watersimple.bmp"))
shine = Material(spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT, texture = Texture("textures/shine.bmp"))


# Opacas - Izquierda
rt.scene.append( Sphere(position = [-2.5, -1.25, -5], radius = 1, material = brick))
rt.scene.append( Sphere(position = [-2.5, 1.25, -5], radius = 1, material = pavement))

# Reflectivas - Centro
rt.scene.append( Sphere(position = [0, -1.25, -5], radius = 1, material = ice))
rt.scene.append( Sphere(position = [0, 1.25, -5], radius = 1, material = marble))

# Refractivas - Derecha
rt.scene.append( Sphere(position = [2.5, -1.25, -5], radius = 1, material = shine))
rt.scene.append( Sphere(position = [2.5, 1.25, -5], radius = 1, material = water))

# Dos adicionales para mostrar Refraccion / Refleccion
rt.scene.append( Sphere(position = [2.5, -1.25, -7.5], radius = 0.5, material = paint))


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