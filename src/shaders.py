
from src.mathlib import *


def vertexShader(vertex, **kwargs):

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt = viewMatrix * modelMatrix * vt

    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3],
          ]

    print(vt)

    return vt
