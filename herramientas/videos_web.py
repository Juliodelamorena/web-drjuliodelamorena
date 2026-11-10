"""Apartado /videos/ de la web (es, en, fr, ru, ka).

Para añadir un vídeo: poner los archivos en /video/ (<nombre>.<idioma>.mp4 y .jpg de portada;
<nombre>.jpg si el cartel es único), añadir una entrada a CATALOGO y regenerar (articulos.py lo llama).
"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as G
import idiomas as I

SITE, ROOT, esc = G.SITE, G.ROOT, html.escape
LANGS = ["es", "en", "fr", "ru", "ka"]

# art: ruta relativa (sin idioma) de la página que amplía el vídeo; vacío = portada
CATALOGO = [
 dict(f="osgood-schlatter", art="blog/osgood-schlatter-diagnostico-tratamiento.html", poster="{f}.{l}.jpg", dur="PT31S", fecha="2026-11-14T10:00:00+01:00",
      t=dict(es="Osgood-Schlatter: diagnóstico y tratamiento", en="Osgood-Schlatter: diagnosis and treatment", fr="Osgood-Schlatter : diagnostic et traitement",
             ru="Осгуд — Шлаттер: диагностика и лечение", ka="ოსგუდ-შლატერი: დიაგნოსტიკა და მკურნალობა")),
 dict(f="prp-artrosis", art="blog/prp-artrosis-tres-estudios.html", poster="{f}.{l}.jpg", dur="PT46S", fecha="2026-11-10T10:00:00+01:00",
      t=dict(es="PRP en la artrosis: tres estudios donde sí funciona", en="PRP for osteoarthritis: three studies where it works", fr="Le PRP dans l'arthrose : trois études où il fonctionne",
             ru="PRP при артрозе: три исследования, где он работает", ka="PRP ართროზის დროს: სამი კვლევა, სადაც ის მოქმედებს")),
 dict(f="prp-evidencia", art="blog/factores-crecimiento-evidencia.html", poster="{f}.{l}.jpg", dur="PT60S", fecha="2026-11-03T03:00:00+01:00",
      t=dict(es="Qué dice la literatura médica sobre el PRP", en="What the medical literature says about PRP", fr="Ce que dit la littérature médicale sur le PRP",
             ru="Что говорит медицинская литература о PRP", ka="რას ამბობს სამედიცინო ლიტერატურა PRP-ზე")),
 dict(f="unidad", es_file="unidad.es.mp4", art="", poster="{f}.jpg", dur="PT34S", fecha="2026-11-02T14:00:00+01:00",
      t=dict(es="Recorrido por la unidad en el Hospital Memorial Publio Cordón (Pozuelo, Madrid)", en="A walk through the unit at Hospital Memorial Publio Cordón (Pozuelo, Madrid)",
             fr="Visite de l'unité à l'Hôpital Memorial Publio Cordón (Pozuelo, Madrid)", ru="Прогулка по отделению в больнице Memorial Publio Cordón (Посуэло, Мадрид)",
             ka="განყოფილების დათვალიერება საავადმყოფო Memorial Publio Cordón-ში (პოსუელო, მადრიდი)")),
 dict(f="terapias-regenerativas", es_file="terapias-regenerativas.mp4", art="factores-crecimiento-autologos", poster="{f}.jpg", dur="PT35S", fecha="2026-11-01T22:00:00+01:00",
      t=dict(es="PRP (plasma rico en plaquetas) con el Dr. Julio De la Morena", en="PRP (platelet-rich plasma)", fr="PRP (plasma riche en plaquettes)",
             ru="PRP (плазма, обогащённая тромбоцитами)", ka="PRP (თრომბოციტებით მდიდარი პლაზმა)")),
 dict(f="codo-de-padel", es_file="codo-de-padel.mp4", art="codo-de-tenista", poster="{f}.jpg", dur="PT33S", fecha="2026-11-01T23:40:00+01:00",
      t=dict(es="Codo de pádel: exploración, ecografía y tratamiento", en="Tennis and padel elbow (lateral epicondylitis)", fr="Coude du tennisman et du joueur de padel (épicondylite latérale)",
             ru="Локоть теннисиста и паделиста (латеральный эпикондилит)", ka="ჩოგბურთელისა და პადელის მოთამაშის იდაყვი (ლატერალური ეპიკონდილიტი)")),
]

UI = {
 "es": dict(h1="Vídeos del Dr. Julio De la Morena", lead="Vídeos breves sobre lesiones, infiltraciones y terapias regenerativas, con los estudios en los que se basan.",
            title="Vídeos · Dr. Julio De la Morena", desc="Vídeos del Dr. Julio De la Morena sobre lesiones, infiltraciones ecoguiadas y terapias regenerativas, con los estudios en los que se basan.", art="Leer el artículo", more="Más información", home="Inicio"),
 "en": dict(h1="Videos by Dr Julio De la Morena", lead="Short videos on injuries, injections and regenerative therapies, with the studies they are based on.",
            title="Videos · Dr Julio De la Morena", desc="Videos by Dr Julio De la Morena on injuries, ultrasound-guided injections and regenerative therapies, with the studies they are based on.", art="Read the article", more="More information", home="Home"),
 "fr": dict(h1="Vidéos du Dr Julio De la Morena", lead="Courtes vidéos sur les blessures, les infiltrations et les thérapies régénératives, avec les études sur lesquelles elles reposent.",
            title="Vidéos · Dr Julio De la Morena", desc="Vidéos du Dr Julio De la Morena sur les blessures, les infiltrations échoguidées et les thérapies régénératives, avec les études sur lesquelles elles reposent.", art="Lire l'article", more="En savoir plus", home="Accueil"),
 "ru": dict(h1="Видео доктора Хулио де ла Морена", lead="Короткие видео о травмах, инъекциях и регенеративной терапии, с исследованиями, на которых они основаны.",
            title="Видео · Д-р Хулио де ла Морена", desc="Видео доктора Хулио де ла Морена о травмах, инъекциях под контролем УЗИ и регенеративной терапии, с исследованиями, на которых они основаны.", art="Читать статью", more="Подробнее", home="Главная"),
 "ka": dict(h1="ექიმ ხულიო დე ლა მორენას ვიდეოები", lead="მოკლე ვიდეოები ტრავმებზე, ინექციებზე და რეგენერაციულ თერაპიაზე, იმ კვლევებთან ერთად, რომლებსაც ეყრდნობა.",
            title="ვიდეოები · ექიმი ხულიო დე ლა მორენა", desc="ექიმ ხულიო დე ლა მორენას ვიდეოები ტრავმებზე, ექოგრაფიით კონტროლირებად ინექციებზე და რეგენერაციულ თერაპიაზე, იმ კვლევებთან ერთად, რომლებსაც ეყრდნობა.", art="სტატიის წაკითხვა", more="დაწვრილებით", home="მთავარი"),
}


def _poster(v, l): return "/video/" + v["poster"].format(f=v["f"], l=l)
N = {"es": "Español", "en": "English", "fr": "Français", "ru": "Русский", "ka": "ქართული"}
def _src(v, l):
    if l == "es" and v.get("es_file"): return "/video/" + v["es_file"]
    return f"/video/{v['f']}.{l}.mp4"


def _disponible(v, l):
    return os.path.isfile(os.path.join(ROOT, _src(v, l).lstrip("/")))


def pagina(l):
    u = UI[l]; base = "/" if l == "es" else f"/{l}/"
    vs = [v for v in CATALOGO if _disponible(v, l)]
    url = f"{SITE}{base}videos/"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url, "url": url, "name": u["title"], "inLanguage": l,
          "author": G.DOCTOR_REF,
          "hasPart": [{"@type": "VideoObject", "name": v["t"][l], "description": v["t"][l], "thumbnailUrl": SITE + _poster(v, l),
                       "uploadDate": v["fecha"], "duration": v["dur"], "contentUrl": SITE + _src(v, l), "inLanguage": l} for v in vs]}
    cards = []
    for v in vs:
        href = (I.path_for(l, v["art"]) or base) if v["art"] else base
        txt = u["art"] if v["art"] else u["more"]
        tracks = "".join(f'<track kind="subtitles" src="/video/subs/{v["f"]}.{c}.vtt" srclang="{c}" label="{N[c]}"{" default" if c == l else ""}>'
                         for c in LANGS if os.path.isfile(os.path.join(ROOT, "video", "subs", f"{v['f']}.{c}.vtt")))
        cards.append(f'<div class="vcard"><figure class="reel"><video controls playsinline preload="none" poster="{_poster(v, l)}" width="720" height="1280">'
                     f'<source src="{_src(v, l)}" type="video/mp4">{tracks}</video></figure>'
                     f'<h3>{esc(v["t"][l])}</h3><a href="{href}">{esc(txt)} →</a></div>')
    body = f'''<main class="block">
<div class="wrap">
<div class="head">
<p class="label">{esc(I.VIDEOS_LABEL[l])}</p>
<h1 class="h2">{esc(u["h1"])}</h1>
<p class="lead">{esc(u["lead"])}</p>
</div>
<div class="vgrid">
{chr(10).join(cards)}
</div>
</div>
</main>
'''
    if l == "es":
        return G.head(u["title"], u["desc"], url, "lumbar.jpg", ld, form=False) + body + G.footer(form=False) + "\n</body>\n</html>\n"
    import contenido_i18n as CI
    C = CI.Chrome(l)
    return C.head(u["title"], u["desc"], "videos/", "lumbar.jpg", ld) + body + C.footer("videos/") + "\n</body>\n</html>\n"


def urls_sitemap():
    return [("/videos/", "0.7")] + [(f"/{l}/videos/", "0.6") for l in LANGS if l != "es"]


def main():
    for l in LANGS:
        d = os.path.join(ROOT, "videos") if l == "es" else os.path.join(ROOT, l, "videos")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pagina(l))
    print("vídeos:", len(CATALOGO))


if __name__ == "__main__":
    main()
