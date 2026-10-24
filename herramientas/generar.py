import json, os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from paginas import PAGES, ABOUT
from paginas_en import SLUG_ES_TO_EN

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

def header(en_url="/en/"):
    return f'''<div class="util">
<div class="wrap">
<span class="util-addr">Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · Pozuelo de Alarcón (Madrid)</span>
<span>Cita previa <a class="tel" href="tel:+34913548990">913 548 990</a><span class="util-hor"> · lunes a viernes, de 15:00 a 21:00</span></span>
</div>
</div>
<header class="top">
<div class="wrap">
<a class="brand" href="/"><strong>Dr. Julio De la Morena</strong><span>Medicina del Deporte · Terapias Regenerativas</span></a>
<nav class="menu" aria-label="Principal">
<a href="/#areas">Especialidades</a>
<a href="/#tratamientos">Tratamientos</a>
<a href="/dr-julio-de-la-morena/">El doctor</a>
<a href="/planes/">Planes de ejercicio</a>
<a href="/blog/">Artículos</a>
<a class="lang" href="{en_url}" hreflang="en" lang="en">English</a>
<a class="btn solo-movil" href="tel:+34913548990">Pedir cita</a><a class="btn solo-escritorio" href="/#contacto">Pedir cita</a>
</nav>
</div>
</header>'''

HEADER = header()

def footer():
    links = "".join(f'<a href="/{p["slug"]}/">{esc(p["nav"])}</a>' for p in PAGES)
    return f'''<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-col">
<strong class="foot-brand">Dr. Julio De la Morena</strong>
<span>Unidad de Terapias Regenerativas y Medicina Deportiva</span>
<span>Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · 28223 Pozuelo de Alarcón (Madrid)</span>
<span>Cita previa: <a class="tel" href="tel:+34913548990">913 548 990</a> · Consulta lunes a viernes, de 15:00 a 21:00</span>
</div>
<nav class="foot-col foot-links" aria-label="Especialidades y tratamientos">{links}<a href="/dr-julio-de-la-morena/">El doctor</a><a href="/planes/">Planes de ejercicio</a><a href="/blog/">Artículos</a></nav>
</div>
<div class="wrap foot-legal">
<span>Dr. Julio De la Morena Garzón · Colegiado nº 281903698 · Medicina de la Educación Física y del Deporte</span>
<nav aria-label="Legal"><a href="/aviso-legal.html">Aviso legal</a><a href="/privacidad.html">Privacidad</a></nav>
</div>
</footer>
<nav class="cta-fija" aria-label="Contacto rápido"><a class="llamar" href="tel:+34913548990">Llamar · 913 548 990</a><a class="cita" href="/#contacto">Que me llamen</a></nav>'''

