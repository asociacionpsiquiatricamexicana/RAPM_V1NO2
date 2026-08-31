# Checklist de citación APA 7.ª edición

**Nota de origen:** el material fuente definía el *formato tipográfico* de las referencias en LaTeX (tamaño, raggedright, hanging indent — ver `03_estructura_manuscrito.md`) pero no un checklist real de estilo de citación APA 7. Este documento lo completa con las reglas estándar de APA 7.ª ed. en español (Manual Moderno, 2020), citado en sesiones previas como referencia (`correccion-medina` skill, línea de instrucciones). Úsalo para revisar manuscritos antes de diagramar, no solo para el formato visual del PDF.

## Citación en texto

| Caso | Formato |
|---|---|
| Un autor | (Apellido, 2025) / Apellido (2025) |
| Dos autores | (Apellido1 & Apellido2, 2025) — usar "&" dentro de paréntesis, "y" fuera |
| Tres o más autores | (Apellido1 et al., 2025) — desde la primera cita (regla APA 7, cambia de APA 6) |
| Autor corporativo (primera vez) | (Asociación Psiquiátrica Mexicana [APM], 2025) |
| Autor corporativo (siguientes) | (APM, 2025) |
| Sin fecha | (Apellido, s.f.) |
| Cita textual <40 palabras | Entre comillas, con número de página: (Apellido, 2025, p. 45) |
| Cita textual ≥40 palabras | Bloque sangrado 1.27cm, sin comillas, sangría francesa no aplica aquí |
| Múltiples obras, mismo paréntesis | Orden alfabético, separadas por punto y coma: (Apellido1, 2024; Apellido2, 2025) |
| Comunicación personal | (Nombre Apellido, comunicación personal, DD de mes de AAAA) — no va en lista de referencias |

## Lista de referencias — estructura por tipo de fuente

**Artículo de revista:**
```
Apellido, N. N., & Apellido2, N. N. (Año). Título del artículo en minúsculas
    excepto primera palabra y nombres propios. Nombre de la Revista en
    Cursivas y Mayúscula Inicial, Volumen(Número), páginas–páginas.
    https://doi.org/xx.xxxx/xxxxx
```

**Libro:**
```
Apellido, N. N. (Año). Título del libro en cursivas (edición si aplica).
    Editorial.
```

**Capítulo de libro editado:**
```
Apellido, N. N. (Año). Título del capítulo. En N. N. Apellido (Ed.),
    Título del libro en cursivas (pp. xx–xx). Editorial.
```

**Fuente electrónica / sitio web:**
```
Apellido, N. N. (Año, DD de mes). Título de la página. Nombre del sitio.
    https://url-completa
```

**Tesis:**
```
Apellido, N. N. (Año). Título de la tesis en cursivas [Tesis de
    doctorado/maestría, Institución]. Repositorio o base de datos.
```

## Reglas de formato APA 7 que se aplican SIEMPRE

- **DOI**: siempre como URL completa `https://doi.org/10.xxxx/xxxxx`, nunca como "DOI:" seguido del número.
- **Hasta 20 autores**: listar todos. Desde 21: primeros 19, coma, puntos suspensivos, último autor.
- **Título del artículo**: minúscula sostenida (solo mayúscula inicial y nombres propios/siglas). El título de la revista SÍ lleva mayúscula en cada palabra principal.
- **Sangría francesa (hanging indent)**: primera línea al margen, siguientes líneas sangradas 1.27cm (equivalente LaTeX: `hangindent` — en el `.cls` está fijado a 12pt, verificar que coincida con la convención de la revista).
- **Sin numeración de referencias**: APA 7 es autor-fecha, nunca numerado (`\hangparas`, no `enumerate` — ver `.cls`).
- **Orden alfabético** por apellido del primer autor; mismo autor y año → sufijo a, b, c según orden de aparición en el texto.
- **Comillas españolas «»** para términos técnicos o traducciones dentro del cuerpo del texto (no usar `\enquote{}` dentro del header por FM23).

## Checklist de revisión antes de diagramar

- [ ] Toda cita en texto tiene su entrada correspondiente en la lista de referencias (y viceversa — sin refs huérfanas).
- [ ] Todas las referencias tienen DOI si existe (buscar en Crossref si el autor no lo incluyó).
- [ ] Formato "et al." aplicado desde 3+ autores en TODAS las citas en texto, no solo la primera.
- [ ] Número de referencias dentro del rango del tipo de artículo (ver tabla en `01_identidad_tipos_articulo.md`).
- [ ] Sin numeración en la lista de referencias.
- [ ] Orden alfabético correcto (revisar especialmente apellidos compuestos y "de/del/de la").
- [ ] Idioma de las referencias coincide con el idioma del artículo cuando aplica, o se mantiene el idioma original de la fuente citada (no se traducen títulos de fuentes).
