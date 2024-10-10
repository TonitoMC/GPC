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
rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Materials
mirror = Material(diffuse=[0.9, 0.9, 0.9], spec=128, Ks=0.2, matType=REFLECTIVE)
blueMirror = Material(diffuse=[0.5, 0.5, 1.0], spec=128, Ks=0.2, matType=REFLECTIVE)
paint = Material(texture=Texture("textures/eee.bmp"))
glass = Material(spec=128, Ks=0.2, ior=1.5, matType=TRANSPARENT)

brick = Material(spec=16, Ks=0.08, matType=OPAQUE, texture=Texture("textures/brick2.bmp"))
pavement = Material(spec=16, Ks=0.1, matType=OPAQUE, texture=Texture("textures/pavement.bmp"))

ice = Material(spec=128, Ks=0.2, matType=REFLECTIVE, texture=Texture("textures/ice.bmp"))
marble = Material(spec=64, Ks=0.25, matType=REFLECTIVE, texture=Texture("textures/marble.bmp"))

water = Material(spec=64, Ks=0.2, ior=1.5, matType=TRANSPARENT, texture=Texture("textures/watwat.bmp"))
shine = Material(diffuse=[1, 1, 1], spec=64, Ks=0.2, ior=1.8, matType=TRANSPARENT, texture=Texture("textures/shine.bmp"))

# Lights
rt.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity=0.8))
rt.lights.append(AmbientLight(intensity=0.1))

# Opaque Triangle
rt.scene.append(Triangle( v0 = [-4.5, 0, -5],v1 = [-4.5, -2, -5], v2 = [-2.5, 0, -5], material = brick))

# Reflective Triangle
rt.scene.append(Triangle( v0 = [-1, 0, -5],v1 = [-1, -2, -5], v2 = [1, 0, -5], material = mirror))

# Refractive Triangle
rt.scene.append(Triangle( v0 = [2.5, 0, -5],v1 = [2.5, -2, -5], v2 = [4.5, 0, -5], material = glass))

# Opaque Cylinder
rt.scene.append(Cylinder(position=[-2.5, 1.25, -5], radius=1, height = 0.5, material=brick))

# Reflective Cylinder
rt.scene.append(Cylinder(position=[0, 1.25, -5], radius=1, height = 0.5, material=mirror))

# Behind Refractive Cylinder for Demonstration
rt.scene.append(Cylinder(position=[2.5, 1.25, -7.5], radius=1, height = 1, material=brick))


# Refractive Cylinder
rt.scene.append(Cylinder(position=[2.5, 1, -5], radius=1, height = 1.5, material=glass))


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