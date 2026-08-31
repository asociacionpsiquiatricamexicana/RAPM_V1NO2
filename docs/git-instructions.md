# Cómo se versiona la revista

El repositorio comparte casa con el libro de la Genealogía, pero son obras
distintas con ramas distintas: la revista vive en su rama por defecto y el
libro en `genealogia`. Nada de una cruza a la otra.

## La rama

El trabajo va en una rama `claude/…`, nunca directamente en la rama por
defecto. Una campaña (un número, o una serie de mejoras del taller) se sigue
por una sola solicitud de fusión en borrador.

## Una tanda, un commit

Una tanda —un artículo compuesto, un cambio de clase, una sonda nueva— se
decide, se aplica, se compila, **se mide** y se asienta junto:

1. **Compilar y medir.** `bash taller/componer.sh <articulo.tex>`: dos
   pasadas, cero errores, cero overfull, linearizado, y la sonda de
   geometría en verde. Tras cambios al taller, además
   `python3 taller/sondas/reproducible.py`.
2. **Anotar en `REGISTRO_DE_PRODUCCION.md`**: qué cambió, cómo se comprobó
   (cifras, no adjetivos) y qué quedó declarado sin resolver. Si un ancla se
   movió, la razón va aquí.
3. **Archivar el entregable** en `numeros/VOL#_NO#/…` con su `.tex` y su
   reporte técnico: lo publicado debe poder regenerarse desde el repositorio.

El mensaje del commit dice qué se produjo o corrigió y con qué se comprobó.
No se incluye el identificador del modelo en mensajes de commit, títulos ni
cuerpos de solicitud de fusión.

## Lo que no se confirma

Artefactos de compilación: `*.aux`, `*.log`, `*.out`, `*.toc`, `taller/pdfs/`.
Sí se confirman los camera-ready publicados en `numeros/`, que son el
entregable, y las anclas de las sondas.
