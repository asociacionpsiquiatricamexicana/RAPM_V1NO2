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
