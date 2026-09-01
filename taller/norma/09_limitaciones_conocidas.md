# Limitaciones conocidas y hallazgos de auditoría

Este documento existe porque el material fuente de este skill contenía specs contradictorias y afirmaciones no verificadas contra el código real. Cada punto de abajo fue confirmado leyendo `apm-editorial.cls` directamente (no inferido de un prompt). Actualízalo cada vez que encuentres una discrepancia nueva entre lo que dice un documento y lo que hace el código.

## 1. `\APMtype{}` ya está conectado al render (corregido el 31 de agosto de 2026)

**Este hallazgo describía un defecto real, ya reparado en `taller/apm-editorial.cls`.** El `.cls` define:

```latex
\newcommand{\APMtype}[1]{\renewcommand{\@apmtype}{#1}}
```

y ahora el header y `\pdfinfo{}`/`\hypersetup{}` (`pdfsubject`) referencian `\@apmtype` en vez del texto literal `Editorial\par` que llevaban antes. Verificado compilando con `\APMtype{Artículo original}`: el rótulo del encabezado y el `pdfsubject` del PDF dicen «Artículo original», no «Editorial». El valor por omisión —cuando el `.tex` no llama `\APMtype{}`— sigue siendo `Editorial`, para no alterar el comportamiento del ejemplo existente (`reproducible.py` lo confirma: mismo hash de texto).

De paso se corrigió un defecto contiguo: la caja de RESUMEN se imprimía siempre, vacía si el autor no llamaba `\APMabstract{}` — relevante porque la norma exime de resumen a Editorial y Carta al Editor. Ahora la caja solo aparece cuando `\@apmabstract` no está vacío. La comparación de vacío por `\ifx` con `\empty` exigió además cambiar `\newcommand`/`\renewcommand` a sus variantes con asterisco en la definición de `\@apmabstract`: las no-asteriscadas producen macros `\long`, y un macro `\long` nunca es `\ifx`-igual a `\empty` aunque su contenido esté vacío — ese fue el primer intento y falló en silencio (la caja seguía imprimiéndose) hasta diagnosticarlo.

**Lo que sigue sin probar** (el punto 2 de abajo, sin cambios): que el layout de dos columnas + IMRaD funcione para cuerpos de 3,000–6,000 palabras con tablas y figuras. Conectar el rótulo no valida el diagramado de un Artículo original real; eso exige un manuscrito de prueba de esa extensión.

## 2. No existe clase probada para artículos de investigación (Original/Revisión/etc.)

`suicide_jalisco.tex` es el único intento de artículo no-Editorial en el material, y **no usa `apm-editorial.cls`** — declara su propio `\documentclass[10pt,letterpaper,twocolumn,twoside]{article}` y reimplementa colores, geometría (2.0/2.0/2.5/2.0cm, distinta a los 1.8/1.8/2.0/1.8cm de la clase) y paquetes desde cero. Es decir: es un fork paralelo, no una prueba de la clase compartida.

Si el usuario pide compilar un Artículo original con `apm-editorial.cls`, el camino correcto es migrar la lógica IMRaD a la clase compartida (extender `\@apmtype`, verificar que el layout de dos columnas + secciones H1/H2 funcione para cuerpos de 3,000–6,000 palabras con tablas/figuras, cosa que nunca se ha probado), no reutilizar `suicide_jalisco.tex` tal cual.

## 3. Código muerto: `\APMfolio{}` y `\APMlogoSixty{}`

### 3a. `\APMfolio{}`

Se define `\@apmfolio` y el setter `\APMfolio[1]`, y `assets/ejemplo_editorial.tex` incluso lo invoca (`\APMfolio{APM-2025-05-02-2824}`), pero `\@apmfolio` no aparece en ningún macro de renderizado (header, footer, running heads ni `\pdfinfo`/`\hypersetup`). El valor se pierde silenciosamente.

Esto es consistente con la regla de spec "Folio eliminado" (sección de elementos eliminados), pero es cruft sin limpiar: si alguien reactiva `\APMfolio` esperando que aparezca en el PDF, se va a llevar una sorpresa. Si el comité editorial SÍ necesita un folio interno visible, hay que reconectar el macro; si no lo necesita, habría que borrar el comando muerto del `.cls`.

En `assets/ejemplo_editorial.tex` la llamada a `\APMfolio{}` está **comentada** con una nota, precisamente para no enseñar la práctica equivocada al usar el ejemplo como plantilla.

### 3b. `\APMlogoSixty{}` (logo del 60 aniversario)

Exactamente el mismo patrón: el `.cls` define `\@apmlogosixty` (línea ~310) y su setter `\APMlogoSixty` (línea ~339), pero `\@apmlogosixty` **no aparece en ningún macro de renderizado**. El logo del 60 aniversario nunca se dibuja, sin importar lo que pases.

Consecuencia: `assets/logo_60anos.png` se conserva en el paquete como archivo de marca disponible, pero **no existe hoy un mecanismo funcional para colocarlo en el PDF**. Si el comité pide una pieza conmemorativa con ese logo, hay que escribir el código de render primero — no basta con llamar `\APMlogoSixty{logo_60anos.png}`.

