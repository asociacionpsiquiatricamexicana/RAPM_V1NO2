#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""armar_numero.py — concatena los artículos ya compilados de un número de la
Revista de la Asociación Psiquiátrica Mexicana, A.C. en un solo PDF: portada +
tabla de contenido + cada artículo camera-ready tal cual salió de
taller/componer.sh, en el orden de su ART#.

No recompone ni re-pagina cada artículo: es una CONCATENACIÓN. El "Página X de
Y" que imprime cada artículo queda relativo a sí mismo (decisión ya tomada,
ver taller/norma/06_gestion_volumenes_numeros.md).

Uso:
    python3 taller/armar_numero.py NUMERO
        [--raiz numeros/]        # por omision "numeros/" desde la raiz del repo
        [--portada RUTA_IMAGEN]  # imagen de portada opcional

Lee <raiz>/<NUMERO>/, busca las subcarpetas <NUMERO>_ART<N>_* (ordenadas por N
ascendente) y dentro de cada una el PDF *_APM_<NUMERO>_*.pdf. Una carpeta de
articulo sin PDF compilado se salta con una advertencia; si NINGUN articulo
tiene PDF, falla con un mensaje claro.

Verificar es medir el PDF construido, nunca estimar (taller/LEEME.md): las
paginas iniciales de cada articulo en la tabla de contenido se miden con
pypdfium2 sobre los PDFs reales, nunca se asumen.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import pypdfium2 as pdfium
except ImportError:
    raise SystemExit(
        "falta pypdfium2 (taller/sondas/requisitos.txt): "
        "python3 -m pip install -r taller/sondas/requisitos.txt"
    )

try:
    import pikepdf
except ImportError:
    raise SystemExit(
        "falta pikepdf (taller/sondas/requisitos.txt): "
        "python3 -m pip install -r taller/sondas/requisitos.txt"
    )

AQUI = os.path.dirname(os.path.abspath(__file__))

# Colores exactos de taller/apm-editorial.cls — no reinventar.
COLOR_BURG = "8B1A2B"
COLOR_BURGDARK = "8B0027"
COLOR_G40 = "2D2D2D"
COLOR_G55 = "666666"
COLOR_RULELT = "E8E8E8"

ART_DIR_RE = re.compile(r"^(?P<numero>.+)_ART(?P<n>\d+)_.+$")
NUMERO_RE = re.compile(r"(?i)^VOL\d+_NO\d+$")


def log(msg):
    print(msg, file=sys.stderr)


# ── Descubrimiento de artículos ─────────────────────────────────────────

def encontrar_carpetas_articulo(dir_numero, numero):
    """Devuelve [(n, ruta_carpeta), ...] ordenado por N ascendente."""
    if not os.path.isdir(dir_numero):
        raise SystemExit(f"no existe el directorio del numero: {dir_numero}")
    candidatas = []
    for nombre in sorted(os.listdir(dir_numero)):
        ruta = os.path.join(dir_numero, nombre)
        if not os.path.isdir(ruta):
            continue
        m = ART_DIR_RE.match(nombre)
        if not m:
            continue
        if m.group("numero") != numero:
            continue
        candidatas.append((int(m.group("n")), nombre, ruta))
    candidatas.sort(key=lambda t: t[0])
    return [(n, ruta) for n, _nombre, ruta in candidatas]


def encontrar_pdf_articulo(carpeta, numero):
    """Busca *_APM_<numero>_*.pdf dentro de la carpeta del articulo."""
    patron = re.compile(r".*_APM_" + re.escape(numero) + r"_.*\.pdf$", re.IGNORECASE)
    encontrados = []
    for nombre in sorted(os.listdir(carpeta)):
        if patron.match(nombre):
            encontrados.append(os.path.join(carpeta, nombre))
    if not encontrados:
        return None
    if len(encontrados) > 1:
        log(f"  aviso: {carpeta} tiene mas de un PDF que coincide, uso el primero: {encontrados[0]}")
    return encontrados[0]


# ── Metadatos y medición de páginas ─────────────────────────────────────

def leer_metadatos_pdf(ruta_pdf):
    doc = pdfium.PdfDocument(ruta_pdf)
    try:
        meta = doc.get_metadata_dict()
        n_paginas = len(doc)
    finally:
        doc.close()
    return meta, n_paginas


