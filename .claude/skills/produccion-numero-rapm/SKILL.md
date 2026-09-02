---
name: produccion-numero-rapm
description: Produce artículos camera-ready y el número completo de la Revista de la Asociación Psiquiátrica Mexicana, A.C. (RAPM) a partir del material que llegue — un .docx, un PDF, fotos o escaneos de hojas, un dictado ya transcrito, o un montón de datos sueltos —, reconstruyendo el manuscrito, preguntando lo que falte en vez de inventarlo, y compilando con taller/recibir_articulo.py y taller/armar_numero.py sin que nadie escriba LaTeX. Actívala en cuanto el usuario entregue material que sea (o contenga) un artículo para la revista, aunque no lo pida explícitamente ("aquí está lo del Dr. X", "esto llegó para el número", "ahí te van los datos"), y también cuando pida componer, diagramar, armar o actualizar un artículo, un número o la revista.
---

# Producción de un número de RAPM a partir de cualquier material

## Qué hace esta skill y por qué

El taller (`taller/`) ya convierte un manuscrito en artículo camera-ready y
junta los artículos en el número. Lo que esta skill agrega es el criterio
para el paso de antes: **el material real no siempre llega como un Word
limpio**. Llega como un PDF, como fotos de hojas impresas, como un dictado
transcrito, como un correo con los datos desperdigados, o como varias cosas
a la vez. Tu trabajo es entender ese material, reconstruir el manuscrito con
él, y solo entonces alimentar el pipeline.

La regla que gobierna todo esto: **deducir lo que se puede sostener,
preguntar lo que no, y no inventar nunca.** Reconstruir no es redactar. Si
del material se desprende con claridad cuál es el título, quiénes firman y
dónde empieza el método, eso se usa. Si algo no se desprende —falta la
afiliación, la tabla está cortada en la foto, no se entiende si dos párrafos
son uno o dos—, se pregunta. Rellenar un hueco con algo verosímil es el peor
resultado posible: produce un artículo que parece completo y no lo es, y en
una revista científica eso llega hasta el lector.

## Reglas de casa que esta skill hereda

De `.claude/CLAUDE.md`, no negociables:

- **No se toca el texto de los autores.** Ni al reconstruirlo. Transcribir
  desde una foto o un PDF es copiar, no editar: se conservan las palabras,
  la ortografía y las cifras tal como están. Si algo parece una errata o un
  dato imposible (una fecha que no existe, una dosis fuera de rango, una
  cifra que no cuadra con su tabla), se **señala** al usuario, no se corrige
  en silencio.
- **El código es la especificación.** `taller/apm-editorial.cls` manda.
  Nunca edites a mano el `.tex` que genera el pipeline.
- **Verificar es medir el PDF construido.** Los scripts corren `componer.sh`
  y las sondas por su cuenta; si terminan sin error, ya está medido.

## De qué formatos puedes partir, realmente

Esto es lo que este entorno sí puede leer. No prometas más:

| Material                      | Cómo lo lees                                                                                                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.docx` de Word               | Va directo al pipeline (paso 3), sin reconstrucción                                                                                                                      |
| PDF con texto                 | `pdftotext archivo.pdf -` o `pdfplumber`/`pymupdf`                                                                                                                       |
| PDF escaneado (imágenes)      | `pdftoppm -png -r 150 archivo.pdf pag` y lee los PNG con visión                                                                                                          |
| Fotos, capturas, escaneos     | Léelos directamente con visión                                                                                                                                           |
| Dictado                       | Solo si ya viene **transcrito como texto**. No hay whisper ni ffmpeg aquí: un archivo de audio no se puede transcribir en este entorno — dilo claramente y pide el texto |
| Datos sueltos, correos, notas | Léelos y organiza lo que haya                                                                                                                                            |

Cuando llegan varias piezas a la vez (el cuerpo en un PDF, las tablas en
fotos, los datos del autor en un mensaje), trátalas como un solo expediente:
léelas todas primero, arma el cuadro completo, y recién entonces decide qué
falta. No proceses pieza por pieza preguntando a cada paso — eso convierte
un envío en un interrogatorio.

## Flujo de trabajo

### 1. Lee todo el material antes de decidir nada

Junta las piezas y léelas completas. Al terminar deberías poder responder:
cuál es el título, quiénes firman, con qué afiliación y contacto, cuál es el
resumen, cómo se divide el cuerpo, qué tablas y figuras hay, y cuáles son las
referencias.

### 2. Pregunta lo que falte — de una sola vez

Haz una sola lista con **todo** lo que no puedas sostener con el material, y
pregúntala junta. Distingue dos cosas, porque no se resuelven igual:

- **Lo que impide componer** y hay que resolver ahora: no se entiende el
  título, falta el cuerpo de una sección, una tabla está cortada en la foto,
  no se sabe quién firma.
- **Lo que el pipeline ya sabe dejar pendiente** y no hace falta preguntar:
  DOI, fechas de aceptación y publicación, ORCID, conflicto de intereses,
  financiamiento. Estos se marcan solos como `[PENDIENTE: ...]` en el
  artículo y se reportan al final — no detengas la compilación por ellos.

Si el material alcanza para componer, **no preguntes de más**: compón y
reporta los pendientes al final. El usuario pidió velocidad; las preguntas
son para lo que de verdad bloquea.

### 3. Reconstruye el manuscrito y conviértelo

Si el material ya era un `.docx`, sáltate esto y ve al paso 4.

Si no, escribe lo reconstruido como Markdown y conviértelo:

```
python3 taller/manuscrito_desde_md.py reconstruido.md
```

El Markdown va así (el formato está documentado en la cabecera del script):

```markdown
# Título del artículo

