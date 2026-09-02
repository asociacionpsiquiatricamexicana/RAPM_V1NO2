#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mide el PDF camera-ready: paginas, caja, tipografias incrustadas, peso.

Leccion del libro de la Genealogia: toda afirmacion sobre el PDF viene de una
medicion, nunca de inspeccion visual ni de memoria. Esta sonda responde cuatro
preguntas concretas y compara contra su ancla (geometria_<base>.txt, una por
documento) si existe; el ancla solo se mueve con razon declarada en el registro.

Uso: python3 sondas/geometria.py [ruta.pdf]   (por omision, el ejemplo compilado)
"""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, os.pardir, 'pdfs', 'ejemplo_editorial.pdf')
if not os.path.exists(RUTA):
    raise SystemExit(f'no existe {RUTA}: compila primero (taller/componer.sh)')

import pypdfium2 as pdfium
doc = pdfium.PdfDocument(RUTA)
paginas = len(doc)
cajas = {(round(p.get_size()[0], 2), round(p.get_size()[1], 2)) for p in doc}
peso = os.path.getsize(RUTA)

fuentes = subprocess.run(['pdffonts', RUTA], capture_output=True, text=True).stdout
# pdffonts: la columna 'emb' es la quinta empezando por el final.
noincrustadas = []
for l in fuentes.splitlines()[2:]:
    c = l.split()
    if len(c) >= 5 and c[-5] == 'no':
        noincrustadas.append(c[0])

# FM06, la fuga de Computer Modern. Estar incrustada no basta: una CM dentro
# de un diseno Times/Nimbus es un defecto de composicion, y la sonda lo daba
# por bueno porque solo miraba la columna 'emb'. Los nombres vienen como
# ABCDEF+CMSY10; el prefijo de subconjunto se descarta.
CM = ('CMR', 'CMBX', 'CMMI', 'CMSY', 'CMEX', 'CMTI', 'CMTT', 'SFRM', 'SFRB')
fugadas = []
for l in fuentes.splitlines()[2:]:
    c = l.split()
    if not c:
        continue
    nombre = c[0].split('+', 1)[-1]
    if nombre.upper().startswith(CM):
        fugadas.append(c[0])

print(f'paginas: {paginas}')
print(f'cajas de pagina distintas: {sorted(cajas)}')
print(f'peso: {peso} bytes ({peso/1024:.0f} KB; el tope de despliegue es 600 KB)')
print(f'tipografias sin incrustar: {len(noincrustadas)} {noincrustadas or ""}')
print(f'fuga de Computer Modern (FM06): {len(fugadas)} {fugadas or ""}')

fallos = []
if len(cajas) != 1:
    fallos.append('las paginas no comparten caja')
if peso > 600 * 1024:
    fallos.append('el archivo excede los 600 KB del despliegue')
if noincrustadas:
    fallos.append('hay tipografias sin incrustar')
if fugadas:
    fallos.append(f'FM06, Computer Modern en un diseno Times/Nimbus: {fugadas}')

# Un ancla por documento: el taller ya compone mas de un ejemplo y cada uno
# tiene su propio numero de paginas esperado.
REF = os.path.join(AQUI, 'geometria_' + os.path.basename(RUTA)[:-4] + '.txt')
if os.path.exists(REF):
    esp = dict(l.split('=', 1) for l in open(REF, encoding='utf-8').read().split() if '=' in l)
    if int(esp.get('paginas', -1)) != paginas:
        fallos.append(f"el ejemplo esperaba {esp['paginas']} paginas y salieron {paginas}")
    print(f"ancla: {esp}")
else:
    print(f'sin ancla ({os.path.basename(REF)}): anclala y dilo en el registro')

if fallos:
    raise SystemExit('GEOMETRIA CON FALLOS:\n  ' + '\n  '.join(fallos))
print('GEOMETRIA EN REGLA.')
