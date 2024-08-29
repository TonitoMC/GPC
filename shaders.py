
import numpy as np
import math
import noise
import random
from mathlib import *
from texture import Texture

#Shaders del Lab

def toonShaderBWWithStatic(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2] ]
    
    r = 1
    g = 1
    b = 1

    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
            u * vtA[1] + v * vtB[1] + w * vtC[1] ]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    
    intensity = dot_product(normal, [-x for x in dirLight] )
    intensity = max(0, intensity)
    # Toon shading
    if intensity < 0.33:
        intensity = 0.3
    elif intensity < 0.66:
        intensity = 0.6
    else:
        intensity = 1.0

    r *= intensity
    g *= intensity
    b *= intensity

    # Se pasa a blanco y negro
    grayscale = (r + g + b) / 3

    # Agrega ruido y estatica
    staticStrength = 0.05
    noise = (random.random() - 0.5) * staticStrength
    dotProbability = 0.05 
    if random.random() < dotProbability:
        grayscale = 0.2 
    grayscale += noise
    grayscale = min(1,max(0,grayscale))
    
    return [grayscale, grayscale, grayscale]

def noiseShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    r = 1
    g = 1
    b = 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Crea ruido con los parametros y perturba las coordenadas de textura
    frequency = 15
    amplitude = 0.025

    perturbed_vtP = [
        vtP[0] + noise.pnoise2(vtP[0] * frequency, vtP[1] * frequency) * amplitude,
        vtP[1] + noise.pnoise2(vtP[1] * frequency, vtP[0] * frequency) * amplitude
    ]

    noise_value = noise.pnoise2(perturbed_vtP[0] * frequency, perturbed_vtP[1] * frequency)

    noise_value = (noise_value + 1) / 2
    # Aplica ruido a los colores
    if texture:
        texColor = texture.getColor(perturbed_vtP[0], perturbed_vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    r *= noise_value ** 0.5
    g *= noise_value ** 0.5
    b *= noise_value ** 0.5

    return (r, g, b)

def pixelShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    # Sabiendo que las coordenadas de textura
    # estan en la 4ta y 5ta posicion de cada
    # indice del vertice, los obtenemos
    # y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # Sabiendo que los valores de las normales
    # estan en la 6ta, 7ma y 8va posicion
    # de cada vertice, lkos obtenemos y guardamos

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    pixelSize = 0.01
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Fuerza a que las coordenadas de textura sean multiplos de pixelSize
    vtP[0] = (vtP[0] // pixelSize) * pixelSize
    vtP[1] = (vtP[1] // pixelSize) * pixelSize
    r = 1
    g = 1
    b = 1
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    
    return [r, g, b]

def onFireShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    onFireTexture = kwargs["onFireTexture"]

    # Interpolating texture coordinates
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    vtP = [
        u * vtA[0] + v * vtB[0] + w * vtC[0],
        u * vtA[1] + v * vtB[1] + w * vtC[1]
    ]

    # Calculate the color from the base texture
    if texture:
        baseColor = texture.getColor(vtP[0], vtP[1])
        r, g, b = baseColor[0], baseColor[1], baseColor[2]
    else:
        r, g, b = 1, 1, 1

    # Calculate the color from the "on fire" texture
    if onFireTexture:
        fireColor = onFireTexture.getColor(vtP[0], vtP[1])
        r2, g2, b2 = fireColor[0], fireColor[1], fireColor[2]
    else:
        r2, g2, b2 = 1, 1, 1

    # Blend the base texture with the "on fire" texture
    blendFactor = 0.5  # Adjust this to control the blending
    finalColor = [
        blendFactor * r + (1 - blendFactor) * r2,
        blendFactor * g + (1 - blendFactor) * g2,
        blendFactor * b + (1 - blendFactor) * b2
    ]

    return [min(1, finalColor[0]), min(1, finalColor[1]), min(1, finalColor[2])]



# Shaders de Clase
def vertexShader(vertex, **kwargs):
    # Se lleva a cabo por cada vertice
    
    # Recibimos las matrices
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    
    # Agregamos un componente W al vertice
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    # Transformamos el vertices por todas las matrices en el orden correcto
    vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix * vt
    
    
    # Dividimos x,y,z por w para regresar el vertices a un tama�o de 3
    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]
    
    return vt

def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    # Sabiendo que las coordenadas de textura
    # estan en la 4ta y 5ta posicion de cada
    # indice del vertice, los obtenemos
    # y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    # Sabiendo que los valores de las normales
    # estan en la 6ta, 7ma y 8va posicion
    # de cada vertice, lkos obtenemos y guardamos

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1

      # P = uA + vB + wC
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    # Se regresa el color
    return [r,g,b]

def unlitShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    # Sabiendo que las coordenadas de textura
    # estan en la 4ta y 5t posicion de cada 
    # indice del vertice, los obtenemos y
    # y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1

    # P = uA + vB + wC
    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
            u * vtA[1] + v * vtB[1] + w * vtC[1] ]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # Se regresa el color
    return [r,g,b]
def gouradShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = [0,0,-1]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2] ]
    
    r = 1
    g = 1
    b = 1

    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
            u * vtA[1] + v * vtB[1] + w * vtC[1] ]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    intensity = dot_product(normal, [-x for x in dirLight] )
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r,g,b]


def flatShader(**kwargs):
    
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]
    
    normal = [  (nA[0] + nB[0] + nC[0]) / 3,
                (nA[1] + nB[1] + nC[1]) / 3,
                (nA[2] + nB[2] + nC[2]) / 3]



    
    r = 1
    g = 1
    b = 1

    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
            u * vtA[1] + v * vtB[1] + w * vtC[1] ]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
        
    # intensity = normal DOT -dirlight
    intensity = dot_product(normal, [-x for x in dirLight] )
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
    
    # Se regresa el color
    return [r,g,b]

    