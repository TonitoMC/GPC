import struct
from camera import Camera
from src.mathlib import Matrix
from math import tan, pi


def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    # 2 bytes
    return struct.pack("=h", w)


def dword(d):
    # 4 bytes
    return struct.pack("=l", d)


POINTS = 0
LINES = 1
TRIANGLES = 2


class Renderer(object):
    def __init__(self, screen):
        self.projectionMatrix = None
        self.screen = screen
        # No se toman las primeras dos, el screen.get_rect nos da las posiciones de origen y unicamente queremos
        # width + height
        _, _, self.width, self.height = screen.get_rect()
        self.count = 0

        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

        self.primitiveType = POINTS

        self.vertexShader = None
        self.models = []

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = width
        self.vpHeight = height

        self.viewportMatrix = Matrix([[width / 2, 0, 0, x + width / 2],
                                      [0, height / 2, 0, y + height / 2],
                                      [0, 0, 0.5, 0.5],
                                      [0, 0, 0, 1]])

    def glProjection(self, n=0.1, f=1000, fov=60):
        aspectRatio = self.vpWidth / self.vpHeight
        fov *= pi / 180
        t = tan(fov / 2) * n
        r = t * aspectRatio

        self.projectionMatrix = Matrix([[n / r, 0, 0, 0],
                                        [0, n / t, 0, 0],
                                        [0, 0, -(f + n) / (f - n), -(2 * f * n) / (f - n)],
                                        [0, 0, -1, 0]])

    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2],
                                   color[1],
                                   color[0]])
                    file.write(color)

    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [r, g, b]

    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r, g, b]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]

    # Pygame dibuja desde superior izquierda
    def glPoint(self, x, y, color=None):
        # Pygame recibe colores de 0 a 255
        if (0 <= x < self.width and (0 <= y < self.height)):
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    # Dibuja poligonos con relleno
    def glFill(self, listaPuntos, color):
        # Dibuja las lineas del poligono
        for i in range(len(listaPuntos)):
            self.glLine(listaPuntos[i], listaPuntos[(i + 1) % len(listaPuntos)], color)

        # Encuentra las coordenadas X y Y
        coords_x = [coord[0] for coord in listaPuntos]
        coords_y = [coord[1] for coord in listaPuntos]

        # Encuentra los minimos y maximos en X y Y para crear el "Boundry Box"
        min_x = min(coords_x)
        max_x = max(coords_x)
        min_y = min(coords_y)
        max_y = max(coords_y)

        # Se recorre todo el "Boundry Box" y se determina si el punto se encuentra dentro, se colorea en caso de estarlo
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if self.pointInPolygon(listaPuntos, j, i):
                    self.glPoint(j, i, color)

    # Determina si un punto se encuentra dentro de un poligono, Raycasting
    def pointInPolygon(self, listaPuntos, x, y):
        # Se inicializan las condiciones iniciales
        n = len(listaPuntos)
        inside = False
        x1, y1 = listaPuntos[0]
        # Se recorre la lista de manera que se regrese al primer punto (para cerrar el poligono)
        for i in range(n + 1):
            x2, y2 = listaPuntos[i % n]
            # Se verifica que se encuentre entre las coordenadas Y de los puntos  del edge
            if min(y1, y2) < y <= max(y1, y2):
                # Se verifica que X no se encuentre mas alla del eje
                if x <= max(x1, x2):
                    # Se calcula el intercepto en X
                    if y1 != y2:
                        interx = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    # Si X se encuentra antes que el intercepto, se invierte "inside"
                    if x1 == x2 or x <= interx:
                        inside = not inside
            # Se actualizan las variables para continuar el ciclo
            x1, y1 = x2, y2
        return inside

    def glLine(self, v0, v1, color=None):
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Algoritmo de Lineas de Bresenham

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x1 < x0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1

    def getPixelColor(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.frameBuffer[x][y]
        return None

    def glRender(self):
        for model in self.models:
            mMat = model.GetModelMatrix()

            vertexBuffer = []

            for face in model.faces:
                vertCount = len(face)

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]
                print(self.projectionMatrix)
                print(self.viewportMatrix)
                print(self.camera.GetViewMatrix())
                print(self.count)
                self.count += 1
                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix=mMat, viewMatrix=self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    v1 = self.vertexShader(v1, modelMatrix=mMat, viewMatrix=self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    v2 = self.vertexShader(v2, modelMatrix=mMat, viewMatrix=self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)
                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix=mMat, viewMatrix=self.camera.GetViewMatrix(), projectionMatrix = self.projectionMatrix, viewportMatrix = self.viewportMatrix)

                vertexBuffer.append(v0)
                vertexBuffer.append(v1)
                vertexBuffer.append(v2)
                if vertCount == 4:
                    vertexBuffer.append(v0)
                    vertexBuffer.append(v2)
                    vertexBuffer.append(v3)

            self.glDrawPrimitives(vertexBuffer)

    def glDrawPrimitives(self, buffer):
        if self.primitiveType == POINTS:
            for point in buffer:
                print(point)
                self.glPoint(int(point[0]), int(point[1]))

        elif self.primitiveType == LINES:
            for i in range(0, len(buffer), 3):
                p0 = buffer[i]
                p1 = buffer[i + 1]
                p2 = buffer[i + 2]

                self.glLine((p0[0], p0[1]), (p1[0], p1[1]))
                self.glLine((p1[0], p1[1]), (p2[0], p2[1]))
                self.glLine((p2[0], p2[1]), (p0[0], p0[1]))
