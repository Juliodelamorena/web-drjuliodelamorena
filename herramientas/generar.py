import json, os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from paginas import PAGES, ABOUT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://drjuliodelamorena.com"
CITA = "https://www.memorialpubliocordon.com/medicos/dr-julio-de-la-morena-garzon/"
REVISION = "2026-10-21"
FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&amp;family=Manrope:wght@400;500;600&amp;display=swap"

# Fix image alt texts that describe the photo, not the topic
ALT_FIX = {
 "tendinopatias": "Ecografía realizada en la consulta",
 "lesiones-musculares": "Estudio con ecografía en la consulta",
 "hombro-doloroso": "El doctor explicando una prueba de imagen en consulta",
}

BY_SLUG = {p["slug"]: p for p in PAGES}

def esc(s): return html.escape(s, quote=True)

HEADER = f'''<div class="util">
<div class="wrap">
<span class="util-addr">Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · Pozuelo de Alarcón (Madrid)</span>
<span>Cita previa <strong>913 548 990</strong></span>
</div>
</div>
<header class="top">
<div class="wrap">
<a class="brand" href="/"><strong>Dr. Julio De la Morena</strong><span>Medicina del Deporte · Terapias Regenerativas</span></a>
<nav class="menu" aria-label="Principal">
<a href="/#areas">Especialidades</a>
<a href="/#tratamientos">Tratamientos</a>
<a href="/dr-julio-de-la-morena/">El doctor</a>
<a href="/#articulos">Artículos</a>
<a class="btn" href="/#contacto">Solicitar cita</a>
</nav>
</div>
</header>'''

def footer():
    links = "".join(f'<a href="/{p["slug"]}/">{esc(p["nav"])}</a>' for p in PAGES)
    return f'''<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-col">
<strong class="foot-brand">Dr. Julio De la Morena</strong>
<span>Unidad de Terapias Regenerativas y Medicina Deportiva</span>
<span>Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · 28223 Pozuelo de Alarcón (Madrid)</span>
<span>Cita previa: 913 548 990</span>
</div>
<nav class="foot-col foot-links" aria-label="Especialidades y tratamientos">{links}<a href="/dr-julio-de-la-morena/">El doctor</a></nav>
</div>
<div class="wrap foot-legal">
<span>Dr. Julio De la Morena Garzón · Colegiado nº 281903698 · Medicina de la Educación Física y del Deporte</span>
<nav aria-label="Legal"><a href="/aviso-legal.html">Aviso legal</a><a href="/privacidad.html">Privacidad</a></nav>
</div>
</footer>'''

