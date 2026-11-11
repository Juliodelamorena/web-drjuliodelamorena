"""Blog, planes de ejercicio y páginas legales en inglés, georgiano, ruso y francés.

Lee las traducciones de herramientas/i18n_extra/<idioma>/ (articulos/*.json, planes/*.json, legal.json, ui.json)
y genera /<idioma>/blog/, /<idioma>/planes/, /<idioma>/aviso-legal.html y /<idioma>/privacidad.html con la
cabecera y el pie de cada idioma. Ejecutar después de generar_en.py y generar_i18n.py:
    python3 herramientas/contenido_i18n.py
Si un artículo nuevo en español aún no tiene traducción en un idioma, simplemente no aparece en ese idioma.
"""
import glob, json, os, re, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as G
import generar_en as E
import generar_i18n as GI
import extras as X
import idiomas as I
from paginas_en import PAGES_EN
import planes as PL

ROOT, SITE = G.ROOT, G.SITE
esc = G.esc
LANGS = ["en", "ka", "ru", "fr", "zh"]
PHONE_INTL = "+34 913 548 990"


class Chrome:
    """Cabecera, pie y bloque de contacto de cada idioma."""
    def __init__(self, lang):
        self.L = lang
        self.base = f"/{lang}/"
        if lang == "en":
            self.pages = PAGES_EN
            self.about = "/en/dr-julio-de-la-morena/"
        else:
            self.B = GI.Builder(lang)
            self.pages = self.B.pages
            self.about = self.B.about_path
        self.by_es = {p["es"]: p for p in self.pages}

    def head(self, title, desc, es_slug, img, ld):
        if self.L == "en":
            url = SITE + I.path_for("en", es_slug)
            return E.head(title, desc, url, SITE + I.path_for("es", es_slug), img, ld, form=True)
        return self.B.head(title, desc, es_slug, img, ld)

    def footer(self, es_slug):
        return E.footer(es_slug) if self.L == "en" else self.B.footer(es_slug)

    def contact(self, ruta):
        return E.contact_block(ruta, compacto=True) if self.L == "en" else self.B.contact_block(ruta, compacto=True)

    def page_url(self, es_slug):
        p = self.by_es.get(es_slug)
        return f"{self.base}{p['slug']}/" if p else None

    def fix_links(self, h):
        """Enlaces internos del texto traducido: llevan a la versión de este idioma cuando existe."""
        def rep(m):
            href = m.group(1)
            if not href.startswith("/") or href.startswith("//"):
                return m.group(0)
            path = href.split("#")[0]
            es = path.strip("/")
            if path in ("/", ""):
                new = self.base
            elif es.startswith("blog/") or es.startswith("planes/") or es in I.LEGAL:
                new = I.path_for(self.L, es if not es.startswith("planes/") else es + "/") or href
            elif es.startswith("img/") or es.startswith("video/"):
                return m.group(0)
            else:
                new = self.page_url(es) or (self.about if es == "dr-julio-de-la-morena" else href)
            return f'href="{new}"'
        h = re.sub(r'href="([^"]*)"', rep, h)
        return h.replace(' hreflang="es"', "")


def fecha(u, iso):
    y, m, d = iso.split("-")
    return u["date_format"].format(d=int(d), month=u["months"][int(m) - 1], y=y)


def cargar(lang, sub):
    out = []
    for f in sorted(glob.glob(os.path.join(X.DIR, lang, sub, "*.json"))):
        out.append(json.load(open(f, encoding="utf-8")))
    return out


def cta_band(u, href_book, lang=None, slug=None):
    h = X.art_cta(lang, slug, u["art_cta_h"]) if lang else u["art_cta_h"]
    return (f'<div class="cta-band"><div><h3>{esc(h)}</h3><p class="ventaja">{esc(u["art_cta_p"])}</p>'
            f'<p>Hospital Memorial Publio Cordón · Pozuelo de Alarcón · <a class="tel" href="tel:+34913548990">{PHONE_INTL}</a> · {esc(u["hours"])}</p></div>'
            f'<a class="btn solo-movil" href="tel:+34913548990">{esc(u["cta_call"])}</a><a class="btn solo-escritorio" href="{href_book}">{esc(u["cta_book"])}</a></div>')


