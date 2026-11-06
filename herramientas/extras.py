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


# --- Llamada a la cita adaptada al tema de cada artículo y nota de consulta privada (3 nov 2026) ---
CIERRE = {"es": "Pida cita con el Dr. De la Morena.", "en": "Book an appointment with Dr De la Morena.",
          "fr": "Prenez rendez-vous avec le Dr De la Morena.", "ru": "Запишитесь на прием к доктору де ла Морена.",
          "ka": "ჩაეწერეთ ექიმ დე ლა მორენასთან."}
ART_CTA = {
 "esguince-tobillo-sigue-fallando": {"es": "¿Su tobillo sigue fallando después de un esguince?", "en": "Does your ankle keep giving way after a sprain?",
    "fr": "Votre cheville lâche encore après une entorse ?", "ru": "Голеностоп продолжает подворачиваться после растяжения?", "ka": "ღრძობის შემდეგ კოჭი ისევ გიცდებათ?"},
 "factores-crecimiento-evidencia": {"es": "¿Quiere saber si el PRP es una opción en su caso?", "en": "Would you like to know whether PRP is an option for you?",
    "fr": "Vous voulez savoir si le PRP est une option dans votre cas ?", "ru": "Хотите узнать, подходит ли Вам PRP?", "ka": "გსურთ გაიგოთ, შეესაბამება თუ არა PRP თქვენს შემთხვევას?"},
 "tendinitis-cronica-cuando-no-se-cura-sola": {"es": "¿Lleva meses con una tendinitis que no se cura?", "en": "Have you had tendinitis for months that will not heal?",
    "fr": "Une tendinite qui ne guérit pas depuis des mois ?", "ru": "Тендинит не проходит уже несколько месяцев?", "ka": "ტენდინიტი თვეების განმავლობაში არ გიქრებათ?"},
 "terapias-regenerativas-que-son": {"es": "¿Quiere saber si una terapia regenerativa puede ayudarle?", "en": "Would you like to know whether a regenerative therapy could help you?",
    "fr": "Vous voulez savoir si une thérapie régénérative peut vous aider ?", "ru": "Хотите узнать, может ли Вам помочь регенеративная терапия?", "ka": "გსურთ გაიგოთ, დაგეხმარებათ თუ არა რეგენერაციული თერაპია?"},
 "ciatica-dolor-espalda-baja-pierna": {"es": "¿Le baja el dolor de la espalda a la pierna?", "en": "Does your back pain run down your leg?",
    "fr": "Votre douleur de dos descend-elle dans la jambe ?", "ru": "Боль в спине отдает в ногу?", "ka": "ზურგის ტკივილი ფეხში გადადის?"},
 "lumbalgia-5-cosas": {"es": "¿Lleva tiempo con dolor lumbar o le baja a la pierna?", "en": "Have you had low back pain for a while, or pain running down your leg?",
    "fr": "Mal de dos depuis un moment, ou une douleur qui descend dans la jambe ?", "ru": "Давно болит поясница или боль отдает в ногу?", "ka": "დიდი ხანია წელი გტკივათ ან ტკივილი ფეხში გადადის?"},
}
PRIVADA = {"es": "Consulta privada, sin intermediarios: tiempo y atención para su caso.",
           "en": "Private practice, no insurers in between: time and attention for your case.",
           "fr": "Consultation privée, sans intermédiaire : du temps et de l'attention pour votre cas.",
           "ru": "Частный прием без посредников: время и внимание Вашему случаю.",
           "ka": "კერძო მიღება, შუამავლების გარეშე: დრო და ყურადღება თქვენს შემთხვევას."}

def art_cta(lang, slug, default):
    q = ART_CTA.get(slug, {}).get(lang)
    return f"{q} {CIERRE[lang]}" if q else default

def privada_html(lang):
    return f'<p class="privada">{esc(PRIVADA[lang])}</p>'


