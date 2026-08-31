#!/bin/bash
# Deja el taller editorial listo desde el primer turno: TeX Live con español y
# fontawesome5, qpdf y poppler-utils. Idempotente; solo en el entorno remoto.
set -euo pipefail
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then exit 0; fi
if command -v pdflatex >/dev/null && command -v qpdf >/dev/null && command -v pdfinfo >/dev/null \
   && kpsewhich spanish.ldf >/dev/null 2>&1 && kpsewhich fontawesome5.sty >/dev/null 2>&1; then
  echo "taller revista: entorno TeX ya presente"; exit 0
fi
echo "taller revista: instalando TeX Live (puede tardar unos minutos la primera vez)"
apt-get update -qq
apt-get install -y -qq --no-install-recommends \
  texlive-latex-base texlive-latex-recommended texlive-latex-extra \
  texlive-fonts-recommended texlive-fonts-extra texlive-lang-spanish \
  qpdf poppler-utils >/dev/null
echo "taller revista: listo"