def byline(C, text):
    # El nombre del doctor enlaza a su página en este idioma.
    t = esc(text)
    for name in ("Dr Julio De la Morena Garzón", "Dr. Julio De la Morena Garzón"):
        if name in t:
            t = t.replace(name, f'<a href="{C.about}">{name}</a>', 1); break
    return f'<div class="byline"><img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy"><p>{t}</p></div>'


def related(C, u, slugs):
    rel = "".join(f'<a class="rel" href="{C.page_url(s)}"><span>{esc(C.by_es[s]["nav"])}</span><span aria-hidden="true">→</span></a>' for s in slugs if s in C.by_es)
    return f'<div class="related"><p class="label">{esc(u["related"])}</p>{rel}</div>' if rel else ""


def articulo(C, u, a):
    es_slug = f"blog/{a['slug']}.html"
    url = SITE + I.path_for(C.L, es_slug)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url, "url": url, "headline": a["titulo"], "name": a["titulo"],
         "description": a["descripcion"], "inLanguage": C.L, "datePublished": a["fecha"], "lastReviewed": a["fecha"],
         "image": f"{SITE}/img/{a['imagen']}", "about": [{"@type": "MedicalCondition", "name": t} for t in a.get("temas", [])],
         "audience": {"@type": "Patient"}, "author": G.DOCTOR_REF, "reviewedBy": G.DOCTOR_REF, "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": SITE + C.base},
            {"@type": "ListItem", "position": 2, "name": u["blog_label"], "item": f"{SITE}{C.base}blog/"},
            {"@type": "ListItem", "position": 3, "name": a["titulo"], "item": url}]}]}
    if a.get("faq"):
        ld["@graph"].append(G.faq_ld([tuple(x) for x in a["faq"]]))
    def _ok(h):  # skip sections that embed a video file not yet produced in this language
        import re as _re
        return all(os.path.isfile(os.path.join(ROOT, m.lstrip("/"))) for m in _re.findall(r'src="(/video/[^"]+\.mp4)"', h))
    secs = "\n".join(f"<h2>{esc(s[0])}</h2>\n{C.fix_links(s[1])}" for s in a["secciones"] if _ok(s[1]))
    faq = ""
    if a.get("faq"):
        faq = f'<h2>{esc(u["faq"])}</h2>\n<div class="faq">\n' + "\n".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>" for q, r in a["faq"]) + "\n</div>"
    w, h = a.get("imagen_wh", [1200, 800])
    body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{C.base}">{esc(u["home"])}</a><span aria-hidden="true">/</span><a href="{C.base}blog/">{esc(u["blog_label"])}</a><span aria-hidden="true">/</span><span>{esc(a['categoria'])}</span></nav>
<p class="label">{esc(a['categoria'])} · {fecha(u, a['fecha'])}</p>
<h1>{esc(a['titulo'])}</h1>
<p class="answer">{esc(a['entradilla'])}</p>
<img class="wide" src="/img/{a['imagen']}" alt="{esc(a['imagen_alt'])}" width="{w}" height="{h}">
{secs}
{X.evidencia_html(C.L, a["slug"])}
{faq}
{cta_band(u, "#contact", C.L, a["slug"])}
{byline(C, u["art_byline"])}
{related(C, u, a.get("relacionadas", []))}
</article>
{C.contact(C.base + "blog/" + a["slug"] + ".html")}
</main>
'''
    t = a["titulo"] + (" · Dr. Julio De la Morena" if len(a["titulo"]) <= 35 else "")
    return C.head(t, a["descripcion"], es_slug, a["imagen"], ld) + body + C.footer(es_slug) + "\n</body>\n</html>\n"


def tarjeta(C, u, a):
    w, h = a.get("imagen_wh", [1200, 800])
    mes = u["months"][int(a["fecha"][5:7]) - 1]
    mes = mes[:1].upper() + mes[1:]
    return (f'<a class="post" href="{C.base}blog/{a["slug"]}.html">\n'
            f'<img src="/img/{a["imagen"]}" alt="{esc(a["imagen_alt"])}" width="{w}" height="{h}" loading="lazy">\n'
            f'<span class="meta">{esc(a["categoria"])} · {mes} {a["fecha"][:4]}</span>\n'
            f'<h3>{esc(a["titulo"])}</h3>\n<p>{esc(a["resumen"])}</p>\n</a>')


def indice_blog(C, u, arts):
    url = f"{SITE}{C.base}blog/"
    ld = {"@context": "https://schema.org", "@type": "Blog", "@id": url, "url": url, "name": u["blog_title"],
          "inLanguage": C.L, "author": G.DOCTOR_REF,
          "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"], "url": f"{url}{a['slug']}.html", "datePublished": a["fecha"]} for a in arts]}
    cards = "\n".join(tarjeta(C, u, a) for a in arts)
    body = f'''<main class="block">
