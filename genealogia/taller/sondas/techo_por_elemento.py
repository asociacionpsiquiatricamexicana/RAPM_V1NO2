"""Halla, para cada rotulo de seguimiento ancho, el maximo que no rompe la copia.

Se compone cada uno con su tipografia, su cuerpo y su texto reales, uno por
pagina para que la extraccion no pueda desalinearse, y se extrae con el mismo
lector que usan los visores.

El seguimiento que cada elemento lleva HOY se lee de `bookstyle_extraido.js`,
no se copia aqui. Cuando iba copiado, la sonda siguio anunciando los valores
de antes de la tanda que los bajo, y recomendaba cambios ya hechos sobre un
libro que ya no existia: una sonda que guarda copia del libro acaba midiendo
su copia. Si un ancla deja de casar exactamente una vez, se dice y se sale con
codigo uno, en vez de suponer un valor.

El barrido empieza en 0,04 em y no en 0,10: los rotulos en versalitas viven por
debajo de 0,10, y un barrido que empieza encima de lo que el libro usa devuelve
«ninguno limpio» por no haber mirado, que es la peor forma de decir que no.
"""
import os
import re
import sys
import tempfile
from playwright.sync_api import sync_playwright
import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
TALLER = os.path.dirname(HERE)          # las sondas viven un piso mas abajo
ESTILO = os.path.join(TALLER, 'bookstyle_extraido.js')


def _chromium():
    """El navegador que compone las paginas.

    Se toma de la variable CHROME si esta definida; si no, del directorio de
    navegadores de Playwright, y en ultimo termino se deja que Playwright
    resuelva el suyo. Antes iba una ruta fija, valida solo en la maquina donde
    se compuso el libro.
    """
    import glob
    ruta = os.environ.get('CHROME')
    if ruta and os.path.exists(ruta):
        return ruta
    base = os.environ.get('PLAYWRIGHT_BROWSERS_PATH', '')
    for patron in (os.path.join(base, 'chromium*', 'chrome-linux', 'chrome'),
                   os.path.join(base, 'chromium*', 'chrome-*', 'chrome'),
                   os.path.join(base, 'chromium')):
        hallado = sorted(glob.glob(patron))
        if hallado:
            return hallado[-1]
    return None


CHROME = _chromium()
fuentes = open(os.path.join(TALLER, 'fuentes', 'fuentes.css'), encoding='utf-8').read()
estilo = open(ESTILO, encoding='utf-8').read()
HEAD = "'Cormorant Garamond','Gentium Griego',Georgia,serif"

# nombre, cuerpo en puntos, extras de estilo, texto, ancla en la hoja de estilo
CASOS = [
    ("portadilla · ordinal", 7.2, "text-transform:uppercase", "Primera Parte",
     r"fontSize: \(7\.2 \* k \* ts\) \+ 'px', letterSpacing: '([\d.]+)em'"),
    ("cubierta · aniversario", 7.2, "text-transform:uppercase", "Sexagésimo Aniversario · 1966–2026",
     r"line\(76, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("cubierta · titulo", 30, "font-variant:small-caps", "Genealogía",
     r"line\(168, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("cubierta · subtitulo", 12.5, "font-variant:small-caps", "de la Asociación Psiquiátrica Mexicana, A.C.",
     r"line\(222, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("cubierta · cargos", 6.4, "text-transform:uppercase", "Historiador Compilador",
     r"line\(442, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("cubierta · congreso", 9.5, "font-variant:small-caps", "XXX Congreso Nacional",
     r"line\(524, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("cubierta · sede", 6.4, "text-transform:uppercase",
     "Expo Santa Fe, Ciudad de México · 10 a 12 de septiembre de 2026",
     r"line\(541, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("cubierta · sello", 6.6, "text-transform:uppercase", "Asociación Psiquiátrica Mexicana, A.C.",
     r"line\(594, \{[^}]*letterSpacing: '([\d.]+)em'"),
    ("contracubierta · titulo", 11.5, "font-variant:small-caps",
     "Genealogía de la Asociación Psiquiátrica Mexicana, A.C.",
     r"lineHeight: 1\.35, fontVariant: 'small-caps', letterSpacing: '([\d.]+)em'"),
    ("contracubierta · pie", 6.6, "text-transform:uppercase",
     "Ciudad de México, 2026 · Acceso abierto · CC BY-NC-ND 4.0",
     r"lineHeight: 1\.7, letterSpacing: '([\d.]+)em'"),
    ("contracubierta · doi", 6.6, "text-transform:uppercase", "DOI 10.5281/zenodo.22035217",
     r"lineHeight: 1\.7, letterSpacing: '([\d.]+)em'"),
]
VAL = [round(0.04 + 0.01 * i, 2) for i in range(27)]   # de 0,04 a 0,30

