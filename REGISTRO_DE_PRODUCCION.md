# Registro de producción · Revista de la APM

Una sección por tanda: qué se compuso o cambió, **cómo se comprobó** (cifras
de sondas, no adjetivos) y qué quedó declarado sin resolver. Es el mismo
oficio que el registro de correcciones del libro de la Genealogía: el
registro es parte de la revista, no documentación accesoria.

## Tanda: el taller entra al repositorio (31 de agosto de 2026)

La revista no tenía sus herramientas versionadas: la clase, la plantilla y la
norma vivían en una skill de cuenta, ya desactualizada, y las ramas del
repositorio solo guardaban diagnósticos. Entra `taller/` con la clase
(`apm-editorial.cls`, la especificación), la plantilla, los logos, la prueba
en frío, `componer.sh` (pdflatex ×2 + linearizado + medición) y dos sondas
nuevas escritas con las lecciones del libro: `geometria.py` (páginas, caja,
tipografías incrustadas, peso, contra ancla) y `reproducible.py`
(recompilación en limpio desde lo versionado, hash del texto, contra ancla).
La norma heredada queda en `taller/norma/`, datada: ante divergencia gana el
`.cls` y gana la medición. El taller lleva LICENSE MIT propio; los artículos
siguen bajo la licencia de la revista.

**Cómo se comprobó.** `comprobar_entorno.sh`: entorno apto, compilación real
del ejemplo. `componer.sh`: dos pasadas, cero errores, cero overfull,
linearizado. `geometria.py`: 2 páginas (ancladas), caja única 612 × 792 pt,
0 tipografías sin incrustar, 431 KB < 600 KB. `reproducible.py`: se
recompone idéntico desde lo versionado (hash anclado `5090412e…`). La cifra
de páginas del ejemplo es **2 con las dos pasadas de rigor** (la «3» del
registro anterior era de una sola pasada, que deja totpages sin resolver).

**Declarado sin resolver.** El sistema solo produce Editoriales; los demás
tipos de artículo son desarrollo nuevo. `diagnostico_rapm.py` automatiza 4 de
las 14 capas del diagnóstico histórico. El logo del 60 aniversario no tiene
render funcional. La skill de cuenta `rapm-editorial` quedó atrás de este
taller y conviene regenerarla desde aquí.

## Tanda: `\APMtype{}` se conecta al render (31 de agosto de 2026)

El hallazgo mayor de `norma/09_limitaciones_conocidas.md §1`: la clase definía
`\APMtype{}`, pero el encabezado imprimía «Editorial\par» a mano y el
`pdfsubject` de los metadatos hacía lo mismo, de modo que el sistema no
podía producir, con el código tal cual estaba, ningún artículo etiquetado
como Original, Revisión, Reporte breve, Caso clínico o Carta al Editor —
solo Editoriales, sin importar lo que pidiera el `.tex`. Es justo la
carencia con la que se cerró la tanda del taller: «esto requiere
extenderlo».

**Lo que se corrigió.** El rótulo del encabezado y `pdfsubject` en
`taller/apm-editorial.cls` ahora referencian `\@apmtype` en vez del texto
fijo. El valor por omisión, cuando el `.tex` no llama `\APMtype{}`, se dejó
en `Editorial` (antes era `EDITORIAL` en mayúsculas, sin efecto porque
nunca se imprimía) para no alterar el ejemplo existente.

**Un defecto contiguo, hallado al verificar.** La caja de RESUMEN se
imprimía siempre, vacía cuando el autor no llamaba `\APMabstract{}` —
relevante porque la norma exime de resumen a Editorial y a Carta al
Editor. Se condicionó a que `\@apmabstract` no esté vacío. El primer
intento (`\ifx\@apmabstract\empty`) falló en silencio —la caja seguía
imprimiéndose— porque `\newcommand`/`\renewcommand` producen macros
`\long`, y un macro `\long` nunca es `\ifx`-igual a `\empty` así su
contenido esté vacío. Se corrigió con las variantes con asterisco
(`\newcommand*`/`\renewcommand*`), que sí lo son.

