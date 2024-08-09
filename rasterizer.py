import pygame
from pygame.locals import *
from gl import Renderer, LINES, POINTS
from model import Model
from shaders import vertexShader, fragmentShader
from mathlib import Matrix


width = 512
height = 512

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader


modelo1 = Model("models/razenade.obj")
modelo1.LoadTexture("textures/razenade.bmp")
modelo1.translate[2] = -5
modelo1.rotate[1] = 180
modelo1.scale = [20,20,20]
rend.models.append(modelo1)


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