Desde el 1 de septiembre de 2026 la llamada `\APMlogoSixty{}` de `taller/ejemplo_editorial.tex` está **comentada**, como la de `\APMfolio{}`, por la misma razón: la plantilla no debe enseñar una llamada sin efecto. El PDF no cambia (`reproducible.py`, mismo hash).

### 3c. Cinco macros definidos y sin uso: `\APMcheckabstract`, `\APMchecktitle`, `\fixellipsis`, `\APMrule`, `\APMcenterblock`

Hallados en la revisión del código del 1 de septiembre de 2026 (`REGISTRO_DE_PRODUCCION.md`). Ningún `.tex` del taller los llama (`grep` en `taller/*.tex`: cero ocurrencias). Son de dos clases distintas:

- **Dos «comprobaciones» que no comprueban nada.** `\APMcheckabstract{#1}` ejecuta un `\newcount\APM@wc` y lo pone en cero; su propio comentario dice «word count is approximate — manual verification recommended». `\APMchecktitle{#1}` tiene el cuerpo vacío: «compile-time check not possible». Llamarlos no produce aviso, error ni conteo. Un diagramador que los use esperando el aviso de resumen largo (más de 250 palabras) o de título largo (más de 15 palabras) no lo recibirá: es el mismo defecto que las sondas que decían «EN REGLA» sin medir, y una comprobación que no comprueba engaña más que ninguna. Esos conteos se hacen sobre el texto extraído del PDF, fuera de la compilación.
- **Tres ayudas de composición sin ocurrencia.** `\fixellipsis` (puntos suspensivos con 0.1 em de aire a cada lado; el paquete `ellipsis`, que la clase ya carga, corrige el espaciado de `\dots` por su cuenta), `\APMrule[ancho]` (regla borgoña de 0.5 pt con 3 pt de aire arriba y abajo) y `\APMcenterblock[ancho]{texto}` (minipágina centrada al 85 % del ancho de texto). Funcionan, pero no forman parte de la disposición medida de ninguno de los dos ejemplos.

**Decisión (1 de septiembre de 2026):** se documentan como interfaz no conectada y se dejan en el `.cls`, igual que `\APMfolio` (§3a) y `\APMlogoSixty` (§3b). Retirarlos es cambio de especificación (`CLAUDE.md`), no corrección, y corresponde al comité editorial. Mientras tanto no se llaman desde un `.tex` esperando efecto, y el check 21 de `10_checklist_auditoria_codigo.md` lo vigila.

## 4. Historial de specs contradictorias (ya resuelto, documentado por trazabilidad)

El material original incluía al menos 4 versiones de la especificación visual, algunas incompatibles entre sí:

| Documento                                   | Color primario                | Papel           | Notas                                                                                                                                                           |
| ------------------------------------------- | ----------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PROMPT_v3_FINAL_LaTeX_journal_PDF.md`      | (genérico, sin marca)         | a4paper         | Plantilla genérica pre-RAPM, benchmarks contra AJP/BJP/Lancet Psychiatry — nunca fue RAPM-específico                                                            |
| `PROMPT_CORRECTION_full_spec_compliance.md` | Rojo APM #C41E3A              | —               | Incluye íconos CC, abstract bilingüe obligatorio, running heads even/odd — descartado                                                                           |
| `PROMPT_CORRECTION_v4_definitivo.md`        | Borgoña #8B1A2B (ya correcto) | —               | Pero con Folio visible y layout de header distinto (VOL-line arriba, dos logos enmarcados, footer con nombres de Editor) — layout descartado                    |
| `RAPM_SISTEMA_EDITORIAL_v2.md`              | Borgoña #8B1A2B               | letterpaper     | Casi correcto pero desactualizado: 39 paquetes (el `.cls` real tiene 45), 583 líneas (el real tiene 665), 12 capas de diagnóstico (el proceso real usa 14, A–N) |
| **`apm-editorial.cls` (código real)**       | **Borgoña #8B1A2B**           | **letterpaper** | **Ground truth — todo este skill está alineado a esto**                                                                                                         |

Si en el futuro aparece un documento nuevo de sesiones anteriores que contradiga lo que hace el `.cls`, repite este proceso: verifica contra el código antes de creer al prompt.

## 5. Cobertura desigual del material original

El material fuente estaba fuertemente sesgado hacia producción/diagramaje LaTeX (9 de 10 documentos). La normalización APA 7 y la gestión de volúmenes/números no tenían artefactos propios — los archivos `06_gestion_volumenes_numeros.md` y `07_checklist_apa7.md` de este skill son construcciones nuevas para cerrar ese hueco, marcadas como tal en su propio encabezado. Revísalas con el comité editorial antes de tratarlas como proceso oficial ya aprobado.

## 6. Rutas hardcodeadas (riesgo operativo, no de diseño)

Versiones anteriores de `suicide_jalisco.tex` usaban rutas absolutas (`/home/claude/logo_perfect.png`) que no existían fuera de esa sesión. `assets/apm-editorial.cls` y `assets/ejemplo_editorial.tex` en este paquete usan rutas relativas a la carpeta del artículo — mantenlo así en cualquier `.tex` nuevo. Nunca hardcodees una ruta absoluta de una sesión anterior.
