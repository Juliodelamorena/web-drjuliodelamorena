import json, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(D, "..", "prp", "fonts")
W, H, FPS = 1080, 1920, 30
NAVY, NAVY2, GOLD, WHITE, SOFT, RED = (12, 27, 51), (20, 40, 72), (196, 163, 103), (255, 255, 255), (200, 210, 225), (214, 92, 80)

def cor(size, wght=600):
    f = ImageFont.truetype(os.path.join(FD, "Cor.ttf"), size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
def inter(size, w="Bold"):
    return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", size)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def tw(d, s, f): b = d.textbbox((0, 0), s, font=f); return b[2] - b[0], b[3] - b[1]

def wrap(d, s, f, maxw):
    out, line = [], ""
    for w_ in s.split(" "):
        t = (line + " " + w_).strip()
        if tw(d, t, f)[0] <= maxw: line = t
        else:
            if line: out.append(line)
            line = w_
    out.append(line); return out

def ctext(d, y, s, f, fill, maxw=940, lh=1.18, spacing=0):
    for ln in wrap(d, s, f, maxw):
        w_, h_ = tw(d, ln, f)
        d.text(((W - w_) // 2, y), ln, font=f, fill=fill)
        y += int(f.size * lh)
    return y

marks = json.load(open(os.path.join(D, "marks.json")))
T_IN, T_OUT = 4.2, 3.6
VOZ = marks[-1][1] + 0.6
TOTAL = T_IN + VOZ + T_OUT

foto = Image.open("/home/claude/web-drjuliodelamorena/img/consulta.jpg").convert("RGB")
sc = 1240 / foto.width
foto = foto.resize((1240, int(foto.height * sc)), Image.LANCZOS)

F_SERIE = inter(40, "Bold"); F_BIG = cor(132, 700); F_NAME = inter(38, "Medium")
F_K = cor(118, 700); F_K2 = cor(92, 700); F_S = inter(44, "Medium"); F_SUB = inter(50, "Bold"); F_TAG = inter(30, "Bold")

def fondo():
    im = Image.new("RGB", (W, H), NAVY)
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse((-300, -200, W + 300, 1100), fill=70); g = g.filter(ImageFilter.GaussianBlur(160))
    im.paste(Image.new("RGB", (W, H), NAVY2), (0, 0), g); return im
BG = fondo()

def intro(t):
    fr = BG.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # 1) línea dorada que nace del centro
    k0 = ease(t / 0.6); lw = int(760 * k0)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.rectangle(((W - lw) // 2, 600, (W + lw) // 2, 612), fill=GOLD + (200,))
    lay.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
    d.rectangle(((W - lw) // 2, 604, (W + lw) // 2, 608), fill=GOLD + (255,))
    # 2) "LOS LUNES DE…" letra a letra
    s = "L O S   L U N E S   D E …"; n = int(len(s) * max(0, min(1, (t - 0.35) / 0.8)))
    w_, _ = tw(d, s, F_SERIE); d.text(((W - w_) // 2, 650), s[:n], font=F_SERIE, fill=GOLD + (255,))
    # 3) tres golpes: cada línea cae con fuerza
    shake = 0
    for j, (ln, t0) in enumerate([("LO QUE", 1.35), ("CASI NADIE", 1.75), ("TE CUENTA", 2.15)]):
        k = ease((t - t0) / 0.28)
        if t < t0: continue
        sc = 2.2 - 1.2 * k
        tmp = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
        w_, _ = tw(td, ln, F_BIG); td.text(((W - w_) // 2, 10), ln, font=F_BIG, fill=WHITE + (255,))
        im = tmp.resize((int(W * sc), int(200 * sc)), Image.LANCZOS)
        if k < 1: im = im.filter(ImageFilter.GaussianBlur(int(10 * (1 - k))))
        im.putalpha(im.getchannel("A").point(lambda v: int(v * min(1, k * 1.4))))
        lay.alpha_composite(im, ((W - im.width) // 2, 760 + j * 150 - (im.height - 200) // 2))
        if 0 <= t - t0 - 0.28 < 0.18: shake = int(14 * (1 - (t - t0 - 0.28) / 0.18))
    # 4) destello de luz que barre el título
    if 2.6 < t < 3.4:
        p = (t - 2.6) / 0.8; x = int(-400 + (W + 800) * p)
        sw = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sw)
        sd.polygon([(x, 700), (x + 160, 700), (x + 20, 1260), (x - 140, 1260)], fill=(255, 240, 210, 70))
        lay.alpha_composite(sw.filter(ImageFilter.GaussianBlur(45)))
    # 5) nombre
    a3 = ease((t - 2.9) / 0.5)
    lw2 = int(220 * a3); d.rectangle(((W - lw2) // 2, 1250, (W + lw2) // 2, 1255), fill=GOLD + (255,))
    s = "Dr. Julio De la Morena"; w_, _ = tw(d, s, F_NAME); d.text(((W - w_) // 2, 1285), s, font=F_NAME, fill=SOFT + (int(255 * a3),))
    if t > T_IN - 0.35:
        fo = int(255 * ease((t - (T_IN - 0.35)) / 0.35)); d.rectangle((0, 0, W, H), fill=NAVY + (fo,))
    fr.alpha_composite(lay, (0, shake) if shake else (0, 0))
    if shake: fr.alpha_composite(lay, (0, 0)) if False else None
    out = fr.convert("RGB")
    # destello blanco breve en cada golpe
    for t0 in (1.35, 1.75, 2.15):
        dt = t - t0 - 0.28
        if 0 <= dt < 0.12: out = Image.blend(out, Image.new("RGB", (W, H), (255, 255, 255)), 0.18 * (1 - dt / 0.12))
    return out

def strike(d, x0, x1, y, p, col=RED, wdt=10):
    if p > 0: d.line((x0, y, x0 + (x1 - x0) * p, y), fill=col + (255,), width=wdt)

def panel(d, i, lt):
    """Gráfico de la mitad de arriba para la frase i (lt = segundos desde que empieza)."""
    a = int(255 * ease(lt / 0.4))
    if i == 0:
        s = "TENDINITIS"; w_, _ = tw(d, s, F_K); d.text(((W - w_) // 2, 400), s, font=F_K, fill=WHITE + (a,))
        ctext(d, 560, "¿seguro?", F_S, GOLD + (int(255 * ease((lt - 1.0) / 0.4)),))
    elif i == 1:
        s = "INFLAMACIÓN"; w_, _ = tw(d, s, F_K2); x = (W - w_) // 2
        d.text((x, 300), s, font=F_K2, fill=WHITE + (a,)); strike(d, x - 10, x + w_ + 10, 360, ease((lt - 1.4) / 0.5))
        b = int(255 * ease((lt - 3.2) / 0.5)); s = "DEGENERACIÓN"; w_, _ = tw(d, s, F_K2)
        d.text(((W - w_) // 2, 500), s, font=F_K2, fill=GOLD + (b,))
        ctext(d, 640, "el tendón pierde calidad", F_S, SOFT + (b,))
    elif i == 2:
        ctext(d, 250, "British Medical Journal · 1999", F_S, GOLD + (a,))
        s = "TENDINITIS"; w_, _ = tw(d, s, F_K2); x = (W - w_) // 2
        d.text((x, 360), s, font=F_K2, fill=WHITE + (a,)); strike(d, x - 10, x + w_ + 10, 420, ease((lt - 2.0) / 0.5))
        b = int(255 * ease((lt - 2.8) / 0.5)); s = "TENDINOPATÍA"; w_, _ = tw(d, s, F_K2)
        d.text(((W - w_) // 2, 520), s, font=F_K2, fill=GOLD + (b,))
    elif i == 3:
        ctext(d, 280, "ANTIINFLAMATORIOS", F_K2, WHITE + (a,))
        b = int(255 * ease((lt - 2.2) / 0.4)); c = int(255 * ease((lt - 3.4) / 0.4))
        ctext(d, 450, "alivian el dolor", F_SUB, SOFT + (b,))
        ctext(d, 540, "no reparan el tendón", F_SUB, GOLD + (c,))
    elif i == 4:
        ctext(d, 230, "CARGA PROGRESIVA", F_K2, WHITE + (a,))
        for k in range(6):
            p = ease((lt - 0.6 - k * 0.35) / 0.4)
            hgt = int((60 + k * 45) * p); x0 = 260 + k * 100
            d.rounded_rectangle((x0, 700 - hgt, x0 + 70, 700), 8, fill=GOLD + (int(255 * min(1, p * 1.5)),))
        ctext(d, 730, "ejercicio bien dosificado", F_S, SOFT + (int(255 * ease((lt - 2.8) / 0.4)),))
    elif i == 5:
        ctext(d, 330, "¿Y por qué se sigue llamando", F_S, SOFT + (a,))
        ctext(d, 400, "TENDINITIS?", F_K, WHITE + (a,))

def cuerpo(t):
    lt_all = t - T_IN
    fr = Image.new("RGB", (W, H), NAVY)
    # mitad de abajo: foto con zoom lento
    z = 1.0 + 0.06 * (lt_all / VOZ)
    fw, fh = int(foto.width * z), int(foto.height * z)
    fz = foto.resize((fw, fh), Image.BILINEAR)
    ox = (fw - W) // 2 + int(20 * lt_all / VOZ); oy = int(fh * 0.04)
    fr.paste(fz.crop((ox, oy, ox + W, oy + 960)), (0, 960))
    top = BG.crop((0, 200, W, 1160)); fr.paste(top, (0, 0))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # banda de la serie
    d.rectangle((0, 0, W, 110), fill=(8, 18, 36, 255))
    s = "LO QUE CASI NADIE TE CUENTA"; w_, _ = tw(d, s, F_TAG); d.text(((W - w_) // 2, 40), s, font=F_TAG, fill=GOLD + (255,))
    d.rectangle((0, 955, W, 965), fill=GOLD + (255,))
    i = max([k for k, m in enumerate(marks) if m[0] <= lt_all] or [0])
    panel(d, i, lt_all - marks[i][0])
    # subtítulo sobre la foto
    s0, s1, txt = marks[i]
    txt = txt.replace('mil novecientos noventa y nueve', '1999')
    if s0 <= lt_all <= s1 + 0.3:
        lines = wrap(d, txt, F_SUB, 900)
        # trocea frases largas en dos mitades según el tiempo
        if len(lines) > 2:
            half = (len(lines) + 1) // 2
            lines = lines[:half] if lt_all < s0 + (s1 - s0) * half / len(lines) else lines[half:]
        y = 1640 - len(lines) * 62
        for ln in lines:
            w_, h_ = tw(d, ln, F_SUB)
            d.rounded_rectangle(((W - w_) // 2 - 22, y - 8, (W + w_) // 2 + 22, y + 66), 14, fill=(0, 0, 0, 165))
            d.text(((W - w_) // 2, y), ln, font=F_SUB, fill=WHITE + (255,)); y += 82
    if lt_all < 0.35:
        d.rectangle((0, 0, W, H), fill=NAVY + (int(255 * (1 - ease(lt_all / 0.35))),))
    fr = fr.convert("RGBA"); fr.alpha_composite(lay); return fr.convert("RGB")

def cierre(t):
    lt = t - T_IN - VOZ
    fr = BG.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    a = int(255 * ease(lt / 0.5)); b = int(255 * ease((lt - 0.5) / 0.5)); c = int(255 * ease((lt - 1.0) / 0.5))
    y = ctext(d, 700, "Dr. Julio De la Morena", cor(96, 700), WHITE + (a,))
    ctext(d, y + 10, "Medicina Deportiva y Terapias Regenerativas", inter(36, "Medium"), SOFT + (a,))
    lw = int(240 * ease((lt - 0.4) / 0.5)); d.rectangle(((W - lw) // 2, 1000, (W + lw) // 2, 1005), fill=GOLD + (255,))
    ctext(d, 1050, "drjuliodelamorena.com", inter(50, "Bold"), WHITE + (b,))
    ctext(d, 1125, "@drjuliodelamorena", inter(50, "Bold"), GOLD + (b,))
    ctext(d, 1290, "Cada lunes, lo que casi nadie te cuenta", inter(34, "Medium"), SOFT + (c,))
    if lt < 0.3: d.rectangle((0, 0, W, H), fill=NAVY + (int(255 * (1 - lt / 0.3)),))
    fr.alpha_composite(lay); return fr.convert("RGB")

def frame(t):
    if t < T_IN: return intro(t)
    if t < T_IN + VOZ: return cuerpo(t)
    return cierre(t)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for x in sys.argv[1:]: frame(float(x)).resize((540, 960)).save(os.path.join(D, f"prev_{x}.jpg"))
        sys.exit()
    out = os.path.join(D, "v.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(int(TOTAL * FPS)):
        p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait()
    json.dump({"T_IN": T_IN, "VOZ": VOZ, "TOTAL": TOTAL}, open(os.path.join(D, "tiempos.json"), "w"))
    print(out, TOTAL)
