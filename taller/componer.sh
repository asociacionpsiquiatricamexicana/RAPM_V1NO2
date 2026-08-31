#!/usr/bin/env bash
# componer.sh — compila un articulo al camera-ready y lo mide.
#
#   bash taller/componer.sh ruta/al/articulo.tex
#
# pdflatex x2 (referencias cruzadas y totpages piden dos pasadas), exige cero
# errores, lineariza con qpdf y corre la sonda de geometria. Sin argumento,
# compila el ejemplo del taller a taller/pdfs/.
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEX="${1:-$AQUI/ejemplo_editorial.tex}"
DIR="$(cd "$(dirname "$TEX")" && pwd)"; BASE="$(basename "$TEX" .tex)"
# la clase y los logos deben ser visibles desde el directorio del articulo
for f in apm-editorial.cls logo_hires.png logo_60anos.png; do
  [[ -f "$DIR/$f" ]] || cp "$AQUI/$f" "$DIR/"
done
for pasada in 1 2; do
  (cd "$DIR" && pdflatex -interaction=nonstopmode -halt-on-error "$BASE.tex" >"$BASE.pass$pasada.log" 2>&1) \
    || { echo "COMPILACION FALLIDA (pasada $pasada): vease $DIR/$BASE.pass$pasada.log y taller/norma/04_failure_modes.md"; exit 1; }
done
OVER="$(grep -c "Overfull" "$DIR/$BASE.pass2.log" || true)"
[[ "$OVER" == "0" ]] || { echo "OVERFULL: $OVER cajas desbordadas — no es camera-ready"; exit 1; }
mkdir -p "$AQUI/pdfs"
DESTINO="$DIR/$BASE.pdf"; [[ "$TEX" == "$AQUI/ejemplo_editorial.tex" ]] && DESTINO="$AQUI/pdfs/$BASE.pdf"
qpdf --linearize "$DIR/$BASE.pdf" "$DESTINO.lin" && mv "$DESTINO.lin" "$DESTINO"
echo "escrito: $DESTINO ($(stat -c%s "$DESTINO") bytes)"
python3 "$AQUI/sondas/geometria.py" "$DESTINO"
