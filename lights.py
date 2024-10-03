from MathLib import *
from math import cos, pi
class Light(object):
    def __init__(self, color = [1,1,1], intensity = 1.0, type = None):
        self.color = color
        self.intensity = intensity
        self.type = type
    
    def GetLightColor(self, intercept = None):
        return [(i * self.intensity) for i in self.color]
    
    def GetSpecularColor(self, intercept, viewPos):
        return [0,0,0]
    
class AmbientLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0):
        super().__init__(color, intensity)
        self.lightType = "Ambient"
    def GetSpecularColor(self, intercept, viewPos):
        return [0,0,0]

class DirectionalLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0, direction = [0, -1, 0]):
        super().__init__(color, intensity, "Directional")
        self.direction = [x / vec_norm(direction) for x in direction]

    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor()
        if intercept:
            dir = [(i * -1) for i in self.direction]
            intensity = dot_product(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * intensity) for i in lightColor]
        return lightColor
    
    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [(i * -1) for i in self.direction]
            reflect = reflectVector(intercept.normal, dir)

            viewDir = vec_sub(viewPos, intercept.point)
            viewDir = [x / vec_norm(viewDir) for x in viewDir]

            specularity = max(0, dot_product(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            specColor = [(i * specularity) for i in specColor]

        return specColor
    
class PointLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1, position = [0,0,0]):
        super().__init__(color,intensity)
        self.position = position
        self.lightType = "Point"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            dir = np.subtract(self.position, intercept.point)
            R = np.linalg.norm(dir)
            dir /= R
            intensity = np.dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)

             # Ley de cuadrados inversos
             # attenuation = intensity / R^2
             # R es la distancia del punto intercepto a la luz punto

            if R != 0:
                intensity /= R**2

            lightColor = [(i * intensity) for i in lightColor]

        return lightColor
    
    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = np.subtract(self.position, intercept.point)
            R = np.linalg.norm(dir)
            dir /= R

            reflect = reflectVector(intercept.normal, dir)

            viewDir = vec_sub(viewPos, intercept.point)
            viewDir = [x / vec_norm(viewDir) for x in viewDir]

            specularity = max(0, dot_product(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            if R != 0:
                specularity /= R**2
            specColor = [(i * specularity) for i in specColor]


        return specColor

class SpotLight(PointLight):
    def __init__(self, color = [1,1,1], intensity = 1, position = [0,0,0], direction = [0,-1,0], innerAngle = 50, outerAngle = 60):
        super().__init__(color, intensity, position)
        self.direction = direction / np.linalg.norm(direction)
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lightType = "Spot"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)
        if intercept:
            lightColor = [i * self.SpotlightAttenuation(intercept) for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)
        if intercept:
            specularColor = [i * self.SpotlightAttenuation(intercept) for i in specularColor]
        return specularColor
    def SpotlightAttenuation(self, intercept = None):
        if intercept == None:
            return 0
        
        wi = np.subtract(self.position, intercept.point)
        wi /= np.linalg.norm(wi)

        innerAngleRads = self.innerAngle * pi / 180
        outerAngleRads = self.outerAngle * pi / 180

        attenuation = (-np.dot(self.direction, wi) - cos(outerAngleRads)) / (cos(innerAngleRads) - cos(outerAngleRads))

        attenuation = min(1, max(0, attenuation))

        return attenuation