<div class="wrap">
<div class="head">
<p class="label">{esc(u["blog_label"])}</p>
<h1 class="h2">{esc(u["blog_h1"])}</h1>
<p class="lead">{esc(u["blog_lead"])}</p>
</div>
<div class="posts">
{cards}
</div>
</div>
</main>
'''
    return C.head(u["blog_title"], u["blog_desc"], "blog/", "lumbar.jpg", ld) + body + C.footer("blog/") + "\n</body>\n</html>\n"


def plan(C, u, p):
    es_slug = f"planes/{p['slug']}/"
    url = SITE + I.path_for(C.L, es_slug)
    n = 0
    tabs, panes = [], []
    for i, f in enumerate(p["fases"]):
        tabs.append(f'<button class="tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{esc(f["nombre"].split("·")[0].strip())}</button>')
        exs = []
        for e in f["ejercicios"]:
            n += 1
            foto = f"img/planes/{p['slug']}/{n}.jpg"
            img = f'<img src="/{foto}" alt="{esc(e[0])}" loading="lazy" width="760" height="570">' if os.path.isfile(os.path.join(ROOT, foto)) else ""
            exs.append(f'''<li class="ex">
<label class="ex-head" for="e{n}"><input type="checkbox" id="e{n}"><span class="ex-n">{n}</span><span><strong>{esc(e[0])}</strong><small>{esc(e[1])}</small></span></label>
{img}<p>{esc(e[2])}</p>
<p class="dosis">{esc(e[3])}</p>
</li>''')
        panes.append(f'''<section class="pane" role="tabpanel"{"" if i == 0 else " hidden"}>
<h2>{esc(f["nombre"])}</h2>
<p class="cuando">{esc(f["cuando"])}</p>
<p>{esc(f["texto"])}</p>
<ol class="exs">{"".join(exs)}</ol>
</section>''')
    li2 = lambda xs: "".join(f"<li><strong>{esc(a)}.</strong> {esc(b)}</li>" for a, b in xs)
    li = lambda xs: "".join(f"<li>{esc(x)}</li>" for x in xs)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url, "url": url, "name": p["titulo"], "description": p["descripcion"],
         "inLanguage": C.L, "lastReviewed": p["fecha"], "audience": {"@type": "Patient"},
         "about": {"@type": "MedicalCondition", "name": p["corto"]},
         "mainEntity": {"@type": "ExercisePlan", "name": p["titulo"], "activityFrequency": u["plan_freq"]},
         "author": G.DOCTOR_REF, "reviewedBy": G.DOCTOR_REF, "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": SITE + C.base},
            {"@type": "ListItem", "position": 2, "name": u["plans_label"], "item": f"{SITE}{C.base}planes/"},
            {"@type": "ListItem", "position": 3, "name": p["corto"], "item": url}]}]}
    script = PL.SCRIPT.replace("n+' de '+boxes.length+' hechos hoy'",
                               "'" + u["plan_count"].replace("'", "\\'").replace("{n}", "'+n+'").replace("{t}", "'+boxes.length+'") + "'")
    body = f'''<main class="article plan">
