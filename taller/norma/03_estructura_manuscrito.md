# Estructura del manuscrito

## Primera página (de arriba a abajo)

```
1. [REVISTA APM logo LEFT] ←→ [DOI badge + URL RIGHT]
   Logo bottom y DOI baseline alineados a Δ ≤ 0.05pt
   Ambos a 3.7pt arriba de la regla decorativa
   Logo alineado al margen izquierdo (18mm)
   DOI alineado al margen derecho (18mm)

2. ━━━ REGLA DECORATIVA (borgoña 0.5pt, full textwidth) ━━━

3. "Editorial" — Georgia bold 12pt carbón, centrado
   (tipo de artículo — ver limitación en 09_limitaciones_conocidas.md:
   el header solo imprime "Editorial", no está conectado a \APMtype)

4. TÍTULO — Georgia bold 14/18pt borgoña, centrado, Title Case APA 7.ª
   Puede ser multilínea con \\ forzado

5. ━━━ REGLA DECORATIVA (borgoña 0.5pt) ━━━

6. Autor(es) — Georgia bold 10.5/13pt carbón, centrado
7. Afiliación(es) — sans-serif 7.5/10pt gris medio, centrado
8. email · teléfono — una línea, centrado, separados por ·
9. ORCID: https://orcid.org/XXXX-XXXX-XXXX-XXXX — centrado
10. Dirección completa — línea propia, centrada
11. Recibido: DD mes AAAA · Aceptado: DD mes AAAA · Publicado: DD mes AAAA
    — una sola línea, centrada, separados por ·
12. Artículo revisado por pares (doble ciego) — centrado

13. ┌─ RESUMEN ──── bg=#FEF8F8, borde=#D9B5B9, roundcorner=3pt ──┐
    │  Texto del resumen...                                        │
    │  Palabras clave: término1, término2, término3                │
    └──────────────────────────────────────────────────────────────┘

14. INTRODUCCIÓN (H1 inline, no \section*)
    Drop cap + body text en dos columnas
```

## Footer (idéntico en TODAS las páginas)

```
VOL. X · NO. X · PERÍODO AÑO    Página X de Y    CC BY-NC 4.0 · Open Access · e-ISSN 3061-7979
```
- [L]: VOL · NO · período año — [C]: Página X de Y (dinámico, `\thepage`/`\pageref{LastPage}`) — [R]: CC BY-NC 4.0 · Open Access · e-ISSN
- Regla borgoña 0.5pt arriba del footer, sans-serif 7/9pt gris medio.
- El footer NO incluye nombres del Editor/Editor Adjunto (versiones antiguas del proyecto los incluían; se retiraron).

## Running heads (P2+)

```
[LE] (par, izquierda):  Apellido(s) Autor (Año)
[RO] (impar, derecha):  Título abreviado (≤50 chars)
[RE/LO]:                VOL. X · NO. X
```
7/9pt gris medio, regla borgoña 0.5pt debajo. Requiere `twoside` en `\LoadClass` para que LE/RO funcionen (ya está fijado en el `.cls`).

## Reglas de headings

```
H1: UPPERCASE BOLD borgoña 9.5/12pt, línea propia, before=6pt after=4pt
H2: Bold Italic borgoña 9/11pt, línea propia, before=6pt after=4pt
H3: Bold carbón 8.5/11pt, línea propia, before=5pt after=3pt
```

**Regla crítica:** el body text negro NUNCA comparte línea Y con un heading borgoña. Siempre empieza en la línea siguiente.

INTRODUCCIÓN es caso especial: usa heading inline (`\noindent\fontsize{9.5}{12}...INTRODUCCIÓN\par`) en vez de `\section*`, con `\vspace{4pt}` antes del drop cap — esto minimiza el offset entre columnas inherente al `twocolumn`.

REFERENCIAS usa el mismo formato que H1. Regla decorativa a 0.95×columnwidth (no invade el gutter). Entries en 7.5/10pt, raggedright, hanging indent, parskip=1.5pt.

