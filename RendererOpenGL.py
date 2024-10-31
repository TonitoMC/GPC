import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

width = 600
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen)

vshader = vertex_shader
fshader = fragment_shader

renderer.SetShaders(vshader, fshader)

nadeModel = Model('models/razenade.obj')
nadeModel.AddTextures('textures/razenade.bmp')
renderer.scene.append(nadeModel)
nadeModel.rotation.y = 180
nadeModel.scale = (15,15,15)
nadeModel.translation.z = -4
isRunning = True

while isRunning:
	deltaTime = clock.tick(60) / 1000
	keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
			elif event.key == pygame.K_1:
				vshader = vertex_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_2:
				vshader = breathing_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_3:
				vshader = spring_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_4:
				vshader = bubble_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_5:
				fshader = fragment_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_6:
				fshader = aberration_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_7:
				fshader = grayscale_shader
				renderer.SetShaders(vshader, fshader)
			elif event.key == pygame.K_8:
				fshader = light_mouse_shader
				renderer.SetShaders(vshader, fshader)

	if keys[K_LEFT]:
		nadeModel.rotation.y -= 45 * deltaTime

	elif keys[K_RIGHT]:
		nadeModel.rotation.y += 45 * deltaTime

	elif keys[K_a]:
		renderer.camera.position.x -= 1 * deltaTime
	elif keys[K_d]:
		renderer.camera.position.x += 1 * deltaTime
	elif keys[K_s]:
		renderer.camera.position.y -= 1 * deltaTime
	elif keys[K_w]:
		renderer.camera.position.y += 1 * deltaTime
	mouse_x, mouse_y = pygame.mouse.get_pos()
	renderer.SetMousePos(mouse_x, mouse_y)
	renderer.time += deltaTime
	renderer.Render()
	pygame.display.flip()

pygame.quit()