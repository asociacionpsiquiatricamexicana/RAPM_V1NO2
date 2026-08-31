# Taller editorial de la Revista

Aquí está lo que hace falta para producir un número de la *Revista de la
Asociación Psiquiátrica Mexicana, A.C.* desde cero, en cualquier máquina.
Hasta esta tanda, las herramientas vivían fuera del repositorio (en una
skill de cuenta, ya desactualizada): el camera-ready publicado no se podía
regenerar desde aquí. Esa es la primera lección heredada del taller del
libro de la Genealogía, y la razón de este directorio.

## Qué es cada cosa

- **`apm-editorial.cls`** — la clase LaTeX. **El código es la especificación**:
  cuando un documento diga otra cosa, gana el `.cls`. Hoy solo produce
  Editoriales (el rótulo va fijo en el encabezado); cualquier otro tipo de
  artículo es desarrollo nuevo, no configuración (véase
  `norma/09_limitaciones_conocidas.md`).
- **`ejemplo_editorial.tex`** — la plantilla base. Un artículo nuevo parte de
  aquí, nunca de cero.
- **`logo_hires.png` / `logo_60anos.png`** — los activos de cabecera. El del
  60 aniversario no tiene código de render funcional (norma/09, §3b).
- **`comprobar_entorno.sh`** — la prueba en frío. Se corre antes de comprometer
  un artículo; un fallo aquí es del entorno, no del manuscrito.
- **`componer.sh`** — la secuencia estándar en una orden: `pdflatex` ×2
  (cero errores, cero overfull), `qpdf --linearize`, y la sonda de geometría.
- **`sondas/`** — las comprobaciones sobre el PDF construido:

| Sonda | Qué mide |
| --- | --- |
| `geometria.py` | páginas, caja única, tipografías incrustadas, peso < 600 KB, contra su ancla |
| `reproducible.py` | que el ejemplo se recomponga idéntico desde lo versionado (compilación en limpio, hash del texto) |
| `diagnostico_rapm.py` | 4 de las 14 capas del diagnóstico histórico (A, B parcial, M, N); las demás piden medición dirigida |

- **`norma/`** — la norma editorial heredada (identidad, geometría, estructura,
  24 modos de fallo, APA 7, preferencias del editor). Datada al 28 de agosto
  de 2026: describe el sistema tal como era antes de este taller; ante
  divergencia, gana el `.cls` y gana la medición.

## Cómo se trabaja (las lecciones del libro, aplicadas aquí)

1. **Verificar es medir el archivo, no leer el código.** Toda afirmación sobre
   el PDF (márgenes, páginas, peso, tipografías) sale de una sonda, nunca de
   memoria ni de inspección visual.
2. **Las cifras van ancladas.** `sondas/*_referencia.txt` guarda lo esperado;
   una sonda avisa cuando la realidad se mueve, en los dos sentidos. El ancla
   solo se mueve con razón declarada en el registro.
3. **Una tanda, un commit.** Un artículo (o un cambio de clase) se decide, se
   aplica, se compila, se mide y se asienta junto, en
   `../REGISTRO_DE_PRODUCCION.md`: qué cambió, cómo se comprobó, qué quedó
   declarado sin resolver.
4. **No se toca el texto de los autores.** La capa cero de la revista: erratas
   de contenido se devuelven al autor o se anotan, no se corrigen en silencio
   al diagramar. Las citas y referencias se verifican contra APA 7
   (`norma/07_checklist_apa7.md`), y toda corrección se declara.
5. **Lo que no se puede regenerar desde el repositorio no existe.**
   `reproducible.py` lo vigila para el ejemplo; cada artículo publicado deja
   su `.tex` y su reporte junto al PDF en `../numeros/`.

## Trampas conocidas

- `pdflatex` necesita **dos pasadas** (totpages y referencias cruzadas): el
  ejemplo da 3 páginas con una pasada y **2** con las dos. La cifra buena es 2.
- Motor: **pdfLaTeX** (TeX Live 2023+). Nunca lualatex sin verificar
  `luatexbase.sty`.
- `\pdfinfo{}` va en octal para UTF-8 (acentos rotos en los metadatos si no).
- Los dos paquetes que faltan en un entorno recién levantado:
  `texlive-lang-spanish` y `texlive-fonts-extra` — el hook de arranque los
  instala en el entorno remoto.
