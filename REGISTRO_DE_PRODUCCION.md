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
