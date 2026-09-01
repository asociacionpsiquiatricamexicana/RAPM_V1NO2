#!/usr/bin/env python3
"""
Diagnóstico PARCIAL para PDFs de la Revista APM (RAPM).

ALCANCE REAL: automatiza 4 de las 14 capas (A, B parcial, M, N).
Las capas C-L (logo/DOI, reglas decorativas, header P1, caja de resumen,
columnas, headings, footer, running heads, referencias, colofón) NO están
implementadas y requieren medición dirigida sobre coordenadas del layout.

Un "OK" de este script NO equivale a un diagnóstico completo aprobado.
No emitas veredicto "APTO PARA PRODUCCIÓN" basándote solo en esta salida.

Implementa las mediciones descritas en
norma/05_workflow_produccion_y_diagnostico.md contra un PDF ya
compilado con apm-editorial.cls.

Requiere: pdfplumber, PyMuPDF (fitz), pikepdf
    pip install pdfplumber pymupdf pikepdf

Uso:
    python diagnostico_rapm.py archivo.pdf
    python diagnostico_rapm.py archivo.pdf --json reporte.json

Este script es un punto de partida, no un validador infalible. Varias
capas (F: curvas de mdframed, G: alineación fina de columnas) requieren
juicio humano además de la medición automática — repórtalas, no las
"apruebes" solo porque el script no lanzó una excepción. Ver notas
operativas en 05_workflow_produccion_y_diagnostico.md.
"""

import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    # El nombre vigente es `pymupdf`; `fitz` es el alias viejo y desde la
    # version 1.26 escupe un aviso de obsolescencia POR STDOUT, que se cuela
    # dentro del JSON y lo vuelve ilegible para `--json`. Se importa primero
    # el nombre nuevo y se deja el viejo como respaldo.
    import pymupdf as fitz
except ImportError:
    try:
        import fitz  # PyMuPDF < 1.26
    except ImportError:
        fitz = None

try:
    import pikepdf
except ImportError:
    pikepdf = None


# ─────────────────────────────────────────────────────────────────
# SPEC — valores canónicos, verificados contra apm-editorial.cls
# ─────────────────────────────────────────────────────────────────

SPEC = {
    "paper_pt": (612.0, 792.0),  # letterpaper
    "margin_left_pt": 51.0,
    "margin_right_pt": 51.0,
    "margin_top_pt": 56.7,
    "margin_bottom_pt": 51.0,
    "gutter_pt": 14.2,
    "colors": {
        "burg": (0x8B, 0x1A, 0x2B),
        "burgdark": (0x8B, 0x00, 0x27),
        "g40": (0x2D, 0x2D, 0x2D),
        "g55": (0x66, 0x66, 0x66),
        "rulelt": (0xE8, 0xE8, 0xE8),
        "cream": (0xFE, 0xF8, 0xF8),
        "creamborder": (0xD9, 0xB5, 0xB9),
        "linkblue": (0x1A, 0x52, 0x76),  # reservado, no en uso actual
    },
    "issn": "3061-7979",
    "license": "CC BY-NC 4.0",
    "max_size_kb": 600,
}

TOLERANCE = {
    "margin_left_pt": 3.0,
    "margin_right_pt": 5.0,   # microtype protrusion
    "margin_top_pt": 5.0,
    "margin_bottom_pt": 10.0,  # enlargethispage variable
    "gutter_pt": 4.0,          # microtype
    "logo_doi_delta_pt": 1.0,
    "column_width_delta_pt": 2.0,
}

# La misma lista que vigila geometria.py (FM06): las dos sondas deben decir
# lo mismo sobre que es Computer Modern. Faltaban CMEX, CMTI y CMTT.
FORBIDDEN_FONT_PREFIXES = ("CMR", "CMBX", "CMMI", "CMSY", "CMEX", "CMTI", "CMTT", "SFRM", "SFRB")


# ─────────────────────────────────────────────────────────────────
# WCAG AA
# ─────────────────────────────────────────────────────────────────

def luminancia(r, g, b):
    rs, gs, bs = [x / 255 for x in (r, g, b)]
    rs = rs / 12.92 if rs <= 0.03928 else ((rs + 0.055) / 1.055) ** 2.4
    gs = gs / 12.92 if gs <= 0.03928 else ((gs + 0.055) / 1.055) ** 2.4
    bs = bs / 12.92 if bs <= 0.03928 else ((bs + 0.055) / 1.055) ** 2.4
    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs


