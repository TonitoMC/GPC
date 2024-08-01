from math import cos, pi, sin
import numpy as np


# Clase matrix para manejar operaciones con matrices
class Matrix:
    def __init__(self, data):
        self.data = data

    def matrix_mul(self, other):
        mat1 = self.data
        mat2 = other.data
        result = [
            [0 for _ in range(len(mat2[0]))] for _ in range(len(mat1))
        ]
        for i in range(len(mat1)):
            for j in range(len(mat2[0])):
                for k in range(len(mat2)):
                    result[i][j] += mat1[i][k] * mat2[k][j]
        return Matrix(result)

    def vector_mul(self, other):
        mat = self.data
        vec = other
        result = [0 for _ in range(len(mat))]

        for i in range(len(mat)):
            for j in range(len(vec)):
                result[i] += mat[i][j] * vec[j]

        return result

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.matrix_mul(other)
        if isinstance(other, list):
            return self.vector_mul(other)

    def identity(self):
        size = len(self.data[0])
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    def __repr__(self):
        return f"Matrix({self.data})"

    def transpose(self):
        mat = self.data
        return [list(row) for row in zip(*mat)]
    def getMinor(self, i, j):
        mat = self.data
        return [row[:j] + row[j + 1:] for row in (mat[:i] + mat[i + 1:])]

    def determinant(self):
        mat = self.data
        if len(mat) == 2:
            return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

        det = 0

        for i in range(len(mat)):
            det += ((-1) ** i) * mat[0][i] * Matrix(self.getMinor(0, i)).determinant()
        return det

    def inverse(self):
        mat = self.data
        det = self.determinant()

        n = len(mat)

        if n == 2:
            return Matrix([[mat[1][1] / det, -1 * mat[0][1] / det],
                           [-1 * mat[1][0] / det, mat[0][0] / det]])

        cofactors = []
        for r in range(n):
            cofactorRow = []
            for c in range(n):
                minor = Matrix(self.getMinor(r, c))
                cofactorRow.append(((-1) ** (r + c)) * minor.determinant())
            cofactors.append(cofactorRow)

        cofactorMatrix = Matrix(cofactors)
        cofactors_transposed = cofactorMatrix.transpose()

        inverse_matrix = []
        for r in range(n):
            row = [value / det for value in cofactors_transposed[r]]
            inverse_matrix.append(row)

        return Matrix(inverse_matrix)


def TranslationMatrix(x, y, z):
    return Matrix([[1, 0, 0, x],
                   [0, 1, 0, y],
                   [0, 0, 1, z],
                   [0, 0, 0, 1],
                   ])


def ScaleMatrix(x, y, z):
    return Matrix([[x, 0, 0, 0],
                   [0, y, 0, 0],
                   [0, 0, z, 0],
                   [0, 0, 0, 1],
                   ])


def RotateMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180

    pitchMat = Matrix([
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1],
    ])

    yawMat = Matrix([
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1],
    ])

    rollMat = Matrix([
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    return pitchMat * yawMat * rollMat
