#!/bin/bash
# Deja el taller editorial listo desde el primer turno: TeX Live con español y
# fontawesome5, qpdf y poppler-utils, y las dependencias de Python de las
# sondas (taller/sondas/requisitos.txt). Idempotente; solo en el entorno remoto.
set -euo pipefail
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then exit 0; fi
RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

if command -v pdflatex >/dev/null && command -v qpdf >/dev/null && command -v pdfinfo >/dev/null \
   && kpsewhich spanish.ldf >/dev/null 2>&1 && kpsewhich fontawesome5.sty >/dev/null 2>&1; then
  echo "taller revista: entorno TeX ya presente"
else
  echo "taller revista: instalando TeX Live (puede tardar unos minutos la primera vez)"
  apt-get update -qq
  apt-get install -y -qq --no-install-recommends \
    texlive-latex-base texlive-latex-recommended texlive-latex-extra \
    texlive-fonts-recommended texlive-fonts-extra texlive-lang-spanish \
    qpdf poppler-utils >/dev/null
  echo "taller revista: TeX listo"
fi

# Las sondas son la mitad del taller y este hook no las instalaba: un
# contenedor recien levantado compilaba y no podia medir nada. Se instalan
# desde lo versionado, no de memoria.
if python3 -c "import pypdfium2, pymupdf, pdfplumber, pikepdf" >/dev/null 2>&1; then
  echo "taller revista: sondas de Python ya presentes"
else
  echo "taller revista: instalando las dependencias de las sondas"
  python3 -m pip install -q -r "$RAIZ/taller/sondas/requisitos.txt"
  echo "taller revista: sondas listas"
fi
