"""Cierre común (4,6 s) de todos los vídeos. Uso: python3 cierre.py [dia] [t...]
dia: lunes|martes|miercoles|jueves|viernes|sabado (cambia solo la última frase)."""
import math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
W, H, FPS = 1080, 1920, 30
NAVY, NAVY2, GOLD, WHITE, SOFT = (12, 27, 51), (20, 40, 72), (196, 163, 103), (255, 255, 255), (200, 210, 225)
from PIL import ImageFont
def cor(size, wght=700):
    f = ImageFont.truetype(os.path.join(D, "fonts", "Cor.ttf"), size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
def inter(size, w="Bold"): return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", size)
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0], b[3] - b[1]

T = 4.6
FRASE = {"lunes": "Nos vemos el próximo lunes", "martes": "Nos vemos el próximo martes", "miercoles": "Nos vemos el próximo miércoles",
         "jueves": "Nos vemos el próximo jueves", "viernes": "Nos vemos el próximo viernes", "sabado": "Nos vemos el próximo sábado"}

def fondo():
    im = Image.new("RGB", (W, H), NAVY); g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse((-300, 100, W + 300, 1300), fill=90); g = g.filter(ImageFilter.GaussianBlur(170))
    im.paste(Image.new("RGB", (W, H), NAVY2), (0, 0), g); return im
BG = fondo()

FOTO = os.path.join(D, "..", "..", "img", "hero.jpg")
src = Image.open(FOTO).convert("RGB")
cx0, cy0, half = int(src.width * 0.62), int(src.height * 0.27), int(src.width * 0.30)
cara = src.crop((cx0 - half, cy0 - half, cx0 + half, cy0 + half)).resize((400, 400), Image.LANCZOS)
mask = Image.new("L", (400, 400), 0); ImageDraw.Draw(mask).ellipse((0, 0, 399, 399), fill=255)

random.seed(7)
PART = [(random.uniform(0, 2 * math.pi), random.uniform(250, 900), random.uniform(3, 9)) for _ in range(110)]
CX, CY, R = W // 2, 560, 200

def globo(d, x, y, col):
    d.ellipse((x - 22, y - 22, x + 22, y + 22), outline=col, width=4)
    d.ellipse((x - 10, y - 22, x + 10, y + 22), outline=col, width=3)
    d.line((x - 22, y, x + 22, y), fill=col, width=3)
def camara(d, x, y, col):
    d.rounded_rectangle((x - 22, y - 22, x + 22, y + 22), 12, outline=col, width=4)
    d.ellipse((x - 10, y - 10, x + 10, y + 10), outline=col, width=4)
    d.ellipse((x + 10, y - 16, x + 15, y - 11), fill=col)

