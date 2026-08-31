# -*- coding: utf-8 -*-
"""Mide, sobre el PDF construido, si la bajada se compone pegada a su titulo.

Una bajada —el subtitulo que sigue inmediatamente a un rotulo o a una seccion—
pertenece al titulo que la precede. Si el aire que la separa de su titulo es
mayor que el que la separa del cuerpo, el ojo la lee como entradilla del texto
y no como parte del titulo. Aqui se comprueba lo contrario, renglon a renglon:

    arriba  = base del ultimo renglon del titulo  -  base del primero de la bajada
    abajo   = base del ultimo renglon de la bajada - base del primero del cuerpo

Se espera arriba < abajo en todas las parejas. Las parejas las declara la
fuente («bajada: 1» en el titulo y en el subtitulo); libro.py las vuelve a
derivar en cada corrida y aborta si la fuente ya no las dice bien.

    python3 sondas/aire_de_la_bajada.py [pdf]
"""
import json
import os
import sys
import unicodedata
import pypdfium2 as pdfium

AQUI = os.path.dirname(os.path.abspath(__file__))
TALLER = os.path.dirname(AQUI)
RUTA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TALLER, 'pdfs', 'libro.pdf')
BIN = os.path.join(TALLER, 'assets', '08fffc00-d395-438c-88b0-a0545e4c4793.bin')
DBG = os.path.join(TALLER, 'pdfs', 'pages_debug.json')

if not os.path.exists(DBG):
    raise SystemExit(f'falta {DBG}: esta sonda necesita la paginacion de la misma '
                     'corrida que el PDF (la escribe libro.py).')

B = json.load(open(BIN, encoding='utf-8'))['blocks']
dbg = json.load(open(DBG, encoding='utf-8'))
pdf = pdfium.PdfDocument(RUTA)

# pages_debug.json cubre el interior; la cubierta va delante y la contracubierta
# detras, de modo que la pagina n del interior es la n+1 del PDF (base cero).
DESFASE = (len(pdf) - len(dbg)) // 2
pagina_de = {}
for n, p in enumerate(dbg):
    for s in p.get('segs', []):
        pagina_de.setdefault(s[0], n + DESFASE)


def texto(b):
    return ''.join(' ' if p.get('br') else (p.get('x') or '') for p in b.get('parts') or [])


def clave(s):
    s = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in s.lower() if c.isalnum())


def renglones(pno, tol=4.0):
    """Los renglones de una pagina, en orden de lectura.

    La caja holgada de un glifo no da la misma base para todos los de su
    renglon: las letras con rasgo descendente y las versalitas bajan hasta tres
    puntos respecto de las demas. Agrupar por igualdad exacta parte cada renglon
    en docenas de trozos —y con un margen corto, en dos o tres—, de modo que la
    sonda medía el interlineado dentro de un renglon y no el aire entre
    renglones. Se agrupa por cercania a la base mas alta del renglon en curso,
    que es la de las letras sin descendente, con holgura menor que el
    interlineado del cuerpo (15 pt).
    """
    tp = pdf[pno].get_textpage()
    n = tp.count_chars()
    filas, cur, base = [], [], None
    for i in range(n):
        c = tp.get_text_range(i, 1)
        _, lb, _, _ = tp.get_charbox(i, loose=True)
        if not c.strip():
            if cur:
                cur.append((c, lb))
            continue
        if base is None or abs(lb - base) <= tol:
            base = lb if base is None else max(base, lb)
            cur.append((c, lb))
        else:
            if cur:
                filas.append(cur)
            cur, base = [(c, lb)], lb
    if cur:
        filas.append(cur)
    out = []
    for f in filas:
        bases = [b for c, b in f if c.strip()]
        if not bases:
            continue
        out.append({'txt': ''.join(c for c, _ in f), 'base': max(bases)})
    return out


parejas = [i for i, b in enumerate(B) if b.get('t') == 'sub' and b.get('bajada')]
if not parejas:
    raise SystemExit('la fuente no declara ninguna pareja titulo+bajada.')

print(f'{"blq":>5} {"pag":>4} {"arriba":>7} {"abajo":>7}   bajada')
mal = perdidas = 0
for i in parejas:
    pno = pagina_de.get(i)
    if pno is None:
        print(f'{i:>5}    ?                     {texto(B[i])[:44]}  (sin pagina)')
        perdidas += 1
        continue
    R = renglones(pno)
    k = clave(texto(B[i]))
    ini = next((j for j, r in enumerate(R) if clave(r['txt'])[:16] and k.startswith(clave(r['txt'])[:16])), None)
    if ini is None:
        print(f'{i:>5} {pno+1:>4}                     {texto(B[i])[:44]}  (no localizada)')
        perdidas += 1
        continue
    fin, visto = ini, ''
    while fin < len(R) and len(visto) < len(k):
        visto += clave(R[fin]['txt'])
        fin += 1
    fin -= 1
    if ini == 0 or fin + 1 >= len(R):
        print(f'{i:>5} {pno+1:>4}                     {texto(B[i])[:44]}  (al borde de la pagina)')
        perdidas += 1
        continue
    arriba = R[ini - 1]['base'] - R[ini]['base']
    abajo = R[fin]['base'] - R[fin + 1]['base']
    marca = '  <-- la bajada se separa mas de su titulo que del cuerpo' if arriba >= abajo else ''
    if arriba >= abajo:
        mal += 1
    print(f'{i:>5} {pno+1:>4} {arriba:7.1f} {abajo:7.1f}   {texto(B[i])[:44]}{marca}')

print()
if perdidas:
    print(f'{perdidas} bajadas no medidas (parten pagina o no se localizaron).')
if mal:
    print(f'{mal} de {len(parejas) - perdidas} bajadas se leen como entradilla del cuerpo.')
    raise SystemExit(1)
print(f'LAS {len(parejas) - perdidas} BAJADAS MEDIDAS SE COMPONEN PEGADAS A SU TITULO.')
