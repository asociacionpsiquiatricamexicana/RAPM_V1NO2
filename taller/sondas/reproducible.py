#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba que el ejemplo se recompone igual desde lo versionado.

Leccion del libro: si el entregable no se puede regenerar desde el
repositorio, el repositorio no guarda el sistema, guarda un recuerdo. Copia
SOLO los archivos rastreados por git a un directorio limpio, compila alli y
compara paginas y texto contra el ancla (reproducible_<base>.txt, una por
documento).

Uso: python3 sondas/reproducible.py [ejemplo.tex] [--anclar]
     (por omision, ejemplo_editorial.tex; el .tex debe vivir en taller/,
     porque se compila solo con lo que taller/ tiene versionado)
"""
import hashlib, os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
TALLER = os.path.join(AQUI, os.pardir)
args = [a for a in sys.argv[1:] if not a.startswith('--')]
TEX = os.path.basename(args[0]) if args else 'ejemplo_editorial.tex'
BASE = TEX[:-4]
seguidos = subprocess.run(['git', '-C', TALLER, 'ls-files'], capture_output=True, text=True).stdout.split()
if TEX not in seguidos:
    raise SystemExit(f'{TEX} no esta versionado en taller/: esta sonda solo prueba lo que git guarda')

# El directorio temporal se retira siempre, tambien al anclar o al fallar:
# antes cada corrida dejaba un taller entero huerfano en /tmp.
with tempfile.TemporaryDirectory() as tmp:
    for rel in seguidos:
        src = os.path.join(TALLER, rel)
        dst = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    print(f'taller versionado: {len(seguidos)} archivos · compilando en limpio...')
    for _ in range(2):
        r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', TEX],
                           # pdflatex emite bytes latin-1 en sus avisos (nombres
                           # con acento); sin errors= la captura estricta revienta.
                           cwd=tmp, capture_output=True, text=True, errors='replace')
        if r.returncode != 0:
            raise SystemExit('NO COMPILA desde lo versionado:\n' + r.stdout[-800:])
    pdf = os.path.join(tmp, BASE + '.pdf')
    texto = subprocess.run(['pdftotext', pdf, '-'], capture_output=True).stdout
    h = hashlib.sha256(texto).hexdigest()
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf)
    paginas = len(doc)
    doc.close()  # si no, pypdfium2 avisa por stderr al salir

print(f'paginas: {paginas}\nhash del texto: {h}')
REF = os.path.join(AQUI, 'reproducible_' + BASE + '.txt')
if '--anclar' in sys.argv:
    open(REF, 'w', encoding='utf-8').write(f'{h}\n{paginas}\n')
    print('anclado en ' + os.path.basename(REF)); sys.exit(0)
if not os.path.exists(REF):
    raise SystemExit('sin ancla: corre con --anclar la primera vez y dilo en el registro')
eh, ep = open(REF, encoding='utf-8').read().split()
if (eh, int(ep)) != (h, paginas):
    raise SystemExit(f'NO SE RECOMPONE IGUAL: se esperaban {ep} paginas y {eh[:16]}..., '
                     f'salieron {paginas} y {h[:16]}...\n'
                     'Si el cambio era buscado, vuelve a anclar con --anclar y dilo en el registro.')
print('SE RECOMPONE IGUAL desde lo versionado.')