def head(title, desc, url, img, ld):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/estilos.css">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
{HEADER}
'''

DOCTOR_REF = {"@type": "Person", "@id": f"{SITE}/#julio", "name": "Dr. Julio De la Morena Garzón"}

def breadcrumb(name, url):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}

def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def page(p):
    url = f"{SITE}/{p['slug']}/"
    atype, aname, alt_names = p["about"]
    about = {"@type": atype, "name": aname, "alternateName": alt_names}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url, "url": url, "name": p["seo"], "description": p["desc"],
         "inLanguage": "es-ES", "about": about, "audience": {"@type": "Patient"},
         "lastReviewed": REVISION, "datePublished": REVISION,
         "author": DOCTOR_REF, "reviewedBy": DOCTOR_REF,
         "primaryImageOfPage": f"{SITE}/img/{p['img']}",
         "isPartOf": {"@id": f"{SITE}/#web"}},
        breadcrumb(p["nav"], url), faq_ld(p["faq"])]}
    w, h = p["img_wh"]
    alt = ALT_FIX.get(p["slug"], p["img_alt"])
    secs = "\n".join(f'<h2>{esc(t)}</h2>\n{body}' for t, body in p["sections"])
    faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"])
    rel = "".join(f'<a class="rel" href="/{s}/"><span>{esc(BY_SLUG[s]["nav"])}</span><span aria-hidden="true">→</span></a>' for s in p["related"])
    extra = ""
    if p.get("extra_link"):
        extra = f'<p><a href="{p["extra_link"][0]}">{esc(p["extra_link"][1])} →</a></p>'
    body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/#{'areas' if p['label']=='Especialidades' else 'tratamientos'}">{esc(p['label'])}</a><span aria-hidden="true">/</span><span>{esc(p['nav'])}</span></nav>
<p class="label">{esc(p['label'])}</p>
<h1>{esc(p['h1'])}</h1>
<p class="answer">{esc(p['lead'])}</p>
<img class="wide" src="/img/{p['img']}" alt="{esc(alt)}" width="{w}" height="{h}">
{secs}
{extra}
<h2>Preguntas frecuentes</h2>
<div class="faq">
{faqs}
</div>
<div class="cta-band">
<div><h3>Solicite una valoración</h3><p>Unidad de Terapias Regenerativas y Medicina Deportiva · Hospital Memorial Publio Cordón · 913 548 990</p></div>
<a class="btn" href="{CITA}">Solicitar cita</a>
</div>
<div class="byline">
<img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy">
<p>Contenido elaborado y revisado por el <a href="/dr-julio-de-la-morena/">Dr. Julio De la Morena Garzón</a>, especialista en Medicina de la Educación Física y del Deporte (colegiado nº 281903698). Última revisión: octubre de 2026. Información divulgativa que no sustituye una consulta médica.</p>
</div>
<div class="related"><p class="label">Relacionado</p>{rel}</div>
</article>
</main>
'''
    return head(p["seo"], p["desc"], url, p["img"], ld) + body + footer() + "\n</body>\n</html>\n"

def about_page():
    a = ABOUT; url = f"{SITE}/{a['slug']}/"
    faq = [
     ("¿Quién es el Dr. Julio De la Morena?", "Es médico especialista en Medicina de la Educación Física y del Deporte, colegiado nº 281903698 en el Colegio de Médicos de Madrid. Pasa consulta en la Unidad de Terapias Regenerativas y Medicina Deportiva del Hospital Memorial Publio Cordón, en Pozuelo de Alarcón (Madrid). Trabajó catorce años en los servicios médicos del Real Madrid, cuatro como médico del primer equipo, y es director médico de la Real Federación Española de Rugby."),
     ("¿Qué trata el Dr. Julio De la Morena?", "Artrosis, tendinopatías, lumbalgia y ciática, dolor de hombro, esguinces y lesiones musculares, en deportistas y en personas que no hacen deporte. Utiliza ecografía en la misma consulta, infiltraciones guiadas por ecografía y factores de crecimiento autólogos cuando están indicados."),
     ("¿Cómo pedir cita con el Dr. Julio De la Morena?", "Por teléfono en el 913 548 990, en la web del Hospital Memorial Publio Cordón o mediante el formulario de drjuliodelamorena.com."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfilePage", "@id": url, "url": url, "name": a["seo"], "inLanguage": "es-ES",
         "mainEntity": {"@id": f"{SITE}/#julio"}, "dateModified": REVISION, "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "Person", "@id": f"{SITE}/#julio", "name": "Julio De la Morena Garzón",
         "alternateName": ["Dr. Julio De la Morena", "Julio de la Morena", "Dr. De la Morena"], "honorificPrefix": "Dr.",
         "jobTitle": "Médico especialista en Medicina de la Educación Física y del Deporte",
         "image": f"{SITE}/img/retrato.jpg", "url": f"{SITE}/",
         "worksFor": {"@type": "Hospital", "name": "Hospital Memorial Publio Cordón", "url": "https://www.memorialpubliocordon.com/"},
         "workLocation": {"@type": "Place", "name": "Hospital Memorial Publio Cordón", "address": {"@type": "PostalAddress", "streetAddress": "Paseo de la Casa de Campo, 5", "postalCode": "28223", "addressLocality": "Pozuelo de Alarcón", "addressRegion": "Madrid", "addressCountry": "ES"}},
         "memberOf": [{"@type": "SportsOrganization", "name": "Real Federación Española de Rugby"}, {"@type": "Organization", "name": "Ilustre Colegio Oficial de Médicos de Madrid"}],
         "hasOccupation": {"@type": "Occupation", "name": "Médico deportivo", "occupationLocation": {"@type": "City", "name": "Madrid"}},
         "knowsAbout": [p["about"][1] for p in PAGES],
         "identifier": {"@type": "PropertyValue", "propertyID": "Número de colegiado (Colegio de Médicos de Madrid)", "value": "281903698"},
         "sameAs": ["https://www.instagram.com/drjuliodelamorena/", CITA]},
        breadcrumb("El doctor", url), faq_ld(faq)]}
    areas = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["nav"])}</a></li>' for p in PAGES)
    faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(x)}</p></details>' for q, x in faq)
    body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a><span aria-hidden="true">/</span><span>El doctor</span></nav>
