

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import *
width = 512
height = 512

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

rt.lights.append( AmbientLight(intensity = 0.3))
rt.lights.append( SpotLight(position = [-1, 5.5,-7.5], direction = [0,-1,0], intensity = 10))
rt.lights.append( PointLight(position = [4.99, 5.99,-5], intensity = 10))

# Disk on floor
rt.scene.append( Disk(position = [2, 2, -7.5], normal = [-1,-1,1], radius = 1.5,  material = mirror))

# Brick cube
rt.scene.append( AABB(position = [-1.5,-2.25,-7.5], sizes = [1.5,1.5,1.5], material = brick2))

#Pavement Cube
rt.scene.append( AABB(position = [1.5,-2.25,-7.5], sizes = [1,1,1], material = pavement))

# Wool Mat / Disk
rt.scene.append( Disk(position = [1.5, -2.7499, -7.5], normal = [0,1,0], radius = 1.5, material = wool))

# Floor
rt.scene.append( Plane(position = [0, -2.75, -7.5], normal = [0,1,0], material = floor, texture_scale = (0.5,0.5)))

# Ceiling
rt.scene.append( Plane(position = [0, 6, -7.5], normal = [0,-1,0], material = pavement, texture_scale = (0.2,0.2)))

# Back wall
rt.scene.append( Plane(position = [0, -2.75, -15], normal = [0,0,1], material = pavement, texture_scale = (0.2,0.2)))

# Wall behind
rt.scene.append( Plane(position = [0, -2.75, 2], normal = [0,0,-1], material = brick2, texture_scale = (0.2,0.2)))

# Left wall
rt.scene.append( Plane(position = [-5, -2.75, -15], normal = [1,0,0], material = pavement, texture_scale = (0.2,0.2)))

# Right wall
rt.scene.append( Plane(position = [5, -2.75, -15], normal = [-1,0,0], material = pavement, texture_scale = (0.2,0.2)))

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