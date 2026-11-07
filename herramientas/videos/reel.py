"""Versión reel: gancho -> sello de 1 s -> resto -> cierre corto (3,4 s)."""
import json, os, subprocess, sys
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D); sys.path.append("/home/claude/web-drjuliodelamorena/herramientas/videos")
import render as R
import entradas as E
import cierre as C

STING = 1.5
GAP = 0.15

def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)

# frases: gancho + resto (reutiliza f2..f5 del ejemplo)
partes = [("h0.wav", "La tendinitis… casi nunca es una inflamación."),
          ("h1.wav", "En un tendón que lleva meses doliendo, lo que hay es un tendón degenerado, que ha perdido calidad."),
          ("f2.wav", "En mil novecientos noventa y nueve, el British Medical Journal ya pidió dejar de llamarla tendinitis."),
          ("f3.wav", "Por eso los antiinflamatorios no la curan: alivian el dolor, pero el tendón sigue igual."),
          ("f4.wav", "Lo que de verdad lo recupera es cargarlo de forma progresiva, con ejercicio bien dosificado."),
          ("f5.wav", "El nombre sigue porque es fácil de decir… y de recetar.")]
marks, t, lst = [], 0.2, []
for i, (f, txt) in enumerate(partes):
    d_ = dur(os.path.join(D, f)); marks.append([t, t + d_ - 0.35, txt]); lst.append((t, f)); t += d_
    if i == 0: HOOK_END = t; t += STING + GAP
VOZ = t + 0.5
R.marks = marks; R.T_IN = 0.0; R.VOZ = VOZ
R.BANDA = "LOS LUNES DE…  LO QUE CASI NADIE TE CUENTA"

def sello_base(dia):
    if dia == "lunes": return R.intro(3.6)
    return E.SECC[dia](3.7)
_t = R.T_IN; R.T_IN = 4.2
BASE = sello_base("lunes")
R.T_IN = _t

def sello(lt):
    from render import ease
    s = 1.25 - 0.25 * ease(lt / 0.25)
    im = BASE.resize((int(R.W * s), int(R.H * s)), Image.LANCZOS)
    x, y = (im.width - R.W) // 2, (im.height - R.H) // 2
    out = im.crop((x, y, x + R.W, y + R.H))
    if lt < 0.1: out = Image.blend(out, Image.new("RGB", (R.W, R.H), (255, 245, 225)), 0.35 * (1 - lt / 0.1))
    return out

C_INI = 1.2
T_CIERRE = C.T - C_INI
TOTAL = VOZ + T_CIERRE

def frame(t):
    if HOOK_END <= t < HOOK_END + STING: return sello(t - HOOK_END)
    if t < VOZ: return R.cuerpo(t)
    return C.frame(t - VOZ + C_INI, "lunes")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for x in sys.argv[1:]: frame(float(x)).resize((360, 640)).save(os.path.join(D, f"rv_{x}.jpg"))
        sys.exit()
    v = os.path.join(D, "reel_v.mp4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{R.W}x{R.H}", "-r", str(R.FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", v], stdin=subprocess.PIPE)
    for n in range(int(TOTAL * R.FPS)): p.stdin.write(frame(n / R.FPS).tobytes())
    p.stdin.close(); p.wait()
    json.dump({"HOOK_END": HOOK_END, "VOZ": VOZ, "TOTAL": TOTAL, "voz": lst}, open(os.path.join(D, "reel.json"), "w"))
    print(v, HOOK_END, VOZ, TOTAL)