<p class="label">El doctor</p>
<h1>{esc(a['h1'])}</h1>
<p class="answer">El Dr. Julio De la Morena Garzón es médico especialista en Medicina de la Educación Física y del Deporte (colegiado nº 281903698, Colegio de Médicos de Madrid). Pasa consulta en la Unidad de Terapias Regenerativas y Medicina Deportiva del Hospital Memorial Publio Cordón, en Pozuelo de Alarcón (Madrid). Trabajó catorce años en los servicios médicos del Real Madrid, cuatro de ellos como médico del primer equipo, y es director médico de la Real Federación Española de Rugby. Trata artrosis, tendinopatías, dolor de espalda y lesiones del aparato locomotor en cualquier persona, haga deporte o no, con ecografía en la misma consulta y tratamiento sin cirugía siempre que sea posible.</p>
<img class="wide" src="/img/trayectoria.jpg" alt="El Dr. Julio De la Morena con el trofeo de Liga del Real Madrid" width="1018" height="1024" style="aspect-ratio: 4 / 3; object-position: center 30%">
<h2>Trayectoria</h2>
<ul class="cvlist">
<li><strong>Especialidad:</strong> Medicina de la Educación Física y del Deporte.</li>
<li><strong>Colegiado</strong> nº 281903698 en el Ilustre Colegio Oficial de Médicos de Madrid.</li>
<li><strong>Real Madrid:</strong> catorce años en los servicios médicos del club, cuatro como médico del primer equipo.</li>
<li><strong>Rugby:</strong> director médico de la Real Federación Española de Rugby.</li>
<li><strong>Deportistas:</strong> seguimiento de jugadores profesionales de rugby, pádel y fútbol.</li>
<li><strong>Investigación:</strong> formación certificada en Buenas Prácticas Clínicas para ensayos clínicos.</li>
<li><strong>Actualidad:</strong> Unidad de Terapias Regenerativas y Medicina Deportiva del Hospital Memorial Publio Cordón.</li>
</ul>
<h2>Forma de trabajar</h2>
<p>Consulta de alta resolución: en una misma visita se explora al paciente, se estudia con ecografía, se establece el diagnóstico y, cuando está indicado, se inicia el tratamiento, en coordinación con radiología intervencionista, fisioterapia y traumatología. La cirugía se reserva para los casos que de verdad la necesitan.</p>
<h2>Qué trata</h2>
<ul class="arealist">{areas}</ul>
<h2>Preguntas frecuentes</h2>
<div class="faq">
{faqs}
</div>
<div class="cta-band">
<div><h3>Solicite una valoración</h3><p>Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · Pozuelo de Alarcón · 913 548 990</p></div>
<a class="btn" href="{CITA}">Solicitar cita</a>
</div>
</article>
</main>
'''
    return head(a["seo"], a["desc"], url, "retrato.jpg", ld) + body + footer() + "\n</body>\n</html>\n"

if __name__ == "__main__":
  for p in PAGES:
      os.makedirs(f"{ROOT}/{p['slug']}", exist_ok=True)
      open(f"{ROOT}/{p['slug']}/index.html", "w").write(page(p))
  os.makedirs(f"{ROOT}/{ABOUT['slug']}", exist_ok=True)
  open(f"{ROOT}/{ABOUT['slug']}/index.html", "w").write(about_page())
  print("ok", len(PAGES) + 1)
