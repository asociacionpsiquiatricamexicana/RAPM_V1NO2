# Workflow de producción y diagnóstico de 14 capas

## Workflow de producción

```
PASO 1: Preparar .tex
  - \documentclass{apm-editorial} (usar assets/apm-editorial.cls)
  - Partir de assets/ejemplo_editorial.tex como plantilla, no desde cero
  - Configurar: \APMtitleEN, \APMauthor, \APMaffiliation, \APMdates, \APMvolume, \APMdoi, etc.
  - Agregar \pdfinfo{} con metadata en octal para UTF-8 (ver 03_estructura_manuscrito.md)
  - Insertar contenido con \section*, \subsection*, drop cap

PASO 2: Compilar
  - pdflatex -interaction=nonstopmode archivo.tex   (×2, para refs cruzadas y LastPage)
  - Verificar: 0 errores, 0 overfull (overfull en colofón es aceptable con \hfuzz)

PASO 3: Post-proceso
  - qpdf --linearize archivo.pdf archivo_final.pdf
  - Verificar tamaño < 600KB

PASO 4: Diagnóstico de 14 capas (A–N, ver abajo)

PASO 5: Reporte técnico
  - Generar reporte con mediciones reales del PDF (no estimaciones)
  - Archivar en la carpeta del artículo

PASO 6: Deploy
  - Nomenclatura: PRIMERAPALABRA_APM_VOL#_NO#_AÑO.pdf
  - Carpeta: VOL#_NO#_ART#_PRIMERAPALABRA/
  - Ejemplo: NEUROMODULACION_APM_VOL5_NO2_2025.pdf en VOL5_NO2_ART1_NEUROMODULACION/
```

## Diagnóstico de 14 capas (A–N)

Cada capa exige mediciones reales extraídas del PDF (PyMuPDF/pdfplumber/pikepdf), no estimaciones visuales.

**Estado del script:** `scripts/diagnostico_rapm.py` automatiza únicamente **A, B (parcial), M y N**. Las capas **C–L siguen sin implementar** — hay que medirlas a mano con pdfplumber sobre las coordenadas del layout, o extender el script. No emitas un veredicto "APTO PARA PRODUCCIÓN" con solo la salida del script: cubre 4 de 14 capas.

