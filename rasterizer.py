import pygame
from pygame.locals import *
from gl import Renderer, LINES, POINTS
from model import Model
from shaders import *
from mathlib import Matrix


width = 960
height = 512

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader


modelo1 = Model("models/Melee_Reaver.obj")
modelo1.LoadTexture("textures/Melee_Reaver.bmp")
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = toonShaderBWWithStatic
modelo1.translate[0] = -1
modelo1.translate[1] = -0.6
modelo1.translate[2] = 2
modelo1.scale = [3.5,3.5,3.5]
rend.models.append(modelo1)

modelo2 = Model("models/Melee_Reaver.obj")
modelo2.LoadTexture("textures/Melee_Reaver.bmp")
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = noiseShader
modelo2.translate[0] = 0
modelo2.translate[1] = -0.6
modelo2.translate[2] = 2
modelo2.scale = [3.5,3.5,3.5]
rend.models.append(modelo2)

modelo3 = Model("models/Melee_Reaver.obj")
modelo3.LoadTexture("textures/Melee_Reaver.bmp")
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = pixelShader
modelo3.translate[0] = 1
modelo3.translate[1] = -0.6
modelo3.translate[2] = 2
modelo3.scale = [3.5,3.5,3.5]
rend.models.append(modelo3)


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
	rend.glRender()


	pygame.display.flip()
	clock.tick(60)
	
rend.glGenerateFrameBuffer("renders/output.bmp")

pygame.quit()