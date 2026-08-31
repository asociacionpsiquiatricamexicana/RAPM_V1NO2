# Paleta, tipografía y geometría de página

Todos los valores de este documento fueron verificados línea por línea contra `assets/apm-editorial.cls` (no contra prompts históricos). Si algo cambia en el `.cls`, actualiza primero el código y luego este archivo.

## Paleta de colores (WCAG AA/AAA)

```
Borgoña APM:     #8B1A2B   (8.8:1 WCAG AAA)  — Títulos, reglas, H1/H2, badge DOI
Borgoña oscuro:  #8B0027   (9.9:1)           — Drop cap, URLs
Gris carbón:     #2D2D2D   (14.4:1)          — Body text, "Editorial", autor
Gris medio:      #666666   (5.7:1)           — Metadata, footer, headers P2+
Gris claro:      #E8E8E8                     — Separadores, regla colofón
Rosado tenue:    #FEF8F8                     — Fondo caja RESUMEN
Borde rosado:    #D9B5B9                     — Borde caja RESUMEN
Azul enlace:     #1A5276   (7.5:1)           — Reservado, NO en uso actual (no lo actives sin confirmar con el editor)
```

**Regla absoluta:** URLs en borgoña oscuro (#8B0027). Nunca azul en el body. Todo color de texto debe cumplir WCAG AA (≥4.5:1 contra blanco); fórmula y script en `05_workflow_produccion_y_diagnostico.md`.

Advertencia histórica: versiones anteriores del proyecto usaron Rojo APM `#C41E3A` como color primario (5.8:1, apenas AA) y colores de fondo/borde distintos (`#F8F5F2`, `#FDF2F2`). Esos valores fueron descartados por el editor a favor de la paleta de arriba. Si ves `#C41E3A` en algún documento de referencia antiguo, ignóralo.

## Geometría de página

```
Papel:              Letterpaper 612×792pt (215.9×279.4mm) — NUNCA a4paper
Margen izquierdo:   1.8cm (51.0pt)
Margen derecho:     1.8cm (51.0pt)
Margen superior:    2.0cm (56.7pt)
Margen inferior:    1.8cm (51.0pt)
Columnsep (gutter): 5mm (14.2pt)
Headheight:         14pt
Headsep:            8pt
```

Guías de maquetación: activar con `\APMenableguides` antes de `\begin{document}`. Muestra regla izquierda (cm 0–27), regla superior (cm 0–21), rectángulo rojo punteado (área de texto), línea azul (eje central), líneas verdes (bordes del gutter), etiquetas T/L/R/B en mm.

## Tipografía completa

```
Título artículo:   Georgia (ptm) 14/18pt bold borgoña, centrado, Title Case APA 7.ª
"Editorial" label: Georgia (ptm) 12/15pt bold carbón, centrado
H1 (secciones):    Sans-serif 9.5/12pt bold UPPERCASE borgoña, línea propia
H2 (subsecciones): Sans-serif 9/11pt bold italic borgoña, línea propia
H3:                Sans-serif 8.5/11pt bold carbón, línea propia
Body text:         Georgia (ptm) 10pt regular carbón
Autor:             Georgia (ptm) 10.5/13pt bold carbón, centrado
Afiliación:        Sans-serif 7.5/10pt regular gris medio, centrado
Metadata:          Sans-serif 7/9.5pt regular gris medio, centrado
RESUMEN label:     Sans-serif 7.5/9pt bold borgoña
RESUMEN body:      Sans-serif 8/11pt regular carbón, justificado
Palabras clave:    Sans-serif 7.5/10pt: "Palabras clave:" bold + términos gris medio
REFERENCIAS label: Sans-serif 9.5/12pt bold borgoña (mismo que H1)
Refs entries:      Serif 7.5/10pt regular carbón, raggedright, hanging indent 12pt
Footer:            Sans-serif 7/9pt regular gris medio
Header P2+:        Sans-serif 7/9pt regular gris medio
Drop cap:          Georgia 3 líneas bold borgoña oscuro
Colofón:           Sans-serif 7/9.5pt regular gris medio
```

Nota: "Georgia" aquí es un alias de trabajo para `mathptmx`/Times (ptm) — pdfLaTeX no tiene Georgia real. No intentes cargar Georgia con `fontspec`; el proyecto usa `pdflatex`, no `lualatex`/`xelatex`.

### Parámetros de párrafo
```
parindent: 1em
parskip:   0pt
```
Deben fijarse UNA sola vez, dentro de `\makeAPMeditorial` (o equivalente). Si aparecen en más de un lugar del `.cls`, es un bug — ver `10_checklist_auditoria_codigo.md`.

### Microtype
```
Protrusion:          habilitado (puntuación extiende ±1pt al margen)
Expansion:           habilitado (glifos ±1%)
Small caps tracking:  50/1000em
Kerning extra:       em-dash=200, en-dash=250, comillas=400
```

### Control de viudas/huérfanas
```
widowpenalty:         10000 (prohibición absoluta)
clubpenalty:          10000
brokenpenalty:        4991
doublehyphendemerits: 10000 (nunca 2 líneas seguidas con guión)
finalhyphendemerits:  5000
hyphenpenalty:        50
tolerance:            200
pretolerance:         100
```

## Elementos eliminados (no deben aparecer)

- Folio ("Folio: APM-..."). Nota técnica: el comando `\APMfolio{}` sigue existiendo en el `.cls` y algunos `.tex` lo siguen llamando, pero no tiene ningún efecto visible — es código muerto, no lo uses como si funcionara. Ver `09_limitaciones_conocidas.md`.
- Íconos FontAwesome en metadata (faOrcid, faEnvelope, faPhone, etc.) — el paquete `fontawesome5` sigue cargado en el `.cls` para otros usos, pero no debe usarse para decorar la metadata del header.
- Logo del 60 aniversario en el header estándar — se usa solo "Revista APM". Nota técnica: `\APMlogoSixty{}` también es código muerto (setter sin render, igual que `\APMfolio`). `assets/logo_60anos.png` se conserva como archivo de marca, pero **no hay forma funcional de colocarlo en el PDF hoy** — requeriría escribir el código de render. Ver `09_limitaciones_conocidas.md` §3b.