def contraste(c1, c2=(255, 255, 255)):
    l1, l2 = luminancia(*c1), luminancia(*c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


# ─────────────────────────────────────────────────────────────────
# Capas de diagnóstico
# ─────────────────────────────────────────────────────────────────

def layer_a_ficha(path, doc_info):
    size_kb = path.stat().st_size / 1024
    return {
        "capa": "A. Ficha del artículo",
        "archivo": path.name,
        "tamano_kb": round(size_kb, 1),
        "paginas": doc_info.get("paginas"),
        "titulo_pdfinfo": doc_info.get("title"),
        "autor_pdfinfo": doc_info.get("author"),
        **({"error": doc_info["error"]} if "error" in doc_info else {}),
    }


def layer_b_geometria(page0):
    w, h = page0.width, page0.height
    spec_w, spec_h = SPEC["paper_pt"]
    ok_paper = abs(w - spec_w) <= 2 and abs(h - spec_h) <= 2
    return {
        "capa": "B. Página y geometría",
        "papel_medido_pt": (round(w, 1), round(h, 1)),
        "papel_spec_pt": (spec_w, spec_h),
        "papel_ok": ok_paper,
        "nota": "Márgenes reales requieren medir bbox del contenido vs bordes de página; "
                "usar pdfplumber page.chars/rects con filtrado por posición.",
    }


def layer_m_fonts_metadata(pdf_path):
    result = {"capa": "M. Fonts y metadata"}
    if pikepdf is None:
        result["error"] = "pikepdf no instalado"
        return result
    with pikepdf.open(str(pdf_path)) as pdf:
        meta = pdf.docinfo
        result["metadata"] = {
            "/Title": str(meta.get("/Title", "")),
            "/Author": str(meta.get("/Author", "")),
            "/Subject": str(meta.get("/Subject", "")),
            "/Keywords": str(meta.get("/Keywords", "")),
            "/Creator": str(meta.get("/Creator", "")),
        }
        result["campos_presentes"] = sum(1 for v in result["metadata"].values() if v)
        result["campos_totales"] = 5
    return result


def layer_n_wcag(colors=None):
    colors = colors or SPEC["colors"]
    rows = []
    for name, rgb in colors.items():
        c = contraste(rgb)
        rows.append({
            "color": name,
            "hex": "#%02X%02X%02X" % rgb,
            "contraste_vs_blanco": round(c, 2),
            "cumple_AA_normal": c >= 4.5,
            "cumple_AA_grande": c >= 3.0,
        })
    return {"capa": "N. WCAG AA", "colores": rows}


def layer_m_fonts_embebidas(pdf_path):
    """Mide con pdffonts lo que antes solo se pedia correr a mano: que toda
    tipografia este incrustada y que ninguna sea Computer Modern (FM06).
    Mismo criterio y mismo parseo que geometria.py."""
    result = {"capa": "M (complemento). Fonts embebidas"}
    if shutil.which("pdffonts") is None:
        result["error"] = "pdffonts no instalado: apt install poppler-utils"
        return result
    salida = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True).stdout
    fuentes, sin_incrustar, computer_modern = [], [], []
    for linea in salida.splitlines()[2:]:
        c = linea.split()
        if len(c) < 5:
            continue
        fuentes.append(c[0])
        # columnas desde el final: emb sub uni objeto generacion
        if c[-5] == "no":
            sin_incrustar.append(c[0])
        # los nombres llegan como ABCDEF+CMSY10; el prefijo de subconjunto sobra
        if c[0].split("+", 1)[-1].upper().startswith(FORBIDDEN_FONT_PREFIXES):
            computer_modern.append(c[0])
    result.update({
        "fuentes": fuentes,
        "sin_incrustar": sin_incrustar,
        "computer_modern_FM06": computer_modern,
        "ok": not sin_incrustar and not computer_modern,
    })
    return result


def run_diagnostico(pdf_path: Path):
    report = {"archivo": str(pdf_path), "capas": []}

    doc_info = {}
    if fitz is not None:
        doc = fitz.open(str(pdf_path))
        doc_info["paginas"] = doc.page_count
        doc_info["title"] = doc.metadata.get("title")
        doc_info["author"] = doc.metadata.get("author")
        doc.close()
    else:
        # Sin PyMuPDF la capa A imprimia null en paginas y titulo: parecia una
        # medicion y era una ausencia. Se declara la falta, como ya hace la
        # capa B con pdfplumber; un hueco dicho no engana, un null si.
        doc_info["error"] = "PyMuPDF no instalado: pip install pymupdf"

    report["capas"].append(layer_a_ficha(pdf_path, doc_info))

    if pdfplumber is not None:
        with pdfplumber.open(str(pdf_path)) as pdf:
            if pdf.pages:
                report["capas"].append(layer_b_geometria(pdf.pages[0]))
    else:
        report["capas"].append({"capa": "B. Página y geometría", "error": "pdfplumber no instalado"})

    report["capas"].append(layer_m_fonts_metadata(pdf_path))
    report["capas"].append(layer_m_fonts_embebidas(pdf_path))
    report["capas"].append(layer_n_wcag())

    report["nota_general"] = (
        "Este script cubre A, B (parcial), M y N de forma automática. "
        "Las capas C-L (logo/DOI, reglas decorativas, header, caja de resumen, "
        "columnas, headings, footer, running heads, referencias, colofón) requieren "
        "medición dirigida con pdfplumber.chars/rects/lines sobre coordenadas "
        "específicas del layout — implementar por artículo o extender este script "
        "según norma/05_workflow_produccion_y_diagnostico.md."
    )
    return report


def main():
    parser = argparse.ArgumentParser(description="Diagnóstico RAPM de 14 capas (parcial-automático)")
    parser.add_argument("pdf", type=Path, help="Ruta al PDF a diagnosticar")
    parser.add_argument("--json", type=Path, default=None, help="Ruta de salida JSON")
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"No existe: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    report = run_diagnostico(args.pdf)

    if args.json:
        args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Reporte JSON escrito en {args.json}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
