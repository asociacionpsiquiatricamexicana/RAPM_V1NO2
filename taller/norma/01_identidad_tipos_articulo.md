# Identidad de la revista y tipos de artículo

## Ficha completa

```
Nombre:       Revista de la Asociación Psiquiátrica Mexicana, A.C.
Abreviatura:  Rev Asoc Psiquiatr Mex
Frecuencia:   Cuatrimestral (3 números/año: Ene–Abr, May–Ago, Sep–Dic)
e-ISSN:       3061-7979
Licencia:     CC BY-NC 4.0
Editor:       Dr. David Eduardo Saucedo Martínez
Dep. Editor:  Dr. José Carlos Medina-Rodríguez
Contacto:     revistaapm@psiquiatrasapm.org.mx
Peer review:  Doble ciego
Citación:     APA 7.ª edición
Volúmenes:    2025=Vol.5, 2026=Vol.6, 2027=Vol.7
Motor:        pdfLaTeX (TeX Live 2023+)
Clase:        apm-editorial.cls (665 líneas, 45 paquetes)
```

Nota de nomenclatura: el nombre de la asociación siempre lleva "A.C." Verificado en `\@apmeditor` del `.cls` y en el colofón — no omitir.

## Tipos de artículo (spec aspiracional — ver limitación)

| Tipo | Palabras (body) | Abstract | Tablas+Figs | Refs |
|---|---|---|---|---|
| Original | 3,000–5,000 | 250 (estructurado) | ≤5 | 30–50 |
| Revisión / Meta-análisis | 5,000–6,000 | 250 (estructurado) | ≤5 | 50–100 |
| Reporte breve | 1,800 | 150 (estructurado) | 1 | ≤15 |
| Caso clínico | 2,000–3,000 | 150 (no estructurado) | ≤3 | ≤20 |
| Editorial | 1,000–1,500 | No requerido | 0 | ≤10 |
| Carta al Editor | 500 | No requerido | 1 | ≤5 |

**Actualizado el 31 de agosto de 2026:** el rótulo del encabezado y `pdfsubject` ya siguen a `\APMtype{}` — verificado compilando con los seis nombres de la tabla. Lo que esta tabla sigue siendo es la especificación editorial (extensión, resumen, referencias); el `.cls` no cuenta palabras ni referencias por sí solo, y **no hay layout probado para un cuerpo IMRaD de 3,000–6,000 palabras con tablas y figuras** — solo el rótulo y los metadatos cambian con `\APMtype{}`, no la estructura del cuerpo. Ver `09_limitaciones_conocidas.md §1`.

Si el usuario pide un tipo distinto de Editorial:
1. `\APMtype{Artículo original}` (o el nombre que corresponda de la tabla) ya produce el rótulo y los metadatos correctos — no hace falta avisar que "solo soporta Editorial".
2. Sí avisa si el cuerpo excede lo que una columna sencilla ha probado: el ejemplo validado es un Editorial de una página y media a dos columnas; un Original de 3,000+ palabras con tablas es terreno no verificado, y el diagnóstico de geometría (`sondas/geometria.py`) debe correr sobre ese artículo en concreto, no asumirse del ejemplo.
3. No reutilices `suicide_jalisco.tex` como base sin antes migrarlo a `apm-editorial.cls` (actualmente reimplementa su propio preámbulo con geometría distinta: 2.0/2.0/2.5/2.0cm en vez de 1.8/1.8/2.0/1.8cm).

## Estructura IMRaD esperada (para Original/Revisión/Reporte)

```
INTRODUCCIÓN
MÉTODO
  Participantes
  Instrumentos (condicional)
  Procedimiento
  Análisis de datos
RESULTADOS
DISCUSIÓN
  Limitaciones
CONCLUSIONES
```

Detalle completo del árbol de secciones (front matter + body + back matter, con marcado Obligatorio/Opcional/Condicional) en `03_estructura_manuscrito.md`.
