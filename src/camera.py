
from src.mathlib import *


class Camera(object):
    def __init__(self):
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

    def GetViewMatrix(self):
        translateMat = TranslationMatrix(self.translate[0],
                                         self.translate[1],
                                         self.translate[2])

        rotateMat = RotateMatrix(self.rotate[0],
                                 self.rotate[1],
                                 self.rotate[2])

        camMatrix = translateMat * rotateMat

        # Inversa de la matriz
        return camMatrix.inverse()