# el seguimiento vigente, leido de la hoja de estilo
ahora, sin_ancla = {}, []
for nom, pt, extra, txt, ancla in CASOS:
    hallado = re.findall(ancla, estilo)
    if len(set(hallado)) != 1:
        sin_ancla.append((nom, len(hallado)))
    else:
        ahora[nom] = float(hallado[0])

if sin_ancla:
    print("NO SE PUDO LEER EL SEGUIMIENTO VIGENTE DE LA HOJA DE ESTILO:")
    for nom, n in sin_ancla:
        print(f"   {nom}: el ancla casa {n} veces, y debe casar una")
    print("\nLa hoja de estilo cambio de forma y las anclas de esta sonda quedaron")
    print("atras. Se corrigen aqui; suponer el valor seria medir un libro inventado.")
    raise SystemExit(1)

pags, clave = [], []
for nom, pt, extra, txt, _ in CASOS:
    for v in VAL:
        pags.append(f'<div class="pg" style="font-family:{HEAD};font-size:{pt}pt;font-weight:600;'
                    f'{extra};letter-spacing:{v}em;word-spacing:{-v}em">{txt}</div>')
        clave.append((nom, v, txt, extra))
html = ('<!doctype html><meta charset="utf-8"><style>' + fuentes +
        '@page{size:320mm 30mm;margin:6mm}body{margin:0}'
        '.pg{page-break-after:always;white-space:nowrap}</style><body>' + "".join(pags))

tmp = os.path.join(tempfile.mkdtemp(prefix='techo_'), 'techo.pdf')
with sync_playwright() as p:
    b = p.chromium.launch(**({'executable_path': CHROME} if CHROME else {}))
    pg = b.new_page()
    pg.set_content(html, wait_until='load')
    pg.pdf(path=tmp, width='320mm', height='30mm',
           margin={'top': '6mm', 'bottom': '6mm', 'left': '6mm', 'right': '6mm'})
    b.close()

pdf = pdfium.PdfDocument(tmp)
if len(pdf) != len(clave):
    print(f"SE COMPUSIERON {len(pdf)} PAGINAS Y SE ESPERABAN {len(clave)}:")
    print("la extraccion iria desalineada y cada veredicto seria de otro rotulo.")
    raise SystemExit(1)

techo = {}
for i, (nom, v, txt, extra) in enumerate(clave):
    got = " ".join(pdf[i].get_textpage().get_text_bounded().split())
    esp = " ".join((txt.upper() if "uppercase" in extra else txt).split())
    if got.replace(" ", "") == esp.replace(" ", "") and got.count(" ") == esp.count(" "):
        techo[nom] = v

print(f"{'elemento':<26}{'ahora':<9}{'techo limpio':<14}{'veredicto'}")
altos, ciegos = [], []
for nom, pt, extra, txt, _ in CASOS:
    t, act = techo.get(nom), ahora[nom]
    if t is None:
        est = "NINGUNO LIMPIO"
        ciegos.append(nom)
    elif t >= act:
        est = "cabe"
    else:
        est = f"SE PASA: {act} -> {t}"
        altos.append((nom, act, t))
    print(f"  {nom:<26}{act:<9}{str(t):<14}{est}")

print(f"\nbarrido de {VAL[0]} a {VAL[-1]} em · {len(CASOS)} rotulos")
if altos or ciegos:
    print()
    for nom, act, t in altos:
        print(f"«{nom}» va en {act} em y se parte al copiar desde {round(t + 0.01, 2)}.")
    for nom in ciegos:
        print(f"«{nom}» no sale entero a ningun seguimiento del barrido.")
    raise SystemExit(1)

print("\nCADA ROTULO VA POR DEBAJO DEL SEGUIMIENTO QUE ROMPE SU COPIA.")
raise SystemExit(0)
