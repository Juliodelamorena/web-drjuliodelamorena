# -*- coding: utf-8 -*-
"""Vídeos de tarjetas de estudios en chino (PRP evidencia, PRP en artrosis): voz clonada de Julio + tarjetas renderizadas.
Uso: python3 estudios_zh.py prp-evidencia|prp-artrosis"""
import json, os, subprocess, sys, html, urllib.request
D = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(D)
WEB = os.path.abspath(os.path.join(V, "..", ".."))
KEY = open(os.path.join(V, ".key")).read().strip(); VOZ = "FMUNJCsKXSdEGNKTCd7w"
sys.path.insert(0, os.path.join(V, ".."))
W, H, FPS = 1080, 1920, 30
LATIN = "'Inter','Noto Sans CJK SC',sans-serif"
SERIF = "'Noto Serif CJK SC','Cormorant Garamond',serif"
FOTO = os.path.join(WEB, "img", "retrato.jpg")

def card(journal, title, authors, ref, tag):
    return f'''<div class="card"><div class="tag">{html.escape(tag)}</div><div class="j">{html.escape(journal)}</div>
<div class="t">{html.escape(title)}</div><div class="a">{html.escape(authors)}</div><div class="r">{html.escape(ref)} · PubMed</div></div>'''

CSS = f'''<style>
@font-face{{font-family:Cor;src:url(file://{V}/fonts/Cor.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;background:radial-gradient(ellipse 900px 700px at 50% 35%,#142848,#0c1b33 70%);font-family:{LATIN};color:#fff;position:relative;overflow:hidden}}
.top{{position:absolute;top:300px;width:100%;text-align:center;color:#c4a367;letter-spacing:.14em;font-size:34px;font-weight:600}}
.card{{position:absolute;left:100px;right:100px;top:420px;background:#f7f3e8;color:#1b1b1b;border-radius:10px;padding:46px 52px 40px;box-shadow:0 40px 80px rgba(0,0,0,.55),0 0 0 1px rgba(0,0,0,.1);border-top:12px solid #8c1c2c;transform:rotate(-1.6deg)}}
.card .tag{{color:#8c1c2c;font-weight:700;font-size:22px;letter-spacing:.08em;margin-bottom:18px}}
.card .j{{font-style:italic;font-size:27px;color:#444;margin-bottom:22px;font-family:Georgia,serif}}
.card .t{{font-family:Georgia,'Times New Roman',serif;font-weight:700;font-size:43px;line-height:1.22;margin-bottom:26px}}
.card .a{{font-style:italic;font-size:27px;color:#333;font-family:Georgia,serif;margin-bottom:16px}}
.card .r{{font-size:22px;color:#777}}
.q{{position:absolute;left:90px;right:90px;top:1180px;text-align:center;font-size:36px;line-height:1.5;color:#b8c4d8;font-family:{SERIF};font-style:normal}}
.box{{position:absolute;left:90px;right:90px;top:1380px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.28);border-radius:20px;padding:34px 40px;text-align:center;font-size:44px;line-height:1.45;font-weight:700}}
.box b{{color:#c4a367}}
.hero{{position:absolute;left:0;right:0;top:640px;text-align:center}}
.hero h1{{font-family:{SERIF};font-weight:700;font-size:92px;line-height:1.25}}
.hero h1 em{{font-style:normal;color:#c4a367}}
.hero .l{{width:140px;height:3px;background:#c4a367;margin:46px auto}}
.hero p{{font-size:46px;color:#d5deec;line-height:1.5}}
.hero p.s{{font-size:36px;color:#c4a367;margin-top:20px}}
.ph{{position:absolute;left:50%;top:470px;width:380px;height:380px;margin-left:-190px;border-radius:50%;border:6px solid #c4a367;overflow:hidden}}
.ph img{{width:100%;height:100%;object-fit:cover}}
.nm{{position:absolute;top:900px;width:100%;text-align:center;font-family:Cor,serif;font-weight:700;font-size:92px}}
.sb{{position:absolute;top:1030px;width:100%;text-align:center;font-size:44px;color:#d5deec;font-family:{SERIF}}}
.web{{position:absolute;top:1160px;width:100%;text-align:center;font-size:42px;color:#c4a367;font-weight:600}}
.web2{{position:absolute;top:1230px;width:100%;text-align:center;font-size:36px;color:#d5deec}}
</style>'''