def partir_subject(subject):
    """/Subject = '{Tipo} -- Revista APM Vol. X No. X, PERIODO ANO'. El
    separador puede salir como ' -- ' o como en-dash ' – ' segun como
    pdflatex/hyperref lo reescriba (confirmado con pdfinfo real sobre los
    PDFs de ejemplo del taller). Se parte por el ULTIMO separador que
    aparezca; todo lo anterior es el Tipo."""
    if not subject:
        return "", subject or ""
    ultimo_idx = -1
    ultimo_sep_len = 0
    for sep in (" -- ", " – "):
        idx = subject.rfind(sep)
        if idx > ultimo_idx:
            ultimo_idx = idx
            ultimo_sep_len = len(sep)
    if ultimo_idx == -1:
        return "", subject
    tipo = subject[:ultimo_idx].strip()
    resto = subject[ultimo_idx + ultimo_sep_len:].strip()
    return tipo, resto


# ── Escape de LaTeX ──────────────────────────────────────────────────────

_LATEX_ESPECIALES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escapar_latex(texto):
    if texto is None:
        return ""
    out = []
    for ch in texto:
        out.append(_LATEX_ESPECIALES.get(ch, ch))
    return "".join(out)


# ── Generación del .tex de portada+contenido ────────────────────────────

PORTADA_PREAMBULO = r"""\documentclass[10pt,letterpaper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[letterpaper,left=1.8cm,right=1.8cm,top=2.0cm,bottom=1.8cm]{geometry}
\usepackage{mathptmx}
\usepackage{xcolor}
\usepackage{graphicx}
\definecolor{burg}{HTML}{%s}
\definecolor{burgdark}{HTML}{%s}
\definecolor{g40}{HTML}{%s}
\definecolor{g55}{HTML}{%s}
\definecolor{rulelt}{HTML}{%s}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\begin{document}
""" % (COLOR_BURG, COLOR_BURGDARK, COLOR_G40, COLOR_G55, COLOR_RULELT)

PORTADA_CIERRE = r"""
\end{document}
"""


def generar_tex_portada(numero_legible, vol, no, periodo, anio, ruta_imagen_portada,
                          entradas_contenido):
    """entradas_contenido: lista de dicts con tipo, titulo, autor (ya
    escapados), y 'pagina' (str, puede ser placeholder en el primer paso)."""
    partes = [PORTADA_PREAMBULO]

    # ── Página 1: portada ──────────────────────────────────────────
    partes.append(r"\begin{center}")
    partes.append(r"\vspace*{1.2cm}")
    partes.append(
        r"{\Large\bfseries Revista de la Asociaci\'on Psiqui\'atrica Mexicana, A.C.}\par"
    )
    partes.append(r"\vspace{6pt}")
    partes.append(
        r"{\large\color{burg}\bfseries Vol. %s \textperiodcentered\ No. %s \textperiodcentered\ %s %s}\par"
        % (escapar_latex(vol), escapar_latex(no), escapar_latex(periodo), escapar_latex(anio))
    )
    partes.append(r"\vspace{2.2cm}")
    if ruta_imagen_portada:
        ruta_tex = ruta_imagen_portada.replace("\\", "/")
        partes.append(r"\includegraphics[width=\textwidth,keepaspectratio]{%s}" % ruta_tex)
    partes.append(r"\vfill")
    partes.append(
        r"{\small\color{g55} e-ISSN 3061-7979 \textperiodcentered\ CC BY-NC 4.0}\par"
    )
    partes.append(r"\vspace{0.6cm}")
    partes.append(r"\end{center}")
    partes.append(r"\clearpage")

    # ── Página(s): contenido ───────────────────────────────────────
    partes.append(
        r"{\Large\bfseries\color{burg}\MakeUppercase{Contenido}}\par"
    )
    partes.append(r"\vspace{10pt}")
    partes.append(r"\noindent\color{rulelt}\rule{\textwidth}{0.6pt}\color{black}\par")
    partes.append(r"\vspace{8pt}")
    for e in entradas_contenido:
        partes.append(r"\noindent{\small\color{burg}\bfseries %s}\par" % e["tipo"])
        partes.append(
            r"\noindent{\bfseries\color{g40}\large %s} \hfill {\bfseries\color{g40} P\'agina %s}\par"
            % (e["titulo"], e["pagina"])
        )
        partes.append(r"\noindent{\color{g55} %s}\par" % e["autor"])
        partes.append(r"\vspace{10pt}")
        partes.append(r"\noindent\color{rulelt}\rule{\textwidth}{0.4pt}\color{black}\par")
        partes.append(r"\vspace{8pt}")

    partes.append(PORTADA_CIERRE)
    return "\n".join(partes)


