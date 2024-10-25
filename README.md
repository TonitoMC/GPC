# Laboratorio 4: Shaders II
## Entrega Inicial 24-10-2024

Teclas:

No. 1: Llenado de Texturas

No. 2: Unicamente Lineas

No. 3: Vertex Shader Normal

No. 4: Vertex Shader Explode

No. 5: Fragment Shader Normal

No. 6: Fragment Shader Pixel

No. 7: Fragment Shader Grayscale


### Vertex Shader: Explode

Calcula un 'factor explosion' basado en el tiempo y agranda / disminuye en tamaño (todavía falta agregarle más cosas)

```
{
    float explosionFactor = abs(sin(time)) * 0.01;

    vec3 explodedPosition = position + normalize(position) * explosionFactor;

    gl_Position = modelMatrix * vec4(explodedPosition, 1.0);

    outTextCoords = textCoords;
    outNormals = normals;
}
```

### Vertex Shader: Pixel

Redondea las coordenadas de textura para un efecto pixeleado

```
{
    vec2 pixelatedCoords = vec2(
        floor(outTextCoords.x / pixelSize) * pixelSize,
        floor(outTextCoords.y / pixelSize) * pixelSize
    );

    vec3 texColor = texture(tex, pixelatedCoords).rgb;

    fragColor = vec4(texColor, 1.0);
}
```

### Vertex Shader: Grayscale

Toma los colores y los pasa a una escala de grises, bastante simple pero voy a estar construyendo sobre el para la entrega final

```
{
    vec3 texColor = texture(tex, outTextCoords).rgb;

    float grayscale = (texColor.r + texColor.g + texColor.b) / 3.0;

    fragColor = vec4(vec3(grayscale), 1.0);
}
```


