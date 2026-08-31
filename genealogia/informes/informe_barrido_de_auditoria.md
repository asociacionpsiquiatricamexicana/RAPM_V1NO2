---
obra: Gran Proyecto Historiográfico
documento: Informe del barrido de auditoría sobre el volumen compuesto y su taller
lugar_y_fecha: Ciudad de México, a 31 de agosto de 2026
de: el taller de composición del volumen
para: Dr. José Carlos Medina-Rodríguez, compilador
estado: barrido de solo lectura; nada corregido, once hallazgos declarados a decisión
---

# Informe del barrido de auditoría

Barrido de diecisiete dimensiones sobre el PDF ya compuesto
(`genealogia/APM60_Genealogia__corregido.pdf`, 332 páginas, cabeza `901de04`
del repositorio) y sobre el taller que lo produce. Todo se midió contra el
archivo construido; nada se leyó del código y se dio por cierto. El barrido
fue de solo lectura: no se modificó ningún archivo del libro ni del taller.
Cada hallazgo trae la cifra que lo sostiene y con qué se obtuvo.

## Método, y una falla que debe constar

Estaba previsto orquestar el barrido como flujo de trabajo: sondas en paralelo
por dimensión, verificación adversarial de cada hallazgo y síntesis. Ese flujo
se lanzó y falló entero —los diecinueve agentes devolvieron el límite semanal
de capacidad, con cero dimensiones completadas y cero hallazgos—, y las
diecisiete dimensiones se recorrieron después una a una en el hilo principal,
que no está afectado. La verificación adversarial se hizo a mano sobre los
propios hallazgos: retiró cuatro y bajó uno de grado, como consta al final.

## Las comprobaciones de control

| Comprobación | Resultado |
|---|---|
| `cmp.py` contra su ancla | 722 de 722, ni una de más |
| `reproducible.py` | se recompone idéntico: 332 páginas, hash `968f7ff9…` |
| `verificar_toc.py` | 47 entradas cuadran + 2 ciegas sin folio = 49 de 49 |
| `marcadores.py` | los 49 caen sobre su rótulo |
| `cierre_pdf.py` | 0 de 7 700 renglones se parten al copiar |
| `chk_colas.py` | 0 colas perdidas de 2 187 bloques |
| `debug_espacios.py` | 0 renglones con hueco anómalo |
| `depurar_pdf.py` | 28 tipos cubiertos, 0 sin compositor, 0 compuestos dos veces |
| Geometría | las 332 páginas miden 438,96 × 652,08 pt, ninguna caja desborda |
| Extensión declarada | «332 páginas» en página legal y ficha de catalogación: real |
| Caracteres de control | 0 U+0002 en 0 páginas |
| Bibliografía | 64 de 64 claves autor-año con asiento localizable |

## Lo que hay que corregir en el libro

### 1. La nomenclatura se partió en dos: el libro navega por Episodios y la prosa remite a capítulos

Las cuatro divisiones de la parte histórica se titulan «Primer Episodio» a
«Cuarto Episodio» en el Contenido, en las cornisas y en los cuarenta y nueve
marcadores del PDF. La prosa del compilador las llama veintinueve veces
«capítulo»; dieciocho de esas son remisiones por ordinal —«Véase el capítulo
tercero, nota 8», «El capítulo segundo lo consigna con esa reserva expresa»—
que mandan a un rótulo que no existe en el libro. El bloque 1411 lleva las dos
nomenclaturas dentro del mismo párrafo: «sus cuatro capítulos […] Cada episodio
se narra en un solo párrafo». El cambio dejó además rastro inverso: «episodio»
quedó con dos sentidos a la vez —división del libro y suceso—, con diez usos
narrativos; el bloque 370 los cruza en una sola línea, «la reconstrucción del
episodio de mil novecientos sesenta y cinco que el capítulo primero expone»,
cada palabra puesta donde iría la otra.

Capa cero: las veintinueve están en la voz del compilador (tipos `p`, `note`,
`fnote`, `field`, `trow`), ninguna dentro de cita. Quedan fuera y no se tocan:
los bloques 1105 y 1323 (citas `epi`), el 824 (el «Capítulo VII del Título
Tercero» de la Ley General de Salud), el 1509 (la entrada de glosario del
capítulo estatal) y los cuarenta y nueve usos territoriales, que están bien.

