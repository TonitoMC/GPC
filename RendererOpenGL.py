import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

MAX_CAM_DISTANCE = 8
MIN_CAM_DISTANCE = 1.5
MAX_CAM_HEIGHT = 4
MIN_CAM_HEIGHT = -4

width = 600
height = 600

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen)

skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

vshader = vertex_shader
fshader = fragment_shader

renderer.CreateSkybox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

camDistance = 5
camAngle = 0

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

	if keys[K_RIGHT]:
		nadeModel.rotation.y += 45 * deltaTime

	if keys[K_a]:
		camAngle -= 45 * deltaTime

	if keys[K_d]:
		camAngle += 45 * deltaTime

	if keys[K_w]:
		newPos = renderer.camera.position.y + 2 * deltaTime
		if newPos > MAX_CAM_HEIGHT:
			newPos = renderer.camera.position.y
		renderer.camera.position.y = newPos

	if keys[K_s]:
		newPos = renderer.camera.position.y - 2 * deltaTime
		if newPos < MIN_CAM_HEIGHT:
			newPos = renderer.camera.position.y
		renderer.camera.position.y = newPos
	if keys[K_UP]:
		camDistance -= 2 * deltaTime
		if camDistance  < MIN_CAM_DISTANCE:
			camDistance = MIN_CAM_DISTANCE

	if keys[K_DOWN]:
		camDistance += 2 * deltaTime
		if camDistance > MAX_CAM_DISTANCE:
			camDistance = MAX_CAM_DISTANCE

	mouse_x, mouse_y = pygame.mouse.get_pos()
	renderer.SetMousePos(mouse_x, mouse_y)
	renderer.time += deltaTime
	renderer.camera.LookAt(nadeModel.translation)
	renderer.camera.Orbit(nadeModel.translation, camDistance, camAngle)
	renderer.Render()
	pygame.display.flip()

pygame.quit()