# Checklist de auditoría de código (`.cls` / `.tex`)

Este checklist es para revisar el CÓDIGO fuente antes de compilar — complementa el diagnóstico de 14 capas de `05_workflow_produccion_y_diagnostico.md`, que revisa el PDF ya compilado. Úsalo cuando el usuario pida "auditar el sistema", antes de aceptar un `.cls` o `.tex` nuevo, o cuando algo se comporta de forma extraña y sospechas que es un bug de código, no de contenido.

## Protocolo

1. Lee el archivo completo antes de tocar nada (`cat -n apm-editorial.cls`, ~665 líneas).
2. Corre los checks estáticos de abajo contra el CÓDIGO FUENTE, no contra el PDF.
3. Compila y verifica: 0 errores, 0 overfull >1pt.
4. Solo entonces corre el diagnóstico de 14 capas sobre el PDF resultante.

Nunca arregles "por sensación" — mide primero.

## Checks sobre `apm-editorial.cls`

| #   | Check                                                                                    | Cómo verificar                                                                                                                                                                                                                                                       |
| --- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 1   | Papel = `letterpaper` (no `a4paper`)                                                     | `grep LoadClass apm-editorial.cls`                                                                                                                                                                                                                                   |
| 2   | Cero definiciones de color redundantes                                                   | Contar valores hex únicos en `\definecolor`                                                                                                                                                                                                                          |
| 3   | Cero colores definidos y nunca usados                                                    | `grep` cada nombre de color en todo el archivo                                                                                                                                                                                                                       |
| 4   | Sin valores de vol/año/período hardcodeados por defecto                                  | `\newcommand{\@apmvol}{}` etc. deben quedar vacíos, no con un valor de ejemplo                                                                                                                                                                                       |
| 5   | `\parindent` y `\parskip` se fijan UNA sola vez                                          | `grep parindent`/`grep parskip` — solo debe aparecer en el macro de construcción del documento                                                                                                                                                                       |
| 6   | `\sloppy` se invoca una sola vez por entorno                                             | `grep '\\sloppy'` en el arranque/quiebre de referencias                                                                                                                                                                                                              |
| 7   | Running heads LE/RO usan formato consistente entre sí                                    | Comparar `\fancyhead[LE]` contra `\fancyhead[RO]`                                                                                                                                                                                                                    |
| 8   | `pdfborder={0 0 0}` en `\hypersetup` (sin cajas visibles en links)                       | `grep pdfborder`                                                                                                                                                                                                                                                     |
| 9   | Tamaño de fuente del colofón coincide con el de referencia                               | Comparar `\fontsize` en el colofón vs en el inicio de referencias                                                                                                                                                                                                    |
| 10  | `\APMrefsbreak` no puede duplicarse                                                      | Revisar contenido de los `.tex`                                                                                                                                                                                                                                      |
| 11  | Cada `\begingroup` tiene su `\endgroup`                                                  | Contar pares                                                                                                                                                                                                                                                         |
| 12  | `\APMtype{}` está conectado al render del header                                         | `grep '@apmtype' apm-editorial.cls` — debe aparecer en el setter, en el macro que construye el header y en `pdfsubject`. Conectado el 31 de agosto de 2026 (ver `09_limitaciones_conocidas.md` #1).                                                                  |
| 13  | `\APMfolio{}` está conectado a algún render, o se documenta explícitamente como no-usado | `grep 'apmfolio'` — **hoy es código muerto, ver `09_limitaciones_conocidas.md` #3**                                                                                                                                                                                  |
| 14  | `\emergencystretch` está fijado (para el colofón)                                        | `grep emergencystretch`                                                                                                                                                                                                                                              |
| 15  | No se carga `academicons` ni `stfloats` (FM02, FM15)                                     | `grep -E "academicons                                                                                                                                                                                                                                                | stfloats"` — no debe haber coincidencias |
| 16  | `hyperxmp` se carga DESPUÉS de `hyperref` (FM16)                                         | Revisar orden de `\RequirePackage`/`\usepackage`                                                                                                                                                                                                                     |
| 17  | Todas las rutas a imágenes/logos son relativas, no absolutas                             | `grep -E "includegraphics.\*\/home                                                                                                                                                                                                                                   | \/Users"` — no debe haber coincidencias  |
| 18  | NO se carga `lastpage` (FM24)                                                            | `grep -n 'RequirePackage{lastpage}' apm-editorial.cls` — cero coincidencias. `hyperxmp` ya trae `totpages` y son incompatibles. (Usa este patrón exacto, no `grep lastpage` a secas: la palabra aparece legítimamente en el comentario explicativo de la línea ~278) |
| 19  | El total de páginas usa `\ref{TotPages}`, no `\pageref{LastPage}` (FM24)                 | `grep -c 'pageref{LastPage}'` → 0, y `grep -c 'de \\ref{TotPages}'` → 2 (los dos footers: `fancyfoot[C]` normal y el de `firstpage`)                                                                                                                                 |
| 20  | `\APMlogoSixty` está conectado al render, o se documenta como no-usado                   | `grep 'apmlogosixty'` — **hoy es código muerto, ver `09_limitaciones_conocidas.md` §3b**                                                                                                                                                                             |

## Checks sobre archivos `.tex` de contenido

| #   | Check                                                                                                            | Cómo verificar                                             |
| --- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------- |
| 1   | `\documentclass{apm-editorial}` (no reimplementa su propio preámbulo)                                            | Primera línea no-comentario del archivo                    |
| 2   | `\APMvolume`/`\APMnum`/`\APMperiod`/`\APMyear` están fijados explícitamente                                      | `grep` cada uno                                            |
| 3   | `\APMdates` tiene 3 fechas plausibles (recibido ≤ aceptado ≤ publicado)                                          | Revisar valores                                            |
| 4   | El año de la licencia (©) coincide con el año del artículo                                                       | Comparar `\textcopyright\ AAAA` con `\APMvolume{}{}{AAAA}` |
| 5   | Título, resumen y palabras clave están en el idioma del artículo                                                 | Lectura directa                                            |
| 6   | `\APMrefsbreak` solo se usa con ≥12 referencias (FM05)                                                           | Contar `\APMref{`                                          |
| 7   | No hay `\APMrefsbreak` duplicado                                                                                 | `grep -c APMrefsbreak`                                     |
| 8   | Cada `\APMref` tiene su `\url{}` con DOI o URL                                                                   | Revisar cada entrada                                       |
| 9   | Sin rutas absolutas hardcodeadas de otra sesión (`/home/claude/...`)                                             | `grep -E "\/home\/                                         | \/Users\/"` |
| 10  | Si el artículo no es Editorial, se confirmó primero el punto #12 del checklist del `.cls` (`\APMtype` conectado) | Manual                                                     |

## Verificación de compilación

```bash
pdflatex -interaction=nonstopmode archivo.tex   # ×2
# Verificar: 0 errores, 0 overfull >1pt, número de páginas esperado
qpdf --check archivo.pdf
```