# --- Vídeo "El PRP en la literatura médica": siete estudios reales, una versión por idioma (3 nov 2026) ---
EVID_SLUGS = {"factores-crecimiento-autologos", "factores-crecimiento-evidencia"}
EVID_REFS = [
 ("Laver L, Filardo G, Sanchez M, et al.", "The use of injectable orthobiologics for knee osteoarthritis: A European ESSKA-ORBIT consensus. Part 1-Blood-derived products (platelet-rich plasma).", "Knee Surg Sports Traumatol Arthrosc. 2024;32(4):783-797", "10.1002/ksa.12077"),
 ("Li YF, Xing HH, Wei CK, et al.", "Platelet-Rich Plasma Is More Effective Than Hyaluronic Acid Injections for Osteoarthritis of the Knee: A Meta-analysis Based on Randomized, Double-Blinded, Controlled Clinical Trials.", "Arthroscopy. 2025;41(12):5304-5318", "10.1016/j.arthro.2025.06.033"),
 ("A Hamid MS, Sazlina SG.", "Platelet-rich plasma for rotator cuff tendinopathy: A systematic review and meta-analysis.", "PLoS One. 2021;16(5):e0251111", "10.1371/journal.pone.0251111"),
 ("Pei X, Liu C, Wang J, et al.", "Platelet-rich plasma therapy for low back pain: A comprehensive systematic review and meta-analysis.", "J Back Musculoskelet Rehabil. 2026;39(6):1830-1844", "10.1177/10538127261448983"),
 ("Fitzpatrick J, Bulsara MK, O'Donnell J, et al.", "The Effectiveness of Platelet-Rich Plasma Injections in Gluteal Tendinopathy: A Randomized, Double-Blind Controlled Trial Comparing a Single Platelet-Rich Plasma Injection With a Single Corticosteroid Injection.", "Am J Sports Med. 2018;46(4):933-939", "10.1177/0363546517745525"),
 ("Hohmann E, Tetsworth K, Glatt V.", "Corticosteroid injections for the treatment of lateral epicondylitis are superior to platelet-rich plasma at 1 month but platelet-rich plasma is more effective at 6 months: an updated systematic review and meta-analysis of level 1 and 2 studies.", "J Shoulder Elbow Surg. 2023;32(9):1770-1783", "10.1016/j.jse.2023.04.018"),
 ("Herber A, Covarrubias O, Daher M, et al.", "Platelet rich plasma therapy versus other modalities for treatment of plantar fasciitis: A systematic review and meta-analysis.", "Foot Ankle Surg. 2024;30(4):285-293", "10.1016/j.fas.2024.02.004"),
]
EVID_TXT = {
 "es": ("Qué dice la literatura médica sobre el PRP", "Siete estudios publicados sobre el PRP (plasma rico en plaquetas) en rodilla, hombro, espalda, cadera, codo y pie.", "Los siete estudios del vídeo (fuente: PubMed)"),
 "en": ("What the medical literature says about PRP", "Seven published studies on PRP (platelet-rich plasma) for the knee, shoulder, lower back, hip, elbow and foot.", "The seven studies in the video (source: PubMed)"),
 "fr": ("Ce que dit la littérature médicale sur le PRP", "Sept études publiées sur le PRP (plasma riche en plaquettes) pour le genou, l'épaule, le dos, la hanche, le coude et le pied.", "Les sept études de la vidéo (source : PubMed)"),
 "ru": ("Что говорит медицинская литература о PRP", "Семь опубликованных исследований PRP (плазмы, обогащённой тромбоцитами) при болях в колене, плече, пояснице, бедре, локте и стопе.", "Семь исследований из видео (источник: PubMed)"),
 "ka": ("რას ამბობს სამედიცინო ლიტერატურა PRP-ზე", "შვიდი გამოქვეყნებული კვლევა PRP-ზე (თრომბოციტებით მდიდარი პლაზმა): მუხლი, მხარი, წელი, თეძო, იდაყვი და ტერფი.", "ვიდეოში ნაჩვენები შვიდი კვლევა (წყარო: PubMed)"),
}

def evidencia_html(lang, slug):
    if slug not in EVID_SLUGS or lang not in EVID_TXT: return ""
    h2, cap, lista = EVID_TXT[lang]; n = f"prp-evidencia.{lang}"
    refs = "".join(f'<li>{esc(a)} {esc(t)} <em>{esc(c)}</em>. <a href="https://doi.org/{d}" rel="noopener" target="_blank">doi:{d}</a></li>' for a, t, c, d in EVID_REFS)
    ld = {"@context": "https://schema.org", "@type": "VideoObject", "name": h2, "description": cap,
          "thumbnailUrl": f"{SITE}/video/{n}.jpg", "uploadDate": "2026-11-03T03:00:00+01:00", "duration": "PT60S",
          "contentUrl": f"{SITE}/video/{n}.mp4", "inLanguage": lang}
    return (f'<h2>{esc(h2)}</h2>\n<figure class="reel"><video controls playsinline preload="none" poster="/video/{n}.jpg" width="720" height="1280">'
            f'<source src="/video/{n}.mp4" type="video/mp4"></video><figcaption>{esc(cap)}</figcaption></figure>\n'
            f'<details class="refs"><summary>{esc(lista)}</summary><ol>{refs}</ol></details>\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
