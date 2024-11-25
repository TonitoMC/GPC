import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model
import glm

MAX_CAM_DISTANCE = 8
MIN_CAM_DISTANCE = 1.5
MAX_CAM_HEIGHT = 4
MIN_CAM_HEIGHT = -2.75

width = 600
height = 600

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen)

skyboxTextures = ["skybox/right.png",
                  "skybox/left.png",
                  "skybox/top.png",
                  "skybox/bottom.png",
                  "skybox/front.png",
                  "skybox/back.png"]

vshader = vertex_shader
fshader = fragment_shader

renderer.CreateSkybox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

camDistance = 5
camAngle = 0

renderer.SetShaders(vshader, fshader)

# Modelo de Dizzy (Gekko Flash)
gekkoFlash = Model('models/dizzy.obj', vshader, energy_shader)
gekkoFlash.AddTextures('textures/dizzy.bmp')
renderer.scene.append(gekkoFlash)
gekkoFlash.rotation.x -= 25
gekkoFlash.rotation.y = 180
gekkoFlash.rotation.z -= 25
gekkoFlash.scale = (0.0125, 0.0125, 0.0125)
gekkoFlash.translation.x = -3.5
gekkoFlash.translation.y = -0.25
gekkoFlash.translation.z = -14

dizzySound = pygame.mixer.Sound('audio/dizzy.ogg')

# Modelo de granada de Raze
nadeModel = Model('models/razenade.obj', bubble_shader, aberration_shader)
nadeModel.AddTextures('textures/razenade.bmp')
renderer.scene.append(nadeModel)
nadeModel.scale = (5, 5, 5)

nadeModel.rotation.x -= 25
nadeModel.rotation.y = 180
nadeModel.rotation.z -= 25
nadeModel.translation.x = -4.5
nadeModel.translation.y = -0.75
nadeModel.translation.z = -16

nadeSound = pygame.mixer.Sound('audio/nade.ogg')

# Modelo de Torreta de Killjoy
turretModel = Model('models/turret.obj', spring_shader, light_mouse_shader)
turretModel.AddTextures('textures/turret.bmp')
renderer.scene.append(turretModel)
turretModel.scale = (0.9, 0.9, 0.9)
turretModel.rotation.y -= 15
turretModel.translation.x = -6.6
turretModel.translation.y = -2
turretModel.translation.z = -15

# Piso
floor = Model('models/floor.obj', vshader, fshader)
floor.AddTextures('textures/floor2.bmp')
renderer.scene.append(floor)
floor.translation.x = -5
floor.translation.y = -3
floor.rotation.y += 180
floor.translation.z = -15
floor.scale = (3, 3, 3)

# Pared
wall = Model('models/floor.obj', vshader, fshader)
wall.AddTextures('textures/wall2.bmp')
renderer.scene.append(wall)
wall.translation.x = -5
wall.translation.y = 0
wall.translation.z = -18
wall.rotation.x -= 90
wall.scale = (3, 3, 3)

# Modelo de una Caja
crateModel = Model('models/box.obj', vshader, grayscale_shader)
crateModel.AddTextures('textures/crate.bmp')
renderer.scene.append(crateModel)
crateModel.scale = (0.5, 0.5, 0.5)
crateModel.rotation.y += 75
crateModel.translation.x = -6.5
crateModel.translation.y = -3
crateModel.translation.z = -15

turretSound = pygame.mixer.Sound('audio/turret.ogg')

orbittedModel = floor

isRunning = True

current_sound = None
isDragging = False

while isRunning:
    deltaTime = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_0:
                orbittedModel = floor
            elif event.key == pygame.K_1:
                orbittedModel = turretModel
                if current_sound:
                    current_sound.stop()
                turretSound.play()
                current_sound = turretSound
            elif event.key == pygame.K_2:
                orbittedModel = gekkoFlash
                if current_sound:
                    current_sound.stop()
                dizzySound.play()
                current_sound = dizzySound
            elif event.key == pygame.K_3:
                orbittedModel = nadeModel
                if current_sound:
                    current_sound.stop()
                nadeSound.play()
                current_sound = nadeSound
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                isDragging = True
                pygame.mouse.get_rel()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                isDragging = False

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
        if camDistance < MIN_CAM_DISTANCE:
            camDistance = MIN_CAM_DISTANCE

    if keys[K_DOWN]:
        camDistance += 2 * deltaTime
        if camDistance > MAX_CAM_DISTANCE:
            camDistance = MAX_CAM_DISTANCE

    if isDragging:
        rel = pygame.mouse.get_rel()
        camAngle -= rel[0] * deltaTime * 7.5
        newPos = renderer.camera.position.y + rel[1] * deltaTime * 1
        if newPos > MAX_CAM_HEIGHT:
            newPos = renderer.camera.position.y
        elif newPos < MIN_CAM_HEIGHT:
            newPos = renderer.camera.position.y
        else:
            renderer.camera.position.y = newPos

    mouse_x, mouse_y = pygame.mouse.get_pos()
    renderer.SetMousePos(mouse_x, mouse_y)
    renderer.time += deltaTime
    renderer.camera.LookAt(orbittedModel.translation)
    renderer.camera.Orbit(orbittedModel.translation, camDistance, camAngle)
    renderer.Render()
    pygame.display.flip()

pygame.quit()