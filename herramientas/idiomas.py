"""Language registry shared by all generators.

Spanish (/) and English (/en/) have their own generators; Georgian, Russian and French
(/ka/, /ru/, /fr/) are built by generar_i18n.py from packs paginas_<lang>.py.
This module answers two questions for any Spanish slug: which URL does each language have
for it (hreflang) and how to draw the language menu.
"""
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SITE = "https://drjuliodelamorena.com"
PACKS = ["ka", "ru", "fr"]                      # built by generar_i18n.py
ORDER = ["es", "en", "ka", "ru", "fr"]          # order in the language menu
NAMES = {"es": "Español", "en": "English", "ka": "ქართული", "ru": "Русский", "fr": "Français"}
SHORT = {"es": "ES", "en": "EN", "ka": "KA", "ru": "RU", "fr": "FR"}

_cache = {}

def pack(code):
    if code not in _cache:
        try:
            _cache[code] = importlib.import_module(f"paginas_{code}")
        except ImportError:
            print(f"idiomas: no pack for {code} (paginas_{code}.py missing), skipped", file=sys.stderr)
            _cache[code] = None
    return _cache[code]

def slug_map(code):
    """Spanish slug -> slug in `code` ('' is the home page)."""
    if code == "es":
        return None
    pk = pack(code)
    if pk is None:
        return {}
    if code == "en":
        m = dict(pk.SLUG_ES_TO_EN); m[""] = ""
        return m
    return pk.SLUGS

EXTRA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n_extra")
LEGAL = ("aviso-legal.html", "privacidad.html")

def extra_available(code, es_slug):
    """Blog articles, exercise plans and legal pages translated in i18n_extra/<code>/."""
    d = os.path.join(EXTRA_DIR, code)
    if es_slug in LEGAL:
        return os.path.isfile(os.path.join(d, "legal.json"))
    if es_slug == "videos/":
        return True
    if es_slug in ("blog/", "planes/"):
        return os.path.isdir(os.path.join(d, es_slug.rstrip("/") if es_slug == "planes/" else "articulos"))
    if es_slug.startswith("blog/") and es_slug.endswith(".html"):
        return os.path.isfile(os.path.join(d, "articulos", es_slug[5:-5] + ".json"))
    if es_slug.startswith("planes/"):
        return os.path.isfile(os.path.join(d, "planes", es_slug[7:].strip("/") + ".json"))
    return False

def is_extra(es_slug):
    return es_slug in LEGAL or es_slug == "videos/" or es_slug.startswith("blog/") or es_slug.startswith("planes/")

def path_for(code, es_slug):
    """Site-relative path of the page `es_slug` in language `code`, or None if it has no version."""
    if es_slug in ("blog", "planes", "videos") or (es_slug.startswith("planes/") and not es_slug.endswith("/")):
        es_slug += "/"
    if is_extra(es_slug):
        if code == "es":
            return "/" + es_slug
        return f"/{code}/{es_slug}" if extra_available(code, es_slug) else None
    if code == "es":
        if not es_slug:
            return "/"
        return f"/{es_slug}" if es_slug.endswith(".html") else f"/{es_slug}/"
    m = slug_map(code)
    if es_slug not in m:
        return None
    s = m[es_slug]
    return f"/{code}/{s}/" if s else f"/{code}/"

def urls(es_slug):
    out = {}
    for code in ORDER:
        p = path_for(code, es_slug)
        if p is not None:
            out[code] = SITE + p
    return out

def alternates(es_slug):
    u = urls(es_slug)
    if len(u) < 2:          # Spanish-only page (blog, plans): no hreflang block
        return ""
    tags = [f'<link rel="alternate" hreflang="{c}" href="{u[c]}">' for c in ORDER if c in u]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{u["es"]}">')
    return "\n".join(tags) + "\n"

def og_alternates(current):
    loc = {"es": "es_ES", "en": "en_GB", "ka": "ka_GE", "ru": "ru_RU", "fr": "fr_FR"}
    home = urls("")
    return "".join(f'<meta property="og:locale:alternate" content="{loc[c]}">\n' for c in ORDER if c != current and c in home)

def bandera(code):
    return f'<img class="bandera" src="/img/banderas/{code}.svg" width="20" height="14" alt="" aria-hidden="true">'

def menu(current, es_slug, label="Idioma"):
    """Banderas de todos los idiomas, siempre a la vista. La del idioma actual va marcada y no es enlace.
    Las páginas sin versión en un idioma enlazan a la portada de ese idioma."""
    u, home = urls(es_slug), urls("")
    items = []
    for c in ORDER:
        if c not in home:
            continue
        if c == current:
            items.append(f'<span class="flag actual" lang="{c}" title="{NAMES[c]}" aria-current="true">{bandera(c)}<span class="sr">{NAMES[c]}</span></span>')
        else:
            href = (u.get(c) or home[c]).replace(SITE, "")
            items.append(f'<a class="flag" href="{href}" hreflang="{c}" lang="{c}" title="{NAMES[c]}">{bandera(c)}<span class="sr">{NAMES[c]}</span></a>')
    return f'<nav class="lang-flags" aria-label="{label}">{"".join(items)}</nav>'

def nav_movil(links, label, destacados=()):
    """Menú desplegable para el móvil (details). `links` y `destacados`: lista de (href, texto).
    Solo se ve por debajo de 640 px (CSS .nav-menu); en escritorio los enlaces van sueltos en .menu."""
    import html as _h
    items = "".join(f'<a href="{href}">{_h.escape(t)}</a>' for href, t in links)
    items += "".join(f'<a class="destacado" href="{href}">{_h.escape(t)}</a>' for href, t in destacados)
    return (f'<details class="nav-menu"><summary aria-label="{_h.escape(label)}">{_h.escape(label)}</summary>'
            f'<div>{items}</div></details>')

LEER_MAS = {"es": "Seguir leyendo", "en": "Read more", "ka": "მეტის წაკითხვა", "ru": "Читать дальше", "fr": "Lire la suite"}
_n = [0]
def respuesta(texto_html, lang="es"):
    """Párrafo de respuesta directa. En el móvil se muestra recortado a seis líneas con un
    'Seguir leyendo' (casilla oculta, sin JavaScript); en escritorio sale entero."""
    _n[0] += 1
    i = f"mas-{_n[0]}"
    return (f'<div class="answer-wrap"><input type="checkbox" id="{i}" class="answer-toggle" aria-hidden="true" tabindex="-1">'
            f'<p class="answer">{texto_html}</p><label for="{i}" class="answer-more">{LEER_MAS.get(lang, LEER_MAS["en"])}</label></div>')

def footer_links(current, es_slug=""):
    u, home = urls(es_slug), urls("")
    return "".join(f'<a href="{(u.get(c) or home[c]).replace(SITE, "")}" hreflang="{c}" lang="{c}">{bandera(c)}{NAMES[c]}</a>'
                   for c in ORDER if c != current and c in home)

def es_slug_from_url(url):
    """'https://site/x/' or '/x/' -> 'x'; home -> ''."""
    p = url.replace(SITE, "").strip("/")
    return p


VIDEOS_LABEL = {"es": "Vídeos", "en": "Videos", "fr": "Vidéos", "ru": "Видео", "ka": "ვიდეოები"}
def videos_href(code):
    return "/videos/" if code == "es" else f"/{code}/videos/"
