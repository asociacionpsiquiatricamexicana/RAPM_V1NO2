# Genealogía de la Asociación Psiquiátrica Mexicana, A.C.

_Gran Proyecto Historiográfico._ Obra conmemorativa del sexagésimo aniversario de
la fundación de la Asociación Psiquiátrica Mexicana, A.C. Primera Edición, Ciudad
de México, septiembre de dos mil veintiséis. Compilación de José Carlos Medina
Rodríguez; edición de David Eduardo Saucedo Martínez.

**El archivo que se lee es `genealogia/APM60_Genealogia__corregido.pdf`.** A su
lado van dos flipbooks, que son el mismo libro en un visor de pantalla y no otra
edición. Por indicación del compilador van un paso por detrás del PDF: paginan
con un motor propio, no llevan la tipografía griega y no llevan los techos de
seguimiento.

## Cómo está identificado

|               |                                                              |
| ------------- | ------------------------------------------------------------ |
| Identificador | DOI `10.5281/zenodo.22035217`                                |
| Licencia      | CC BY-NC-ND 4.0 — el texto completo, en `LICENSE`            |
| Edición       | Primera, septiembre de dos mil veintiséis · Ciudad de México |

El libro comparte con la _Revista de la Asociación Psiquiátrica Mexicana_ su
número normalizado electrónico —e-ISSN 3061-7979— y **eso es deliberado**: su
página legal declara que el libro «es una publicación propia y única de la
Asociación […] y no una publicación periódica», y que emplea ese número «con la
debida distinción», como el Instituto Nacional del Derecho de Autor permite al
mismo titular. El DOI y la licencia, en cambio, son suyos y no los de la revista.

## La regla que no se negocia: capa cero

No se altera **nunca** el texto ajeno: ni lo que va dentro de una cita atribuida
a una persona, ni los asientos bibliográficos con sus títulos y direcciones, ni
el nombre de un autor tal como lo firma en cada publicación, aunque en otra parte
del libro se escriba distinto.

Corregir ahí no es mejorar el libro: es falsear una fuente. Si algo parece un
error dentro de una cita, se señala en una nota y se declara; no se toca el
texto.

## Cómo se recompone

El libro entero sale de un solo archivo de contenido y del taller que lo compone.
Desde `genealogia/taller`:

```
python3 libro.py                             # -> pdfs/libro.pdf
python3 extraer_texto_pdf.py pdfs/libro.pdf  # la ruta, siempre
python3 build.py
python3 cmp.py                               # coteja el PDF contra la fuente
python3 sellar_pdf.py                        # metadatos, marcadores, folios
python3 sync_flipbooks.py
```

`genealogia/taller/LEEME.md` explica cada paso, las trampas que cuestan caro y
las sondas con que se verifica. **Léalo antes de tocar nada**: aquí una tanda no
se da por buena leyendo el código, sino midiendo el PDF construido.

## Dónde está lo demás

| Ruta                                     | Qué es                                                                            |
| ---------------------------------------- | --------------------------------------------------------------------------------- |
| `genealogia/REGISTRO_DE_CORRECCIONES.md` | qué cambió en cada tanda, **cómo se comprobó** y qué quedó declarado sin corregir |
| `genealogia/norma/`                      | la norma editorial del proyecto                                                   |
| `genealogia/informes/`                   | documentos satélite del trabajo; no forman parte del libro                        |
| `genealogia/taller/sondas/`              | las comprobaciones, cada una sobre el archivo construido                          |
| `docs/git-instructions.md`               | cómo se versiona un libro que se corrige por tandas                               |

Las cifras de este libro —extensión, número de tandas, diferencias de cotejo— no
se copian aquí a propósito: viven donde se miden, y un README que las repitiera
empezaría a mentir en la tanda siguiente.
