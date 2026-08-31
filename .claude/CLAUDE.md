# Revista de la Asociación Psiquiátrica Mexicana, A.C.

Esta rama produce la revista (e-ISSN 3061-7979, cuatrimestral, CC BY-NC 4.0):
artículos camera-ready compuestos en LaTeX con la clase del taller. El taller
vive en `taller/` y su `LEEME.md` explica el proceso y sus trampas. No es el
libro de la Genealogía: aquello fue una obra única y está en su propia rama.

## Las reglas que no se negocian

- **No se toca el texto de los autores.** Una errata de contenido se devuelve
  al autor o se anota; no se corrige en silencio al diagramar. Citas,
  referencias y datos clínicos son intangibles para el diagramador.
- **El código es la especificación.** Ante divergencia entre la norma escrita
  (`taller/norma/`) y `taller/apm-editorial.cls`, gana el `.cls`; cambiarlo
  es cambio de especificación, no corrección.
- **Verificar es medir el PDF construido**, con las sondas de
  `taller/sondas/`, nunca estimar ni recordar. Las cifras van ancladas y el
  ancla solo se mueve con razón declarada en `REGISTRO_DE_PRODUCCION.md`.

Antes de confirmar una tanda, abre `docs/git-instructions.md`.
