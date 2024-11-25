from obj import Obj
from buffer import Buffer
from pygame import image
from OpenGL.GL import *
import glm
from OpenGL.GL.shaders import compileProgram, compileShader

class Model(object):
    def __init__(self, filename, vShader, fShader):
        objFile = Obj(filename=filename)

        self.vertices = objFile.vertices
        self.texCoords = objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces
        self.buffer = Buffer(self.BuildBuffer())
        self.translation = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

        # Compile and set the shaders
        self.shaders = self.CompileShaders(vShader, fShader)

    def BuildBuffer(self):
        data = []

        for face in self.faces:
            faceVerts = []
            for i in range(len(face)):
                vert = []
                position = self.vertices[face[i][0] - 1]

                for value in position:
                    vert.append(value)

                vts = self.texCoords[face[i][1] - 1]

                for value in vts:
                    vert.append(value)

                normals = self.normals[face[i][2] - 1]

                for norm in normals:
                    vert.append(norm)

                faceVerts.append(vert)

            for value in faceVerts[0]:
                data.append(value)
            for value in faceVerts[1]:
                data.append(value)
            for value in faceVerts[2]:
                data.append(value)

            if len(faceVerts) == 4:
                for value in faceVerts[0]:
                    data.append(value)
                for value in faceVerts[2]:
                    data.append(value)
                for value in faceVerts[3]:
                    data.append(value)
        return data

    def AddTextures(self, textureFilename):
        self.textureSurface = image.load(textureFilename)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)

    def CompileShaders(self, vShader, fShader):
        """Compile and link the vertex and fragment shaders."""
        try:
            vertex_shader = compileShader(vShader, GL_VERTEX_SHADER)
            fragment_shader = compileShader(fShader, GL_FRAGMENT_SHADER)
            program = compileProgram(vertex_shader, fragment_shader)
            return program
        except Exception as e:
            print(f"Shader compilation failed: {e}")
            return None

    def GetModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.translation)

        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yawMat = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        rollMat = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))

        rotationMat = pitchMat * yawMat * rollMat

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def Render(self):
        """Render the model using its specific shaders."""
        if self.shaders is not None:
            glUseProgram(self.shaders)

            # Pass uniforms to the shaders
            model_matrix = self.GetModelMatrix()
            glUniformMatrix4fv(glGetUniformLocation(self.shaders, "modelMatrix"),
                               1, GL_FALSE, glm.value_ptr(model_matrix))

            if self.texture is not None:
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, self.texture)
                glTexImage2D(
                    GL_TEXTURE_2D,
                    0,
                    GL_RGB,
                    self.textureSurface.get_width(),
                    self.textureSurface.get_height(),
                    0,
                    GL_RGB,
                    GL_UNSIGNED_BYTE,
                    self.textureData
                )
                glGenerateMipmap(GL_TEXTURE_2D)

            self.buffer.Render()

        else:
            print("No shaders attached to this model!")
