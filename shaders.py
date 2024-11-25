# Fragment Shaders

# Shader que calcula intensidad de luz basado en la posicion del  mouse
light_mouse_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;
uniform float mouse_x;
uniform float mouse_y;

void main()
{
    // Valores de intensidad de luz
    float intensityRadius = 0.3;
    float maxIntensity = 1.5;

    // Coordenadas normalizadas del fragmento
    vec2 fragCoordNorm = (gl_FragCoord.xy / 300.0) - vec2(1.0, 1.0);

    // Coordenadas normalizadas del mouse
    vec2 mouseNorm = vec2(mouse_x, mouse_y);
    float distToMouse = distance(fragCoordNorm, mouseNorm);

    vec3 texColor = texture(tex, outTextCoords).rgb;

    // Intensidad del color / la luz dependiendo de la distancia al  mouse
    float intensity = 1.0;
    if (distToMouse < intensityRadius) {
        intensity += (1.0 - distToMouse / intensityRadius) * (maxIntensity - 1.0);
    }

    fragColor = vec4(texColor * intensity, 1.0);
}
"""

# Shader que lo pone en escala de grises y agrega estatica
grayscale_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;
uniform float time;

float random(vec2 coords)
{
    return fract(sin(dot(coords, vec2(10, 10))) * 40000.0);
}

void main()
{
    // Calculo color escala de grises
    vec3 texColor = texture(tex, outTextCoords).rgb;
    float grayscale = (texColor.r + texColor.g + texColor.b) / 3.0;

    // Ruido aleatorio / estatica
    float noise = random(outTextCoords * time * 0.1);
    float staticEffect = noise > 0.5 ? 1.0 : 0.0;

    fragColor = vec4(vec3(grayscale * staticEffect), 1.0);
}
"""

# Shader de aberracion de colores, "glitcheado"
aberration_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;
uniform float time;
uniform float aberrationStrength = 0.01;

void main()
{
    // Parametros de la onda
    float waveFrequency = 5.0;
    float waveAmplitude = 0.05;
    float waveSpeed = 1.0;

    // Distorsion tipo onda utilizando ona sinusoidal
    float waveOffset = sin(outTextCoords.y * waveFrequency + time * waveSpeed) * waveAmplitude;

    vec2 wavyCoords = vec2(outTextCoords.x + waveOffset, outTextCoords.y);

    // Desplazamiento de colores
    vec2 redOffset = wavyCoords + vec2(-aberrationStrength, 0.0);
    vec2 greenOffset = wavyCoords + vec2(0.0, aberrationStrength);
    vec2 blueOffset = wavyCoords + vec2(aberrationStrength, -aberrationStrength);

    float red = texture(tex, redOffset).r;
    float green = texture(tex, greenOffset).g;
    float blue = texture(tex, blueOffset).b;

    fragColor = vec4(red, green, blue, 1.0);
}
"""

energy_shader = """
#version 450 core

in vec2 outTextCoords;
in vec3 outNormals;
in vec3 fragPosition;

out vec4 fragColor;

uniform sampler2D tex;    // Base texture (optional)
uniform float time;

float random(vec2 coords) {
    return fract(sin(dot(coords, vec2(12.9898, 78.233))) * 43758.5453);
}

float noise(vec2 coords) {
    vec2 i = floor(coords);
    vec2 f = fract(coords);
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

void main()
{
    vec2 uv = outTextCoords * 10.0;
    float t = time * 0.5;

    float energyPattern = noise(uv + vec2(t, -t)) * 0.5 
                        + noise(uv * 2.0 - vec2(-t, t)) * 0.25;

    energyPattern = pow(energyPattern, 3.0) * 2.0;

    vec3 energyColor = vec3(0.1, 0.4, 1.0) * energyPattern;

    vec3 baseColor = texture(tex, outTextCoords).rgb;
    vec3 finalColor = baseColor + energyColor;

    fragColor = vec4(finalColor, 1.0);
}
"""

# Shader de efecto 'breathing', aumenta y disminuye el tamaño basado en una onda
# sinusoidal
breathing_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
void main()
{
    // 'Factor explosion' sobre que tan grande debe ser el objeto
    float explosionFactor = abs(sin(time)) * 0.01;

    // Ajuste en posicion de vertices
    vec3 explodedPosition = position + normalize(position) * explosionFactor;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(explodedPosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}
"""

# Vertex Shader de efecto de resorte, comprime el objeto y lo mueve en el eje Y basado
# en una onda sinusoidal
spring_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

void main()
{
    // Parametros para el efecto, a futuro pueden ser pasados o modificados dependiendo
    // de la escala del modelo
    float springFrequency = 3.0;
    float maxScaleY = 1.5;
    float minScaleY = 0.5;
    float bounceHeight = 0.2;

    // Calculo de escala y posicion en el eje Y
    float scaleY = mix(minScaleY, maxScaleY, 0.5 + 0.5 * sin(time * springFrequency));
    float verticalBounce = bounceHeight * (0.5 + 0.5 * sin(time * springFrequency));

    // Ajuste posicion y escala
    vec3 springyPosition = vec3(position.x, position.y * scaleY + verticalBounce, position.z);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(springyPosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}"""

# Vertex Shader de efecto de burbujas, más que todo una distorsión más fuerte / pequeña
# que el breathing_shader
bubble_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

// Valores aleatorios similar al grayscale_shader
float random(vec2 coords)
{
    return fract(sin(dot(coords, vec2(10, 10))) * 40000.0);
}

void main()
{
    // Parametros de las burbujas
    float bubbleFrequency = 3.0;
    float bubbleStrength = 0.01;
    float bubbleSpeed = 2.0;

    // Efecto de burbuja / distorsion
    float bubbleEffect = abs(sin(random(position.xy) * bubbleFrequency + time * bubbleSpeed)) * bubbleStrength;

    vec3 bubbledPosition = position + normals * bubbleEffect;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(bubbledPosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}
"""

vertex_shader = """
#version 450 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
  gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""

fragment_shader = """
#version 450 core

in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;

uniform sampler2D tex;

void main()
{
  fragColor = texture(tex, outTextCoords);
}
"""

skybox_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix * viewMatrix * vec4(inPosition, 1.0);
}

'''

skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox, texCoords);
}

'''