def pastilla(lay, texto, icono, y, x_off, alpha, col_txt, col_borde):
    f = inter(46, "Bold"); tmp = Image.new("RGBA", (W, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    w_, _ = tw(d, texto, f); bw = w_ + 140; x0 = (W - bw) // 2
    d.rounded_rectangle((x0, 5, x0 + bw, 105), 50, fill=(255, 255, 255, 18), outline=col_borde + (255,), width=3)
    icono(d, x0 + 60, 55, col_borde + (255,)); d.text((x0 + 105, 26), texto, font=f, fill=col_txt + (255,))
    tmp.putalpha(tmp.getchannel("A").point(lambda v: int(v * alpha)))
    lay.alpha_composite(tmp, (x_off, y))

def frame(t, dia="lunes"):
    fr = BG.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # anillo dorado que se dibuja
    p = ease(t / 0.7)
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
    gd.arc((CX - R - 14, CY - R - 14, CX + R + 14, CY + R + 14), -90, -90 + 360 * p, fill=GOLD + (220,), width=22)
    lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16)))
    d.arc((CX - R - 14, CY - R - 14, CX + R + 14, CY + R + 14), -90, -90 + 360 * p, fill=GOLD + (255,), width=8)
    # foto dentro del anillo
    k = ease((t - 0.35) / 0.6)
    if k > 0:
        s = 1.15 - 0.15 * k; c = cara.resize((int(400 * s), int(400 * s)), Image.LANCZOS)
        c = ImageOps.fit(c, (400, 400)); c.putalpha(mask.point(lambda v: int(v * k)))
        lay.alpha_composite(c, (CX - 200, CY - 200))
    # partículas doradas al final
    if t > 2.6:
        dt = t - 2.6
        for ang, vel, sz in PART:
            dist = R + vel * ease(dt / 1.2); x = CX + dist * math.cos(ang); y = CY + dist * math.sin(ang)
            al = int(230 * max(0, 1 - dt / 1.6))
            if al > 0: d.ellipse((x - sz, y - sz, x + sz, y + sz), fill=GOLD + (al,))
    # nombre con golpe
    if t > 1.0:
        kk = ease((t - 1.0) / 0.28); sc = 2.0 - kk
        tmp = Image.new("RGBA", (W, 160), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp); f = cor(104)
        s_ = "Dr. Julio De la Morena"; w_, _ = tw(td, s_, f); td.text(((W - w_) // 2, 10), s_, font=f, fill=WHITE + (255,))
        im = tmp.resize((int(W * sc), int(160 * sc)), Image.LANCZOS)
        if kk < 1: im = im.filter(ImageFilter.GaussianBlur(int(8 * (1 - kk))))
        im.putalpha(im.getchannel("A").point(lambda v: int(v * min(1, kk * 1.4))))
        lay.alpha_composite(im, ((W - im.width) // 2, 830 - (im.height - 160) // 2))
    a = ease((t - 1.45) / 0.45); f = inter(38, "Medium"); s_ = "Medicina Deportiva y Terapias Regenerativas"
    w_, _ = tw(d, s_, f); d.text(((W - w_) // 2, 990), s_, font=f, fill=SOFT + (int(255 * a),))
    lw = int(300 * ease((t - 1.7) / 0.4)); d.rectangle(((W - lw) // 2, 1070, (W + lw) // 2, 1075), fill=GOLD + (255,))
    # web e Instagram entran deslizando desde los lados
    k1 = back((t - 2.0) / 0.45); k2 = back((t - 2.3) / 0.45)
    if t > 2.0: pastilla(lay, "drjuliodelamorena.com", globo, 1120, int(-W * (1 - k1)), min(1, (t - 2.0) / 0.2), WHITE, GOLD)
    if t > 2.3: pastilla(lay, "@drjuliodelamorena", camara, 1260, int(W * (1 - k2)), min(1, (t - 2.3) / 0.2), GOLD, GOLD)
    # frase final letra a letra
    s_ = FRASE.get(dia, FRASE["lunes"]); n = int(len(s_) * max(0, min(1, (t - 3.0) / 0.7)))
    f = cor(64, 600); w_, _ = tw(d, s_, f); d.text(((W - w_) // 2, 1470), s_[:n], font=f, fill=SOFT + (255,))
    # destello que barre todo
    if 2.55 < t < 3.35:
        q = (t - 2.55) / 0.8; x = int(-400 + (W + 800) * q)
        sw = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sw).polygon([(x, 300), (x + 180, 300), (x + 20, 1400), (x - 160, 1400)], fill=(255, 240, 210, 60))
        lay.alpha_composite(sw.filter(ImageFilter.GaussianBlur(45)))
    if t < 0.25: d.rectangle((0, 0, W, H), fill=NAVY + (int(255 * (1 - t / 0.25)),))
    if t > T - 0.4: d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * ease((t - (T - 0.4)) / 0.4))))
    fr.alpha_composite(lay); out = fr.convert("RGB")
    for t0, fz in ((1.28, 0.2), (2.6, 0.15)):
        dt = t - t0
        if 0 <= dt < 0.12: out = Image.blend(out, Image.new("RGB", (W, H), (255, 245, 225)), fz * (1 - dt / 0.12))
    return out

SON = [("whoosh.wav", 0.0, 0.7), ("kick.wav", 1.28, 1.0), ("whoosh.wav", 2.0, 0.8), ("whoosh.wav", 2.3, 0.8), ("boom.wav", 2.6, 0.6), ("ding.wav", 2.62, 0.7)]

def render(dia, out=None):
    out = out or os.path.join(D, "cierres", f"cierre-{dia}.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    v = out + ".v.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", v], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(frame(n / FPS, dia).tobytes())
    p.stdin.close(); p.wait()
    so = os.path.join(D, "sonidos")
    args = ["ffmpeg", "-v", "error", "-y", "-i", v, "-i", os.path.join(so, "musica_larga.wav")]
    for f_, _, _ in SON: args += ["-i", os.path.join(so, f_)]
    fc = f"[1]atrim=20:{20 + T},asetpts=PTS-STARTPTS,volume=0.2,afade=t=out:st={T - 0.8}:d=0.8[m];"; labs = ["[m]"]
    for i, (_, t0, vol) in enumerate(SON):
        fc += f"[{i + 2}]adelay={int(t0 * 1000)}:all=1,volume={vol}[s{i}];"; labs.append(f"[s{i}]")
    fc += "".join(labs) + f"amix=inputs={len(labs)}:normalize=0,apad,atrim=0:{T},alimiter=limit=0.9[a]"
    subprocess.run(args + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(v); return out

if __name__ == "__main__":
    dia = sys.argv[1] if len(sys.argv) > 1 else "lunes"
    if len(sys.argv) > 2:
        for x in sys.argv[2:]: frame(float(x), dia).resize((360, 640)).save(os.path.join(D, f"pv_cierre_{x}.jpg"))
    else:
        print(render(dia))
