

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

brick = Material(diffuse = [1.0,1.0,1.0], spec = 128, Ks = 0.25)
grass = Material(diffuse = [0.2,1.0,0.2], spec = 64, Ks = 0.2)
mirror = Material(diffuse = [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
pavement = Material(spec = 16, Ks = 0.1, matType = OPAQUE, texture = Texture("textures/conc.bmp"))
floor = Material(diffuse = [1,1,1], spec = 16, Ks = 0.1, matType = REFLECTIVE, texture = Texture("textures/floor.bmp"))
wool = Material(spec = 64, Ks = 0.2, ior = 1.5, matType = OPAQUE, texture = Texture("textures/wool.bmp"))
brick2 = Material(spec = 16, Ks = 0.08, matType = OPAQUE, texture = Texture("textures/brick2.bmp"))
glass = Material(spec = 128, Ks = 0.2, ior = 1.5, matType = TRANSPARENT)

rt.lights.append( AmbientLight(intensity = 0.3))
rt.lights.append( DirectionalLight(direction = [-1,-1,-1], intensity = 0.8))
#rt.scene.append( Plane(position = [0, -2.25, -7.5], normal = [0,1,0], material = brick2))
marble = Material(spec = 64, Ks = 0.25, matType = REFLECTIVE, texture = Texture("textures/marble.bmp"))

#rt.scene.append( Triangle(v0 = [0,-2.25,-7.5], v1 = [-1, -2.25, -7.5], v2 = [-0.5, 0, -7.5], material=mirror))
#rt.scene.append( Sphere(position = [0, 1.25, -5], radius = 1, material = marble))

# Left Pyramid (Opaque)
rt.scene.append( Pyramid(base_center = [-2.5,0.25,-5], base_size = 2, height = 2, material=brick2))

#Middle Pyramid (Reflective)
rt.scene.append( Pyramid(base_center = [0,0.25,-5], base_size = 2, height = 2, material=mirror))

#Right Pyramid (Refractive)
#rt.scene.append( Pyramid(base_center = [2.5,0.25,-5], base_size = 2, height = 2, material=glass))


# rt.scene.append( Sphere(position = [-2.5,1.25,-5], radius = 1, material=brick2))

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