**Cómo se comprobó.** Compilación de prueba con `\APMtype{Artículo
original}`: el rótulo y el `pdfsubject` del PDF dicen «Artículo original».
Con `\APMtype{Carta al Editor}` y `\APMabstract{}` vacío: el rótulo cambia
y la caja de RESUMEN desaparece del PDF (`pdftotext` no encuentra
«RESUMEN»). El ejemplo sin modificar, sin llamar a `\APMtype{}`:
`reproducible.py` confirma que se recompone idéntico —mismo hash de
texto—, de modo que el valor por omisión no cambió el comportamiento
existente. `geometria.py` en verde: 2 páginas, caja única, 0 tipografías
sin incrustar, 431 KB. Norma actualizada en `01_identidad_tipos_articulo.md`
y `09_limitaciones_conocidas.md §1`, con la fecha de la corrección.

**Declarado sin resolver.** Conectar el rótulo no valida el diagramado de
un Artículo original real: el layout de dos columnas con estructura IMRaD
para cuerpos de 3,000–6,000 palabras con tablas y figuras sigue sin
probarse contra un manuscrito de esa extensión.

## Tanda: el artículo largo se compone, y sale una fuga de Computer Modern (1 de septiembre de 2026)

Cierra lo que la tanda anterior dejó abierto —el IMRaD de dos columnas con
tabla y figura sin probar— y, al medirlo, aparece un defecto que llevaba
tiempo en todos los PDFs sin que nadie lo viera.

**El artículo largo.** Entra `ejemplo_articulo_original.tex`, fixture de
diagramación con resumen, IMRaD, subsecciones, tabla y figura a ancho de
página; los autores y las cifras son inventados y así queda dicho en el
`LEEME.md`, para que nadie los reutilice como material editorial. La clase
necesitaba tres cosas que el Editorial nunca pidió: `booktabs` y `caption`,
el formato de `\subsection` (estaba en la especificación de la cabecera del
archivo y sin escribir) y los pies de tabla y figura, con «Tabla» y
«Figura» forzados vía `\captionsspanish` como pide APA 7. Las sondas pasan
a un ancla por documento (`geometria_<base>.txt`, `reproducible_<base>.txt`)
porque el taller ya compone más de un ejemplo.

**La fuga (FM06).** El separador de cabeceras, pie y colofón era `$\cdot$`,
en modo matemático. `mathptmx` remapea casi todo a `ztmcm`, pero ese símbolo
vive en codificación OMS y caía a `cmsy10`: metía Computer Modern en un
diseño Times/Nimbus, en los dos PDFs, en las nueve ocurrencias de la clase.
Es el modo de fallo FM06 que el propio diagnóstico advierte por escrito.
Nadie lo detectó porque `geometria.py` solo miraba la columna `emb` de
`pdffonts`, y la CM **estaba** incrustada: la sonda decía «EN REGLA» sobre
un defecto de composición. Va `\textperiodcentered`, mismo glifo en modo
texto, que trae la propia Nimbus; y la sonda aprende a ver la fuga.

**Las sondas que mentían.** La capa A del diagnóstico imprimía `paginas:
null` y `titulo: null` cuando faltaba PyMuPDF: parecía una medición y era
una ausencia. Ahora declara la falta, como ya hacía la capa B con
`pdfplumber`. Y el alias viejo `fitz` escupe su aviso de obsolescencia por
**stdout**, dentro del JSON, de modo que el `--json` que el script anuncia
producía un archivo ilegible; se importa por el nombre nuevo. En
`geometria.py` había además un cálculo de tipografías sin incrustar que la
línea siguiente pisaba entero: código muerto, retirado.

