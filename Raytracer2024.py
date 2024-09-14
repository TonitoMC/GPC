

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import Material
from lights import *

width = 512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)

brick = Material(diffuse = [1,0.2,0.2], spec = 32, Ks = 0.75)
grass = Material(diffuse = [0.2,1.0,0.2], spec = 32, Ks = 0.75)
snow = Material(diffuse = [1,1,1], spec = 2, Ks = 0.01)
carrot = Material(diffuse = [1,0.5,0], spec = 128, Ks = 0.75)
charcoal = Material(diffuse = [0.2,0.2,0.2], spec = 2, Ks = 0.01)
button = Material(diffuse = [0.2,0.2,0.2], spec = 128, Ks = 0.75)
eyewhite = Material(diffuse = [1,1,1], spec = 128, Ks = 0.75)
eyeblack = Material(diffuse = [0.2,0.2,0.2], spec = 128, Ks = 0.75)



rt.lights.append( DirectionalLight(direction = [-1,-1,-1]))
rt.lights.append( AmbientLight(intensity = 0.2))

# Bottom Snowball
rt.scene.append( Sphere(position = [0,-1.5,-5], radius = 1, material = snow))

# Bottom button

rt.scene.append( Sphere(position = [0, -1.15, -4], radius = 0.2, material = charcoal))

# Mid Button

rt.scene.append( Sphere(position = [0, -0.65, -4.3], radius = 0.2, material = charcoal))

# Middle Snowball
rt.scene.append( Sphere(position = (0, 0, -5), radius = 0.85, material = snow))

# Top Button
rt.scene.append( Sphere(position = [0, 0.15, -4.2], radius = 0.2, material = charcoal))

# Left 1

# Head
rt.scene.append( Sphere(position = (0, 1.1, -5), radius = 0.65, material = snow))
#Mouth

# R1
rt.scene.append( Sphere (position = (-0.1, 0.8, -4.435), radius = 0.055, material = button))

#2
rt.scene.append( Sphere (position = (-0.25, 0.9, -4.44), radius = 0.055, material = button))

# L1
rt.scene.append( Sphere (position = (0.1, 0.8, -4.435), radius = 0.055, material = button))

#L2
rt.scene.append( Sphere (position = (0.25, 0.9, -4.44), radius = 0.055, material = button))

# Nose
rt.scene.append(Sphere(position = (0, 1.05, -4.5), radius = 0.2, material = carrot))
# Left Eye
# White
rt.scene.append( Sphere (position = (0.25, 1.2, -4.4325), radius = 0.075, material = eyewhite))
# Black
rt.scene.append( Sphere (position = (0.25, 1.2, -4.4), radius = 0.05, material = eyeblack))


# Right Eye
# White
rt.scene.append( Sphere (position = (-0.25, 1.2, -4.4325), radius = 0.085, material = eyewhite))
rt.scene.append( Sphere (position = (-0.25, 1.2, -4.4), radius = 0.05, material = eyeblack))


rt.glRender()




isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
	pygame.display.flip()
	clock.tick(60)
	
pygame.quit()