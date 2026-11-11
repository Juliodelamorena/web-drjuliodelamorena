"""Dobla los vídeos de la web al georgiano con la voz clonada de Julio (ElevenLabs).
Uso: python3 doblar.py <video> [modelo]"""
import json, os, subprocess, sys, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
WEB = "/home/claude/web-drjuliodelamorena/video"
KEY = open(os.path.join(D, ".key")).read().strip()
VOZ = "FMUNJCsKXSdEGNKTCd7w"

GUIONES_KA = {
    "codo-de-padel": {"fondo": "ambiente", "frases": [
        (1.9, "გტკივათ იდაყვი პადელის თამაშის შემდეგ?"),
        (4.65, "ეს წინამხრის მყესების გადატვირთვაა და მხოლოდ მოსვენებით არ იკურნება."),
        (10.0, "ჯერ იდაყვს ვსინჯავ და ულტრაბგერით ვიკვლევ, რომ მყესები დავინახო."),
        (15.0, "შემდეგ — ვარჯიში, ჩოგნისა და ტექნიკის შემოწმება."),
        (19.8, "თუ არ უმჯობესდება — აუტოლოგიური ზრდის ფაქტორები ულტრაბგერითი კონტროლით: რასაც პი-არ-პის უწოდებენ."),
        (26.2, "ჩაეწერეთ ჩემთან შესაფასებლად, პოსუელოში, მადრიდში."),
    ]},
    "terapias-regenerativas": {"fondo": "ambiente", "frases": [
        (0.0, "თვეებია, მუხლი გტკივათ და უკვე პროთეზზე გელაპარაკებიან?"),
        (4.95, "ხშირ შემთხვევაში არსებობს წინა ნაბიჯი."),
        (8.0, "პი-არ-პი: თრომბოციტებით მდიდარი პლაზმა."),
        (10.4, "აუტოლოგიური ზრდის ფაქტორები, რომლებიც თქვენივე სისხლიდან მიიღება."),
        (15.7, "ყოველთვის ულტრაბგერითი კონტროლით, ინტერვენციულ რადიოლოგთან ერთად და სავარჯიშო გეგმით."),
        (24.4, "ჩაეწერეთ შესაფასებლად ექიმ ხულიო დე ლა მორენასთან, საავადმყოფო მემორიალ პუბლიო კორდონში, პოსუელოში, მადრიდში."),
    ]},
    "unidad": {"fondo": "musica", "frases": [
        (0.3, "ეს ჩემი კაბინეტია — საავადმყოფო მემორიალ პუბლიო კორდონი, პოსუელოში, მადრიდში."),
        (4.2, "ახალი საავადმყოფო, თქვენი კომფორტისთვის შექმნილი."),
        (8.1, "ფართო და მშვიდი სივრცეები."),
        (12.0, "რეგენერაციული თერაპიისა და სპორტული მედიცინის განყოფილება."),
        (15.3, "აქ მოგისმენთ, გაგსინჯავთ და აგიხსნით, რა გჭირთ."),
        (19.9, "ულტრაბგერა იმავე ვიზიტზე, დამატებითი ჩაწერის გარეშე."),
        (23.5, "ულტრაბგერით მართული მკურნალობა, ზუსტად საჭირო წერტილში."),
        (26.8, "ექიმი ხულიო დე ლა მორენა — თოთხმეტი წელი რეალ მადრიდის სამედიცინო სამსახურში."),
    ]},
}


GUIONES_ZH = {
    "codo-de-padel": {"fondo": "musica", "frases": [
        (1.9, "打帕德尔之后，肘部疼吗？"),
        (4.65, "这是前臂肌腱的过度负荷，仅靠休息治不好。"),
        (10.0, "我先检查肘部，并做超声，观察肌腱。"),
        (15.0, "然后是运动，检查球拍和技术。"),
        (19.8, "如果没有改善，就用自体生长因子，在超声引导下进行：也就是所谓的富血小板血浆。"),
        (26.2, "请到马德里波苏埃洛，向我预约评估。"),
    ]},
    "terapias-regenerativas": {"fondo": "musica", "frases": [
        (0.0, "膝盖疼了几个月，就已经在谈关节置换了吗？"),
        (4.95, "在许多情况下，之前还有一步。"),
        (8.0, "富血小板血浆。"),
        (10.4, "自体生长因子，取自您自己的血液。"),
        (15.7, "始终在超声引导下，与介入放射科医生共同完成，并配合运动方案。"),
        (24.4, "请向胡里奥·德拉莫雷纳医生预约评估，地点是马德里波苏埃洛的 Memorial Publio Cordón 医院。"),
    ]},
    "unidad": {"fondo": "musica", "frases": [
        (0.3, "这是我的门诊：马德里波苏埃洛的 Memorial Publio Cordón 医院。"),
        (4.2, "全新的医院，以您的舒适为设计出发点。"),
        (8.1, "宽敞、安静的空间。"),
        (12.0, "再生疗法与运动医学科。"),
        (15.3, "在这里，我倾听、检查，并向您解释发生了什么。"),
        (19.9, "同一次就诊中完成超声，无需另约时间。"),
        (23.5, "超声引导治疗，精准到达需要治疗的部位。"),
        (26.8, "胡里奥·德拉莫雷纳医生，曾在皇家马德里医疗团队工作十四年。"),
    ]},
}

