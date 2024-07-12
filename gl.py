import struct

def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    # 2 bytes
    return struct.pack("=h", w)

def dword(d):
    # 4 bytes
    return struct.pack("=l", d)



class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        # No se toman las primeras dos, el screen.get_rect nos da las posiciones de origen y unicamente queremos width + height
        _, _, self.width, self.height = screen.get_rect()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

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

    #Implementacion de scanline
    def glFill(self, listaPuntos, color):
        listaPuntosConEdges = [p for p in listaPuntos]
        #Dibuja el poligono
        for i in range(len(listaPuntos)):
            listaPuntosConEdges += [
                punto for punto in self.glLineWithPoints(listaPuntos[i], listaPuntos[(i + 1) % len(listaPuntos)], color)
                if punto not in listaPuntosConEdges
            ]
        #Encuentra las coordenadas
        coords_x = [coord[0] for coord in listaPuntosConEdges]
        coords_y = [coord[1] for coord in listaPuntosConEdges]

        min_x = min(coords_x)
        max_x = max(coords_x)
        min_y = min(coords_y)
        max_y = max(coords_y)
        #Recorre las lineas en Y una por una, no se llena la linea de "tope" ni la linea de hasta abajo
        for y in range(min_y + 1, max_y):
            #Crea una lista ordenada por los valores de X de las coordenadas con la misma coordenada y
            validCoords = [coord for coord in listaPuntosConEdges if coord[1] == y]
            sortedCoords = sorted(validCoords, key=lambda x: x[0])

            #Verifica que tenga mas de un elemento
            if len(sortedCoords) < 2:
                continue

            #Recorre para eliminar elementos con un valor de X consecutivo (Lineas horizontales)
            x = 1
            while x < len(sortedCoords):
                if sortedCoords[x][0] == sortedCoords[x - 1][0] + 1:
                    sortedCoords.pop(x - 1)
                else:
                    x += 1
            #Rellena el poligono dibujando lineas
            for p in range(0, len(sortedCoords) - 1, 2):
                self.glLine(sortedCoords[p], sortedCoords[p + 1], color)

    #glLine pero retorna una lista de tuplas con los puntos que dibujo
    def glLineWithPoints(self, v0, v1, color):
        points = []
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Algoritmo de Lineas de Bresenham

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, color)

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
                points.append((y,x))
            else:
                self.glPoint(x, y, color or self.currColor)
                points.append((x,y))
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1
        return points

    def glLine(self, v0, v1, color):
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Algoritmo de Lineas de Bresenham

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, color)

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

