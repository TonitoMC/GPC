import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import *
width = 500
height = 500

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("textures/MOP.bmp")
rt.glClearColor(0.5, 0.0, 0.0)
rt.glClear()

# Materiales

# Mirror, material reflectivo simple
mirror = Material(diffuse=[0.9, 0.9, 0.9], spec=128, Ks=0.2, matType=REFLECTIVE)

# Material de las cruces, blanco solido
whiteSolid = Material(spec=16, Ks=0.1, matType=OPAQUE, texture=Texture("textures/conc.bmp"))

# Material para el casco militar
military = Material(diffuse=[0.9, 0.9, 0.9], spec=128, Ks=0.2, matType=OPAQUE, texture =Texture("textures/military.bmp"))

# Material para el piso, carga una textura de grama obscura
grass = Material(diffuse = [1,1,1], spec = 16, Ks = 0.1, matType = OPAQUE, texture = Texture("textures/grasss.bmp"))

# Ladrillos para la piramide
brick = Material(spec=16, Ks=0.08, matType=OPAQUE, texture=Texture("textures/brick2.bmp"))

# Textura de pavimento / concreto para las cruces
pavement = Material(diffuse=[0.9, 0.9, 0.9], spec=16, Ks=0.1, matType=OPAQUE)


# Luces de la escena

# Luz direccional apuntando en diagonal hacia delante / izquierda / abajo
rt.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity=0.7))

# Luz direccional apuntando en diagonal hacia delante / derecha / abajo
rt.lights.append(DirectionalLight(direction=[1, -1, -1], intensity=0.8))

# Luz ambiental para iluminar la escena
rt.lights.append(AmbientLight(intensity=0.3))

# Spotlight sobre la cruz izquierda de color rojo para hacer mas interesante la escena, baja intensidad
rt.lights.append( SpotLight(position = [-3, 2.25, -8.5], color = [1, 0, 0], innerAngle = 30, outerAngle = 40, direction = [0, -1, 0], intensity = 3))

# Spotlight sobre la cruz derecha de color amarillo para hacer mas interesante la escena, baja intensidad
rt.lights.append( SpotLight(position = [3, 2.25, -8.5], color = [1, 1, 0], innerAngle = 30, outerAngle = 40, direction = [0, -1, 0], intensity = 3))

# Objetos

#Piramide a lo lejos
rt.scene.append( Pyramid(base_center = [0, -3.5, -100], base_size = 30, height = 20, material = brick))

# Piso, un plano hecho de grama
rt.scene.append( Plane(position = [0, -3.5, -7.5], normal = [0,1,0], material = grass, texture_scale = (0.5,0.5)))

# Fila de mas hacia la izquierda de cruces
rt.scene.append( Cross(position = [-6, -3.5, -8.5], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [-6, -3.5, -17], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [-6, -3.5, -25.5], block_size = 0.75, material = whiteSolid))

# Fila medio-izquierda de las cruces
rt.scene.append(HalfSphere(position = [-3.75, -1.625, -8.5], radius = 0.7, material = military)) # Casco colgando de la primera cruz
rt.scene.append( Cross(position = [-3, -3.5, -8.5], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [-3, -3.5, -17], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [-3, -3.5, -25.5], block_size = 0.75, material = whiteSolid))

# Fila del centro
rt.scene.append(Cylinder(position=[0, -3.5, -8.5], radius=1.25, height = 1.5, material=mirror))
rt.scene.append( Cross(position = [0, -3.5, -17], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [0, -3.5, -25.5], block_size = 0.75, material = whiteSolid))

# Fila de Centro-Derecha
rt.scene.append( Cross(position = [3, -3.5, -8.5], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [3, -3.5, -17], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [3, -3.5, -25.5], block_size = 0.75, material = whiteSolid))

# Fila mas hacia la derecha
rt.scene.append( Cross(position = [6, -3.5, -8.5], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [6, -3.5, -17], block_size = 0.75, material = whiteSolid))
rt.scene.append( Cross(position = [6, -3.5, -25.5], block_size = 0.75, material = whiteSolid))

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