def alternates(es_url, en_url):
    return (f'<link rel="alternate" hreflang="es" href="{es_url}">\n'
            f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{es_url}">\n')

def head(title, desc, url, img, ld, en_url=None):
    alt = alternates(url, en_url) if en_url else ""
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{alt}<meta property="og:type" content="article">
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
{header(en_url.replace(SITE, '') if en_url else '/en/')}
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
<div><h3>{esc(p.get("cta", "Solicite una valoración"))}</h3><p class="ventaja">Exploración y ecografía en la misma consulta: sale con diagnóstico y plan. Primera consulta sin compromiso de tratamiento: si no está indicado, se lo decimos.</p><p>Hospital Memorial Publio Cordón · Pozuelo de Alarcón · <a class="tel" href="tel:+34913548990">913 548 990</a> · lunes a viernes, de 15:00 a 21:00</p></div>
<a class="btn solo-movil" href="tel:+34913548990">Llamar para pedir cita</a><a class="btn solo-escritorio" href="/#contacto">Pedir cita</a>
</div>
<div class="byline">
<img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy">
<p>Contenido elaborado y revisado por el <a href="/dr-julio-de-la-morena/">Dr. Julio De la Morena Garzón</a>, especialista en Medicina de la Educación Física y del Deporte (colegiado nº 281903698). Última revisión: octubre de 2026. Información divulgativa que no sustituye una consulta médica.</p>
</div>
<div class="related"><p class="label">Relacionado</p>{rel}</div>
</article>
</main>
'''
    en = SLUG_ES_TO_EN.get(p["slug"])
    return head(p["seo"], p["desc"], url, p["img"], ld, f"{SITE}/en/{en}/" if en else None) + body + footer() + "\n</body>\n</html>\n"

def about_page():
    a = ABOUT; url = f"{SITE}/{a['slug']}/"
    faq = [
     ("¿Quién es el Dr. Julio De la Morena?", "Es médico especialista en Medicina de la Educación Física y del Deporte por la vía MIR (Universidad Complutense de Madrid), colegiado nº 281903698 en el Colegio de Médicos de Madrid, con más de veinte años de experiencia. Pasa consulta en la Unidad de Terapias Regenerativas y Medicina Deportiva del Hospital Memorial Publio Cordón, en Pozuelo de Alarcón (Madrid). Trabajó catorce años en los servicios médicos del Real Madrid, cuatro como médico del primer equipo, y es director médico de la Real Federación Española de Rugby."),
     ("¿Qué trata el Dr. Julio De la Morena?", "Artrosis, tendinopatías, lumbalgia y ciática, dolor de hombro, esguinces y lesiones musculares, en deportistas y en personas que no hacen deporte. Utiliza ecografía en la misma consulta, infiltraciones guiadas por ecografía y factores de crecimiento autólogos cuando están indicados."),
     ("¿Cómo pedir cita con el Dr. Julio De la Morena?", "Por teléfono en el 913 548 990 (consulta de lunes a viernes, de 15:00 a 21:00) o con el formulario de drjuliodelamorena.com, y le llamamos para darle cita."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfilePage", "@id": url, "url": url, "name": a["seo"], "inLanguage": "es-ES",
         "mainEntity": {"@id": f"{SITE}/#julio"}, "dateModified": REVISION + "T09:00:00+02:00", "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "Person", "@id": f"{SITE}/#julio", "name": "Julio De la Morena Garzón",
         "alternateName": ["Dr. Julio De la Morena", "Julio de la Morena", "Dr. De la Morena"], "honorificPrefix": "Dr.",
         "jobTitle": "Médico especialista en Medicina de la Educación Física y del Deporte",
         "image": f"{SITE}/img/retrato.jpg", "url": f"{SITE}/",
         "worksFor": {"@type": "Hospital", "name": "Hospital Memorial Publio Cordón", "url": "https://www.memorialpubliocordon.com/"},
         "workLocation": {"@type": "Place", "name": "Hospital Memorial Publio Cordón", "address": {"@type": "PostalAddress", "streetAddress": "Paseo de la Casa de Campo, 5", "postalCode": "28223", "addressLocality": "Pozuelo de Alarcón", "addressRegion": "Madrid", "addressCountry": "ES"}},
         "memberOf": [{"@type": "SportsOrganization", "name": "Real Federación Española de Rugby"}, {"@type": "Organization", "name": "Ilustre Colegio Oficial de Médicos de Madrid"}],
         "hasOccupation": {"@type": "Occupation", "name": "Médico deportivo", "occupationLocation": {"@type": "City", "name": "Madrid"}},
         "knowsAbout": [p["about"][1] for p in PAGES],
         "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidad de Alcalá"}, {"@type": "CollegeOrUniversity", "name": "Universidad Complutense de Madrid"}],
         "award": ["Premio Manuel Clavel Nolla, Jornadas Nacionales de Traumatología del Deporte (2007)"],
         "knowsLanguage": ["es", "en"],
         "subjectOf": [
           {"@type": "VideoObject", "name": "Cómo prevenir lesiones en tendones y ligamentos", "url": "https://www.youtube.com/watch?v=FxVOJ4pY-Y4", "thumbnailUrl": "https://drjuliodelamorena.com/img/videos/tve-tendones-ligamentos.jpg", "publisher": {"@type": "Organization", "name": "Sanitas"}},
           {"@type": "VideoObject", "name": "Entrevista a Julio de la Morena y a Eduardo Vizcaíno", "url": "https://www.youtube.com/watch?v=PCEiHsOmEHU", "thumbnailUrl": "https://drjuliodelamorena.com/img/videos/esradio-entrevista.jpg", "publisher": {"@type": "Organization", "name": "esRadio"}},
           {"@type": "NewsArticle", "headline": "El Comité de Competición anula la roja al médico del Castilla", "url": "https://www.libertaddigital.com/deportes/futbol/2014-05-14/competicion-anula-la-roja-al-medico-del-castilla-1276518574/", "datePublished": "2014-05-14", "publisher": {"@type": "Organization", "name": "Libertad Digital"}}
         ],
         "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": "Especialista en Medicina de la Educación Física y del Deporte (MIR)", "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Universidad Complutense de Madrid"}}, {"@type": "EducationalOccupationalCredential", "name": "Certificación ICH-GCP E6(R3) Buenas Prácticas Clínicas", "recognizedBy": {"@type": "Organization", "name": "NIDA Clinical Trials Network, National Institutes of Health"}}],
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
<h2>Formación</h2>
<ul class="cvlist">
<li><strong>Especialista en Medicina de la Educación Física y del Deporte</strong> por la vía MIR · Universidad Complutense de Madrid (2006).</li>
<li><strong>Licenciado en Medicina y Cirugía</strong> · Universidad de Alcalá (1998), mejor expediente de su promoción.</li>
<li><strong>Suficiencia investigadora</strong> (Diploma de Estudios Avanzados) · Universidad de Alcalá (2001).</li>
<li><strong>Certificación en Buenas Prácticas Clínicas</strong> para ensayos clínicos (ICH-GCP E6 R3) · NIDA Clinical Trials Network, National Institutes of Health (2026–2029).</li>
<li><strong>Médico habilitado para el control antidopaje</strong> por el Consejo Superior de Deportes.</li>
</ul>
<h2>Trayectoria profesional</h2>
<ul class="cvlist">
<li><strong>2026 – actualidad · Hospital Memorial Publio Cordón</strong> (Pozuelo de Alarcón). Unidad de Terapias Regenerativas y Medicina Deportiva: ecografía musculoesquelética diagnóstica e intervencionista y terapias biológicas guiadas por ecografía. Desarrollo del programa de terapias avanzadas del hospital, incluido un ensayo clínico en lesión muscular.</li>
<li><strong>2022 – actualidad · Real Federación Española de Rugby.</strong> Director médico: responsable clínico de las selecciones nacionales, protocolos de prevención, diagnóstico y vuelta segura al juego.</li>
<li><strong>2021 – 2026 · Hospital Ruber Internacional</strong> (Madrid). Unidad de Medicina Deportiva, Regenerativa y Biomecánica: tratamiento conservador con soporte ecográfico, tendinopatías crónicas y patología articular.</li>
<li><strong>2007 – 2021 · Real Madrid C. F.</strong> Catorce años en los servicios médicos del club: fútbol base (2007–2013), Real Madrid Castilla (2013–2017) y médico del primer equipo (2017–2021).</li>
<li><strong>2019 – 2021 · GO fit Athletics.</strong> Jefe de los servicios médicos de un club de atletismo de alto rendimiento.</li>
<li><strong>2012 – 2019 · Hospital Sanitas La Moraleja</strong> (Madrid). Unidad de Medicina del Deporte.</li>
<li><strong>2006 – 2007 · Consejo Superior de Deportes.</strong> Centro de Medicina del Deporte: asistencia e investigación con deportistas de alto nivel.</li>
<li><strong>Antes de 2007:</strong> Fundación Provincial de Deportes de la Diputación de Guadalajara, C. D. Guadalajara, cantera del Club Atlético de Madrid, Centro de Medicina Deportiva de la Comunidad de Madrid y colaboración con las federaciones españolas de judo, atletismo y balonmano.</li>
</ul>
<h2>Docencia, investigación y reconocimientos</h2>
<ul class="cvlist">
<li><strong>Premio «Manuel Clavel Nolla»</strong> (Jornadas Nacionales de Traumatología del Deporte, 2007) por un estudio ecográfico del tendón cuadricipital en halterofilia de élite.</li>
<li><strong>Profesor asociado</strong> de prácticas clínicas en los másteres universitarios de Entrenamiento y Nutrición Deportiva y de Fisioterapia Deportiva · Universidad Europea de Madrid (2013–2016).</li>
<li><strong>Docente colaborador</strong> del Máster Universitario en Traumatología del Deporte · Universidad Complutense de Madrid (2011–2012). Colaborador honorífico de la Universidad Complutense (2007–2008).</li>
<li><strong>Autor</strong> del capítulo «Beneficios psicológicos del ejercicio en la mujer» en <em>Mujer y Deporte. La salud como meta</em> (Sanitas Hospitales y Cátedra Olímpica Marqués de Samaranch, 2018), y coautor de publicaciones en revistas internacionales y comunicaciones en congresos nacionales e internacionales.</li>
<li><strong>Idiomas:</strong> español e inglés (nivel alto; cursó la educación secundaria en el Reino Unido). Atiende en los dos idiomas.</li>
</ul>
<h2>Entrevistas y divulgación</h2>
<div class="videos">
<a class="video" href="https://www.youtube.com/watch?v=FxVOJ4pY-Y4" target="_blank" rel="noopener"><img src="/img/videos/tve-tendones-ligamentos.jpg" alt="El Dr. Julio De la Morena entrevistado en La mañana de La 1 sobre el tendón de Aquiles" width="960" height="540" loading="lazy"><span class="video-t"><strong>Cómo prevenir lesiones en tendones y ligamentos</strong><span>Entrevista en televisión (La mañana de La 1) · Canal de Sanitas en YouTube</span></span></a>
<a class="video" href="https://www.youtube.com/watch?v=PCEiHsOmEHU" target="_blank" rel="noopener"><img src="/img/videos/esradio-entrevista.jpg" alt="Entrevista al Dr. Julio De la Morena en esRadio" width="960" height="540" loading="lazy"><span class="video-t"><strong>Entrevista en esRadio</strong><span>«Es la mañana de Federico», con Eduardo Vizcaíno · YouTube</span></span></a>
</div>
<h3>En la prensa</h3>
<ul class="prensa">
<li><a href="https://www.libertaddigital.com/deportes/futbol/2014-05-14/competicion-anula-la-roja-al-medico-del-castilla-1276518574/" target="_blank" rel="noopener">El Comité de Competición anula la tarjeta roja al médico del Castilla</a><span>Libertad Digital · 14 de mayo de 2014. Expulsado por entrar al campo sin permiso para atender a un jugador que había perdido el conocimiento; el Comité dejó sin efecto la sanción.</span></li>
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
<div><h3>¿Quiere que valore su caso?</h3><p class="ventaja">Exploración y ecografía en la misma consulta: sale con diagnóstico y plan. Primera consulta sin compromiso de tratamiento: si no está indicado, se lo decimos.</p><p>Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · Pozuelo de Alarcón · <a class="tel" href="tel:+34913548990">913 548 990</a> · lunes a viernes, de 15:00 a 21:00</p></div>
<a class="btn solo-movil" href="tel:+34913548990">Llamar para pedir cita</a><a class="btn solo-escritorio" href="/#contacto">Pedir cita</a>
</div>
</article>
</main>
'''
    return head(a["seo"], a["desc"], url, "retrato.jpg", ld, f"{SITE}/en/{SLUG_ES_TO_EN[a['slug']]}/") + body + footer() + "\n</body>\n</html>\n"

if __name__ == "__main__":
  for p in PAGES:
      os.makedirs(f"{ROOT}/{p['slug']}", exist_ok=True)
      open(f"{ROOT}/{p['slug']}/index.html", "w").write(page(p))
  os.makedirs(f"{ROOT}/{ABOUT['slug']}", exist_ok=True)
  open(f"{ROOT}/{ABOUT['slug']}/index.html", "w").write(about_page())
  print("ok", len(PAGES) + 1)
