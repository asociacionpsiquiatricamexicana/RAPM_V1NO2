# Prerequisitos del entorno

**Lee esto antes de intentar compilar cualquier cosa.** En una instalación limpia de TeX Live, `assets/ejemplo_editorial.tex` NO compila hasta cubrir estas dependencias. Verificado empíricamente: sin ellas la compilación aborta con `Fatal error occurred, no output PDF file produced!`.

## Verificación rápida

```bash
which pdflatex qpdf pdffonts pdfinfo pdftoppm
kpsewhich fontawesome5.sty          # debe devolver una ruta
kpsewhich spanish.ldf               # patrones de guionado español (babel)
python3 -c "import pdfplumber, fitz, pikepdf; print('python ok')"
```

Si `kpsewhich` no devuelve nada para alguno de los dos `.sty`/`.ldf`, instálalo antes de seguir.

## Dependencias LaTeX

| Requisito | Síntoma si falta | Instalación (Debian/Ubuntu) |
|---|---|---|
| `texlive-lang-spanish` | `! Package babel Error: Unknown option 'spanish'` (FM19) | `sudo apt install texlive-lang-spanish` |
| `fontawesome5` | `! LaTeX Error: File 'fontawesome5.sty' not found.` | `sudo apt install texlive-fonts-extra` o `tlmgr install fontawesome5` |
| TeX Live 2023+ base | Varios | `sudo apt install texlive-latex-recommended texlive-latex-extra` |
| `qpdf` | No se puede linearizar (paso 3 del workflow) | `sudo apt install qpdf` |
| `poppler-utils` | Faltan `pdffonts`, `pdfinfo`, `pdftoppm` | `sudo apt install poppler-utils` |

Con TeX Live vía `tlmgr` (macOS/MacTeX o instalación manual):
```bash
tlmgr install fontawesome5 babel-spanish hyphen-spanish totpages hyperxmp \
              microtype mdframed lettrine hanging nowidow widows-and-orphans \
              flushend dblfloatfix
```

Si `updmap-sys` falla durante la instalación, espera a que `dpkg` libere el lock y vuelve a correrlo (FM20).

## Dependencias Python (para el diagnóstico)

```bash
pip install pdfplumber pymupdf pikepdf
```

`pymupdf` provee el módulo `fitz`. Es el único indispensable para la capa I (footer) — `pdfplumber` intercala caracteres en texto <8pt (FM21).

## Nota sobre `fontawesome5`

El `.cls` carga `fontawesome5` (línea ~130) aunque las preferencias del editor dicen "sin íconos en metadata". El paquete sigue siendo una dependencia dura de compilación: si no está instalado, el documento no compila aunque no uses ningún ícono. Si en algún momento se decide eliminar los íconos por completo del sistema, retirar también el `\RequirePackage{fontawesome5}` para quitar la dependencia.

## Comprobación de humo

Antes de empezar un artículo nuevo, compila el ejemplo canónico para confirmar que el entorno está sano:

```bash
cd assets/
pdflatex -interaction=nonstopmode ejemplo_editorial.tex
pdflatex -interaction=nonstopmode ejemplo_editorial.tex
# Esperado: 0 errores, 0 overfull, 2 páginas, footer "Página 1 de 2"
qpdf --linearize ejemplo_editorial.pdf ejemplo_final.pdf
```

Si esto falla, el problema es el entorno, no tu manuscrito.
