"""Blog del Dr. Julio De la Morena.

Uso:
  1. Añadir un artículo nuevo como archivo JSON en herramientas/articulos/<slug>.json
     (ver articulos/ejemplo explicado en GUIA.md).
  2. Ejecutar:  python3 herramientas/articulos.py
     Genera blog/<slug>.html, la página /blog/, los últimos 3 artículos de la portada,
     el sitemap.xml y el apartado de artículos de llms.txt.
"""
import glob, json, os, re, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as G
from paginas import PAGES

ROOT = G.ROOT
SITE = G.SITE
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
esc = G.esc


def fecha_larga(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {y}"


def cargar():
    arts = []
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "articulos", "*.json")):
        a = json.load(open(f, encoding="utf-8"))
        arts.append(a)
    arts.sort(key=lambda a: a["fecha"], reverse=True)
    return arts


def articulo(a):
    url = f"{SITE}/blog/{a['slug']}.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url, "url": url, "headline": a["titulo"], "name": a["titulo"],
         "description": a["descripcion"], "inLanguage": "es-ES", "datePublished": a["fecha"],
         "lastReviewed": a["fecha"], "image": f"{SITE}/img/{a['imagen']}",
         "about": [{"@type": "MedicalCondition", "name": t} for t in a.get("temas", [])],
         "audience": {"@type": "Patient"},
         "author": G.DOCTOR_REF, "reviewedBy": G.DOCTOR_REF, "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Artículos", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": a["titulo"], "item": url}]}]}
    if a.get("faq"):
        ld["@graph"].append(G.faq_ld([tuple(x) for x in a["faq"]]))
    secs = "\n".join(f"<h2>{esc(s[0])}</h2>\n{s[1]}" for s in a["secciones"])
    faq = ""
    if a.get("faq"):
        faq = "<h2>Preguntas frecuentes</h2>\n<div class=\"faq\">\n" + "\n".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>" for q, r in a["faq"]) + "\n</div>"
    by = {p["slug"]: p for p in PAGES}
    rel = "".join(f'<a class="rel" href="/{s}/"><span>{esc(by[s]["nav"])}</span><span aria-hidden="true">→</span></a>'
                  for s in a.get("relacionadas", []) if s in by)
    rel_html = f'<div class="related"><p class="label">Relacionado</p>{rel}</div>' if rel else ""
    w, h = a.get("imagen_wh", [1200, 800])
    body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/blog/">Artículos</a><span aria-hidden="true">/</span><span>{esc(a['categoria'])}</span></nav>
<p class="label">{esc(a['categoria'])} · {fecha_larga(a['fecha'])}</p>
<h1>{esc(a['titulo'])}</h1>
<p class="answer">{esc(a['entradilla'])}</p>
<img class="wide" src="/img/{a['imagen']}" alt="{esc(a['imagen_alt'])}" width="{w}" height="{h}">
{secs}
{faq}
<div class="cta-band">
<div><h3>¿Se reconoce en lo que acaba de leer?</h3><p class="ventaja">Exploración y ecografía en la misma consulta: sale con diagnóstico y plan. Primera consulta sin compromiso de tratamiento: si no está indicado, se lo decimos.</p><p>Hospital Memorial Publio Cordón · Pozuelo de Alarcón · <a class="tel" href="tel:+34913548990">913 548 990</a> · lunes a viernes, de 15:00 a 21:00</p></div>
<a class="btn solo-movil" href="tel:+34913548990">Llamar para pedir cita</a><a class="btn solo-escritorio" href="/#contacto">Pedir cita</a>
</div>
<div class="byline">
<img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy">
<p>Artículo del <a href="/dr-julio-de-la-morena/">Dr. Julio De la Morena Garzón</a>, especialista en Medicina de la Educación Física y del Deporte (colegiado nº 281903698). Información divulgativa que no sustituye una consulta médica.</p>
</div>
{rel_html}
</article>
</main>
'''
    t = f"{a['titulo']} · Dr. Julio De la Morena"
    return G.head(t, a["descripcion"], url, a["imagen"], ld) + body + G.footer() + "\n</body>\n</html>\n"


def tarjeta(a):
    w, h = a.get("imagen_wh", [1200, 800])
    mes = MESES[int(a["fecha"][5:7]) - 1].capitalize()
    return (f'<a class="post" href="/blog/{a["slug"]}.html">\n'
            f'<img src="/img/{a["imagen"]}" alt="{esc(a["imagen_alt"])}" width="{w}" height="{h}" loading="lazy">\n'
            f'<span class="meta">{esc(a["categoria"])} · {mes} {a["fecha"][:4]}</span>\n'
            f'<h3>{esc(a["titulo"])}</h3>\n<p>{esc(a["resumen"])}</p>\n</a>')


def indice(arts):
    url = f"{SITE}/blog/"
    ld = {"@context": "https://schema.org", "@type": "Blog", "@id": url, "url": url,
          "name": "Artículos del Dr. Julio De la Morena", "inLanguage": "es-ES",
          "author": G.DOCTOR_REF,
          "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"], "url": f"{SITE}/blog/{a['slug']}.html",
                        "datePublished": a["fecha"]} for a in arts]}
    cards = "\n".join(tarjeta(a) for a in arts)
    body = f'''<main class="block">