**La prueba en frío no cubría lo que hacía falta.** `comprobar_entorno.sh`
declaraba «entorno apto» en una máquina sin `booktabs` ni `caption`, que
reventaba al componer un Original, y no miraba **ni una sola** dependencia
de Python, siendo las sondas la mitad del taller. Ahora verifica las dos
`.sty` nuevas y los cuatro módulos, `pypdfium2` como dura y los tres del
diagnóstico como blandas. También decía «3 página(s)» sin advertir que era
su compilación de una pasada, contradiciendo la cifra buena documentada.

**Cómo se comprobó.** `componer.sh` sobre los dos ejemplos: dos pasadas,
cero errores, cero overfull, linearizado. Editorial: 2 páginas, caja única
612 × 792 pt, 0 sin incrustar, **0 fuga de CM**, 433,598 bytes. Artículo
original: 4 páginas, misma caja, 0 sin incrustar, **0 fuga de CM**, 465,145
bytes. Quitar la CM adelgazó los PDFs ~8 KB cada uno (441,681 → 433,598 y
473,321 → 465,145): era un subconjunto de `cmsy10` incrustado para un solo
signo. `pdffonts` ya no lista ninguna `CM*` en ninguno de los dos. El
`pdftotext` del separador da los bytes `C2 B7`, U+00B7 MIDDLE DOT, el
carácter correcto; el `\cdot` matemático extraía un operador matemático,
peor para copiado e indización. `diagnostico_rapm.py` entrega JSON limpio y
parseable, con las capas A y B midiendo de verdad.

**Anclas movidas, con razón.** Las de geometría **no** se movieron: 2 y 4
páginas antes y después. Las de `reproducible.py` sí, porque el texto
extraído cambió con el separador, y se reanclaron: editorial
`b431039408039a94…` (2 páginas), artículo original `e538a776a5b1fc76…`
(4 páginas).

**Declarado sin resolver.** El fixture del artículo largo es de
diagramación, no un manuscrito real: valida el layout, no el flujo
editorial con un autor. `diagnostico_rapm.py` sigue automatizando 4 de las
14 capas; las capas C–L piden medición dirigida sobre coordenadas y ninguna
de las correcciones de esta tanda las toca. El logo del 60 aniversario
sigue sin render funcional. Las dependencias de Python quedan **declaradas
y verificadas** por la prueba en frío, pero su instalación sigue siendo del
entorno, no del repositorio: en un contenedor recién levantado hay que
instalarlas, y la prueba en frío es la que avisa.

## Tanda: la norma alcanza al código (1 de septiembre de 2026)

Tres notas de `taller/norma/` contradecían lo que el `.cls` y las sondas ya
hacen, y una de ellas era una trampa activa: `04_failure_modes.md` seguía
diciendo que la Computer Modern de `$\cdot$` «no cuenta como CM font leak»,
justo lo contrario de lo que `geometria.py` vigila desde la tanda anterior.
Un diagramador que la leyera daría por aceptable el defecto que la sonda
rechaza. Se retira esa excepción (tachada, con fecha, no borrada), la fila
FM06 gana la causa raíz real —signo de texto en modo matemático— y su
remedio, y el check 12 de `10_checklist_auditoria_codigo.md` deja de decir
que `\APMtype{}` «hoy NO está conectado» cuando lo está desde el 31 de
agosto. Sin cambios al `.cls` ni a los `.tex`.

**Cómo se comprobó.** No hay PDF nuevo que medir. `geometria.py` sobre los
dos PDFs vigentes sigue en verde: editorial 2 páginas, original 4, caja
única 612 × 792 pt, 0 sin incrustar, 0 fuga de CM, anclas sin moverse.

**Declarado sin resolver.** Lo mismo que la tanda anterior; esta solo pone
la norma al día. La campaña queda en una solicitud de fusión en borrador.

## Tanda: revisión del código del taller, con las correcciones que se dejan medir (1 de septiembre de 2026)

Revisión de la clase, las tres sondas y los dos scripts, aplicando solo lo
que es defecto comprobable, no gusto.

