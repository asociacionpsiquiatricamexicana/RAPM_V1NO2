"""Comprueba que cada marcador del PDF cae sobre su propio rotulo.

Diecinueve de los cuarenta y nueve mandaban una pagina antes: quien pinchaba
«Enrique Chavez Leon» en el panel de su visor aterrizaba en la pagina anterior.
La causa era que la entrada apunta a un bloque `anchor`, que no ocupa altura y
al que el paginador dejaba en la cola de la pagina que se cierra. Se arreglo en
libro.py, pero la medicion vivia en un guion desechable: si el desfase
reapareciera, nada lo cazaria. Aqui queda hecha sonda.

    python3 sondas/marcadores.py [ruta.pdf]

Sin argumento toma el PDF publicado. Sale 1 si algun marcador cae mal.

Un marcador que aterriza en una portadilla NO esta mal: es lo que se busca para
las aperturas de parte, y su rotulo se imprime en la pagina siguiente. Se
distinguen por la mancha: una portadilla lleva unos pocos caracteres frente a
los mas de mil de una pagina de texto.
"""
import os
import re
import sys

import pikepdf
import pypdfium2 as pdfium

AQUI = os.path.dirname(os.path.abspath(__file__))
POR_OMISION = os.path.join(AQUI, os.pardir, os.pardir,
                           "APM60_Genealogia__corregido.pdf")
RUTA = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(POR_OMISION)
UMBRAL_PORTADILLA = 300   # caracteres; una portadilla real ronda los 80

if not os.path.exists(RUTA):
    raise SystemExit(f"no encuentro el PDF en {RUTA}")

px, pdf = pikepdf.open(RUTA), pdfium.PdfDocument(RUTA)
pagina_de = {px.pages[i].obj.objgen: i for i in range(len(px.pages))}


def recorrer(nodo, salida=None):
    salida = [] if salida is None else salida
    hijo = nodo.get("/First")
    while hijo is not None:
        destino = hijo.get("/Dest") or (hijo.get("/A", {}) or {}).get("/D")
        pagina = None
        try:
            pagina = pagina_de.get(destino[0].objgen)
        except Exception:
            pagina = None
        salida.append((str(hijo.get("/Title", "")), pagina))
        if hijo.get("/First") is not None:
            recorrer(hijo, salida)
        hijo = hijo.get("/Next")
    return salida


raiz = px.Root.get("/Outlines")
marcadores = recorrer(raiz) if raiz is not None else []
print(f"marcadores: {len(marcadores)}")

cache = {}


def texto(i):
    if i not in cache:
        cache[i] = re.sub(r"[^a-záéíóúñü ]", "",
                          pdf[i].get_textpage().get_text_range().lower())
    return cache[i]


desfasados, sin_destino, en_portadilla = [], [], 0
for titulo, pagina in marcadores:
    if pagina is None:
        sin_destino.append(titulo)
        continue
    clave = [p for p in re.sub(r"[^A-Za-zÁÉÍÓÚÑáéíóúñü ]", " ", titulo).lower().split()
             if len(p) > 3][:3]
    if not clave:
        continue
    if all(p in texto(pagina) for p in clave):
        continue
    if len(texto(pagina).strip()) < UMBRAL_PORTADILLA:
        en_portadilla += 1
        continue
    if pagina + 1 < len(pdf) and all(p in texto(pagina + 1) for p in clave):
        desfasados.append((titulo, pagina + 1))

if en_portadilla:
    print(f"  {en_portadilla} aterrizan en una portadilla: correcto, "
          f"su rotulo va en la pagina siguiente")
if sin_destino:
    print(f"  {len(sin_destino)} sin pagina de destino: {sin_destino}")

if not desfasados:
    print("\nCADA MARCADOR CAE SOBRE SU ROTULO.")
    raise SystemExit(0)

print(f"\n{len(desfasados)} MARCADORES CAEN UNA PAGINA ANTES DE SU ROTULO:")
for titulo, pagina in desfasados:
    print(f"  «{titulo[:56]}» -> pagina {pagina} del PDF; el rotulo esta en la {pagina + 1}")
print("\nQuien los pinche en el panel de su visor aterriza en la pagina anterior.")
print("Se construyen en libro.py, no en sellar_pdf.py: mira que el destino")
print("avance desde el `anchor` hasta el primer bloque que de verdad pinta.")
raise SystemExit(1)
