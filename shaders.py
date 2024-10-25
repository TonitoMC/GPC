
explode_shader = """
#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform float time;

void main()
{
    float explosionFactor = abs(sin(time)) * 0.01;

    vec3 explodedPosition = position + normalize(position) * explosionFactor;

    gl_Position = modelMatrix * vec4(explodedPosition, 1.0);

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

void main()
{
  gl_Position = modelMatrix * vec4(position, 1.0);
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

pixel_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;
uniform float pixelSize = 0.015;
void main()
{
    vec2 pixelatedCoords = vec2(
        floor(outTextCoords.x / pixelSize) * pixelSize,
        floor(outTextCoords.y / pixelSize) * pixelSize
    );

    vec3 texColor = texture(tex, pixelatedCoords).rgb;

    fragColor = vec4(texColor, 1.0);
}
"""

grayscale_shader = """
#version 450 core

in vec2 outTextCoords;
out vec4 fragColor;

uniform sampler2D tex;

void main()
{
    vec3 texColor = texture(tex, outTextCoords).rgb;

    float grayscale = (texColor.r + texColor.g + texColor.b) / 3.0;

    fragColor = vec4(vec3(grayscale), 1.0);
}
"""