<article class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{C.base}">{esc(u["home"])}</a><span aria-hidden="true">/</span><a href="{C.base}planes/">{esc(u["plans_label"])}</a><span aria-hidden="true">/</span><span>{esc(p['zona'])}</span></nav>
<p class="label">{esc(u["plan_label"])} · {esc(p['zona'])}</p>
<h1>{esc(p['titulo'])}</h1>
<div class="aviso">{u["plan_notice"]}</div>
<details class="bloque"><summary>{esc(u["plan_why"])}</summary>{"".join(f"<p>{esc(x)}</p>" for x in p["intro"])}</details>
<div class="regla"><p class="label">{esc(u["plan_rule"])}</p><p>{esc(p['regla'])}</p></div>
<details class="bloque"><summary>{esc(u["plan_phase_q"])}</summary><p>{esc(u["plan_phase_hint"])}</p><ul>{li2(p["elegir_fase"])}</ul></details>
<details class="bloque"><summary>{esc(u["plan_before"])}</summary><ul>{li2(p["antes"])}</ul></details>
<div class="plan-bar"><div class="tabs" role="tablist">{"".join(tabs)}</div><span class="cuenta" data-cuenta></span></div>
{"".join(panes)}
<details class="bloque"><summary>{esc(u["plan_avoid"])}</summary><ul>{li(p["evitar"])}</ul></details>
<details class="bloque"><summary>{esc(u["plan_extra"])}</summary><p>{esc(p['complementario'])}</p></details>
<div class="box"><h3>{esc(u["plan_when"])}</h3><ul>{li(p["consultar"])}</ul><p style="margin-top:12px">{esc(p['normal'])}</p></div>
<p class="no-print"><button class="btn btn-dark" id="imprimir" type="button">{esc(u["plan_print"])}</button></p>
<div class="cta-band no-print"><div><h3>{esc(u["plan_cta_h"])}</h3><p>{esc(u["plan_cta_p"])} · <a class="tel" href="tel:+34913548990">{PHONE_INTL}</a> · {esc(u["hours"])}</p></div><a class="btn solo-movil" href="tel:+34913548990">{esc(u["cta_call"])}</a><a class="btn solo-escritorio" href="{C.base}#contact">{esc(u["cta_book"])}</a></div>
{byline(C, u["plan_byline"])}
<div class="no-print">{related(C, u, p.get("relacionadas", []))}</div>
</article>
</main>
{script}
'''
    t = p["titulo"] + (" · Dr. Julio De la Morena" if len(p["titulo"]) <= 35 else "")
    return C.head(t, p["descripcion"], es_slug, "retrato.jpg", ld) + body + C.footer(es_slug) + "\n</body>\n</html>\n"


def indice_planes(C, u, ps):
    url = f"{SITE}{C.base}planes/"
    cards = "\n".join(f'<a class="card" href="{C.base}planes/{p["slug"]}/"><span class="meta">{esc(p["zona"])}</span><h3>{esc(p["corto"])}</h3><p>{esc(u["plan_card"].format(n=sum(len(f["ejercicios"]) for f in p["fases"]), f=len(p["fases"])))}</p></a>' for p in ps)
    body = f'''<main class="block"><div class="wrap">
<div class="head"><p class="label">{esc(u["plans_label"])}</p><h1 class="h2">{esc(u["plans_h1"])}</h1>
<p class="lead">{esc(u["plans_lead"])}</p></div>
<div class="cards">{cards}</div></div></main>
'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "url": url, "name": u["plans_title"], "inLanguage": C.L, "author": G.DOCTOR_REF}
    return C.head(u["plans_title"], u["plans_desc"], "planes/", "retrato.jpg", ld) + body + C.footer("planes/") + "\n</body>\n</html>\n"


