#!/usr/bin/env bash
# comprobar_entorno.sh — Prueba en frío del entorno de producción de RAPM.
#
# Ejecuta lo que `norma/00_prerequisitos.md` documenta, en lugar de
# limitarse a describirlo, y termina con una compilación real de
# `ejemplo_editorial.tex`. Corrase al inicio de sesión, antes de
# comprometer un artículo: un fallo aquí es del entorno, no del manuscrito.
#
# Uso:  bash taller/comprobar_entorno.sh   (o ./comprobar_entorno.sh desde taller/)
# Salida: 0 si el entorno compila; 1 si falta algo bloqueante.

set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FALLOS=0

titulo() { printf '\n== %s ==\n' "$1"; }

comprobar_orden() {
  local orden="$1" remedio="$2"
  if command -v "$orden" >/dev/null 2>&1; then
    printf '  presente  %s\n' "$orden"
  else
    printf '  AUSENTE   %s   →  %s\n' "$orden" "$remedio"
    FALLOS=$((FALLOS + 1))
  fi
}

comprobar_estilo() {
  local archivo="$1" remedio="$2"
  if kpsewhich "$archivo" >/dev/null 2>&1; then
    printf '  presente  %s\n' "$archivo"
  else
    printf '  AUSENTE   %s   →  %s\n' "$archivo" "$remedio"
    FALLOS=$((FALLOS + 1))
  fi
}

titulo "Órdenes de sistema"
comprobar_orden pdflatex "apt install texlive-latex-recommended texlive-latex-extra"
comprobar_orden qpdf     "apt install qpdf"
comprobar_orden pdffonts "apt install poppler-utils"
comprobar_orden pdfinfo  "apt install poppler-utils"

titulo "Paquetes de LaTeX (dependencias duras del .cls)"
comprobar_estilo spanish.ldf      "apt install texlive-lang-spanish"
comprobar_estilo fontawesome5.sty "apt install texlive-fonts-extra"
comprobar_estilo hyperxmp.sty     "apt install texlive-latex-extra"
comprobar_estilo totpages.sty     "apt install texlive-latex-extra"

titulo "Activos de la clase"
for activo in apm-editorial.cls ejemplo_editorial.tex logo_hires.png logo_60anos.png; do
  if [[ -f "$RAIZ/$activo" ]]; then
    printf '  presente  %s\n' "$activo"
  else
    printf '  AUSENTE   %s\n' "$activo"
    FALLOS=$((FALLOS + 1))
  fi
done

titulo "Compilación de prueba"
if (( FALLOS > 0 )); then
  printf '  omitida: repárense primero las carencias anteriores.\n'
else
  TEMPORAL="$(mktemp -d)"
  trap 'rm -rf "$TEMPORAL"' EXIT
  cp "$RAIZ"/apm-editorial.cls "$RAIZ"/ejemplo_editorial.tex "$RAIZ"/logo_hires.png "$RAIZ"/logo_60anos.png "$TEMPORAL/"
  if (cd "$TEMPORAL" && pdflatex -interaction=nonstopmode -halt-on-error \
        ejemplo_editorial.tex >compilacion.log 2>&1); then
    PAGINAS="$(pdfinfo "$TEMPORAL/ejemplo_editorial.pdf" 2>/dev/null \
               | awk '/^Pages:/{print $2}')"
    printf '  correcta: ejemplo_editorial.pdf, %s página(s).\n' "${PAGINAS:-?}"
  else
    printf '  FALLIDA. Primeros errores:\n'
    grep -m 3 -A 3 '^!' "$TEMPORAL/compilacion.log" | sed 's/^/    /'
    printf '  Diagnóstico por modo de fallo: norma/04_failure_modes.md\n'
    FALLOS=$((FALLOS + 1))
  fi
fi

titulo "Veredicto"
if (( FALLOS == 0 )); then
  printf '  Entorno apto para producción camera-ready.\n'
  exit 0
fi
printf '  %d carencia(s). Véase norma/00_prerequisitos.md.\n' "$FALLOS"
exit 1
