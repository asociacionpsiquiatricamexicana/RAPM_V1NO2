# -*- coding: utf-8 -*-
"""Sigue cada entrada del Contenido hasta la pagina cuyo folio anuncia.

El folio se toma de las etiquetas de pagina del propio PDF —las que fija el
sellado y las que usa el visor—, no de leer el numero impreso, que puede caer
en cualquier sitio del flujo de texto extraido.

Las entradas no se adivinan leyendo renglones con una expresion regular: se
toman de la fuente del libro y se busca cada una en las paginas del Contenido.
Antes se barrian las veinte primeras paginas y se daba por entrada todo renglon
que acabase en numero, de modo que la sonda leia cuarenta y dos de las cuarenta
y nueve entradas —sin decir que faltaban siete— y acusaba de descuadre la
direccion postal de la pagina de creditos. Una sonda que calla lo que no midio
es peor que ninguna.

    python3 sondas/verificar_toc.py [pdf ya sellado]
"""
import json
import os
import re
import sys
import unicodedata
import pikepdf
import pypdfium2 as pdfium

AQUI = os.path.dirname(os.path.abspath(__file__))
TALLER = os.path.dirname(AQUI)
RUTA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    TALLER, os.pardir, 'APM60_Genealogia__corregido.pdf')
BIN = os.path.join(TALLER, 'assets', '08fffc00-d395-438c-88b0-a0545e4c4793.bin')

# Portada y contracubierta son paginas ciegas: se listan sin folio, y desde esta
# tanda tampoco llevan linea de puntos, que solo existe para llevar el ojo hasta
# un numero. La misma pareja la declara toc_html() en libro.py.
CIEGAS = ('portada', 'contracubierta')

TOC = json.load(open(BIN, encoding='utf-8'))['toc']
px = pikepdf.open(RUTA)
pdf = pdfium.PdfDocument(RUTA)
N = len(pdf)
pag = [pdf[i].get_textpage().get_text_bounded() for i in range(N)]

ROM = [(1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'), (100, 'c'), (90, 'xc'),
       (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]


def romano(n):
    s = ''
    for v, r in ROM:
        while n >= v:
            s += r
            n -= v
    return s


if "/PageLabels" not in px.Root:
    raise SystemExit(f"{RUTA} no lleva etiquetas de pagina: esta sonda necesita el PDF "
                     "ya sellado (sellar_pdf.py), no el recien compuesto.")
labels = px.Root.PageLabels.Nums
reglas = [(int(labels[i]), labels[i + 1]) for i in range(0, len(labels), 2)]
folio_de = {}
for k, (ini, d) in enumerate(reglas):
    fin = reglas[k + 1][0] if k + 1 < len(reglas) else N
    estilo = str(d.get("/S", ""))
    st = int(d.get("/St", 1))
    pref = str(d.get("/P", "")) if "/P" in d else ""
    for j in range(ini, fin):
        n = st + (j - ini)
        folio_de[j] = pref + (romano(n) if estilo == "/r" else str(n) if estilo == "/D" else "")
pagina_de = {}
for i, f in folio_de.items():
    if f:
        pagina_de.setdefault(f, i)
print(f'etiquetas de pagina: {len(reglas)} reglas, {len(pagina_de)} folios distintos')


def clave(s):
    s = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in s.lower() if c.isalnum())


# Las paginas del Contenido se reconocen por su cornisa, no por su posicion.
hojas = [i for i in range(N) if pag[i].strip().split('\n')[0].strip().upper() == 'CONTENIDO']
if not hojas:
    raise SystemExit('no encuentro ninguna pagina con la cornisa «CONTENIDO».')
cuerpo = '\n'.join(pag[i] for i in hojas)
plano = clave(cuerpo)
print(f'Contenido: paginas {", ".join(str(i + 1) for i in hojas)} del PDF · '
      f'{len(TOC)} entradas en la fuente')

# folio impreso junto a cada entrada: el numero que sigue al rotulo en el renglon
renglones = [l.strip() for l in cuerpo.replace('\r\n', '\n').split('\n') if l.strip()]
folio_junto = {}
for l in renglones:
    m = re.match(r'^(.*?)\s+(\d{1,3}|[ivxl]{1,7})$', l)
    if m:
        folio_junto[clave(m.group(1))] = m.group(2)

print()
bien = mal = ciegas = sin_rotulo = 0
for t in TOC:
    k = clave(t['label'])
    if k not in plano:
        sin_rotulo += 1
        print(f'  FALTA «{t["label"][:52]}»: no aparece en las paginas del Contenido')
        continue
    fol = folio_junto.get(k)
    if fol is None:
        if t.get('key') in CIEGAS:
            ciegas += 1
        else:
            mal += 1
            print(f'  SIN FOLIO «{t["label"][:52]}»: figura en el Contenido y no anuncia pagina')
        continue
    if t.get('key') in CIEGAS:
        mal += 1
        print(f'  «{t["label"][:52]}» es pagina ciega y anuncia el folio {fol}')
        continue
    p = pagina_de.get(fol)
    if p is None:
        mal += 1
        print(f'  «{t["label"][:52]}» -> folio {fol}: no hay pagina con ese folio')
        continue
    palabras = [w for w in re.sub(r'[^\wáéíóúñÁÉÍÓÚÑ ]', ' ', t['label']).split() if len(w) > 3][:3]
    zona = clave(' '.join(pag[max(0, p - 1):p + 2]))
    if all(clave(w) in zona for w in palabras):
        bien += 1
    else:
        mal += 1
        print(f'  MAL «{t["label"][:52]}» -> folio {fol} (pagina {p + 1} del PDF): no aparece ahi')

print(f'\n  cuadran {bien} · sin folio por ser ciegas {ciegas} · '
      f'no cuadran {mal} · ausentes del Contenido {sin_rotulo}')
if mal or sin_rotulo:
    raise SystemExit(1)
print(f'  LAS {len(TOC)} ENTRADAS DEL CONTENIDO ESTAN Y CAEN DONDE ANUNCIAN.')
