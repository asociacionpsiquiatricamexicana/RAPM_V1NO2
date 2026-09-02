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
  texto corto y el artículo largo con IMRaD, tabla y figura (véase
  `norma/09_limitaciones_conocidas.md`).
- **`ejemplo_editorial.tex`** — la plantilla de un texto corto (Editorial,
  Carta al Editor; la norma no les exige resumen, y la caja solo se imprime
  si `\APMabstract{}` trae texto: este ejemplo lo trae). Un artículo nuevo
  parte de aquí, nunca de cero.
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
- **`recibir_articulo.py`** — recibe el manuscrito `.docx` del autor y
  produce el `.tex` camera-ready, compilado y medido. Nadie escribe LaTeX a
  mano. Ver la sección propia más abajo.
- **`armar_numero.py`** — toma todos los artículos ya compilados de un
  número y produce el PDF del número completo: portada, tabla de contenido y
  cada artículo, concatenados. Ver la sección propia más abajo.
- **`manuscrito_desde_md.py`** — el puente para cuando el material no llegó
  en Word: un Markdown reconstruido (desde un PDF, fotos de hojas, un
  dictado ya transcrito o datos sueltos) se convierte en el `.docx` que
  `recibir_articulo.py` sabe leer. El `.md` queda como fuente auditable de
  la reconstrucción — el repositorio exige poder regenerar lo entregado, y
  «lo dijo la conversación» no es una fuente. Dos zonas donde cada renglón
  es una unidad y no se unen entre sí: el bloque de cabecera (autor,
  afiliación, correo, ORCID son campos distintos) y la lista de
  referencias; en el cuerpo sí se unen, para que la prosa fluya.

## De un `.docx` al número completo

Esto es lo que hace posible que producir un número no exija que nadie
escriba una línea de LaTeX ni sepa qué es `apm-editorial.cls`: se anexa el
manuscrito del autor en Word y, opcionalmente, una imagen de portada, y el
resto es automático.

```
python3 taller/recibir_articulo.py MANUSCRITO.docx
    [--tipo "Artículo original"]   # fuerza \APMtype; por omisión, heurística
    [--numero VOL6_NO3]            # carpeta destino; por omisión, la de HOY
    [--raiz numeros/]              # por omisión numeros/ desde la raíz del repo
    [--art N]                      # ART# a usar; por omisión, el siguiente libre

python3 taller/armar_numero.py NUMERO
    [--raiz numeros/]
    [--portada RUTA_IMAGEN]        # por omisión, logo_hires.png
```

`recibir_articulo.py` extrae del `.docx`, en el orden real del documento
(no por separado — texto, tablas e imágenes intercalados se pierden si se
iteran aparte): título, autores, afiliación, ORCID/correo/teléfono,
resumen, palabras clave, cuerpo (encabezados de Word → `\section*`/
`\subsection*`), tablas (→ `booktabs`, `table`/`table*` según ancho),
figuras incrustadas (→ `figure`/`figure*`), y referencias (envueltas
literales en `\APMref{}` — **nunca reformateadas ni reordenadas**: no es
tarea del receptor corregir APA 7, solo diagramar lo que el autor entregó).
La heurística de `\APMtype` y qué se hizo con cada campo quedan declarados
en `reporte_tecnico.md`, junto al `.tex` y al PDF. Un dato editorial que el
manuscrito no trae (fechas de aceptación/publicación, DOI, ORCID,
conflicto de intereses, financiamiento) se deja como
`[PENDIENTE: ...]`, nunca inventado — ver `norma/01_identidad_tipos_articulo.md`
para la heurística completa de `\APMtype`.

Si el manuscrito no tiene NINGÚN encabezado de sección y su cuerpo es
demasiado corto para distinguirlo de una línea de afiliación, el script se
niega a producir un PDF con el cuerpo en blanco: falla con un mensaje que
pide un encabezado o un párrafo más largo, en vez de fabricar un artículo
que parece terminado y no lo está.

