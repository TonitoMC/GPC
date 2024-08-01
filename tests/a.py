from src.mathlib import *

mat = Matrix([[2, 5, 7],
                      [6, 3, 4],
                      [5, -2, -3]])

inv = mat.inverse()

print(inv)
print(mat)