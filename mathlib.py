from math import cos, pi, sin
import numpy as np
from math import acos, asin, pi

def refractVector(normal, incident, n1, n2):
    # Snell's Law
    c1 = dot_product(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        normal = [x * -1 for x in normal]
        n1, n2 = n2, n1

    n = n1 / n2
    
    # Calculating refracted vector
    temp = vec_sum(incident, [c1 * x for x in normal])
    T = vec_sub([n * x for x in temp], [normal[i] * ((1 - n**2 * (1 - c1**2)) ** 0.5) for i in range(len(normal))])
    
    norm_T = vec_norm(T)
    return [x / norm_T for x in T]

def totalInternalReflection(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1
        
    if n1 < n2:
        return False
    
    theta1 = acos(c1)
    thetaC = asin(n2 / n1)
    
    return theta1 >= thetaC

def fresnel(normal, incident, n1, n2):
    c1 = dot_product(normal, incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1**2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5
    
    F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt

def dot_product(a,b):
     if len(a) != len(b):
         raise ValueError("Los vectores deben tener la misma longitud")
     return sum(x*y for x,y in zip(a,b))

def vec_mul(a, b):
    if len(a) != len(b):
        raise ValueError("Los vectores deben tener la misma longitud")

    result = []

    for i in range(len(a)):
        result.append(a[i] * b[i])

    return result
def vec_sub(a, b):
    if len(a) != len(b):
        raise ValueError("Both vectors must have the same length")
    return [a[i] - b[i] for i in range(len(a))]

def vec_sum(a, b):
    if len(a) != len(b):
        raise ValueError("Los vectores deben tener la misma longitud")

    result = []

    for i in range(len(a)):
        result.append(a[i] + b[i])

    return result

def vec_norm(v):
     return sum(x**2 for x in v) ** 0.5

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

def barycentricCoords(A, B, C, P):
	
	# Se saca el �rea de los subtri�ngulos y del tri�ngulo
	# mayor usando el Shoelace Theorem, una f�rmula que permite
	# sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el �rea del tri�ngulo es 0, retornar nada para
	# prevenir divisi�n por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baric�ntricas dividiendo el 
	# �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC


	# Si cada coordenada est� entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son v�lidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None
	
def reflectVector(normal, direction):
	reflect = 2 * dot_product(normal, direction)
	reflect = [x * reflect for x in  normal]
	reflect = vec_sub(reflect, direction)
	reflect = [x / vec_norm(reflect) for x in reflect]
	return reflect
