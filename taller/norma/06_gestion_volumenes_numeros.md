# Gestión de volúmenes y números

**Nota de origen:** el material fuente no traía ningún artefacto para esta fase — solo la identidad de la revista (cuatrimestral, 3 números/año) y ejemplos de artículos individuales ya producidos. Esta plantilla es una propuesta construida a partir de esa identidad, para cerrar el hueco. Valídala con el Dr. Medina-Rodríguez y ajústala a como realmente se organiza el comité editorial antes de tratarla como proceso oficial.

## Mapeo volumen ↔ año ↔ número ↔ período

```
Vol. 5 = 2025   |   Vol. 6 = 2026   |   Vol. 7 = 2027   (Vol. = Año − 2020)

No. 1 = Enero–Abril
No. 2 = Mayo–Agosto
No. 3 = Septiembre–Diciembre
```

## Tabla maestra de número (plantilla)

Mantener una tabla así por cada número en preparación, antes de compilar cualquier artículo individual — evita colisiones de ART# y permite ver de un vistazo qué falta.

| ART# | Título | Tipo | Autor(es) | Estado | Recibido | Aceptado | Publicado | Carpeta |
|---|---|---|---|---|---|---|---|---|
| 1 | Neuromodulación en psiquiatría... | Editorial | Aldana López | ✓ Compilado, diagnóstico 100% | 11-mar-2025 | 27-abr-2025 | 30-abr-2025 | VOL5_NO2_ART1_NEUROMODULACION/ |
| 2 | ... | ... | ... | En dictamen | | | | |

Estados sugeridos: `Recibido` → `En dictamen` → `Aceptado (pendiente diagramaje)` → `Diagramado (pendiente diagnóstico)` → `✓ Compilado, diagnóstico 100%` → `Publicado`.

## Paginación continua dentro del número

Cada número lleva paginación continua entre artículos (el ART1 empieza en la página 1 del número, el ART2 continúa donde terminó el ART1, etc.). Esto significa que el `\thepage`/`LastPage` de cada `.tex` individual **no** es la paginación final del número — al armar el número completo hay que:

1. Compilar cada artículo por separado para diagnóstico individual (con su propia numeración 1..N).
2. Al ensamblar el número, recompilar en secuencia o usar `\setcounter{page}{N}` al inicio de cada artículo según dónde caiga en la secuencia del número.
3. Actualizar el footer "Página X de Y" para que Y sea el total de páginas del NÚMERO, no del artículo individual, si la revista publica el número como PDF único. Si cada artículo se publica como PDF independiente (como en `VOL5_NO2_ART1_NEUROMODULACION/`), "Página X de Y" es relativo al artículo — confirmar con el editor cuál de los dos modelos aplica antes de asumir.

## Asignación de DOI y folio

- El campo `\APMdoi` se usa activamente y se renderiza en el header (ver `03_estructura_manuscrito.md`).
- El campo `\APMfolio` **no se renderiza en ningún lado** (código muerto — ver `09_limitaciones_conocidas.md`). No lo uses como mecanismo real de tracking interno; usa la tabla maestra de arriba (columna ART#) o un sistema externo (hoja de cálculo, base de datos del comité) para folio interno.
- Formato de DOI observado en el ejemplo canónico: confirmar con el editor el prefijo real asignado por Crossref/DOI.org antes de publicar — no inventar un DOI.

## Checklist antes de cerrar un número

- [ ] Todos los artículos del número tienen VOL/NO/AÑO/PERÍODO consistentes entre sí.
- [ ] Ningún ART# se repite dentro del número.
- [ ] Cada artículo pasó diagnóstico de 14 capas con veredicto "APTO PARA PRODUCCIÓN".
- [ ] Tabla de contenidos del número (si existe como documento aparte) coincide con los títulos exactos usados en cada `.tex`.
- [ ] Fechas de "Publicado" son coherentes con el período del número (p. ej., no publicar en abril un artículo del No. 2 Mayo–Agosto).