*Medido:* 79 ocurrencias de «capítulo(s)» en la fuente; 49 territoriales o
ajenas, 30 estructurales de las que una (824) es falsa coincidencia.

### 2. El flipbook plano que se publica va una tanda atrás

`genealogia/Genealogia_APM_Flipbook__plano.html` lleva fecha del treinta de
agosto a las 15:52; el PDF corregido y el flipbook autónomo son del treinta y
uno a la 1:38. El plano conserva la cornisa corta anterior a la unificación en
ocho de los quince apéndices —III, IV, V, VI, VII, IX, XI y XII—, repartida en
271 bloques: dice «Apéndice VI · Mesas Directivas» donde el libro dice
«Apéndice VI · Mesas Directivas, 1966-2027». La tanda de hoy ya declaró que no
pudo rearmarse porque `flatten.py` necesita `template.html`, que no vive en el
repositorio; lo que la declaración no dice es que el artefacto atrasado sigue
publicándose. Mientras no se pueda rearmar, la decisión honesta es retirarlo o
marcarlo por su fecha.

### 3. El cuarto Episodio termina en dos años distintos según dónde se lea

El Contenido dice «Mesas Directivas del cuarto episodio, 2020-2027» y el
Apéndice VI cubre «1966-2027»; el bloque 1433 dice que el cuarto cubre «de dos
mil veinte a dos mil veintiséis» y el rótulo interno `anchor` 813 dice
«2020-2026». El bienio 2026-2027 (Saucedo Martínez, bloque 1606) cae dentro
del cuarto Episodio. Puede que «hasta dos mil veintiséis» quiera decir el corte
del objeto —el Sexagésimo Aniversario— y no la extensión de la división, pero
entonces la división se llama de dos maneras; qué año rige es decisión del
compilador.

### 4. Catorce años sobreviven en numeral dentro de la prosa narrativa

En los bloques 0 a 1399 —la parte narrativa— la prosa corrida escribe 417 años
con letra y 14 con cifra: bloques 206 y 208 (1971), 265 (2008), 392 (1996 y
2015), 411 (1985), 415 (2020), 449 (1989), 744 (1980), 761 (1978), 781 (2011 y
2014), 798 (2020) y 908 (2022). Los tres de la página legal (bloques 8, 9 y 17)
quedan fuera: ahí el numeral es el correcto. En apéndices y aparato hay 107
más, y ahí también corresponde: son cajas de datos.

### 5. La misma cifra aparece con letra en un sitio y con numeral en otro

Tres estadísticas se dan más de una vez con grafía distinta: el 60,34 % de
concentración geográfica va en numeral en los bloques 580 y 1156 y con letra
—«sesenta coma treinta y cuatro por ciento»— en el 2095; la tasa 3,68 va en
numeral en el 579 y con letra en el 2095; la densidad 1,6 va en numeral en el
619 y con letra en el 2097. Las tasas 3,47 y 20,3 solo aparecen en numeral, de
modo que en ellas no hay discrepancia.

## El taller, el registro y la norma

### 6. El LEEME describe mal el formato de la fuente, y quien lo siga extrae cero caracteres sin ver un error

Las líneas 11 y 12 de `genealogia/taller/LEEME.md` dicen que un bloque tiene
«una lista de fragmentos (`parts`), cada uno con su texto». Es inexacto por
tres lados: la clave del texto es `x` —lo confirma el propio módulo de estilo,
`b.parts.map((p) => (p.br ? ' ' : p.x || ''))`—; 373 bloques `trow` y 33
`thead` no llevan `parts` sino `rows`, cada fila con los suyos; y 58 bloques
llevan prosa en `title`, `sub` o `label`, donde ni `parts` ni `rows` llegan
(las once portadillas `plate`, los `anchor`, los `field` y los `fnote` con
rótulo). El costo no es teórico: un extractor escrito desde esa descripción
devuelve cero caracteres y ninguna excepción, y ese silencio se lee como
hallazgo. Extraído correctamente: 484 765 caracteres en 2 027 de 2 187 bloques.

### 7. Los cuarenta y seis rótulos de navegación conservan la nomenclatura anterior — y no los ve nadie

