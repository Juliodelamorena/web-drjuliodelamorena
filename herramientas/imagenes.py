"""Optimiza las fotos de img/ y envuelve las etiquetas <img> en <picture> con versión WebP.

Uso (después de generar las páginas):  python3 herramientas/imagenes.py

1. Cada img/**/*.jpg se recomprime (progresivo, calidad 80, sin metadatos) con un lado mayor de
   1200 px como máximo, manteniendo la proporción exacta para que los width/height del HTML sigan
   valiendo. Se guarda además una copia .webp. Los originales grandes quedan en herramientas/img_originales/
   la primera vez, por si hacen falta.
2. En todos los .html del sitio, <img src="/img/x.jpg" ...> pasa a
   <picture><source srcset="/img/x.webp" type="image/webp"><img ...></picture>. Es idempotente.
"""
import io, os, re, sys, pathlib
from PIL import Image, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parent.parent
IMG = RAIZ / "img"
ORIG = RAIZ / "herramientas" / "img_originales"
MAX_LADO = 1200
EXCLUIR = {"compartir.jpg"}      # imagen para compartir en redes: se deja tal cual (1200 px exactos)

def optimizar():
    ORIG.mkdir(exist_ok=True)
    total_antes = total_despues = 0
    for f in sorted(IMG.rglob("*.jpg")):
        rel = f.relative_to(IMG)
        copia = ORIG / rel
        if not copia.exists():
            copia.parent.mkdir(parents=True, exist_ok=True)
            copia.write_bytes(f.read_bytes())
        im = ImageOps.exif_transpose(Image.open(copia)).convert("RGB")
        antes = f.stat().st_size
        if f.name not in EXCLUIR and max(im.size) > MAX_LADO:
            im.thumbnail((MAX_LADO, MAX_LADO), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        if buf.tell() < antes or im.size != Image.open(f).size:
            f.write_bytes(buf.getvalue())
        im.save(f.with_suffix(".webp"), "WEBP", quality=78, method=6)
        total_antes += antes; total_despues += f.stat().st_size
        print(f"  {rel}: {antes//1024} KB -> {f.stat().st_size//1024} KB jpg + {f.with_suffix('.webp').stat().st_size//1024} KB webp {im.size}")
    print(f"jpg: {total_antes//1024} KB -> {total_despues//1024} KB")

PATRON = re.compile(r'(?<!type="image/webp">)(<img\b(?=[^>]*\bsrc="/img/([^"]+)\.jpg")[^>]*>)')

def envolver():
    n = 0
    for h in RAIZ.rglob("*.html"):
        if "herramientas" in h.parts or "ig" in h.parts:
            continue
        s = h.read_text()
        def rep(m):
            ruta = m.group(2)
            if not (IMG / f"{ruta}.webp").exists():
                return m.group(0)
            return f'<picture><source srcset="/img/{ruta}.webp" type="image/webp">{m.group(1)}</picture>'
        s2 = PATRON.sub(rep, s)
        if s2 != s:
            h.write_text(s2); n += 1
    print(f"picture: {n} páginas actualizadas")

if __name__ == "__main__":
    optimizar()
    envolver()
