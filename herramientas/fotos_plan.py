"""Prepara las fotos de un plan de ejercicio para la web.

Uso:  python3 herramientas/fotos_plan.py <slug> <n>=<archivo> [<n>=<archivo> ...]
Deja img/planes/<slug>/<n>.jpg a 760 x 506 (3:2), con «drjuliodelamorena.com» estampado dentro
de la imagen (se ve aunque alguien la guarde o la comparta). Las fotos verticales se colocan
centradas sobre su propio fondo desenfocado. Después hay que pasar imagenes.py (WebP).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 760, 506
TEXTO = "drjuliodelamorena.com"
FUENTES = ["/usr/share/fonts/opentype/inter/Inter-Bold.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def fuente(px):
    for f in FUENTES:
        if os.path.isfile(f):
            return ImageFont.truetype(f, px)
    return ImageFont.load_default()


def preparar(src):
    im = Image.open(src).convert("RGB")
    if abs(im.width / im.height - W / H) < 0.02:
        return im.resize((W, H), Image.LANCZOS)
    fondo = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22))
    k = H / im.height
    fg = im.resize((max(1, round(im.width * k)), H), Image.LANCZOS)
    fondo.paste(fg, ((W - fg.width) // 2, 0))
    return fondo


def estampar(im):
    f = fuente(21)
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    x0, y0, x1, y1 = d.textbbox((0, 0), TEXTO, font=f)
    tw, th = x1 - x0, y1 - y0
    px, py, m = 14, 8, 12
    caja = (W - m - tw - 2 * px, H - m - th - 2 * py, W - m, H - m)
    d.rounded_rectangle(caja, radius=8, fill=(19, 36, 64, 178))
    d.text((caja[0] + px - x0, caja[1] + py - y0), TEXTO, font=f, fill=(255, 255, 255, 255))
    return Image.alpha_composite(im.convert("RGBA"), capa).convert("RGB")


def main(slug, pares):
    d = os.path.join(ROOT, "img", "planes", slug)
    os.makedirs(d, exist_ok=True)
    for p in pares:
        n, src = p.split("=", 1)
        estampar(preparar(src)).save(os.path.join(d, f"{int(n)}.jpg"), quality=82, optimize=True, progressive=True)
    print(len(pares), "fotos en", d)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
