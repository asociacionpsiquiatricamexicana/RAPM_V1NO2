"""Comprueba que cada marcador del PDF cae sobre su propio rotulo.

Dieciocho de los cuarenta y nueve mandaban una pagina antes: quien pinchaba
«Enrique Chavez Leon» en el panel de su visor aterrizaba en la pagina anterior.
La causa era que la entrada apunta a un bloque `anchor`, que no ocupa altura y
al que el paginador dejaba en la cola de la pagina que se cierra. Se arreglo en
libro.py, pero la medicion vivia en un guion desechable: si el desfase
reapareciera, nada lo cazaria. Aqui queda hecha sonda.

    python3 sondas/marcadores.py [ruta.pdf]

Sin argumento toma el PDF publicado. Sale 1 si algo no queda comprobado.

Cada marcador cae en una sola casilla, y solo dos son correctas:

  - su rotulo se imprime en su propia pagina;
  - aterriza en una portadilla y el rotulo se imprime en la siguiente —asi se
    quieren las aperturas de parte—;
  - DESFASE: el rotulo esta en la pagina siguiente y esa pagina no es
    portadilla, sino pagina de texto: es el defecto que se caza aqui;
  - sin pagina de destino resoluble;
  - el titulo no deja ninguna palabra con que buscar;
  - el rotulo no aparece ni en su pagina ni en la siguiente.

Las dos ultimas no son necesariamente defectos, pero tampoco quedan
comprobadas, y una sonda que calla lo que no pudo medir no sirve de sonda: se
declaran por nombre en ROTULO_NO_IMPRESO las que se saben correctas —Portada y
Contracubierta llevan por rotulo el nombre de la pagina, no un texto que este
impreso en ella— y cualquier otra hace salir 1.

El umbral de portadilla esta medido sobre el libro, no supuesto: las
portadillas reales van de setenta y cuatro a ciento diez caracteres, y la
pagina de texto mas rala salta a doscientos cuarenta y cuatro.
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
UMBRAL_PORTADILLA = 160   # caracteres; medido: portadillas 74-110, texto 244+
ROTULO_NO_IMPRESO = {"Portada", "Contracubierta"}

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

if not marcadores:
    print("\nEL PDF NO TRAE UN SOLO MARCADOR.")
    print("Los construye libro.py a partir del TOC; si el panel del visor sale")
    print("vacio, mira ahi antes que en sellar_pdf.py.")
    raise SystemExit(1)

cache = {}


def texto(i):
    if i not in cache:
        cache[i] = re.sub(r"[^a-záéíóúñü ]", "",
                          pdf[i].get_textpage().get_text_range().lower())
    return cache[i]


desfasados, sin_destino, sin_clave, no_impreso = [], [], [], []
en_rotulo = en_portadilla = 0

for titulo, pagina in marcadores:
    if pagina is None:
        sin_destino.append(titulo)
        continue
    clave = [p for p in re.sub(r"[^A-Za-zÁÉÍÓÚÑáéíóúñü ]", " ", titulo).lower().split()
             if len(p) > 3][:3]
    if not clave:
        sin_clave.append(titulo)
        continue
    if all(p in texto(pagina) for p in clave):
        en_rotulo += 1
        continue
    en_la_siguiente = (pagina + 1 < len(pdf)
                       and all(p in texto(pagina + 1) for p in clave))
    if not en_la_siguiente:
        no_impreso.append((titulo, pagina))
    elif len(texto(pagina).strip()) < UMBRAL_PORTADILLA:
        en_portadilla += 1
    else:
        desfasados.append((titulo, pagina))

print(f"  {en_rotulo} caen sobre su rotulo")
if en_portadilla:
    print(f"  {en_portadilla} aterrizan en una portadilla: correcto, "
          f"su rotulo va en la pagina siguiente")

declarados = [t for t, _ in no_impreso if t in ROTULO_NO_IMPRESO]
if declarados:
    print(f"  {len(declarados)} llevan por rotulo el nombre de la pagina, no un "
          f"texto impreso en ella: {declarados}")

sin_comprobar = [(t, p) for t, p in no_impreso if t not in ROTULO_NO_IMPRESO]
fallos = bool(desfasados or sin_destino or sin_clave or sin_comprobar)

if not fallos:
    print("\nCADA MARCADOR CAE SOBRE SU ROTULO.")
    raise SystemExit(0)

if desfasados:
    print(f"\n{len(desfasados)} MARCADORES CAEN UNA PAGINA ANTES DE SU ROTULO:")
    for titulo, pagina in desfasados:
        print(f"  «{titulo[:56]}» -> pagina {pagina} del PDF; "
              f"el rotulo esta en la {pagina + 1}")
    print("\nQuien los pinche en el panel de su visor aterriza en la pagina anterior.")
    print("Se construyen en libro.py, no en sellar_pdf.py: mira que el destino")
    print("avance desde el `anchor` hasta el primer bloque que de verdad pinta.")

if sin_destino:
    print(f"\n{len(sin_destino)} MARCADORES SIN PAGINA DE DESTINO RESOLUBLE:")
    for titulo in sin_destino:
        print(f"  «{titulo[:56]}»")
    print("No se puede decir a donde llevan: en el visor no llevaran a ningun lado.")

if sin_clave:
    print(f"\n{len(sin_clave)} MARCADORES SIN PALABRA CON QUE BUSCAR:")
    for titulo in sin_clave:
        print(f"  «{titulo[:56]}»")
    print("El titulo no deja ninguna palabra de mas de tres letras; quedan sin medir.")

if sin_comprobar:
    print(f"\n{len(sin_comprobar)} MARCADORES CUYO ROTULO NO APARECE NI EN SU "
          f"PAGINA NI EN LA SIGUIENTE:")
    for titulo, pagina in sin_comprobar:
        print(f"  «{titulo[:56]}» -> pagina {pagina} del PDF")
    print("O el destino esta mal, o el rotulo nombra la pagina en vez de estar")
    print("impreso en ella. Si es lo segundo, declaralo en ROTULO_NO_IMPRESO.")

raise SystemExit(1)
