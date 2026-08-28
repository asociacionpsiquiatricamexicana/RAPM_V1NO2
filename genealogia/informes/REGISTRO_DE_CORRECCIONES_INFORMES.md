# Registro de correcciones · informe del barrido léxico y fichero bibliográfico

**Norma aplicada:** OLE 2010 y actualizaciones RAE-ASALE · NGLE · DTM · FundéuRAE · Martínez de Sousa · APA 7 en español

---

## 1. Informe del barrido léxico

Texto de clase **correspondencia formal**: intervención de normalización y registro, sin tocar
dato alguno. Cuatro correcciones.

### 1.1 Saludo de carta

El saludo corría en la misma línea que el cuerpo y en minúscula:

> Estimado doctor Saucedo: me permito informarle de la revisión…

En correspondencia formal el saludo cierra con dos puntos y el cuerpo abre en la línea
siguiente, con mayúscula:

> Estimado doctor Saucedo:
>
> Me permito informarle de la revisión…

### 1.2 Latinismo crudo sin cursiva

En el recuento, «de la más antigua a la más reciente» como criterio de orden del
**in memoriam** → *in memoriam*. Latinismo crudo: cursiva obligatoria. Es la misma corrección
aplicada en los tres lugares equivalentes del volumen.

### 1.3 Cifra en guarismos dentro de una serie deletreada

El informe deletrea sistemáticamente toda cantidad: «sesenta y una secciones», «los cuatro
capítulos», «las treinta fichas», «las catorce piezas», «cincuenta usos de treinta y dos
formas», «una treintena», «las siete coincidencias», «cuatro usos». Una sola cantidad iba en
guarismos, y además dentro de la misma oración que «sesenta y una»:

> …es decir, las **283** páginas del volumen (folios 1-262).

Corregido a **doscientas ochenta y tres**. El intervalo de folios se conserva en guarismos: es
identificador de serie, no cantidad.

### 1.4 Palabras mencionadas como tales, sin marca

Dos enumeraciones iban en redonda mientras el resto del documento marca la mención con
comillas latinas. La misma palabra recibía dos tratamientos a dos páginas de distancia:
*sumamente* en redonda en la página 1 y «sumamente» entrecomillada en la página 2.

Ambas enumeraciones pasan a cursiva, que es la marca que la norma reserva a la palabra
mencionada como tal:

- los intensificadores: *muy*, *tan*, *sumamente*, *considerable*, *notable*, *significativo*,
  *sin duda*, *desde luego*, *por supuesto*;
- el léxico proscrito: *robusto*, *optimizar*, *innovador*, *eficiente*, *sinergia*, *impacto*,
  *relevante*, *paradigma*, *empoderar*, *severidad*, *implementar*.

Se conservan sin tocar las comillas latinas ya existentes en el resto del documento
(«-mente», «el más», «-ísimo», «darse por supuesto», «a través de»…): son decisión del autor
y no se uniforman en sentido contrario.

### Lo que no se tocó

Los verbos sin conjugar que abren las secciones «Cuándo» y «Dónde» («El 27 de agosto de
2026…», «Las sesenta y una secciones fuente…») son respuestas nominales a la pregunta del
epígrafe y cumplen función: se conservan. Se conservan también todas las citas del volumen
entrecomilladas, las etiquetas de repositorio (v84), el identificador de hallazgo (H-167) y
cuantas cifras contiene el recuento.

---

## 2. Fichero bibliográfico

**Sin correcciones.** Las ciento sesenta fichas son asientos bibliográficos: capa intangible por
norma del pipeline, y el propio cuaderno lo declara en su cabecera («Cada ficha reproduce su
entrada sin alteración»). No se altera ni la puntuación de formato.

La prosa propia del cuaderno se reduce al párrafo de cabecera, que se revisó y quedó conforme.

Se comprobó la única coherencia interna verificable sin acudir a los ejemplares: el cuaderno
anuncia ciento sesenta entradas únicas y numera hasta FICHA 160.

---

## 3. Discrepancia que obliga a rectificar el volumen

El informe fija la extensión de la obra:

> …es decir, las doscientas ochenta y tres páginas del volumen (folios 1-262).

El flipbook publicado en este mismo repositorio llevaba «páginas» sin cifra en la portada y en
la ficha de catalogación. En ausencia de otra fuente se había rellenado con **268**, medida
sobre la composición del propio flipbook. El informe del compilador es mejor autoridad que esa
medición: la obra canónica se compone con XeLaTeX sobre la clase memoir, y es esa composición
la que el asiento describe.

Ambos lugares quedan corregidos a **283 páginas**. Si la cifra definitiva fuera otra, procede
sustituirla en los bloques 1 y 32 del volumen.

---

## 4. Lo que no fue posible hacer

Los dos documentos llegaron como PDF ya compuestos, sin sus fuentes LaTeX. Este entorno no
tiene distribución de TeX instalada, de modo que no se regeneraron los PDF: reconstruir su
diseño (los recuadros con rótulo al filo, la versalita del título, la caja de texto) sin la
clase original habría producido un documento distinto, no el mismo documento corregido.

Lo que aquí consta es el texto corregido y la razón de cada cambio. Con las fuentes `.tex` a la
vista, la corrección se aplica sobre ellas y el PDF vuelve a compilarse sin pérdida de diseño.