## Caja de RESUMEN

```
Background:   #FEF8F8 (rosado blanco tenue)
Border color: #D9B5B9 (mauve rosado suave) — \definecolor{creamborder}
Border width: 0.4pt
Esquinas:     roundcorner=3pt
Padding:      10pt lateral, 7pt vertical
Label:        "RESUMEN" sans-serif 7.5pt bold borgoña
Body:         sans-serif 8/11pt carbón, justificado, noindent
Keywords:     "Palabras clave:" bold + términos gris medio
```

## Colofón

```
Conflicto de intereses: [texto] (SIN sangría, \noindent)
Financiamiento: [texto]
Licencia: © AAAA El Autor. Publicado bajo Creative Commons Atribución-No Comercial 4.0 Internacional (CC BY-NC 4.0).
Contacto editorial: revistaapm@psiquiatrasapm.org.mx
```
"No Comercial" (dos palabras, con espacio — nunca "NoComercial"). Sans-serif 7/9.5pt gris medio. `\sloppy\tolerance=9999\emergencystretch=5em\hfuzz=15pt` para evitar overfull en texto largo inline.

## Metadata PDF

```
/Title:    Texto plano del título (sin LaTeX)
/Author:   Via \pdfinfo con codificación octal para UTF-8
/Keywords: Via \pdfinfo con codificación octal
/Subject:  "Editorial -- Revista APM Vol. X No. X, PERÍODO AÑO"
/Creator:  "LaTeX with apm-editorial.cls"
```

**Crítico:** pdfLaTeX no soporta UTF-8 directo en metadata PDF. Usar `\pdfinfo` con octal:
```latex
\pdfinfo{
  /Author (Jes\string\372s Alejandro Aldana L\string\363pez)
  /Keywords (Neuromodulaci\string\363n, Psiquiatr\string\355a)
}
```

Tabla de codificación octal:
```
á = \341    é = \351    í = \355    ó = \363    ú = \372
ñ = \361    ü = \374
```

Otro detalle verificado en el `.cls`: `pdflang` se fija una sola vez en `\hypersetup` (`pdflang={es-MX}`) — si lo duplicas en otro paquete (p. ej. babel) obtienes un warning de compilación (era el failure mode FM13).

## Árbol de secciones del manuscrito

```
FRONT MATTER:
  1. Logo + DOI                    [M]  header
  2. Tipo de artículo              [M]  meta
  3. Título (APA 7th Title Case)   [M]  dc:title
  4. Autor(es) + afiliaciones      [M]  dc:creator
  5. Correspondencia               [M]  meta
  6. ORCID                         [M]  meta
  7. Fechas                        [M]  dc:date
  8. Peer review                   [M]  meta
  9. Resumen / Abstract            [M*] jats:abstract
 10. Palabras clave / Keywords     [M]  meta

BODY (IMRaD para originales):
  H1  INTRODUCCIÓN                 [M]
  H1  MÉTODO                       [M]
      H2  Participantes            [M]
      H2  Instrumentos             [C]
      H2  Procedimiento            [M]
      H2  Análisis de datos        [M]
  H1  RESULTADOS                   [M]
  H1  DISCUSIÓN                    [M]
      H2  Limitaciones             [M]
  H1  CONCLUSIONES                 [M]

BACK MATTER:
 11. Agradecimientos               [O]
 12. Contribuciones (CRediT)       [M]
 13. Financiamiento                [M]
 14. Conflicto de intereses        [M]
 15. Disponibilidad de datos       [M]
 16. Uso de IA                     [C]
 17. Consentimiento / Ética        [C]
 18. Referencias (APA 7, DOI)      [M]  jats:ref-list
 19. Tablas                        [O]
 20. Figuras + alt text            [O]
 21. Material suplementario        [O]

[M]=Obligatorio  [O]=Opcional  [C]=Condicional
*Abstract no requerido para Editoriales y Cartas al Editor
```
