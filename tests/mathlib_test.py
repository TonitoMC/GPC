import unittest
from math import isclose
from src.mathlib import Matrix, TranslationMatrix, ScaleMatrix, RotateMatrix


class TextMatrixOperationsTest(unittest.TestCase):

    def text_matrix_mul(self):
        mat1 = Matrix([[1, 2],
                       [3, 4]])
        mat2 = Matrix([[5, 6],
                       [7, 8]])
        result = mat1 * mat2
        expected = Matrix([[19, 22],
                           [43, 50]])
        self.assertEqual(result.data, expected.data)

    def test_vector_mul(self):
        mat = Matrix([[1, 2, 3],
                      [4, 5, 6]])
        vec = [1, 2, 3]
        result = mat * vec
        expected = [14, 32]
        self.assertEqual(result, expected)