**Un defecto de composición en la clase.** `\APMrefsbreak` cerraba el grupo
de referencias y lo reabría sin `\sloppy\raggedright`, que `\APMrefsstart`
sí fija: las referencias anteriores al corte iban en bandera y las
posteriores, justificadas, en la misma lista. En el editorial, que sí usa
el corte, la justificación forzada partía **cinco URL** a mitad de cadena
(`https://doi.org/` en una línea y `10.1016/…` en la siguiente) y pegaba
`treatment-resistant` en `treatmentresistant` al extraer el texto. Ahora el
macro reabre con los mismos ajustes que `\APMrefsstart`; su comentario, que
seguía diciendo «úsalo con ≥12 referencias, parte por la mitad», dice la
regla medida en el artículo original. `\@twocolumnfalse`, suelto tras
`\LoadClass[twocolumn]` con el comentario «improve column breaks», se retira:
no hacía nada, y el original se recompone con el mismo hash sin él. La
versión declarada en `\ProvidesClass` (v1.0, 2025) pasa a la que anuncia la
cabecera del archivo (v2.0).

**Las sondas.** `reproducible.py` creaba un directorio temporal por corrida y
nunca lo retiraba: había 19 talleres huérfanos en `/tmp`; ahora se retira
siempre, también al anclar o al fallar, y rechaza un `.tex` que no esté
versionado en `taller/` en vez de fallar con un error de pdflatex.
`diagnostico_rapm.py` pedía correr `pdffonts` «por separado» para la capa M:
ahora lo mide, con el mismo parseo y la misma lista de prefijos de Computer
Modern que `geometria.py` (le faltaban `CMEX`, `CMTI` y `CMTT`); su
`papel_spec_pt` traía solo el ancho, ahora el par; y sus rutas a la norma
apuntaban a un `references/` que no existe. Docstrings de las dos sondas de
ancla, que aún hablaban de `*_referencia.txt`.

**Los scripts.** `componer.sh` decidía el destino comparando la cadena del
argumento con una ruta absoluta: con `taller/ejemplo_editorial.tex` relativo
el editorial se escapaba a `taller/` en vez de `pdfs/`, y el original nunca
llegaba a `pdfs/`. Ahora compara directorios resueltos: todo `.tex` que viva
en `taller/` va a `taller/pdfs/`; los de `numeros/` se quedan junto a su
fuente. Avisa si el `.tex` no existe. `comprobar_entorno.sh` no contaba el
fixture del artículo original entre los activos.

**La norma.** FM05 y el check 6 del checklist de `.tex` repetían la regla
del conteo de referencias; dicen la regla medida. El `LEEME.md` deja de
avisar que el comentario del `.cls` contradice la práctica.

**Cómo se comprobó.** `componer.sh` sobre los dos ejemplos: dos pasadas,
cero errores, cero overfull, linearizado. Editorial 2 páginas, 432,845
bytes; original 4 páginas, 465,145 bytes; ambos caja única 612 × 792 pt, 0
sin incrustar, 0 fuga de CM, anclas de geometría sin moverse. El original
**se recompone idéntico** (hash `e538a776…`): las retiradas en la clase
fueron neutras. El editorial cambió de hash por el corte de referencias, y
se midió qué: compilado con la clase anterior y comparado por `pdftotext`,
el diff cae entero en las referencias posteriores al corte; líneas con URL
partida al final, **5 antes y 0 después**; reanclado en `22bb002dc34abb2c…`
(2 páginas). `diagnostico_rapm.py --json` entrega JSON parseable con la capa
M midiendo cinco Nimbus, cero sin incrustar, cero CM. `comprobar_entorno.sh`
apto, con los cinco activos. `bash -n` y `py_compile` limpios en los cinco
archivos.