Los bloques `anchor` guardan un `label` congelado antes de dos renumeraciones:
dicen «Capítulo I. Fundación e identidad, 1966-1980» donde el libro dice
«Primer Episodio», y numeran los apéndices una posición atrás —la Nota
metodológica sigue siendo «Apéndice I», duplicando al de la Línea del Tiempo,
y el In memoriam figura como «Apéndice XII» cuando en el libro es el XV—.
Verificado que no llegan al lector: cero apariciones de esos rótulos en las
332 páginas, el módulo de estilo no compone el tipo `anchor` (está en
`INVISIBLES`) y los marcadores del PDF se construyen desde `toc`, que sí está
al día. Es metadato muerto, no defecto del libro; se anota porque es la clase
de rastro que hace confiar a una tanda futura en un rótulo caduco, y porque el
`anchor` 813 es una de las voces que datan el cuarto Episodio en 2026.

### 8. El registro anuncia como vigente un hallazgo mayor que él mismo retracta

La línea 2678 de `REGISTRO_DE_CORRECCIONES.md` abre una sección de primer
nivel: «Hallazgo mayor sin corregir: mil seiscientas cuarenta y cuatro
palabras llevan un carácter invisible dentro». La retractación existe y está
bien escrita, pero es un `###` anidado debajo del título que desmiente, de
modo que en cualquier lectura de encabezados el hallazgo retirado sigue
anunciándose como el defecto mayor pendiente. Medido hoy sobre el PDF
publicado: cero caracteres U+0002 en cero páginas.

### 9. La sonda nueva de hoy no entró en la tabla del LEEME

`aire_de_la_bajada.py` se escribió en la tanda de hoy, denuncia once de once
contra el PDF anterior y ninguna contra el nuevo, y es la única de las once
sondas que no figura en la tabla del LEEME.

### 10. El taller hereda una licencia que prohíbe derivar de él

No hay `LICENSE` dentro de `genealogia/taller/`; el código hereda el de la
raíz, Creative Commons BY-NC-ND 4.0, sin obras derivadas. Para el libro esa
licencia es la decisión editorial y está bien; sobre el taller, el LEEME
enseña a componer el volumen, advierte que los dos archivos de estilo se
editan juntos y documenta once sondas para que alguien las corra: es
documentación para modificar un programa bajo una licencia que no permite
distribuir modificaciones. Un `LICENSE` propio en `taller/` haría que la
invitación y el permiso digan lo mismo.

### 11. La norma gobierna un volumen que ya no es este, y nombra cinco archivos que no existen

Los documentos de `genealogia/norma/` describen 283 páginas (el libro tiene
332), apéndices I a XIV (hay I a XV) y «cuatro capítulos, de 1966 a 2026», y
`CONTENIDO_DE_LAS_PARTES.txt` da nombre de archivo a cinco entregas por partes
de las que no existe ninguna en el repositorio. La salvedad ya está declarada
con precisión en `norma/LEEME.md` —la norma rige un volumen XeLaTeX cuyas
fuentes y scripts no viven aquí—; lo que queda por resolver es que
`CONTENIDO_DE_LAS_PARTES.txt` se lee como documento vigente y que su única
auditoría cruzada es del veintiocho de agosto, anterior a los Episodios, al
Apéndice XV y a la unificación de cornisas.

## Dos comprobaciones que merecen su nota

El flipbook autónomo es de verdad autónomo: se abrió su manifiesto y se
descomprimió; las diecinueve entradas están incrustadas, incluidas las dos
bibliotecas que declara desde la red, y el `.bin` que lleva dentro es byte a
byte el del taller. No necesita red para abrirse, y es el archivo que
sobrevive al repositorio.

Los dos archivos de estilo gemelos difieren en 34 líneas, todas del envoltorio
de módulo más la línea de retorno; sustantivamente son el mismo archivo. La
advertencia del LEEME sobre editarlos juntos se está respetando.

## Lo que la verificación adversarial retiró

Cuatro hallazgos aparentes no sobrevivieron: «Trillas, 1982» y «Edamex, 1995»
son editoriales dentro de una lista de libros en una semblanza, no citas sin
asiento; «Page y colaboradores, 2021» sí tiene asiento, en la nota al pie 1446
y no en la tabla; y «Silva, 2015» lo tiene en el bloque 126. Y uno bajó de
grado: los rótulos `anchor` caducos no llegan a ninguna página, y se declaran
como lo que son, metadato muerto.
