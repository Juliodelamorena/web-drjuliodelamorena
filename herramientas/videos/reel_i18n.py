"""Versiones en otros idiomas de un reel ya publicado en español (vídeo con rótulos y subtítulos incrustados).

Uso: python3 reel_i18n.py <reel> <idioma|all>      (reel = clave de CFG en reels_cfg.py)
Qué hace: dobla la voz con la voz clonada de Julio (ElevenLabs, clave en .key), cubre el rótulo de arriba, los subtítulos
y las líneas de la tarjeta final con versiones traducidas, y genera el .vtt de subtítulos. Se parte siempre del vídeo
original en español (ENTRADA/<reel>.mp4). Salida: out/<f>.<idioma>.mp4 y out/<f>.<idioma>.vtt
"""
import json, os, subprocess, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
KEY = open(os.path.join(D, ".key")).read().strip()
VOZ = "FMUNJCsKXSdEGNKTCd7w"
W, H = 1080, 1920
NAVY, GOLD, WHITE, SOFT = (12, 25, 51), (196, 161, 105), (255, 255, 255), (200, 210, 225)
CAPBOX = (16, 28, 54, 255)
ENTRADA = os.environ.get("REEL_ENTRADA", "/home/claude/reels_src")
CJK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
CJKS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def sh(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True).stdout


def dur(f):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f))


def f_titulo(lang, size):
    if lang == "ka": return ImageFont.truetype(os.path.join(D, "fonts", "KaSerif.ttf"), size)
    if lang == "zh": return ImageFont.truetype(CJK, size, index=2)
    f = ImageFont.truetype(os.path.join(D, "fonts", "Cor.ttf"), size)
    try: f.set_variation_by_axes([700])
    except Exception: pass
    return f


def f_texto(lang, size, bold=True):
    if lang == "ka": return ImageFont.truetype(os.path.join(D, "fonts", "KaSans.ttf"), size)
    if lang == "zh": return ImageFont.truetype(CJKS, size, index=2)
    return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{'Bold' if bold else 'Regular'}.otf", size)


def ancho(d, s, f):
    b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]


def ajusta(d, s, make, size, maxw):
    f = make(size)
    while ancho(d, s, f) > maxw and size > 20:
        size -= 2; f = make(size)
    return f


def centro(d, s, f, cx, cy, fill):
    b = d.textbbox((0, 0), s, font=f)
    d.text((cx - (b[0] + b[2]) / 2, cy - (b[1] + b[3]) / 2), s, font=f, fill=fill)


def corta_lineas(s, f, maxw, lang):
    """Parte un texto en líneas que caben en maxw."""
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    toks = list(s) if lang == "zh" else s.split(" ")
    sep = "" if lang == "zh" else " "
    lineas, cur = [], ""
    for t in toks:
        prueba = (cur + sep + t) if cur else t
        if ancho(d, prueba, f) <= maxw: cur = prueba
        else:
            lineas.append(cur); cur = t
    if cur: lineas.append(cur)
    return lineas


def tts(texto, out, lang):
    if os.path.exists(out): return
    modelo = "eleven_v3" if lang == "ka" else "eleven_multilingual_v2"
    vs = {"stability": 0.5, "similarity_boost": 0.85, "style": 0.0}
    if modelo != "eleven_v3": vs["speed"] = 1.10
    p = {"text": texto, "model_id": modelo, "voice_settings": vs}
    if modelo == "eleven_v3": p["language_code"] = lang
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128",
                                 data=json.dumps(p).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r: open(out, "wb").write(r.read())


