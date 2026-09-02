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

| ART# | Título                            | Tipo      | Autor(es)    | Estado                        | Recibido    | Aceptado    | Publicado   | Carpeta                        |
| ---- | --------------------------------- | --------- | ------------ | ----------------------------- | ----------- | ----------- | ----------- | ------------------------------ |
| 1    | Neuromodulación en psiquiatría... | Editorial | Aldana López | ✓ Compilado, diagnóstico 100% | 11-mar-2025 | 27-abr-2025 | 30-abr-2025 | VOL5_NO2_ART1_NEUROMODULACION/ |
| 2    | ...                               | ...       | ...          | En dictamen                   |             |             |             |                                |

Estados sugeridos: `Recibido` → `En dictamen` → `Aceptado (pendiente diagramaje)` → `Diagramado (pendiente diagnóstico)` → `✓ Compilado, diagnóstico 100%` → `Publicado`.

## Paginación del número — decisión tomada (2 de septiembre de 2026)

Este documento dejaba dos modelos abiertos ("confirmar con el editor cuál
aplica"). Con `taller/armar_numero.py` ya construido, quedó decidido por la
vía más simple y más verificable: **cada artículo se sigue publicando también
como PDF independiente**, y el PDF del número **no recompone ni re-pagina**
cada artículo — es una **concatenación**: portada + tabla de contenido +
cada artículo camera-ready tal cual salió de `componer.sh`, en el orden de
su ART#. El "Página X de Y" que imprime cada artículo queda **relativo a sí
mismo**, no al número.

Por qué esta vía y no recomponer con `\setcounter{page}{N}`: recomponer
exigiría reunir todos los `.tex` del número en un solo documento LaTeX antes
de compilar, lo que rompe la garantía de que cada artículo se compila y se
mide de forma independiente (la sonda de un artículo dejaría de corresponder
al PDF que de verdad se publica). La concatenación conserva esa garantía: lo
que `geometria.py` midió sobre `ACOMPANAMIENTO_APM_VOL6_NO3_2026.pdf` es
exactamente lo que termina dentro de `REVISTA_VOL6_NO3.pdf`.

La tabla de contenido del número sí lleva una página inicial correcta por
artículo — se mide, nunca se asume: `armar_numero.py` compila primero
portada+contenido con las páginas en un valor de relleno, mide cuántas
páginas ocupa esa portada+contenido, y con esa cifra ya real calcula la
página inicial de cada artículo (portada+contenido + páginas acumuladas de
los artículos anteriores) antes de recompilar la versión final.

## Cómo entra un artículo — `taller/recibir_articulo.py`

Desde el 2 de septiembre de 2026, un artículo no se diagrama a mano: se
recibe el manuscrito del autor en Word (`.docx`) y `recibir_articulo.py` lo
convierte al `.tex` camera-ready, lo compila con `componer.sh` y lo mide con
`geometria.py`. Ver `taller/LEEME.md` para el contrato completo (heurística
de `\APMtype`, qué campos quedan `[PENDIENTE: ...]` cuando el manuscrito no
los trae, y las cuatro correcciones que la propia verificación encontró:
orden del escapado LaTeX, `\APMtitleEN[]` con corchete vacío, ancho de
columna de tabla, y pie de tabla/figura duplicado).

Sin `--numero`, la carpeta de destino se calcula de la fecha de hoy con la
tabla de arriba (Vol=Año-2020, período por mes) — el flujo normal desde
Cowork no exige que nadie calcule a mano en qué número cae un artículo
recibido hoy.

## Cómo se arma el número completo — `taller/armar_numero.py`

Toma todos los artículos ya compilados de `numeros/<NUMERO>/` (los que
tengan su PDF `*_APM_<NUMERO>_*.pdf`; una carpeta sin PDF se salta con
aviso, no truena) y produce `numeros/<NUMERO>/REVISTA_<NUMERO>.pdf`: portada
(con la imagen que se le dé, o `logo_hires.png` de respaldo) + tabla de
contenido con página inicial medida + cada artículo, concatenados con
`pikepdf`. El tope de 600 KB de `geometria.py` es por artículo individual;
sobre el PDF del número completo es solo un aviso, no una falla.

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