`armar_numero.py` **no recompone ni re-pagina** cada artículo (decisión en
`norma/06_gestion_volumenes_numeros.md`): es una concatenación con
`pikepdf` de portada+contenido (generada aparte, con la misma paleta y
geometría que `apm-editorial.cls`, medida — nunca asumida — para calcular
la página inicial real de cada artículo) más cada PDF camera-ready tal
cual. El tope de 600 KB de `geometria.py` es por artículo individual; sobre
el número completo es solo un aviso.

- **`prueba_intake/`** — el fixture de regresión de `recibir_articulo.py`:
  `generar_manuscrito_prueba.py` construye con `python-docx` un manuscrito
  sintético (IMRaD completo, tabla, figura, ~10 referencias) y lo escribe
  como `manuscrito_prueba.docx`, que queda commiteado — igual que
  `ejemplo_articulo_original.tex` es el fixture del `.cls`, este es el
  fixture del receptor. Datos inventados, rotulados como tales en el propio
  `.docx`: no reutilizar como material editorial.

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
- `\APMrefsbreak` **no** se usa por conteo de referencias (el comentario del
  `.cls` ya dice lo mismo). Parte donde caiga el corte de columna, no donde
  esté la mitad de la lista: en el artículo original, partir por la mitad de
  14 referencias dejó una columna casi vacía y **costó una página entera**
  (5 en vez de 4). Si las referencias no arrancan al tope de una columna,
  deja que fluyan y que `flushend` equilibre. Y el macro reabre el grupo con
  los mismos ajustes que `\APMrefsstart`: hasta el 1 de septiembre de 2026
  olvidaba `\sloppy\raggedright`, y las referencias tras el corte salían
  justificadas mientras las de antes iban en bandera.
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
  para el diagnóstico. Las cuatro están en `sondas/requisitos.txt`
  (`pip install -r`); el hook de arranque las instala en el entorno remoto
  cuando faltan. Ojo con el `cryptography` de Debian:
  si `import pdfplumber` revienta con un panic de pyo3, se repara con
  `pip install --ignore-installed cryptography`. Y `pymupdf` se importa por
  su nombre nuevo: el alias viejo `fitz` escupe su aviso de obsolescencia
  por **stdout** y corrompe el JSON del diagnóstico.
- **`recibir_articulo.py` necesita `python-docx`** (`sondas/requisitos.txt`,
  el hook la instala igual que las de las sondas).
- Sin ningún encabezado de sección "Resumen" ni ningún otro, el barrido de
  metadatos de contacto (afiliación/ORCID/correo/teléfono) no tenía dónde
  parar y se comía el manuscrito entero — el cuerpo quedaba vacío,
  disfrazado de `\APMaffiliation{}`. Corregido con dos topes: cualquier
  encabezado (no solo "Resumen") cierra el bloque de contacto, y sin
  ningún encabezado, un párrafo que "parece cuerpo" (largo, o con dos o
  más oraciones) o el cupo de líneas de afiliación lo cierra igual. Si aun
  así el cuerpo queda vacío, el script se niega a producir el PDF (arriba).
- El escapado de LaTeX debe sustituir `\` por una marca temporal antes de
  escapar `{`/`}`, no por `\textbackslash{}` directamente: si no, las
  llaves recién insertadas se vuelven a escapar y `\textbf{}` sale como
  `\textbackslash\{\}`.
- `\APMtitleEN[]{...}` con el corchete opcional **vacío** deja `pdftitle`
  en blanco pese al fallback documentado en el `.cls`
  (`\ifx\@apmtitleMeta\empty\@apmtitleEN\else...`) — verificado compilando
  un `.tex` mínimo. `recibir_articulo.py` no depende de ese fallback:
  siempre rellena el corchete con una versión plana del título.
- El ancho de columna de una tabla debe restar `\tabcolsep` (6pt) de cada
  lado de cada columna antes de dividir el ancho disponible, o produce
  Overfull en cualquier tabla de 4+ columnas.
- `\caption{}` ya antepone «Tabla N:»/«Figura N:» (vía `captionsspanish`):
  si el párrafo-pie del `.docx` también empieza con «Tabla 1.», hay que
  retirar ese rótulo antes de pasarlo a `\caption{}`, o sale duplicado.