def slide(inner): return f'<!doctype html><meta charset="utf-8">{CSS}<body>{inner}</body>'
def sl_card(top, c, q, box=None):
    return slide(f'<div class="top">{html.escape(top)}</div>{c}<div class="q">«{html.escape(q)}»</div>' + (f'<div class="box">{box}</div>' if box else ''))
def sl_hero(h1, p, s=''):
    return slide(f'<div class="hero"><h1>{h1}</h1><div class="l"></div><p>{p}</p>' + (f'<p class="s">{s}</p>' if s else '') + '</div>')
def sl_out():
    return slide(f'<div class="ph"><img src="file://{FOTO}"></div><div class="nm">Dr. Julio De la Morena</div><div class="sb">运动医学与再生疗法</div><div class="web">drjuliodelamorena.com</div><div class="web2">@drjuliodelamorena</div>')

ESTUDIOS = {
 "belk": card("Am J Sports Med · 2021", "Platelet-Rich Plasma Versus Hyaluronic Acid for Knee Osteoarthritis: A Systematic Review and Meta-analysis of Randomized Controlled Trials", "Belk JW, Kraeutler MJ, Houck DA, Goodrich JA, Dragoo JL, et al.", "doi:10.1177/0363546520909397", "SYSTEMATIC REVIEW AND META-ANALYSIS"),
 "jawanda": card("Arthroscopy · 2024", "Platelet-Rich Plasma, Bone Marrow Aspirate Concentrate, and Hyaluronic Acid Injections Outperform Corticosteroids in Pain and Function Scores at a Minimum of 6 Months as Intra-Articular Injections for Knee Osteoarthritis", "Jawanda H, Khan ZA, Warrier AA, Acuña AJ, Allahabadi S, et al.", "doi:10.1016/j.arthro.2024.01.037", "SYSTEMATIC REVIEW"),
 "nouri": card("BMC Musculoskelet Disord · 2022", "Comparison between the effects of ultrasound guided intra-articular injections of platelet-rich plasma (PRP), high molecular weight hyaluronic acid, and their combination in hip osteoarthritis: a randomized clinical trial", "Nouri F, Babaee M, Peydayesh P, Esmaily H, Raeissadat SA.", "doi:10.1186/s12891-022-05787-8", "RANDOMIZED CLINICAL TRIAL"),
}
EV = [  # (clave de tarjeta, cabecera, cita, caja) por cada estudio de la lista de la web
 ("laver", "膝 · 1/7", "欧洲关于富血小板血浆治疗膝骨关节炎的共识", "欧洲共识：在经过筛选的<b>轻度和中度</b>骨关节炎中，PRP 是合适的"),
 ("li", "膝 · 2/7", "对于膝骨关节炎，PRP 比透明质酸更有效", "<b>15 项</b>双盲试验、<b>1632 名</b>患者：一年后疼痛更少，功能更好"),
 ("hamid", "肩 · 3/7", "富血小板血浆治疗肩袖肌腱病", "对肩痛和肩功能的结果良好，<b>长期安全性</b>无问题"),
 ("pei", "背 · 4/7", "富血小板血浆治疗下背痛", "<b>15 项</b>试验、<b>740 名</b>患者：六个月内疼痛和功能障碍更少"),
 ("fitz", "髋 · 5/7", "PRP 治疗臀肌肌腱病（髋外侧疼痛）的疗效", "明显改善：PRP <b>82 %</b>，皮质类固醇 <b>57 %</b>"),
 ("hohm", "肘 · 6/7", "网球肘：皮质类固醇起效更早，PRP 在六个月时效果更好", "皮质类固醇缓解更早；<b>3 个月和 6 个月</b>时 PRP 效果更好"),
 ("herb", "足 · 7/7", "PRP 与其他治疗足底筋膜炎方法的比较", "<b>21 项</b>试验：比皮质类固醇和安慰剂缓解更多疼痛"),
]
SCRIPT = {
 "prp-evidencia": [
  "PRP 有效吗？医学文献是这样说的。",
  "膝。欧洲共识认为，在经过筛选的轻度和中度骨关节炎中，PRP 是合适的。",
  "在膝骨关节炎中，多项研究显示，一年后与透明质酸相比，疼痛更少，功能更好。",
  "肩。在肩袖肌腱病中，已发表的结果是积极的，长期安全性方面没有问题。",
  "背。在下背痛中，六个月内疼痛更轻，功能障碍更少。",
  "髋。在臀肌肌腱病中，明显改善的比例为百分之八十二，而使用皮质类固醇为百分之五十七。",
  "网球肘。皮质类固醇缓解得更早，但六个月时 PRP 的效果更好。",
  "足。在足底筋膜炎中，一些研究显示，疼痛缓解比使用皮质类固醇或安慰剂更明显。",
  "结果因损伤和个人而异，PRP 并非对所有病例都适用。我们会评估它是否适合您的情况。",
  "胡里奥·德拉莫雷纳医生，马德里波苏埃洛。"],
 "prp-artrosis": [
  "PRP 治疗骨关节炎：三项显示有效的研究。",
  "膝。一项汇总十八项试验、共一千六百零八名患者的分析显示，PRP 使疼痛和功能改善约百分之四十五，而透明质酸约为百分之十三。",
  "同样是膝。四十八项研究、九千多个膝关节：六个月及以后，PRP 优于安慰剂和皮质类固醇。",
  "髋。在一项一百零五名患者的试验中，六个月时 PRP 优于透明质酸。这只是一项试验，还需要更多研究。",
  "一切取决于良好的诊断和恰当的适应证：先检查关节，再根据情况做超声或磁共振。",
  "胡里奥·德拉莫雷纳医生，马德里波苏埃洛。"]}

