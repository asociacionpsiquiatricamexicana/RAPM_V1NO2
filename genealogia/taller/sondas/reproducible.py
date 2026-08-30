"""Comprueba que el libro se vuelve a componer igual desde lo versionado.

Esto se demostro a mano dos veces —copia limpia del taller, recomposicion, y
el mismo hash del texto extraido—, pero una demostracion manual caduca la
primera vez que alguien toca libro.py sin repetirla. Aqui queda hecha sonda.

Que hace: copia a un directorio temporal SOLO los archivos que git sigue,
recompone el libro ahi, extrae su texto y compara el hash contra el anclado.
No mide el PDF byte a byte —dos compilaciones difieren en marcas de tiempo
internas— sino el texto, que es lo que el lector recibe.

Tarda alrededor de un minuto: recompone el volumen entero.

    python3 sondas/reproducible.py            # comprueba contra lo anclado
    python3 sondas/reproducible.py --anclar   # fija el estado actual

Si falla, sospecha primero del entorno: otra version de Chromium puede
componer distinto sin que el codigo haya cambiado. La sonda lo dice.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
TALLER = os.path.dirname(AQUI)
REF = os.path.join(AQUI, "reproducible_referencia.txt")
ANCLAR = "--anclar" in sys.argv


def corre(orden, cwd):
    r = subprocess.run(orden, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print("\n".join(orden) + " fallo:\n" + (r.stderr or r.stdout)[-1500:])
        raise SystemExit(1)
    return r.stdout


seguidos = subprocess.run(["git", "-C", TALLER, "ls-files"],
                          capture_output=True, text=True)
if seguidos.returncode != 0:
    raise SystemExit("no hay repositorio git: esta sonda mide lo versionado.")
archivos = [f for f in seguidos.stdout.split("\n") if f.strip()]
print(f"taller versionado: {len(archivos)} archivos")

tmp = tempfile.mkdtemp(prefix="reproducible-")
try:
    for rel in archivos:
        src, dst = os.path.join(TALLER, rel), os.path.join(tmp, rel)
        if not os.path.exists(src):
            print(f"  falta en disco pero git lo sigue: {rel}")
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    print("recomponiendo desde la copia limpia (un minuto aprox.)…")
    salida = corre([sys.executable, "libro.py"], tmp)
    paginas = 0
    for linea in salida.splitlines():
        if "páginas totales:" in linea:
            paginas = int(linea.split(":")[1].strip())
        if "desborda" in linea:
            print("  " + linea.strip())

    corre([sys.executable, "extraer_texto_pdf.py", "pdfs/libro.pdf"], tmp)
    with open(os.path.join(tmp, "mypages.json"), "rb") as fh:
        hash_texto = hashlib.sha256(fh.read()).hexdigest()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"paginas: {paginas}")
print(f"hash del texto: {hash_texto}")

if ANCLAR:
    with open(REF, "w", encoding="utf-8") as fh:
        fh.write(f"{hash_texto}\n{paginas}\n")
    print(f"anclado en {os.path.basename(REF)}")
    raise SystemExit(0)

if not os.path.exists(REF):
    raise SystemExit("sin estado anclado: corre la sonda con --anclar para fijarlo.")

with open(REF, encoding="utf-8") as fh:
    lineas = [x.strip() for x in fh if x.strip() and not x.startswith("#")]
esp_hash, esp_pag = lineas[0], int(lineas[1])

if hash_texto == esp_hash and paginas == esp_pag:
    print(f"\nSE RECOMPONE IGUAL: {esp_pag} paginas, mismo texto.")
    raise SystemExit(0)

print("\nNO SE RECOMPONE IGUAL:")
if paginas != esp_pag:
    print(f"  paginas: se esperaban {esp_pag}, salieron {paginas}")
if hash_texto != esp_hash:
    print(f"  texto:   se esperaba {esp_hash[:16]}…, salio {hash_texto[:16]}…")
print("  Si no tocaste el contenido ni la composicion, sospecha del entorno:")
print("  otra version de Chromium compone distinto sin que el codigo cambie.")
print("  Si el cambio era buscado, vuelve a anclar con --anclar y dilo en el registro.")
raise SystemExit(1)