def legal_page(C, u, key, es_slug):
    h = C.fix_links(X.legal(C.L)[key])
    title = u["legal_title"] if key == "aviso_legal" else u["privacy_title"]
    url = SITE + I.path_for(C.L, es_slug)
    ld = {"@context": "https://schema.org", "@type": "WebPage", "url": url, "name": title, "inLanguage": C.L}
    body = f'<main class="legal"><div class="wrap">\n{h}\n</div></main>\n'
    return (C.head(title + " · Dr. Julio De la Morena", title, es_slug, "retrato.jpg", ld).replace("<head>", '<head>\n<meta name="robots" content="noindex, follow">', 1)
            + body + C.footer(es_slug) + "\n</body>\n</html>\n")


def build(lang):
    d = os.path.join(X.DIR, lang)
    if not os.path.isdir(d):
        return 0
    C, u = Chrome(lang), X.ui(lang)
    n = 0
    arts = sorted(cargar(lang, "articulos"), key=lambda a: a["fecha"], reverse=True)
    if arts:
        os.makedirs(os.path.join(ROOT, lang, "blog"), exist_ok=True)
        for a in arts:
            open(os.path.join(ROOT, lang, "blog", a["slug"] + ".html"), "w", encoding="utf-8").write(articulo(C, u, a)); n += 1
        open(os.path.join(ROOT, lang, "blog", "index.html"), "w", encoding="utf-8").write(indice_blog(C, u, arts)); n += 1
    ps = cargar(lang, "planes")
    if ps:
        for p in ps:
            pd = os.path.join(ROOT, lang, "planes", p["slug"]); os.makedirs(pd, exist_ok=True)
            open(os.path.join(pd, "index.html"), "w", encoding="utf-8").write(plan(C, u, p)); n += 1
        open(os.path.join(ROOT, lang, "planes", "index.html"), "w", encoding="utf-8").write(indice_planes(C, u, ps)); n += 1
    if os.path.isfile(os.path.join(d, "legal.json")):
        for key, slug in (("aviso_legal", "aviso-legal.html"), ("privacidad", "privacidad.html")):
            open(os.path.join(ROOT, lang, slug), "w", encoding="utf-8").write(legal_page(C, u, key, slug)); n += 1
    # subtítulos de los vídeos
    for f in glob.glob(os.path.join(d, "subs", "*.vtt")):
        name = os.path.basename(f)[:-4]
        os.makedirs(os.path.join(ROOT, "video", "subs"), exist_ok=True)
        open(os.path.join(ROOT, "video", "subs", f"{name}.{lang}.vtt"), "w", encoding="utf-8").write(open(f, encoding="utf-8").read())
    return n


def urls_sitemap():
    """Direcciones de este contenido para el sitemap (las legales no se indexan)."""
    out = []
    for l in LANGS:
        if cargar(l, "articulos"):
            out.append((f"/{l}/blog/", "0.6"))
            out += [(f"/{l}/blog/{a['slug']}.html", "0.5") for a in cargar(l, "articulos")]
        if cargar(l, "planes"):
            out.append((f"/{l}/planes/", "0.6"))
            out += [(f"/{l}/planes/{p['slug']}/", "0.6") for p in cargar(l, "planes")]
    return out


def parchear_manuales():
    """Artículos españoles escritos a mano (no los genera articulos.py): banderas y hreflang hacia sus traducciones."""
    for f in glob.glob(os.path.join(ROOT, "blog", "*.html")):
        es_slug = "blog/" + os.path.basename(f)
        h = open(f, encoding="utf-8").read()
        h = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n', "", h)
        h = re.sub(r'(<link rel="canonical" href="[^"]+">\n)', lambda m: m.group(1) + I.alternates(es_slug), h, count=1)
        menu = I.menu("es", es_slug, "Idioma")
        h = re.sub(r'<nav class="lang-flags util-flags".*?</nav>', lambda m: menu.replace('class="lang-flags"', 'class="lang-flags util-flags"'), h, flags=re.S)
        h = re.sub(r'<nav class="lang-flags" .*?</nav>', lambda m: menu, h, flags=re.S)
        open(f, "w", encoding="utf-8").write(h)


if __name__ == "__main__":
    for l in LANGS:
        print(l, build(l))
    parchear_manuales()