def evid_cards():
    import extras as X
    keys = {"laver": 0, "li": 1, "hamid": 2, "pei": 3, "fitz": 4, "hohm": 5, "herb": 6}
    out = {}
    for k, i in keys.items():
        a, t, c, d = X.EVID_REFS[i]
        out[k] = card(c.split(".")[0] + " · " + c.split(".")[1].strip().split(";")[0], t, a, "doi:" + d, "SYSTEMATIC REVIEW / TRIAL")
    return out

def slides(nombre):
    S = []   # lista de (html_A, html_B|None)
    if nombre == "prp-evidencia":
        C = evid_cards()
        S.append((sl_hero("PRP 有效吗？", "医学文献是这样说的", "（富血小板血浆）"), None))
        for k, top, q, box in EV: S.append((sl_card(top, C[k], q), sl_card(top, C[k], q, box)))
        S.append((sl_hero("PRP 并非<br><em>对所有人</em>都有效", "结果因损伤和个人而异", "我们会评估它是否适合您的情况"), None))
        S.append((sl_out(), None))
    else:
        S.append((sl_hero("PRP 治疗<em>骨关节炎</em>", "3 项研究", "依据医学文献"), None))
        e = ESTUDIOS
        S.append((sl_card("膝 · 1/3", e["belk"], "18 项试验，1608 名患者"), sl_card("膝 · 1/3", e["belk"], "18 项试验，1608 名患者", "PRP 改善疼痛和功能约 <b>45 %</b>，透明质酸约 <b>13 %</b>")))
        S.append((sl_card("膝 · 2/3", e["jawanda"], "48 项研究，9000 多个膝关节"), sl_card("膝 · 2/3", e["jawanda"], "48 项研究，9000 多个膝关节", "六个月及以后：PRP 优于<b>安慰剂和皮质类固醇</b>")))
        S.append((sl_card("髋 · 3/3", e["nouri"], "105 名患者的随机临床试验"), sl_card("髋 · 3/3", e["nouri"], "105 名患者的随机临床试验", "六个月时 PRP 优于透明质酸（仅一项试验，需要更多研究）")))
        S.append((sl_hero("一切取决于<em>良好的诊断</em>", "先检查关节，再根据情况做<br>超声或磁共振", "和恰当的适应证"), None))
        S.append((sl_out(), None))
    return S

def tts(txt, out):
    if os.path.exists(out): return
    body = json.dumps({"text": txt, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0, "use_speaker_boost": True, "speed": 1.1}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128", data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    open(out, "wb").write(urllib.request.urlopen(req, timeout=120).read())

def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True).stdout
def dur(f): return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f))

