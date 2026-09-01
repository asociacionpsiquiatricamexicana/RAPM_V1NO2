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
