"""Estado final del PDF publicado, medido sobre el archivo."""
import collections
import os
import sys
import pikepdf, pypdfium2 as pdfium

R = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir,
                   "APM60_Genealogia__corregido.pdf")
px, pdf = pikepdf.open(R), pdfium.PdfDocument(R)
print(f"paginas: {len(pdf)}")

uso = collections.defaultdict(set)
for i, p in enumerate(px.pages):
    for _, f in ((p.get("/Resources", {}) or {}).get("/Font", {}) or {}).items():
        uso[str(f.get("/BaseFont", "?"))].add(i + 1)
print("tipografias:")
for b, ps in sorted(uso.items(), key=lambda x: -len(x[1])):
    print(f"   {b:<40} {len(ps)} pags")

def renglones(tp):
    """Agrupa los caracteres de una pagina en renglones, con su geometria."""
    ren, cur = [], []
    for k in range(tp.count_chars()):
        c = tp.get_text_range(k, 1)
        if c in ("\r", "\n"):
            if cur:
                ren.append(cur)
                cur = []
            continue
        try:
            cur.append((c, tp.get_charbox(k, loose=False)))
        except Exception:
            cur.append((c, None))
    if cur:
        ren.append(cur)
    return ren


# Un espacio sobra cuando el hueco que salva no es mayor que el que hay entre
# dos letras contiguas de una palabra del mismo renglon. Medirlo asi, y no por
# el reparto de letras sueltas, es lo que distingue «Congre so» —dos trozos de
# una palabra, que la cuenta de sueltas no ve— de la separacion legitima entre
# palabras, que en texto justificado varia de renglon en renglon.
rotas, medidos = [], 0
for i in range(len(pdf)):
    for ln in renglones(pdf[i].get_textpage()):
        espacios, letras = [], []
        for k in range(1, len(ln) - 1):
            c, caja = ln[k]
            ant, sig = ln[k - 1][1], ln[k + 1][1]
            if ant is None or sig is None:
                continue
            if c == " ":
                espacios.append(sig[0] - ant[2])
            elif ln[k - 1][0] != " " and caja is not None:
                letras.append(caja[0] - ant[2])
        if not espacios or not letras:
            continue
        medidos += 1
        letras.sort()
        entre_letras = letras[len(letras) // 2]
        sobran = sum(1 for h in espacios if h <= entre_letras * 1.6)
        if sobran:
            rotas.append((i + 1, "".join(c for c, _ in ln).strip()[:60], sobran))

if not medidos:
    print("\nNINGUN RENGLON PUDO MEDIRSE: el PDF no trae geometria de glifos,")
    print("o la capa de texto esta vacia. Sin eso esta comprobacion no dice nada.")
    raise SystemExit(1)
print(f"renglones que se parten al copiar: {len(rotas)} de {medidos} medidos")
for pag, texto, n in rotas:
    print(f"   pag {pag}: «{texto}» ({n} espacio(s) de mas)")

pruebas = ["Primera parte", "Segunda parte", "Tercera parte", "Sexagésimo Aniversario",
           "de la Asociación Psiquiátrica", "Historiador Compilador", "Síntesis",
           "Mesas Directivas", "XXX Congreso Nacional", "DOI 10.5281/zenodo.22035217", "ἱστορία"]
todo = " ".join(" ".join(pdf[i].get_textpage().get_text_bounded().split()) for i in range(len(pdf)))
print("busqueda dentro del PDF:")
for q in pruebas:
    print(f"   «{q}»: {'la encuentra' if q.lower() in todo.lower() else 'NO LA ENCUENTRA'}")

raise SystemExit(1 if rotas else 0)