| Capa | Qué verifica | Herramienta preferida |
|---|---|---|
| A. Ficha del artículo | Título, tipo, autores, vol/no/año, DOI, ORCID, idioma, páginas, tamaño | pdfinfo + texto P1 |
| B. Página y geometría | Papel 612×792pt, márgenes (51.0/51.0/56.7/51.0pt), gutter 14.2pt | pdfplumber |
| C. Logo y DOI | Alineación logo-DOI Δ < 1.0pt, logo en margen izq., DOI en margen der. | fitz `get_image_rects()` + pdfplumber |
| D. Reglas decorativas | Posición Y, color hex (#8B1A2B / #D9B5B9), ancho, si cruza el gutter | pdfplumber `lines`/`rects` |
| E. Header P1 | Presencia de los 10 elementos obligatorios; ausencia de Folio e íconos | pdfplumber texto |
| F. Caja de RESUMEN | bg #FEF8F8, borde #D9B5B9, roundcorner 3pt, padding 10/7pt | pdfplumber `rects` (curvas no siempre detectables — verificar en el `.cls` si hay duda) |
| G. Columnas | Simetría izq/der (Δ≤2pt), gutter real ~14pt, ningún heading comparte línea Y con body de la otra columna | pdfplumber por rangos de Y |
| H. Headings | H1 UPPERCASE bold, H2 bold italic, H3 bold, cada uno en línea propia | pdfplumber texto + tamaño de fuente |
| I. Footer | Idéntico en todas las páginas salvo número, regla borgoña arriba | fitz (footer es texto pequeño — usar PyMuPDF, no pdfplumber, ver FM21) |
| J. Running heads P2+ | LE/RO/RE-LO correctos, 7/9pt, gris medio, regla borgoña debajo | fitz |
| K. Referencias | Tamaño 7.5/10pt, raggedright, hanging indent, regla ≤0.95×columnwidth | pdfplumber |
| L. Colofón | Ortografía ("No Comercial"), sin sangría, presencia de los 4 bloques | pdfplumber texto |
| M. Fonts y metadata | Fuentes embebidas, sin CM leak, los 5 campos de metadata presentes | `pdffonts` + pikepdf |
| N. WCAG AA | Contraste ≥4.5:1 para cada color de texto contra fondo | fórmula abajo |

## Fórmula de contraste WCAG AA

```python
def luminancia(r, g, b):
    rs, gs, bs = [x/255 for x in (r, g, b)]
    rs = rs/12.92 if rs <= 0.03928 else ((rs+0.055)/1.055)**2.4
    gs = gs/12.92 if gs <= 0.03928 else ((gs+0.055)/1.055)**2.4
    bs = bs/12.92 if bs <= 0.03928 else ((bs+0.055)/1.055)**2.4
    return 0.2126*rs + 0.7152*gs + 0.0722*bs

def contraste(c1, c2):
    l1, l2 = luminancia(*c1), luminancia(*c2)
    return (max(l1,l2)+0.05) / (min(l1,l2)+0.05)
# ≥4.5:1 para texto normal, ≥3:1 para texto grande (>14pt bold)
```

## Herramientas

```
Python:
  pdfplumber     — Caracteres, líneas, rects, posiciones, mediciones
  fitz (PyMuPDF) — Imágenes, texto rápido, footer/small text (mejor que pdfplumber, ver FM21)
  pikepdf        — Metadata, hyperlinks, estructura PDF

CLI:
  pdflatex       — Compilación
  qpdf           — Linearización, validación (--check, --linearize)
  pdffonts       — Lista de fuentes embebidas
  pdfinfo        — Info general del PDF
  pdftoppm       — Renderizado a imagen para inspección visual (400+ DPI recomendado)
```

## Formato de salida del reporte técnico

```
═══════════════════════════════════════════════════════════════
  REPORTE TÉCNICO DE DIAGRAMAJE — RAPM
  [TÍTULO DEL ARTÍCULO]
  [FECHA DEL REPORTE]
═══════════════════════════════════════════════════════════════

A. FICHA DEL ARTÍCULO
   ...
B. PÁGINA Y GEOMETRÍA
   ... [tabla de mediciones vs spec, con desviación y cumple sí/no]
...
N. WCAG AA
   ...

═══════════════════════════════════════════════════════════════
  RESUMEN EJECUTIVO
═══════════════════════════════════════════════════════════════
  Conformes:     XX/XX
  Observaciones: X (severidad baja/media/alta)
  Bloqueantes:   X

  VEREDICTO: [APTO PARA PRODUCCIÓN / REQUIERE CORRECCIÓN / RECHAZADO]

  Detalle de observaciones:
  1. [Descripción — Severidad — Causa — Acción sugerida]
═══════════════════════════════════════════════════════════════
```

## Notas operativas

1. **Nunca aproximes.** Todas las mediciones deben ser reales, extraídas del PDF.
2. Las tolerancias existen porque microtype (protrusion/expansion) ajusta bordes ±1pt — es correcto y deseado, no lo marques como defecto.
3. `\enlargethispage` puede alterar el margen inferior de P1 — documentar, no marcar como error.
4. pdfplumber no detecta bien las curvas de `mdframed roundcorner` — si hay duda, verifica en el código `.cls` en vez de insistir en detectarlo del PDF.
5. El reporte es para el Editor Adjunto (Dr. Medina-Rodríguez). Lenguaje: español técnico, sin adornos.
6. Cada artículo publicado debe tener su reporte técnico archivado en la carpeta del artículo (junto al `.tex`, `.cls` y `.pdf`).

## Receta de build mínima

```bash
pdflatex -interaction=nonstopmode archivo.tex
pdflatex -interaction=nonstopmode archivo.tex
qpdf --linearize archivo.pdf archivo_final.pdf
```