def voz_y_tiempos(cfg, lang, w):
    """Genera la voz por segmentos; devuelve (voz.wav, [(inicio, fin)] real de cada segmento)."""
    segs = cfg["seg"]; total = cfg["dur"]; piezas, tiempos, t_fin = [], [], 0.0
    for i, (ini, textos) in enumerate(segs):
        raw = os.path.join(w, f"{i:02d}.mp3"); tts(textos[lang], raw, lang)
        lim = os.path.join(w, f"{i:02d}.wav")
        sh("ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
           "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
           "-ar", "44100", "-ac", "1", lim)
        d = dur(lim); inicio = max(ini, t_fin + 0.15)
        siguiente = segs[i + 1][0] if i + 1 < len(segs) else cfg["voz_fin"]
        hueco = siguiente - inicio - 0.1; tempo = 1.0
        if d > hueco: tempo = min(1.18, d / max(hueco, 0.1))
        if tempo > 1.001:
            fit = os.path.join(w, f"{i:02d}_t.wav")
            sh("ffmpeg", "-v", "error", "-y", "-i", lim, "-af", f"atempo={tempo:.4f}", fit); lim = fit; d = dur(lim)
        piezas.append((inicio, lim)); tiempos.append((inicio, inicio + d)); t_fin = inicio + d
        print(f"  seg {i}: {inicio:.2f}-{inicio + d:.2f} (hueco {hueco:.2f}, tempo {tempo:.2f})")
    args = ["ffmpeg", "-v", "error", "-y"]
    for _, f in piezas: args += ["-i", f]
    filt = "".join(f"[{k}]adelay={int(t * 1000)}:all=1[a{k}];" for k, (t, _) in enumerate(piezas))
    filt += "".join(f"[a{k}]" for k in range(len(piezas))) + f"amix=inputs={len(piezas)}:normalize=0,apad=whole_dur={total}[v]"
    voz = os.path.join(w, "voz.wav")
    sh(*args, "-filter_complex", filt, "-map", "[v]", "-ar", "44100", "-ac", "1", voz)
    return voz, tiempos


def audio_final(voz, cfg, w):
    musica = os.path.join(D, "sonidos", "musica_larga.wav"); total = cfg["dur"]
    mezcla = (f"[1]apad=whole_dur={total},atrim=0:{total},volume=0.30[m];[0]volume=1.0[v];[m][v]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
              f"[md][0]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[out]")
    out = os.path.join(w, "audio.wav")
    sh("ffmpeg", "-v", "error", "-y", "-i", voz, "-i", musica, "-filter_complex", mezcla, "-map", "[out]", "-ar", "44100", "-ac", "2", out)
    return out


def subtitulos(cfg, lang, tiempos):
    """Trozos de dos líneas con su tiempo, repartidos por segmento según la duración real de la voz."""
    f = f_texto(lang, cfg.get("cap_size", 46)); maxw = 840 if lang != "zh" else 800
    trozos = []
    for i, (ini, textos) in enumerate(cfg["seg"]):
        a, b = tiempos[i]
        lin = corta_lineas(textos[lang], f, maxw, lang)
        grupos = [lin[k:k + 2] for k in range(0, len(lin), 2)]
        pesos = [sum(len(x) for x in g) for g in grupos]; tot = sum(pesos); t = a
        for g, p in zip(grupos, pesos):
            trozos.append([t, t + (b - a) * p / tot, g]); t += (b - a) * p / tot
    for k in range(len(trozos) - 1): trozos[k][1] = trozos[k + 1][0]          # sin huecos: se enlaza con el siguiente
    trozos[0][0] = 0.0; trozos[-1][1] = cfg["cap_fin"]
    return trozos


def fmt(t):
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}"


def png(im, nombre, w):
    p = os.path.join(w, nombre); im.save(p); return p


