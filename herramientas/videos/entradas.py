"""Entradas de 4,2 s para cada sección (martes a sábado). Uso: python3 entradas.py [seccion] [t...]"""
import math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import cor, inter, ease, tw, W, H, FPS, GOLD, WHITE, SOFT

D = os.path.dirname(os.path.abspath(__file__))
T = 4.2
F_DIA = inter(40, "Bold"); F_NAME = inter(38, "Medium")

def grad(c1, c2):
    im = Image.new("RGB", (W, H), c1); g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse((-300, -200, W + 300, 1100), fill=90); g = g.filter(ImageFilter.GaussianBlur(160))
    im.paste(Image.new("RGB", (W, H), c2), (0, 0), g); return im

def golpe(lay, txt, font, y, t, t0, color=WHITE, desde=2.2):
    if t < t0: return
    k = ease((t - t0) / 0.28); sc = desde - (desde - 1) * k
    tmp = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    w_, _ = tw(td, txt, font); td.text(((W - w_) // 2, 10), txt, font=font, fill=color + (255,))
    im = tmp.resize((max(1, int(W * sc)), max(1, int(200 * sc))), Image.LANCZOS)
    if k < 1: im = im.filter(ImageFilter.GaussianBlur(int(10 * (1 - k))))
    im.putalpha(im.getchannel("A").point(lambda v: int(v * min(1, k * 1.4))))
    lay.alpha_composite(im, ((W - im.width) // 2, y - (im.height - 200) // 2))

def letras(d, s, y, t, t0, dur, col):
    n = int(len(s) * max(0, min(1, (t - t0) / dur))); w_, _ = tw(d, s, F_DIA)
    d.text(((W - w_) // 2, y), s[:n], font=F_DIA, fill=col + (255,))

def nombre(d, t, t0, col):
    a = ease((t - t0) / 0.5); lw = int(220 * a)
    d.rectangle(((W - lw) // 2, 1250, (W + lw) // 2, 1255), fill=col + (255,))
    s = "Dr. Julio De la Morena"; w_, _ = tw(d, s, F_NAME); d.text(((W - w_) // 2, 1285), s, font=F_NAME, fill=SOFT + (int(255 * a),))

def cierre_fundido(d, t, col):
    if t > T - 0.35: d.rectangle((0, 0, W, H), fill=col + (int(255 * ease((t - (T - 0.35)) / 0.35)),))

def flash(out, t, golpes, rgb=(255, 255, 255), fuerza=0.18):
    for t0 in golpes:
        dt = t - t0
        if 0 <= dt < 0.12: out = Image.blend(out, Image.new("RGB", (W, H), rgb), fuerza * (1 - dt / 0.12))
    return out

# ---------- MARTES: CÓMO SE DIAGNOSTICA (ecografía, verde azulado) ----------
TEAL, TEAL2, CYAN = (6, 32, 40), (10, 60, 70), (90, 220, 220)
BG_M = grad(TEAL, TEAL2)
def martes(t):
    fr = BG_M.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # abanico de ecografía que se dibuja
    p = ease(t / 1.2); cx, cy = W // 2, 300
    for r in range(120, 1300, 70):
        a = int(70 * p * (1 - r / 1400))
        d.arc((cx - r, cy - r, cx + r, cy + r), 60, 120, fill=CYAN + (a,), width=2)
    # línea de barrido
    ang = math.radians(60 + 60 * ((t * 0.9) % 1)); x2 = cx + 1300 * math.cos(ang); y2 = cy + 1300 * math.sin(ang)
    sw = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sw).line((cx, cy, x2, y2), fill=CYAN + (160,), width=10)
    lay.alpha_composite(sw.filter(ImageFilter.GaussianBlur(8)))
    letras(d, "L O S   M A R T E S   D E …", 650, t, 0.35, 0.8, CYAN)
    golpe(lay, "CÓMO SE", cor(132, 700), 760, t, 1.35)
    golpe(lay, "DIAGNOSTICA", cor(132, 700), 910, t, 1.85, CYAN)
    # electro: pulso
    if t > 2.4:
        k = min(1, (t - 2.4) / 0.8); pts = []
        for i in range(int(60 * k) + 1):
            x = 140 + i * 13.3; yy = 1150
            if 28 <= i <= 34: yy += [-0, -60, 90, -140, 60, -20, 0][i - 28]
            pts.append((x, yy))
        if len(pts) > 1: d.line(pts, fill=CYAN + (230,), width=5)
    nombre(d, t, 3.0, CYAN); cierre_fundido(d, t, TEAL)
    fr.alpha_composite(lay); return flash(fr.convert("RGB"), t, (1.63, 2.13), (200, 255, 255))

# ---------- MIÉRCOLES: EL EJERCICIO DE LA SEMANA (energía, naranja) ----------
OSC, OSC2, NAR = (30, 18, 10), (70, 35, 12), (255, 140, 40)
BG_X = grad(OSC, OSC2)
def miercoles(t):
    fr = BG_X.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # barras de energía que suben y bajan como un ecualizador
    for i in range(12):
        h = (0.35 + 0.65 * abs(math.sin(t * 6 + i * 0.7))) * 260 * ease(t / 0.6)
        x = 90 + i * 78; d.rounded_rectangle((x, 560 - h, x + 50, 560), 10, fill=NAR + (int(110 + 80 * (i % 2)),))
    letras(d, "L O S   M I É R C O L E S   D E …", 610, t, 0.3, 0.8, NAR)
    golpe(lay, "EL EJERCICIO", cor(124, 700), 740, t, 1.35)
    golpe(lay, "DE LA SEMANA", cor(124, 700), 890, t, 1.85, NAR)
    # disco de pesa que entra girando
    if t > 2.3:
        k = ease((t - 2.3) / 0.5); x = int(-200 + (W // 2 + 200) * k); y = 1150; r = 70
        d.ellipse((x - r, y - r, x + r, y + r), outline=NAR + (255,), width=14); d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=NAR + (255,))
        if k > 0.3: d.rectangle((x - r - 260 * k, y - 8, x - r, y + 8), fill=SOFT + (200,))
    nombre(d, t, 3.0, NAR); cierre_fundido(d, t, OSC)
    sh = 10 if 1.63 <= t < 1.75 or 2.13 <= t < 2.25 else 0
    fr.alpha_composite(lay, (0, sh)); return flash(fr.convert("RGB"), t, (1.63, 2.13), (255, 200, 140))

# ---------- JUEVES: ¿MITO O VERDAD? (rojo contra verde) ----------
ROJO, VERDE = (200, 50, 50), (40, 170, 90)
def jueves(t):
    fr = Image.new("RGB", (W, H), (20, 20, 28)).convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    k = ease(t / 0.7)
    d.polygon([(0, 0), (int(W * 0.62 * k), 0), (int(W * 0.38 * k), H), (0, H)], fill=ROJO + (235,))
    d.polygon([(W, 0), (W - int(W * 0.38 * k), 0), (W - int(W * 0.62 * k), H), (W, H)], fill=VERDE + (235,))
    letras(d, "L O S   J U E V E S   D E …", 470, t, 0.3, 0.8, WHITE)
    golpe(lay, "¿MITO", cor(170, 700), 600, t, 1.2)
    golpe(lay, "O VERDAD?", cor(170, 700), 790, t, 1.9)
    # gran interrogación que gira y rebota
    if t > 2.5:
        kk = ease((t - 2.5) / 0.6); ang = 25 * math.sin((t - 2.5) * 9) * (1 - kk)
        q = Image.new("RGBA", (360, 420), (0, 0, 0, 0)); ImageDraw.Draw(q).text((70, -40), "?", font=cor(420, 700), fill=(255, 255, 255, 230))
        q = q.rotate(ang, resample=Image.BICUBIC); s = 0.25 + 0.5 * kk
        q = q.resize((int(360 * s), int(420 * s)), Image.LANCZOS)
        lay.alpha_composite(q, ((W - q.width) // 2, 1010 + (320 - q.height) // 2))
    a = ease((t - 3.1) / 0.5); s_ = "Dr. Julio De la Morena"; w_, _ = tw(d, s_, F_NAME)
    if a > 0: d.text(((W - w_) // 2, 1380), s_, font=F_NAME, fill=WHITE + (int(255 * a),))
    cierre_fundido(d, t, (20, 20, 28))
    fr.alpha_composite(lay); return flash(fr.convert("RGB"), t, (1.48, 2.18))

# ---------- VIERNES: EL ESTUDIO DE LA SEMANA (papel de revista) ----------
PAPEL, TINTA, BURDEOS = (244, 238, 226), (30, 30, 36), (130, 30, 40)
def viernes(t):
    fr = Image.new("RGB", (W, H), PAPEL).convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # líneas de texto de artículo que se escriben solas
    for i in range(16):
        y = 230 + i * 34; L = 0.55 + 0.4 * ((i * 37) % 10) / 10
        p = max(0, min(1, (t - i * 0.05) / 0.5))
        d.rectangle((140, y, 140 + int((W - 280) * L * p), y + 12), fill=(200, 194, 182, 255))
    for i in range(10):
        y = 1340 + i * 34; L = 0.5 + 0.45 * ((i * 53) % 10) / 10
        p = max(0, min(1, (t - 0.4 - i * 0.05) / 0.5))
        d.rectangle((140, y, 140 + int((W - 280) * L * p), y + 12), fill=(200, 194, 182, 255))
    d.rectangle((120, 722, W - 120, 726), fill=BURDEOS + (255,))
    letras(d, "L O S   V I E R N E S   D E …", 640, t, 0.3, 0.8, BURDEOS)
    golpe(lay, "EL ESTUDIO", cor(132, 700), 740, t, 1.35, TINTA, 1.6)
    golpe(lay, "DE LA SEMANA", cor(132, 700), 890, t, 1.85, BURDEOS, 1.6)
    # sello
    if t > 2.5:
        k = ease((t - 2.5) / 0.25); s = 2.0 - k
        st = Image.new("RGBA", (520, 140), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((6, 6, 514, 134), 16, outline=BURDEOS + (255,), width=8)
        tx = "PUBLICADO Y REVISADO"; w_, _ = tw(sd, tx, inter(34, "Bold")); sd.text(((520 - w_) // 2, 48), tx, font=inter(34, "Bold"), fill=BURDEOS + (255,))
        st = st.rotate(-8, expand=True, resample=Image.BICUBIC); st = st.resize((int(st.width * s), int(st.height * s)))
        st.putalpha(st.getchannel("A").point(lambda v: int(v * k)))
        lay.alpha_composite(st, ((W - st.width) // 2, 1175 - st.height // 2))
    a = ease((t - 3.0) / 0.5); s_ = "Dr. Julio De la Morena"; w_, _ = tw(d, s_, F_NAME)
    d.text(((W - w_) // 2, 1290), s_, font=F_NAME, fill=TINTA + (int(255 * a),))
    cierre_fundido(d, t, PAPEL)
    fr.alpha_composite(lay); return fr.convert("RGB")

# ---------- SÁBADO: CURIOSIDADES DEL CUERPO (morado, explosión) ----------
MOR, MOR2, ROSA = (25, 12, 45), (70, 25, 110), (230, 120, 255)
BG_S = grad(MOR, MOR2)
random.seed(4); PART = [(random.uniform(0, 2 * math.pi), random.uniform(300, 1300), random.uniform(5, 16), random.choice([ROSA, GOLD, WHITE])) for _ in range(140)]
def sabado(t):
    fr = BG_S.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # cuenta atrás de energía hacia el centro y explosión en 1,3 s
    cx, cy = W // 2, 900
    if t < 1.3:
        r = int(40 + 30 * math.sin(t * 20)); a = int(255 * min(1, t / 0.5))
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROSA + (a,))
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(20)))
    else:
        dt = t - 1.3
        rr = int(1600 * ease(dt / 0.6)); aa = int(200 * max(0, 1 - dt / 0.6))
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=ROSA + (aa,), width=30)
        for ang, vel, sz, col in PART:
            dist = vel * ease(dt / 1.4); x = cx + dist * math.cos(ang); y = cy + dist * math.sin(ang) + 200 * dt * dt
            al = int(255 * max(0, 1 - dt / 2.2))
            if al > 0: d.ellipse((x - sz, y - sz, x + sz, y + sz), fill=col + (al,))
    letras(d, "L O S   S Á B A D O S   D E …", 640, t, 1.35, 0.6, ROSA)
    golpe(lay, "CURIOSIDADES", cor(124, 700), 760, t, 1.55, WHITE, 2.6)
    golpe(lay, "DEL CUERPO", cor(124, 700), 910, t, 2.05, ROSA, 2.6)
    nombre(d, t, 3.0, ROSA); cierre_fundido(d, t, MOR)
    sh = int(18 * max(0, 1 - (t - 1.3) / 0.3)) if 1.3 <= t < 1.6 else 0
    fr.alpha_composite(lay, (sh, -sh)); out = fr.convert("RGB")
    return flash(out, t, (1.3,), (255, 230, 255), 0.6)

SECC = {"martes": martes, "miercoles": miercoles, "jueves": jueves, "viernes": viernes, "sabado": sabado}

def render(nom):
    f = SECC[nom]; out = os.path.join(D, f"entrada_{nom}_v.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(int(T * FPS)): p.stdin.write(f(n / FPS).tobytes())
    p.stdin.close(); p.wait(); return out

if __name__ == "__main__":
    nom = sys.argv[1]
    if len(sys.argv) > 2:
        for x in sys.argv[2:]: SECC[nom](float(x)).resize((360, 640)).save(os.path.join(D, f"pv_{nom}_{x}.jpg"))
    else:
        print(render(nom))
