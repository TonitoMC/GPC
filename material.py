import numpy as np
class Material(object):
    def __init__(self, diffuse, spec = 1.0, Ks = 0.0):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks

    def GetSurfaceColor(self, intercept, renderer):
        # Phong reflection model
        # LightColor = LightColors + Specular
        # FinalColor = DiffuseColor * LightColor
        lightColor = [0,0,0]
        finalColor = self.diffuse

        for light in renderer.lights:
            shadowRayOrigin = np.add(intercept.point, np.multiply(intercept.normal, 1e-4))  # Offset to avoid self-intersection

            # TODO raycast in right direction
            if light.type == "Directional":
                lightDir = [(i * -1) for i in light.direction]
                lightDir /= np.linalg.norm(lightDir)
                shadowIntercept = renderer.glCastRay(shadowRayOrigin, lightDir)
                if shadowIntercept == None:
                    currentLightColor = light.GetLightColor(intercept)
                    currentSpecularColor = light.GetSpecularColor(intercept, renderer.camera.translate)
                    lightColor = [(lightColor[i] + currentLightColor[i] + currentSpecularColor[i]) for i in range(3)]
            else:
                currentLightColor = light.GetLightColor(intercept)
                currentSpecularColor = light.GetSpecularColor(intercept, renderer.camera.translate)
                lightColor = [(lightColor[i] + currentLightColor[i] + currentSpecularColor[i]) for i in range(3)]

        finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]    
        return finalColor