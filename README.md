# Laboratorio 4: Shaders II
## Autor: Jose Merida | 30 de Octubre 2024
## Ubicacion de Archivos
- Models: Los modelos utilizados en el programa
- Textures: Los archivos BMP utilizados como textura para los modelos dentro del programa
## Demostracion
![Lab4Showoff](https://github.com/user-attachments/assets/1977a996-eeeb-4cbe-8fec-17fa2d3c4803)

### Teclas:

No. 1: Vertex Shader Normal

No. 2: Vertex Shader Breathing

No. 3: Vertex Shader Spring

No. 4: Vertex Shader Bubble

No. 5: Fragment Shader Normal

No. 6: Fragment Shader Glitch / Aberracion de Colores

No. 7: Fragment Shader Grayscale + Noise

No. 8: Fragment Shader Mouse Light

### Fragment Shader: Light Mouse

Aumenta la intensidad de los colores (ilumina) cerca del mouse

```
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
```

### Fragment Shader: Grayscale

Toma los colores y los pasa a una escala de grises, agrega ruido aleatoriamente para efecto de estatica

```
{
    // Calculo color escala de grises
    vec3 texColor = texture(tex, outTextCoords).rgb;
    float grayscale = (texColor.r + texColor.g + texColor.b) / 3.0;

    // Ruido aleatorio / estatica
    float noise = random(outTextCoords * time * 0.1);
    float staticEffect = noise > 0.5 ? 1.0 : 0.0;

    fragColor = vec4(vec3(grayscale * staticEffect), 1.0);
}
```

### Fragment Shader: Aberration

Distorsiona textura usando onda sinusoidal y distorsiona los colores para un efecto "glitch"

```
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
```

### Vertex Shader: Breathing

Aumenta y disminuye el tamaño del objeto utilizando valores de una onda sinusoidal

```
{
    // 'Factor explosion' sobre que tan grande debe ser el objeto
    float explosionFactor = abs(sin(time)) * 0.01;

    // Ajuste en posicion de vertices
    vec3 explodedPosition = position + normalize(position) * explosionFactor;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(explodedPosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}
```

### Vertex Shader: Spring

Traslada el objeto en el eje Y y comprime / descomprime basado en una onda sinusoidal

```
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
}
```

### Vertex Shader: Bubble

Crea "burbujas" que distorsionan la forma del objeto, similar a breathing pero con más distorsión.

```
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
```
