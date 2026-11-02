"""Contenido traducido fuera de los paquetes de páginas: textos de interfaz del blog y los planes,
galería del doctor, aviso legal y privacidad, y los vídeos (reels) con subtítulos por idioma.
Las traducciones viven en herramientas/i18n_extra/<idioma>/ (es = original)."""
import json, os, html
import idiomas as I

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n_extra")
SITE = I.SITE
esc = lambda s: html.escape(s, quote=True)

def _load(lang, name):
    for l in (lang, "es"):
        f = os.path.join(DIR, l, name)
        if os.path.isfile(f):
            return json.load(open(f, encoding="utf-8"))
    return {}

def ui(lang): return _load(lang, "ui.json")
def galeria(lang): return _load(lang, "galeria.json")
def legal(lang): return _load(lang, "legal.json")

SUBS_LANGS = ["es", "en", "ka", "ru", "fr"]
REELS = {  # slug español de la página -> vídeo
 "factores-crecimiento-autologos": {"file": "terapias-regenerativas", "date": "2026-11-01T22:00:00+01:00", "dur": "PT35S", "cap": "video_caption_factores"},
 "codo-de-tenista": {"file": "codo-de-padel", "date": "2026-11-01T23:40:00+01:00", "dur": "PT33S", "cap": "video_caption_codo"},
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _tracks(lang, name):
    out = []
    for l in SUBS_LANGS:
        if os.path.isfile(os.path.join(ROOT, "video", "subs", f"{name}.{l}.vtt")):
            d = " default" if l == lang else ""
            out.append(f'<track kind="subtitles" src="/video/subs/{name}.{l}.vtt" srclang="{l}" label="{I.NAMES[l]}"{d}>')
    if not any(" default" in t for t in out) and out:
        out[0] = out[0].replace(">", " default>", 1)
    return "".join(out)

def reel_html(lang, es_slug):
    r = REELS[es_slug]; n = r["file"]; u = ui(lang)
    return (f'<figure class="reel"><video controls playsinline preload="none" crossorigin="anonymous" poster="/video/{n}.jpg" width="720" height="1280">'
            f'<source src="/video/{n}.mp4" type="video/mp4">{_tracks(lang, n)}</video>'
            f'<figcaption>{esc(u.get(r["cap"], ""))}</figcaption></figure>')

def reel_ld(lang, es_slug, name, desc):
    r = REELS[es_slug]; n = r["file"]
    return {"@type": "VideoObject", "name": name, "description": desc, "thumbnailUrl": f"{SITE}/video/{n}.jpg",
            "uploadDate": r["date"], "duration": r["dur"], "contentUrl": f"{SITE}/video/{n}.mp4", "inLanguage": "es"}

def galeria_html(lang):
    g = galeria(lang)
    if not g: return ""
    figs = "".join(f'<figure><img src="/img/rm/{f}" alt="{esc(a)}" width="800" height="1000" loading="lazy"><figcaption>{esc(c)}</figcaption></figure>' for f, a, c in g["fotos"])
    return f'<h2>{esc(g["titulo"])}</h2>\n<div class="galeria">{figs}</div>\n'


# --- La consulta por dentro: vídeo-recorrido de la unidad y fotos reales (portadas de los cinco idiomas) ---
def unidad(lang): return _load(lang, "unidad.json")

def unidad_video_html(lang):
    u = unidad(lang)
    return (f'<figure class="reel"><video controls playsinline preload="none" crossorigin="anonymous" poster="/video/unidad.jpg" width="720" height="1280">'
            f'<source src="/video/unidad.mp4" type="video/mp4">{_tracks(lang, "unidad")}</video>'
            f'<figcaption>{esc(u.get("caption", ""))}</figcaption></figure>')

def unidad_fotos_html(lang):
    u = unidad(lang)
    figs = "".join(f'<figure><picture><source srcset="/img/unidad/{f}.webp" type="image/webp"><img src="/img/unidad/{f}.jpg" alt="{esc(a)}" width="800" height="1000" loading="lazy"></picture><figcaption>{esc(c)}</figcaption></figure>' for f, a, c in u["fotos"])
    ld = {"@context": "https://schema.org", "@type": "VideoObject", "name": u["caption"], "description": u["caption"],
          "thumbnailUrl": f"{SITE}/video/unidad.jpg", "uploadDate": "2026-11-02T14:00:00+01:00", "duration": "PT34S",
          "contentUrl": f"{SITE}/video/unidad.mp4", "inLanguage": lang}
    return (f'<div class="wrap unidad"><h3 class="h3">{esc(u["titulo"])}</h3><div class="galeria">{figs}</div></div>\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