from guiones import GUIONES
GUIONES["zh"] = GUIONES_ZH
GUIONES["ka"] = {**GUIONES_KA, **GUIONES.get("ka", {})}
MODELO = {"ka": "eleven_v3"}

def sh(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True).stdout

def dur(f):
    return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f))

def tts(texto, out, modelo, lang):
    if os.path.exists(out):
        return
    p = {"text": texto, "model_id": modelo, "voice_settings": {"stability": 0.5, "similarity_boost": 0.85}}
    if modelo == "eleven_v3": p["language_code"] = lang.split("_")[0]
    body = json.dumps(p).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128",
                                 data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(out, "wb").write(r.read())

def main(nombre, lang="ka"):
    modelo = MODELO.get(lang, "eleven_multilingual_v2")
    g = GUIONES[lang][nombre]
    w = os.path.join(D, "work", nombre, lang); os.makedirs(w, exist_ok=True)
    if lang == "es_ig": video = os.path.join(WEB, nombre + "-1080.mp4")
    else: video = os.path.join(D, "orig_prp", f"{nombre}.{lang}.mp4") if nombre == "prp-evidencia" else os.path.join(WEB, nombre + ".mp4")
    total = dur(video)
    frases = g["frases"]
    piezas, t_fin = [], 0.0
    for i, (ini, txt) in enumerate(frases):
        raw = os.path.join(w, f"{i:02d}.mp3"); tts(txt, raw, modelo, lang)
        # recorta silencios de los extremos
        lim = os.path.join(w, f"{i:02d}.wav")
        sh("ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
           "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
           "-ar", "44100", "-ac", "1", lim)
        d = dur(lim)
        inicio = max(ini, t_fin + 0.15)
        siguiente = frases[i + 1][0] if i + 1 < len(frases) else total - 0.4
        hueco = siguiente - inicio - 0.1
        tempo = 1.0
        if d > hueco:
            tempo = min(1.15, d / max(hueco, 0.1))
        if tempo > 1.001:
            fit = os.path.join(w, f"{i:02d}_t.wav")
            sh("ffmpeg", "-v", "error", "-y", "-i", lim, "-af", f"atempo={tempo:.4f}", fit); lim = fit; d = dur(lim)
        piezas.append((inicio, lim)); t_fin = inicio + d
        print(f"{i}: inicio {inicio:.2f} dura {d:.2f} hueco {hueco:.2f} tempo {tempo:.3f}")
    fin = max(total, t_fin + 0.8)
    # voz completa
    args = ["ffmpeg", "-v", "error", "-y"]
    for _, f in piezas: args += ["-i", f]
    filt = "".join(f"[{k}]adelay={int(t*1000)}:all=1[a{k}];" for k, (t, _) in enumerate(piezas))
    filt += "".join(f"[a{k}]" for k in range(len(piezas))) + f"amix=inputs={len(piezas)}:normalize=0,apad=whole_dur={fin}[v]"
    voz = os.path.join(w, "voz.wav")
    sh(*args, "-filter_complex", filt, "-map", "[v]", "-ar", "44100", "-ac", "1", voz)
    fondo = os.path.join(D, f"musica_prp_{lang}.wav") if nombre == "prp-evidencia" else os.path.join(D, "sep/htdemucs", nombre, "no_vocals.wav")
    if not os.path.exists(fondo):
        fondo = os.path.join(D, "sonidos", "musica_larga.wav"); g = {**g, "fondo": "musica"}
    if g["fondo"] == "musica":
        mezcla = (f"[1]apad=whole_dur={fin},volume=0.32[m];[0]volume=1.0[v];[m][v]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
                  f"[md][0]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[out]")
    else:
        mezcla = f"[1]apad=whole_dur={fin},volume=1.0[m];[m][0]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[out]"
    audio = os.path.join(w, "audio.wav")
    sh("ffmpeg", "-v", "error", "-y", "-i", voz, "-i", fondo, "-filter_complex", mezcla, "-map", "[out]", "-ar", "44100", "-ac", "2", audio)
    out = os.path.join(D, "out", f"{nombre}.{lang}.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    vf = [] if fin <= total + 0.01 else ["-vf", f"tpad=stop_mode=clone:stop_duration={fin - total + 0.05:.2f}"]
    sh("ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", *vf,
       "-c:v", "libx264" if vf else "copy", *(["-preset", "veryfast", "-crf", "20"] if vf else []),
       "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out)
    print(out, f"{dur(out):.2f}s (original {total:.2f}s)")

if __name__ == "__main__":
    main(*sys.argv[1:])