Autor Uno, Autor Dos y Autor Tres
Afiliación institucional, Ciudad, País
correo@ejemplo.mx
ORCID: 0000-0000-0000-0000

## Resumen

Texto del resumen...

**Palabras clave:** una, dos, tres

## Introducción

Cuerpo...

### Subsección

Cuerpo...

Tabla 1. Pie de la tabla.
| Columna | Otra |
| --- | --- |
| dato | dato |

Figura 1. Pie de la figura.
![](ruta/a/imagen.png)

## Referencias

Apellido, N. (2024). Título. Revista, 1(1), 1-10.
```

Dos detalles que importan por cómo los lee el pipeline: en el bloque de
cabecera y en las referencias, **cada renglón es una unidad** (el autor, la
afiliación, el correo y el ORCID van en renglones distintos; cada referencia
en el suyo). En el cuerpo, los renglones contiguos se unen en un párrafo.

Guarda el `.md` junto al material: es la fuente de la reconstrucción, y deja
auditable de dónde salió cada párrafo.

### 4. Recibe el manuscrito

```
python3 taller/recibir_articulo.py <ruta al .docx>
```

Añade `--numero VOL6_NO3` solo si el usuario indicó un número explícito (si
no, el script calcula el que corresponde a hoy). Añade `--tipo "..."` solo si
el usuario dijo qué tipo de artículo es; si no, deja que lo decida su
heurística y lo declare.

Si falla, el mensaje viene en español llano, sin traza. Si señala un problema
del manuscrito (cuerpo vacío, `.docx` ilegible), explícaselo al usuario y
pídele lo que falta — nunca rodees el problema inventando contenido. Si
señala un fallo de compilación que no se explica por el contenido, es un
defecto del taller o del entorno: repórtalo, no es del usuario.

### 5. Lee el reporte técnico

Junto al `.tex` y al PDF queda un `reporte_tecnico.md` con los campos que
quedaron `[PENDIENTE: ...]` y la regla que decidió el tipo de artículo. Es
información para el usuario: nunca cierres con "listo, ya quedó" si hay
pendientes.

### 6. Arma el número completo

```
python3 taller/armar_numero.py <el mismo NUMERO>
```

Con `--portada <imagen>` si el usuario entregó una imagen de portada. Si
avisa que otro artículo del número aún no está compilado, es informativo:
sigue con los que sí lo están.

### 7. Entrega

Manda los archivos: el PDF del artículo y el PDF del número completo. Y en
el mensaje, en español llano, sin jerga de LaTeX:

- Qué tipo de artículo se detectó y con qué criterio.
- **Qué dedujiste tú del material** y de dónde (para que el usuario lo
  confirme): "el título lo tomé del encabezado de la primera hoja", "asumí
  que las dos últimas páginas del PDF eran las referencias".
- Qué quedó `[PENDIENTE: ...]` y quién lo completa: el autor (ORCID,
  conflicto de intereses) o el comité editorial (DOI, fechas).
- Cualquier cosa del material que te haya parecido un error de contenido,
  señalada, no corregida.