def main(nombre):
    from playwright.sync_api import sync_playwright
    w = os.path.join(D, "work", nombre); os.makedirs(w, exist_ok=True)
    sc = SCRIPT[nombre]; S = slides(nombre); assert len(sc) == len(S), (len(sc), len(S))
    # voz
    d = []
    for i, t in enumerate(sc):
        mp = f"{w}/v{i}.mp3"; tts(t, mp)
        sh("ffmpeg", "-v", "error", "-y", "-i", mp, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse", "-ar", "44100", "-ac", "1", f"{w}/v{i}.wav")
        d.append(dur(f"{w}/v{i}.wav"))
    # captura de diapositivas
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for i, (a, bb) in enumerate(S):
            for tag, h in (("a", a), ("b", bb)):
                if h is None: continue
                open(f"{w}/s{i}{tag}.html", "w", encoding="utf-8").write(h)
                pg.goto(f"file://{w}/s{i}{tag}.html"); pg.wait_for_timeout(250); pg.screenshot(path=f"{w}/s{i}{tag}.png")
        b.close()
    # línea de tiempo
    GAP, LEAD = 0.45, 0.25
    segs, t, voz_in = [], 0.0, []
    for i, (a, bb) in enumerate(S):
        dd = d[i] + GAP + (LEAD if i == 0 else 0)
        voz_in.append((t + (LEAD if i == 0 else 0), f"{w}/v{i}.wav"))
        reveal = min(1.6, dd * 0.4) if bb else None
        segs.append((i, t, dd, reveal)); t += dd
    total = t + 2.2   # cierre sin voz
    # vídeo: un clip por estado
    clips = []
    for (i, t0, dd, rev) in segs:
        for tag, ini, fin in (("a", 0, rev if rev else dd), ("b", rev, dd)):
            if tag == "b" and not rev: continue
            n = round((fin - ini) * FPS)
            if n <= 0: continue
            c = f"{w}/c{i}{tag}.mp4"
            fade = "" if True else ""
            vf = f"scale=1080:1920,zoompan=z='1+0.00025*on':d={n}:s=1080x1920:fps={FPS}"
            if tag == "a": vf += f",fade=t=in:st=0:d=0.25"
            sh("ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{w}/s{i}{tag}.png", "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", c)
            clips.append(c)
    open(f"{w}/list.txt", "w").write("".join(f"file '{c}'\n" for c in clips))
    mudo = f"{w}/mudo.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{w}/list.txt", "-c", "copy", mudo)
    vid_dur = dur(mudo)
    # audio
    args = ["ffmpeg", "-v", "error", "-y"]
    for _, f in voz_in: args += ["-i", f]
    filt = "".join(f"[{k}]adelay={int(tt*1000)}:all=1[a{k}];" for k, (tt, _) in enumerate(voz_in))
    filt += "".join(f"[a{k}]" for k in range(len(voz_in))) + f"amix=inputs={len(voz_in)}:normalize=0,apad=whole_dur={vid_dur}[v]"
    sh(*args, "-filter_complex", filt, "-map", "[v]", "-ar", "44100", "-ac", "1", f"{w}/voz.wav")
    sh("ffmpeg", "-v", "error", "-y", "-i", f"{w}/voz.wav", "-stream_loop", "-1", "-i", os.path.join(V, "sonidos", "musica_larga.wav"), "-filter_complex",
       f"[1]atrim=0:{vid_dur},volume=0.16[m];[m][0]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5[o]", "-map", "[o]", "-ar", "44100", "-ac", "2", f"{w}/audio.wav")
    # subtítulos suaves (VTT): una frase por bloque, partida por la puntuación, repartida según la duración de la voz
    import re
    def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{x%60:06.3f}"
    cues = []
    for (tt, _), txt, dd in zip(voz_in, sc, d):
        partes = [q for q in re.findall(r"[^，。：；？]+[，。：；？]?", txt) if q.strip()]
        m = []
        for q in partes:
            if m and len(m[-1].strip("，。：；？ ")) < 4: m[-1] += q
            else: m.append(q)
        partes = m; n = sum(len(q) for q in partes); x = tt
        for q in partes:
            dq = dd * len(q) / n; cues.append((x, x + dq, q.strip("，。：；？ ")))
            x += dq
    vtt = "WEBVTT\n\n" + "\n\n".join(f"{ts(a)} --> {ts(b)}\n{q}" for a, b, q in cues) + "\n"
    sd = os.path.join(V, "..", "i18n_extra", "zh", "subs"); os.makedirs(sd, exist_ok=True)
    open(os.path.join(sd, nombre + ".vtt"), "w", encoding="utf-8").write(vtt)
    out = os.path.join(D, "out"); os.makedirs(out, exist_ok=True)
    f = f"{out}/{nombre}.zh.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-i", mudo, "-i", f"{w}/audio.wav", "-vf", "scale=720:1280", "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", f)
    sh("ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", f, "-frames:v", "1", f"{out}/{nombre}.zh.jpg")
    print(f, round(dur(f), 1), "s; voz", [round(x, 1) for x in d])

if __name__ == "__main__": main(sys.argv[1])