**Declarado sin resolver.** `\APMcheckabstract`, `\APMchecktitle`,
`\fixellipsis`, `\APMrule` y `\APMcenterblock` siguen definidos y sin uso en
ningún `.tex`; no se tocan porque son interfaz declarada, pero el checklist
de auditoría debería decidir si se conectan o se retiran, como con
`\APMfolio` y `\APMlogoSixty`. El comentario del `ejemplo_editorial.tex`
sobre «split after ref 5 for optimal balance» sigue diciendo la regla vieja;
es plantilla, no clase, y queda para la próxima vez que se toque ese
archivo. Lo demás, igual que la tanda anterior.

## Tanda: lo que la revisión dejó dicho, resuelto (1 de septiembre de 2026)

Cierra los dos puntos que la tanda anterior declaró sin resolver, y al
tocar la plantilla aparece un corte que no cortaba nada.

**Los cinco macros sin uso.** El checklist de código decide, como decidió
con `\APMfolio` y `\APMlogoSixty`: se documentan como interfaz no
conectada y se dejan en el `.cls`, porque retirarlos es cambio de
especificación, no corrección. Entra el check 21 en
`10_checklist_auditoria_codigo.md` y el §3c en
`09_limitaciones_conocidas.md`, que separa las dos clases: `\APMcheckabstract`
y `\APMchecktitle` son «comprobaciones» que no comprueban nada (un
`\newcount` puesto en cero y un cuerpo vacío: quien las llame esperando el
aviso de resumen o título largo no lo recibirá, el mismo engaño de una
sonda que dice «EN REGLA» sin medir), y `\fixellipsis`, `\APMrule` y
`\APMcenterblock` funcionan pero ningún diseño medido los usa. `grep` en
`taller/*.tex`: cero ocurrencias de los cinco.

**La plantilla del editorial.** Su cabecera decía «Compile: pdflatex
editorial-neuromod.tex», un archivo que no existe; la nota del folio
apuntaba a `references/`, que tampoco; y `\APMlogoSixty{logo_60anos.png}`
seguía llamándose en claro, enseñando la práctica que la nota de al lado
prohíbe para `\APMfolio`. Va comentado igual. Y el comentario «split after
ref 5 for optimal column balance», al medirse, resultó peor que viejo:
en la página 2 las referencias arrancan a media columna (REFERENCIAS a
175 pt del tope, tras el cuerpo) y el corte visual cae tras la **sexta**
entrada, no tras la quinta donde estaba `\APMrefsbreak`, porque `flushend`
reequilibra la última página por su cuenta. Compilado sin el corte: las
mismas 154 líneas en las mismas coordenadas y el mismo hash de texto. El
corte no hacía nada, y la regla del `LEEME.md` dice que ahí no va. Se
retira de la plantilla, con la medición en el comentario. El `LEEME.md`
llamaba «texto corto sin resumen» a un ejemplo que trae resumen; dice ahora
que la norma no lo exige y que la caja aparece solo si `\APMabstract{}`
trae texto. En el checklist del `.cls`, las filas 15 y 17 llevaban una
barra sin escapar dentro de un `grep -E`, que partía la tabla en una cuarta
columna vacía; escapadas, y fuera el separador sobrante.

**Cómo se comprobó.** `reproducible.py` sobre el editorial con la plantilla
nueva: 2 páginas, hash `22bb002dc34abb2c…`, **se recompone igual**; el ancla
no se mueve. `componer.sh`: dos pasadas, cero errores, cero overfull,
linearizado, 2 páginas, caja única 612 × 792 pt, 0 sin incrustar, 0 fuga de
CM, 432,845 bytes (los mismos de la tanda anterior). El artículo original no
se tocó. Comparación línea por línea con `pymupdf` del PDF con corte y sin
corte: 154 líneas, cero diferencias.

**Declarado sin resolver.** Las capas C–L del diagnóstico, en curso en la
tanda siguiente. El logo del 60 aniversario sigue sin render funcional; el
fixture del artículo largo sigue siendo de diagramación, no un manuscrito;
las dependencias de Python siguen siendo del entorno.
