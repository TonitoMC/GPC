

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import Material
from lights import *

width = 256
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)

# Nieve, no refleja mucha luz
snow = Material(diffuse = [1,1,1], spec = 16, Ks = 0.08)

# Zanahoria, refleja mucha luz por motivos demostrativos
carrot = Material(diffuse = [1,0.5,0], spec = 64, Ks = 0.1)

# Botones de carbon, poco especular
charcoal = Material(diffuse = [0.2,0.2,0.2], spec = 16, Ks = 0.1)

# Botones (de plastico? no he hecho un muñeco de nieve) reflejan bastante luz
button = Material(diffuse = [0.2,0.2,0.2], spec = 128, Ks = 0.2)

# Ojos que reflejan bastante
eyewhite = Material(diffuse = [1,1,1], spec = 64, Ks = 0.2)
eyeblack = Material(diffuse = [0.2,0.2,0.2], spec = 64, Ks = 0.2)


# Luz direccional y luz de ambiente
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
rt.scene.append( Sphere (position = (0.25, 1.2, -4.432), radius = 0.085, material = eyewhite))
# Black
rt.scene.append( Sphere (position = (0.25, 1.2, -4.375), radius = 0.05, material = eyeblack))


# Right Eye
# White
rt.scene.append( Sphere (position = (-0.25, 1.2, -4.432), radius = 0.085, material = eyewhite))
rt.scene.append( Sphere (position = (-0.25, 1.2, -4.375), radius = 0.05, material = eyeblack))

brick = Material(diffuse = [1,0.2,0.2], spec = 128, Ks = 0.25)
grass = Material(diffuse = [0.2,1.0,0.2], spec = 128, Ks = 0.2)


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