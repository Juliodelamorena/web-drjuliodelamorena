"""Vídeos de martes a sábado con el formato nuevo.
Uso: python3 semana.py voz <dia>      -> genera las voces (ElevenLabs, voz clonada de Julio)
     python3 semana.py frames <dia> t.. -> fotogramas de prueba
     python3 semana.py render <dia>   -> vídeo final
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/claude/web-drjuliodelamorena/herramientas/videos"
sys.path.insert(0, D); sys.path.append(REPO)
import render as R
import entradas as E
import cierre as C
from guion_semana import DIAS

STING, GAP, C_INI = 1.5, 0.15, 1.2
KEY = open(os.path.join(D, "..", "dub", ".key")).read().strip()
VOICE = "FMUNJCsKXSdEGNKTCd7w"
FONTS = {"K": R.F_K, "K2": R.F_K2, "S": R.F_S, "SUB": R.F_SUB}
COL = {"W": R.WHITE, "G": R.GOLD, "S": R.SOFT, "R": R.RED}

def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

def voz(dia):
    import urllib.request
    cfg = DIAS[dia]
    for i, p in enumerate(cfg["frases"]):
        mp = os.path.join(D, f"{dia}_{i}.mp3")
        if not os.path.exists(mp):
            body = json.dumps({"text": p["voz"], "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.85}}).encode()
            r = urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"}))
            open(mp, "wb").write(r.read())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.35", "-ar", "44100", "-ac", "1", os.path.join(D, f"{dia}_{i}.wav")], check=True)
    print("voces", dia, [round(dur(os.path.join(D, f"{dia}_{i}.wav")), 1) for i in range(len(cfg["frases"]))])

def panel_generico(d, i, lt):
    items = DIAS[panel_generico.dia]["frases"][i]["panel"]
    for it in items:
        kind, y, txt, fk, ck, t0 = it[:6]
        a = int(255 * R.ease((lt - t0) / 0.4)) if (i > 0 or t0 > 0) else 255
        if a <= 0: continue
        f = FONTS[fk]
        if kind == "t":
            R.ctext(d, y, txt, f, COL[ck] + (a,))
        elif kind == "x":  # texto tachado
            w_, _ = R.tw(d, txt, f); x = (R.W - w_) // 2
            d.text((x, y), txt, font=f, fill=COL[ck] + (a,))
            R.strike(d, x - 10, x + w_ + 10, y + int(f.size * 0.62), R.ease((lt - it[6]) / 0.5))
        elif kind == "b":  # barras crecientes
            for k in range(6):
                p = R.ease((lt - t0 - k * 0.3) / 0.4); h = int((60 + k * 45) * p); x0 = 260 + k * 100
                d.rounded_rectangle((x0, y - h, x0 + 70, y), 8, fill=R.GOLD + (int(255 * min(1, p * 1.5)),))

def construir(dia):
    cfg = DIAS[dia]; panel_generico.dia = dia
    R.panel = panel_generico
    marks, lst, t = [], [], 0.2
    HOOK_END = None
    for i, p in enumerate(cfg["frases"]):
        w = os.path.join(D, f"{dia}_{i}.wav"); d_ = dur(w)
        marks.append([t, t + d_ - 0.35, p["sub"]]); lst.append((t, w)); t += d_
        if i == 0: HOOK_END = t; t += STING + GAP
    VOZ = t + 0.5
    R.marks = marks; R.T_IN = 0.0; R.VOZ = VOZ; R.BANDA = cfg["banda"]
    if cfg.get("cierre"): C.manana(dia, cfg["cierre"])
    else: C.FRASE[dia] = cfg["cierre_frase"]
    _t = R.T_IN; R.T_IN = 4.2
    BASE = E.SECC[dia](3.7)
    R.T_IN = _t
    return marks, lst, HOOK_END, VOZ, BASE

def hacer(dia):
    marks, lst, HOOK_END, VOZ, BASE = construir(dia)
    cfg = DIAS[dia]; TOTAL = VOZ + C.T - C_INI

    def sello(lt):
        s = 1.25 - 0.25 * R.ease(lt / 0.25)
        im = BASE.resize((int(R.W * s), int(R.H * s)), Image.LANCZOS)
        x, y = (im.width - R.W) // 2, (im.height - R.H) // 2
        out = im.crop((x, y, x + R.W, y + R.H))
        if lt < 0.1: out = Image.blend(out, Image.new("RGB", (R.W, R.H), (255, 245, 225)), 0.35 * (1 - lt / 0.1))
        return out

    def gancho(im, t):
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        a = 255 if t < HOOK_END - 0.3 else int(255 * max(0, (HOOK_END - t) / 0.3))
        R.ctext(d, 760, cfg["gancho"], R.cor(62, 700), R.GOLD + (a,))
        out = im.convert("RGBA"); out.alpha_composite(lay); return out.convert("RGB")

    def frame(t):
        if HOOK_END <= t < HOOK_END + STING: return sello(t - HOOK_END)
        if t < HOOK_END: return gancho(R.cuerpo(t), t)
        if t < VOZ: return R.cuerpo(t)
        return C.frame(t - VOZ + C_INI, dia)
    return frame, marks, lst, HOOK_END, VOZ, TOTAL

def audio(dia, lst, HOOK_END, VOZ, TOTAL, video, out):
    so = os.path.join(REPO, "sonidos")
    ent = {"martes": [("beep.wav", 0.0, 0.8), ("kick.wav", 0.05, 1.0)], "miercoles": [("whoosh.wav", 0.0, 0.9), ("clank.wav", 0.1, 0.9)],
           "jueves": [("mito.wav", 0.0, 1.2), ("kick.wav", 0.05, 1.0)], "viernes": [("flip.wav", 0.0, 0.9), ("kick.wav", 0.05, 0.8)],
           "sabado": [("boom.wav", 0.0, 1.0), ("kick.wav", 0.05, 0.9)]}[dia]
    fx = [(f, HOOK_END + t0, v) for f, t0, v in ent]
    fx += [(f, VOZ + t0 - C_INI, v) for f, t0, v in C.SON if t0 >= C_INI]
    args = ["ffmpeg", "-v", "error", "-y", "-i", video, "-i", os.path.join(so, "musica_larga.wav")]
    for _, w in lst: args += ["-i", w]
    for f, _, _ in fx: args += ["-i", os.path.join(so, f) if os.path.exists(os.path.join(so, f)) else os.path.join(D, f)]
    fc = f"[1]atrim=10:{10 + TOTAL},asetpts=PTS-STARTPTS,volume=0.10,afade=t=in:d=0.6,afade=t=out:st={TOTAL - 1.0}:d=1.0[m];"; labs = ["[m]"]
    for i, (t0, _) in enumerate(lst):
        fc += f"[{i + 2}]adelay={int(t0 * 1000)}:all=1,volume=1.0[v{i}];"; labs.append(f"[v{i}]")
    base = 2 + len(lst)
    for j, (_, t0, v) in enumerate(fx):
        fc += f"[{base + j}]adelay={int(max(0, t0) * 1000)}:all=1,volume={v * 0.6}[x{j}];"; labs.append(f"[x{j}]")
    fc += "".join(labs) + f"amix=inputs={len(labs)}:normalize=0,apad,atrim=0:{TOTAL},loudnorm=I=-16:TP=-1.5[a]"
    subprocess.run(args + ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", "-movflags", "+faststart", out], check=True)

if __name__ == "__main__":
    cmd, dia = sys.argv[1], sys.argv[2]
    if cmd == "voz": voz(dia)
    elif cmd == "frames":
        frame, *_ = hacer(dia)
        for x in sys.argv[3:]: frame(float(x)).resize((360, 640)).save(os.path.join(D, f"f_{dia}_{x}.jpg"))
    elif cmd == "render":
        frame, marks, lst, HOOK_END, VOZ, TOTAL = hacer(dia)
        v = os.path.join(D, f"{dia}_v.mp4")
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{R.W}x{R.H}", "-r", str(R.FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", v], stdin=subprocess.PIPE)
        for n in range(int(TOTAL * R.FPS)): p.stdin.write(frame(n / R.FPS).tobytes())
        p.stdin.close(); p.wait()
        out = os.path.join(D, f"video-{dia}.mp4"); audio(dia, lst, HOOK_END, VOZ, TOTAL, v, out)
        print(out, round(HOOK_END, 1), round(VOZ, 1), round(TOTAL, 1))