def overlays(cfg, lang, trozos, w):
    """Lista de (png, x, y, t0, t1)."""
    ov = []; d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    # --- rótulos de arriba
    for k, (t0, t1, kind, zona, lineas) in enumerate(cfg["titulos"]):
        T = lineas[lang]; y0, y1 = zona; im = Image.new("RGBA", (W, y1 - y0), NAVY + (255,)); d = ImageDraw.Draw(im)
        if kind == "intro":
            fa = ajusta(d0, T[0], lambda s: f_titulo(lang, s), 112, 900); fb = ajusta(d0, T[1], lambda s: f_titulo(lang, s), 52, 860)
            centro(d, T[0], fa, W // 2, 456 - y0, GOLD); centro(d, T[1], fb, W // 2, 594 - y0, WHITE)
        elif kind == "grande":
            n = len(T); f = ajusta(d0, max(T, key=len), lambda s: f_titulo(lang, s), 92, 900)
            ys = [540] if n == 1 else [496, 628]
            for s_, y_ in zip(T, ys): centro(d, s_, f, W // 2, y_ - y0, WHITE)
        elif kind == "cabecera":
            f = ajusta(d0, T[0], lambda s: f_titulo(lang, s), 62, 900); centro(d, T[0], f, W // 2, 362 - y0, WHITE)
        elif kind == "final":
            f = ajusta(d0, max(T, key=len), lambda s: f_titulo(lang, s), 96, 900)
            centro(d, T[0], f, W // 2, 500 - y0, WHITE); centro(d, T[1], f, W // 2, 630 - y0, GOLD)
        ov.append((png(im, f"t{k}.png", w), 0, y0, t0, t1))
    # --- subtítulos (dos cajas opacas que tapan las originales)
    fc = f_texto(lang, cfg.get("cap_size", 46))
    for k, (a, b, lin) in enumerate(trozos):
        im = Image.new("RGBA", (W, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for j, (x0, x1) in enumerate(cfg["cajas"]):
            y0 = 0 + j * 82
            d.rounded_rectangle((x0, y0, x1, y0 + 78), 20, fill=CAPBOX)
            if j < len(lin): centro(d, lin[j], fc, W // 2, y0 + 39, WHITE)
        ov.append((png(im, f"c{k}.png", w), 0, cfg["cap_y"], a, b))
    # --- tarjeta final: líneas traducidas y zonas que solo se tapan
    def fondo_tarjeta(y0, y1):
        src = Image.open(cfg["_frame_tarjeta"]).convert("RGB"); h = y1 - y0
        izq = np.array(src.crop((0, y0, 24, y1))).mean(axis=1); der = np.array(src.crop((W - 24, y0, W, y1))).mean(axis=1)
        arr = np.zeros((h, W, 3)); xs = np.linspace(0, 1, W)
        for r in range(h): arr[r] = izq[r][None, :] * (1 - xs)[:, None] + der[r][None, :] * xs[:, None]
        return Image.fromarray(arr.astype("uint8")).convert("RGBA")
    if cfg.get("tarjeta"):
        t0, t1, y0, y1 = cfg["tarjeta"]; l1, l2 = cfg["tarjeta_lineas"][lang]
        im = fondo_tarjeta(y0, y1); d = ImageDraw.Draw(im)
        for s_, yc in ((l1, 984), (l2, 1030)):
            f = ajusta(d0, s_, lambda z: f_texto(lang, z, bold=False), 30, 960); centro(d, s_, f, W // 2, yc - y0, SOFT)
        ov.append((png(im, "tarjeta.png", w), 0, y0, t0, t1))
        for k, (a, b, ya, yb) in enumerate(cfg.get("cubre", [])):
            ov.append((png(fondo_tarjeta(ya, yb), f"cubre{k}.png", w), 0, ya, a, b))
    return ov


def render(cfg, lang):
    f = cfg["f"]; w = os.path.join(D, "work", f, lang); os.makedirs(w, exist_ok=True)
    out_dir = os.path.join(D, "out"); os.makedirs(out_dir, exist_ok=True)
    print(f"== {f} [{lang}]")
    voz, tiempos = voz_y_tiempos(cfg, lang, w); audio = audio_final(voz, cfg, w)
    trozos = subtitulos(cfg, lang, tiempos)
    entrada = os.path.join(ENTRADA, cfg["entrada"])
    if cfg.get("tarjeta"):
        cfg["_frame_tarjeta"] = os.path.join(w, "tarjeta_src.png")
        sh("ffmpeg", "-v", "error", "-y", "-ss", str(cfg["tarjeta"][0] + 1.5), "-i", entrada, "-frames:v", "1", cfg["_frame_tarjeta"])
    ov = overlays(cfg, lang, trozos, w)
    args = ["ffmpeg", "-v", "error", "-y", "-i", entrada, "-i", audio]
    for p, *_ in ov: args += ["-i", p]
    filt, last = [], "0:v"
    for k, (p, x, y, t0, t1) in enumerate(ov):
        filt.append(f"[{last}][{k + 2}:v]overlay={x}:{y}:enable='between(t,{t0:.2f},{t1:.2f})'[v{k}]"); last = f"v{k}"
    out = os.path.join(out_dir, f"{f}.{lang}.mp4")
    sh(*args, "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out)
    with open(os.path.join(out_dir, f"{f}.{lang}.vtt"), "w") as v:
        v.write("WEBVTT\n\n")
        for a, b, lin in trozos: v.write(f"{fmt(a)} --> {fmt(b)}\n" + ("" if lang == "zh" else " ").join(lin) + "\n\n")
    print(out, f"{dur(out):.2f}s")


if __name__ == "__main__":
    from reels_cfg import CFG
    reel = sys.argv[1]; langs = ["en", "fr", "ru", "ka", "zh"] if sys.argv[2] == "all" else sys.argv[2:]
    for l in langs: render(CFG[reel], l)
