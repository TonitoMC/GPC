import pygame
from pygame.locals import *
from gl import Renderer, LINES, POINTS, TRIANGLES
from model import Model
from shaders import *
from mathlib import Matrix


width = 960
height = 540

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader
rend.glLoadBackground("textures/test.bmp")


#Razenade
razenade = Model("models/razenade.obj")
razenade.LoadTexture("textures/razenade.bmp")
razenade.vertexShader = vertexShader
razenade.fragmentShader = pixelShader
razenade.translate[0] = 5
razenade.translate[1] = 2
razenade.translate[2] = -6.5
razenade.rotate[0] = -20
razenade.rotate[1] = 180
razenade.rotate[2] = -45
razenade.scale = [20,20,20]
rend.models.append(razenade)

# KJ Turret
kjturret = Model("models/turret.obj")
kjturret.LoadTexture("textures/turret.bmp")
kjturret.vertexShader = vertexShader
kjturret.fragmentShader = toonShaderBWWithStatic
kjturret.translate[0] = -4
kjturret.translate[1] = 0
kjturret.translate[2] = -6.5
kjturret.rotate[0] = 10
kjturret.rotate[1] = -30
kjturret.rotate[2] = -5
kjturret.scale = [1.5,1.5,1.5]
rend.models.append(kjturret)


reaver = Model("models/Melee_Reaver.obj")
reaver.LoadTexture("textures/Melee_Reaver.bmp")
reaver.vertexShader = vertexShader
reaver.fragmentShader = noiseShader
reaver.translate[0] = 3.75
reaver.translate[1] = 0.75
reaver.translate[2] = 4.5
reaver.rotate[0] += 40 # Rotate to match surface
reaver.rotate[1] += 20 #make it turn away from me
reaver.rotate[2] += 90 # Make it fully horizontal
reaver.scale = [4.75,4.75,4.75]
rend.models.append(reaver)

#TODO Fix reaver, looks weird
modelo3 = Model("models/keychain.obj")
modelo3.LoadTexture("textures/keychain.bmp")
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = fragmentShader
modelo3.translate[0] = -2
modelo3.translate[1] = -2.1
modelo3.translate[2] = 4
modelo3.rotate[0] += 0 # Rotate to match surface
modelo3.rotate[1] -= 90 #Turn to camera
modelo3.rotate[2] += 170 # Stand straight
modelo3.scale = [30,30,30]
rend.models.append(modelo3)

rend.primitiveType = LINES

isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
			elif event.key == pygame.K_1:
				rend.primitiveType = POINTS
				
			elif event.key == pygame.K_2:
				rend.primitiveType = LINES
				
			elif event.key == pygame.K_3:
				rend.primitiveType = TRIANGLES
				

			elif event.key == pygame.K_RIGHT:
				rend.camera.translate[0] += 1
			elif event.key == pygame.K_LEFT:
				rend.camera.translate[0] -= 1
			elif event.key == pygame.K_UP:
				rend.camera.translate[1] += 1
			elif event.key == pygame.K_DOWN:
				rend.camera.translate[1] -= 1
				
					
	rend.glClear()
	rend.glClearBackground()
	rend.glRender()


	pygame.display.flip()
	clock.tick(60)
	
rend.glGenerateFrameBuffer("renders/output.bmp")

pygame.quit()