"""Comprueba que se puede recuperar del repositorio lo que hace falta para
volver a componer el libro, y dice que falta."""
import re, json, gzip, base64, hashlib, os
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir)
if not os.path.isdir(REPO):
    raise SystemExit(f"{REPO} no es un directorio: esta sonda recibe la carpeta de "
                     "publicacion (genealogia/), donde estan el PDF y los flipbooks.")
s = open(f"{REPO}/Genealogia_APM_Flipbook__Standalone__corregido.html", encoding="utf-8").read()
man = json.loads(re.search(r'<script type="__bundler/manifest">\n(.*?)\n  </script>', s, re.S).group(1))

libro = gzip.decompress(base64.b64decode(man["08fffc00-d395-438c-88b0-a0545e4c4793"]["data"]))
estilo = gzip.decompress(base64.b64decode(man["a4d0e564-9e95-4331-9b24-990858d9e4e7"]["data"]))

vivo_libro = open("assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin", "rb").read()
vivo_estilo = open("assets/a4d0e564-9e95-4331-9b24-990858d9e4e7.js", "rb").read()

print("recuperable del repositorio:")
print(f"   contenido del libro: {json.loads(libro) == json.loads(vivo_libro)}  "
      f"({len(json.loads(libro)['blocks'])} bloques)")
print(f"   modulo de estilo:    {estilo == vivo_estilo}  ({len(estilo)} bytes)")

print("\nNO esta en el repositorio (solo en el taller efimero):")
faltan = ["libro.py", "componer.py", "build.py", "cmp.py", "extraer_texto_pdf.py",
          "sellar_pdf.py", "sync_flipbooks.py", "flatten.py", "fetch_fonts.py",
          "fuentes_griego.py", "fuentes/fuentes.css"]
for f in faltan:
    if os.path.exists(f):
        print(f"   {f:<26} {os.path.getsize(f)/1024:>8.0f} KB")