def compilar_tex(ruta_tex, timeout=120):
    """Compila con pdflatex (una pasada basta: sin referencias cruzadas ni
    totpages). Exige cero errores. Devuelve la ruta del PDF resultante."""
    dir_tex = os.path.dirname(ruta_tex)
    base = os.path.splitext(os.path.basename(ruta_tex))[0]
    log_path = os.path.join(dir_tex, base + ".log")
    try:
        resultado = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(ruta_tex)],
            cwd=dir_tex,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        raise SystemExit("no se encontro pdflatex en el PATH")
    pdf_path = os.path.join(dir_tex, base + ".pdf")
    if resultado.returncode != 0 or not os.path.exists(pdf_path):
        detalle = ""
        if os.path.exists(log_path):
            with open(log_path, encoding="utf-8", errors="replace") as fh:
                detalle = fh.read()[-3000:]
        raise SystemExit(
            f"COMPILACION DE PORTADA+CONTENIDO FALLIDA (vease {log_path}):\n{detalle}"
        )
    return pdf_path


def contar_paginas_pdf(ruta_pdf):
    doc = pdfium.PdfDocument(ruta_pdf)
    try:
        return len(doc)
    finally:
        doc.close()


# ── Ensamblado final con pikepdf ────────────────────────────────────────

def ensamblar_pdf(ruta_portada_pdf, rutas_articulos, ruta_salida_temporal):
    pdf_final = pikepdf.Pdf.new()
    with pikepdf.Pdf.open(ruta_portada_pdf) as src:
        pdf_final.pages.extend(src.pages)
    for ruta in rutas_articulos:
        with pikepdf.Pdf.open(ruta) as src:
            pdf_final.pages.extend(src.pages)
    pdf_final.save(ruta_salida_temporal)
    pdf_final.close()


def linealizar(ruta_temporal, ruta_destino):
    resultado = subprocess.run(
        ["qpdf", "--linearize", ruta_temporal, ruta_temporal + ".lin"],
        capture_output=True,
        text=True,
    )
    if resultado.returncode != 0:
        raise SystemExit(
            f"qpdf --linearize fallo:\n{resultado.stdout}\n{resultado.stderr}"
        )
    shutil.move(ruta_temporal + ".lin", ruta_destino)


