# Taller editorial de la Revista

Aquí está lo que hace falta para producir un número de la _Revista de la
Asociación Psiquiátrica Mexicana, A.C._ desde cero, en cualquier máquina.
Hasta esta tanda, las herramientas vivían fuera del repositorio (en una
skill de cuenta, ya desactualizada): el camera-ready publicado no se podía
regenerar desde aquí. Esa es la primera lección heredada del taller del
libro de la Genealogía, y la razón de este directorio.

## Qué es cada cosa

- **`apm-editorial.cls`** — la clase LaTeX. **El código es la especificación**:
  cuando un documento diga otra cosa, gana el `.cls`. Rotula los seis tipos de
  artículo vía `\APMtype{}`, y tiene dos disposiciones de cuerpo medidas: el
  texto corto sin resumen y el artículo largo con IMRaD, tabla y figura (véase
  `norma/09_limitaciones_conocidas.md`).
- **`ejemplo_editorial.tex`** — la plantilla de un texto corto sin resumen
  (Editorial, Carta al Editor). Un artículo nuevo parte de aquí, nunca de cero.
- **`ejemplo_articulo_original.tex`** — la plantilla de un artículo largo con
  estructura IMRaD, resumen, subsecciones, tabla y figura a ancho de página.
  Es un fixture de diagramación: los autores, las cifras y los resultados son
  inventados y no deben reutilizarse como material editorial.
- **`logo_hires.png` / `logo_60anos.png`** — los activos de cabecera. El del
  60 aniversario no tiene código de render funcional (norma/09, §3b).
- **`comprobar_entorno.sh`** — la prueba en frío. Se corre antes de comprometer
  un artículo; un fallo aquí es del entorno, no del manuscrito.
- **`componer.sh`** — la secuencia estándar en una orden: `pdflatex` ×2
  (cero errores, cero overfull), `qpdf --linearize`, y la sonda de geometría.
- **`sondas/`** — las comprobaciones sobre el PDF construido. Ambas toman el
  documento como argumento y cada documento tiene su propia ancla
  (`geometria_<base>.txt`, `reproducible_<base>.txt`); sin argumento trabajan
  sobre el editorial:

| Sonda                 | Qué mide                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------ |
| `geometria.py`        | páginas, caja única, tipografías incrustadas, fuga de Computer Modern (FM06), peso < 600 KB, contra su ancla |
| `reproducible.py`     | que el ejemplo se recomponga idéntico desde lo versionado (compilación en limpio, hash del texto)            |
| `diagnostico_rapm.py` | 4 de las 14 capas del diagnóstico histórico (A, B parcial, M, N); las demás piden medición dirigida          |

- **`norma/`** — la norma editorial heredada (identidad, geometría, estructura,
  24 modos de fallo, APA 7, preferencias del editor). Datada al 28 de agosto
  de 2026: describe el sistema tal como era antes de este taller; ante
  divergencia, gana el `.cls` y gana la medición.

## Cómo se trabaja (las lecciones del libro, aplicadas aquí)

1. **Verificar es medir el archivo, no leer el código.** Toda afirmación sobre
   el PDF (márgenes, páginas, peso, tipografías) sale de una sonda, nunca de
   memoria ni de inspección visual.
2. **Las cifras van ancladas.** `sondas/geometria_<base>.txt` y
   `sondas/reproducible_<base>.txt` guardan lo esperado de cada documento;
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
   `reproducible.py` lo vigila para los ejemplos; cada artículo publicado deja
   su `.tex` y su reporte junto al PDF en `../numeros/`.

## Trampas conocidas

- `pdflatex` necesita **dos pasadas** (totpages y referencias cruzadas): el
  ejemplo da 3 páginas con una pasada y **2** con las dos. La cifra buena es 2.
- Motor: **pdfLaTeX** (TeX Live 2023+). Nunca lualatex sin verificar
  `luatexbase.sty`.
- `\pdfinfo{}` va en octal para UTF-8 (acentos rotos en los metadatos si no).
- `\APMrefsbreak` **no** se usa por conteo de referencias, pese a lo que dice
  el comentario del `.cls`. Parte donde caiga el corte de columna, no donde
  esté la mitad de la lista: en el artículo original, partir por la mitad de
  14 referencias dejó una columna casi vacía y **costó una página entera**
  (5 en vez de 4). Si las referencias no arrancan al tope de una columna,
  deja que fluyan y que `flushend` equilibre.
- babel-español rotula las tablas «Cuadro». La clase lo fuerza a «Tabla»
  (APA 7) enganchándose a `\captionsspanish`; un `\renewcommand{\tablename}`
  suelto no sirve, lo pisa `\selectlanguage{spanish}`.
- Los dos paquetes que faltan en un entorno recién levantado:
  `texlive-lang-spanish` y `texlive-fonts-extra` — el hook de arranque los
  instala en el entorno remoto.
- **Nada de modo matemático para signos de texto.** El separador de las
  cabeceras y del colofón era `$\cdot$`: `mathptmx` remapea casi todo a
  `ztmcm`, pero ese símbolo vive en codificación OMS y caía a `cmsy10`,
  metiendo Computer Modern en un diseño Times/Nimbus (FM06) en todos los
  PDFs. Va `\textperiodcentered`, que es el mismo glifo en modo texto y lo
  trae la propia Nimbus. `geometria.py` ya vigila la fuga: estar incrustada
  no basta, una CM aquí es defecto de composición.
- Las sondas piden `pypdfium2` (dura), y `pdfplumber`, `pymupdf` y `pikepdf`
  para las capas B y M del diagnóstico. Ojo con el `cryptography` de Debian:
  si `import pdfplumber` revienta con un panic de pyo3, se repara con
  `pip install --ignore-installed cryptography`. Y `pymupdf` se importa por
  su nombre nuevo: el alias viejo `fitz` escupe su aviso de obsolescencia
  por **stdout** y corrompe el JSON del diagnóstico.