<div class="wrap">
<div class="head">
<p class="label">Artículos</p>
<h1 class="h2">Información para el paciente</h1>
<p class="lead">Artículos del Dr. Julio De la Morena sobre artrosis, tendinopatías, dolor de espalda, lesiones deportivas y terapias regenerativas.</p>
</div>
<div class="posts">
{cards}
</div>
</div>
</main>
'''
    return G.head("Artículos · Dr. Julio De la Morena", "Artículos sobre artrosis, tendinopatías, dolor de espalda, lesiones deportivas y terapias regenerativas del Dr. Julio De la Morena, Hospital Memorial Publio Cordón (Pozuelo de Alarcón).", url, "lumbar.jpg", ld) + body + G.footer() + "\n</body>\n</html>\n"


def portada(arts):
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    cards = "\n".join(tarjeta(a) for a in arts[:3])
    nuevo = f'<div class="posts">\n<!--POSTS-->\n{cards}\n<!--/POSTS-->\n</div>\n<p style="margin: 32px 0 0"><a href="/blog/">Ver todos los artículos →</a></p>'
    s2, n = re.subn(r'<div class="posts">.*?</div>\s*(<p style="margin: 32px 0 0"><a href="/blog/">Ver todos los artículos →</a></p>)?', nuevo, s, count=1, flags=re.S)
    assert n == 1
    open(p, "w", encoding="utf-8").write(s2)


def sitemap(arts):
    urls = [("/", "1.0"), ("/dr-julio-de-la-morena/", "0.9")] + [(f"/{p['slug']}/", "0.8") for p in PAGES] + \
           [("/blog/", "0.7"), ("/planes/", "0.8")] + [(f"/planes/{q['slug']}/", "0.8") for q in __import__("planes").cargar()] + [(f"/blog/{a['slug']}.html", "0.6") for a in arts] + \
           [("/aviso-legal.html", "0.2"), ("/privacidad.html", "0.2")] + \
           [("/en/", "0.8"), ("/en/dr-julio-de-la-morena/", "0.7")] + [(f"/en/{q['slug']}/", "0.7") for q in __import__("paginas_en").PAGES_EN]
    import idiomas as I
    for code in I.PACKS:                      # Georgian, Russian, French (generar_i18n.py)
        pk = I.pack(code)
        if pk is None:
            continue
        urls += [(f"/{code}/", "0.8"), (f"/{code}/{pk.ABOUT['slug']}/", "0.7")] + [(f"/{code}/{q['slug']}/", "0.7") for q in pk.PAGES]
    hoy = max([a["fecha"] for a in arts] + [G.REVISION])
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{hoy}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(x)


def llms(arts):
    p = os.path.join(ROOT, "llms.txt")
    s = open(p, encoding="utf-8").read().split("\n## Artículos")[0].rstrip("\n")
    s = "\n".join(l for l in s.split("\n") if "/blog/" not in l)
    s += "\n\n## Artículos\n\n" + "\n".join(f"- [{a['titulo']}]({SITE}/blog/{a['slug']}.html): {a['descripcion']}" for a in arts) + "\n"
    open(p, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    arts = cargar()
    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    for a in arts:
        if a.get("manual"):
            continue
        open(os.path.join(ROOT, "blog", f"{a['slug']}.html"), "w", encoding="utf-8").write(articulo(a))
    open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8").write(indice(arts))
    portada(arts); sitemap(arts); llms(arts)
    print("artículos:", len(arts))