# ── Programa principal ───────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Arma el PDF de un numero completo de la Revista APM "
                     "concatenando portada+contenido con los articulos ya "
                     "compilados (camera-ready) de numeros/<NUMERO>/."
    )
    ap.add_argument("numero", help="Nombre del numero, p. ej. VOL6_NO2")
    ap.add_argument(
        "--raiz",
        default=None,
        help="Directorio raiz de numeros (por omision: numeros/ desde la raiz del repo)",
    )
    ap.add_argument(
        "--portada",
        default=None,
        help="Ruta a una imagen de portada opcional (por omision: taller/logo_hires.png)",
    )
    args = ap.parse_args()

    numero = args.numero
    if not NUMERO_RE.match(numero):
        # numero termina como componente de ruta (dir_numero, REVISTA_<numero>.pdf):
        # se exige la misma forma VOLx_NOy que numeros/LEEME.md documenta, en vez
        # de aceptar cualquier cadena (nunca separadores de ruta ni "..").
        raise SystemExit(f"numero mal formado: {numero!r} (se espera VOLx_NOy)")
    if args.raiz:
        raiz = os.path.abspath(args.raiz)
    else:
        raiz_repo = os.path.abspath(os.path.join(AQUI, os.pardir))
        raiz = os.path.join(raiz_repo, "numeros")

    dir_numero = os.path.join(raiz, numero)
    log(f"numero: {numero}")
    log(f"raiz: {raiz}")
    log(f"directorio del numero: {dir_numero}")

    carpetas = encontrar_carpetas_articulo(dir_numero, numero)
    if not carpetas:
        raise SystemExit(
            f"no se encontraron subcarpetas {numero}_ART<N>_* dentro de {dir_numero}"
        )

    articulos = []  # lista de dicts: n, carpeta, pdf, meta, paginas
    for n, carpeta in carpetas:
        pdf = encontrar_pdf_articulo(carpeta, numero)
        if pdf is None:
            log(f"AVISO: {carpeta} (ART{n}) no tiene PDF *_APM_{numero}_*.pdf compilado aun — se omite")
            continue
        meta, n_paginas = leer_metadatos_pdf(pdf)
        articulos.append({"n": n, "carpeta": carpeta, "pdf": pdf, "meta": meta, "paginas": n_paginas})
        log(f"ART{n}: {os.path.basename(pdf)} — {n_paginas} paginas")

    if not articulos:
        raise SystemExit(
            f"NINGUN articulo de {numero} tiene PDF compilado todavia "
            f"(revisa {dir_numero}); no se genera un PDF vacio."
        )

    # Determinar Vol/No/Periodo/Ano del numero a partir del primer articulo
    # con Subject parseable — nunca inventados.
    vol = no = periodo = anio = None
    for a in articulos:
        subject = a["meta"].get("Subject", "")
        tipo, resto = partir_subject(subject)
        a["tipo"] = tipo
        # resto: "Revista APM Vol. X No. X, PERIODO ANO"
        m = re.search(
            r"Vol\.\s*(?P<vol>\S+)\s*No\.\s*(?P<no>\S+),\s*(?P<periodo>.+?)\s+(?P<anio>\d{4})\s*$",
            resto,
        )
        if m:
            if vol is None:
                vol = m.group("vol")
                no = m.group("no")
                periodo = m.group("periodo")
                anio = m.group("anio")
        else:
            log(f"  aviso: no se pudo interpretar el Subject de ART{a['n']}: {subject!r}")

    if vol is None:
        log("aviso: no se pudo determinar Vol./No./Periodo/Ano de ningun /Subject; "
            "la portada quedara con placeholders")
        vol = no = periodo = anio = "[PENDIENTE]"

    # Ruta de imagen de portada
    ruta_portada_imagen = args.portada
    if ruta_portada_imagen:
        ruta_portada_imagen = os.path.abspath(ruta_portada_imagen)
        if not os.path.exists(ruta_portada_imagen):
            raise SystemExit(f"no existe la imagen de portada: {ruta_portada_imagen}")
    else:
        respaldo = os.path.join(AQUI, "logo_hires.png")
        if os.path.exists(respaldo):
            ruta_portada_imagen = respaldo
        else:
            log("aviso: no se dio --portada y no existe taller/logo_hires.png; portada sin imagen")
            ruta_portada_imagen = None

    with tempfile.TemporaryDirectory(prefix="armar_numero_") as tmpdir:
        # Copiar imagen de portada al directorio temporal para que pdflatex
        # la encuentre por nombre relativo simple.
        nombre_img_local = None
        if ruta_portada_imagen:
            nombre_img_local = "portada" + os.path.splitext(ruta_portada_imagen)[1]
            shutil.copy(ruta_portada_imagen, os.path.join(tmpdir, nombre_img_local))

        # ── Paso 1: compilar portada+contenido con paginas de contenido en
        # PLACEHOLDER para medir cuantas paginas ocupa el propio portada+
        # contenido (nunca se asume). ──────────────────────────────────
        entradas_medicion = []
        for a in articulos:
            meta = a["meta"]
            entradas_medicion.append({
                "tipo": escapar_latex(a.get("tipo") or "[PENDIENTE]"),
                "titulo": escapar_latex(meta.get("Title") or "[PENDIENTE]"),
                "autor": escapar_latex(meta.get("Author") or "[PENDIENTE]"),
                "pagina": "0",
            })

        tex_medicion = generar_tex_portada(
            numero, vol, no, periodo, anio, nombre_img_local, entradas_medicion
        )
        ruta_tex_medicion = os.path.join(tmpdir, "portada.tex")
        with open(ruta_tex_medicion, "w", encoding="utf-8") as fh:
            fh.write(tex_medicion)
        pdf_medicion = compilar_tex(ruta_tex_medicion)
        paginas_portada = contar_paginas_pdf(pdf_medicion)
        log(f"portada+contenido: {paginas_portada} paginas (medido)")

        # ── Calcular pagina inicial real de cada articulo ───────────────
        pagina_actual = paginas_portada + 1
        for a in articulos:
            a["pagina_inicial"] = pagina_actual
            pagina_actual += a["paginas"]

        # ── Paso 2: recompilar portada+contenido con las paginas reales ──
        entradas_finales = []
        for a in articulos:
            meta = a["meta"]
            entradas_finales.append({
                "tipo": escapar_latex(a.get("tipo") or "[PENDIENTE]"),
                "titulo": escapar_latex(meta.get("Title") or "[PENDIENTE]"),
                "autor": escapar_latex(meta.get("Author") or "[PENDIENTE]"),
                "pagina": str(a["pagina_inicial"]),
            })
        tex_final = generar_tex_portada(
            numero, vol, no, periodo, anio, nombre_img_local, entradas_finales
        )
        ruta_tex_final = os.path.join(tmpdir, "portada_final.tex")
        with open(ruta_tex_final, "w", encoding="utf-8") as fh:
            fh.write(tex_final)
        pdf_portada_final = compilar_tex(ruta_tex_final)
        paginas_portada_final = contar_paginas_pdf(pdf_portada_final)
        if paginas_portada_final != paginas_portada:
            log(
                f"aviso: el numero de paginas de portada+contenido cambio entre "
                f"medicion ({paginas_portada}) y version final ({paginas_portada_final}); "
                f"se recalculan las paginas iniciales"
            )
            paginas_portada = paginas_portada_final
            pagina_actual = paginas_portada + 1
            for a in articulos:
                a["pagina_inicial"] = pagina_actual
                pagina_actual += a["paginas"]
            entradas_finales = []
            for a in articulos:
                meta = a["meta"]
                entradas_finales.append({
                    "tipo": escapar_latex(a.get("tipo") or "[PENDIENTE]"),
                    "titulo": escapar_latex(meta.get("Title") or "[PENDIENTE]"),
                    "autor": escapar_latex(meta.get("Author") or "[PENDIENTE]"),
                    "pagina": str(a["pagina_inicial"]),
                })
            tex_final = generar_tex_portada(
                numero, vol, no, periodo, anio, nombre_img_local, entradas_finales
            )
            with open(ruta_tex_final, "w", encoding="utf-8") as fh:
                fh.write(tex_final)
            pdf_portada_final = compilar_tex(ruta_tex_final)
            paginas_portada_final = contar_paginas_pdf(pdf_portada_final)

        # ── Ensamblado final ──────────────────────────────────────────
        ruta_temporal = os.path.join(tmpdir, f"REVISTA_{numero}.pdf.tmp")
        ensamblar_pdf(pdf_portada_final, [a["pdf"] for a in articulos], ruta_temporal)

        ruta_destino = os.path.join(dir_numero, f"REVISTA_{numero}.pdf")
        linealizar(ruta_temporal, ruta_destino)

    total_esperado = paginas_portada_final + sum(a["paginas"] for a in articulos)
    total_real = contar_paginas_pdf(ruta_destino)
    peso = os.path.getsize(ruta_destino)
    log(f"escrito: {ruta_destino} ({peso} bytes, {peso/1024:.0f} KB)")
    log(f"paginas totales: esperadas {total_esperado}, medidas {total_real}")
    if total_real != total_esperado:
        raise SystemExit(
            f"ENSAMBLADO INCONSISTENTE: se esperaban {total_esperado} paginas y "
            f"salieron {total_real}"
        )
    if peso > 600 * 1024:
        log(f"aviso: {peso/1024:.0f} KB supera los 600 KB (el tope es por articulo individual, no aplica al numero completo)")

    print(ruta_destino)


if __name__ == "__main__":
    main()
