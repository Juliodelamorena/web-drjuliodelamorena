"""English version of the site (/en/).

Usage: python3 herramientas/generar_en.py
Builds /en/index.html, /en/<slug>/index.html, /en/dr-julio-de-la-morena/, /en/thank-you.html
and refreshes the "## English" section of llms.txt.
Content lives in herramientas/paginas_en.py. Spanish pages get hreflang from generar.py.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as G
import idiomas as I
from paginas_en import PAGES_EN, ABOUT_EN, SLUG_ES_TO_EN

ROOT, SITE, CITA, FONTS, esc = G.ROOT, G.SITE, G.CITA, G.FONTS, G.esc
REVISION = G.REVISION
BY = {p["slug"]: p for p in PAGES_EN}
DOCTOR_REF = G.DOCTOR_REF
PHONE = "+34 913 548 990"
MAPA = "https://maps.google.com/?cid=4492723553507247190"   # ficha de Google del doctor (enlace neutro: Cómo llegar)

def header(es_slug=""):
    return f'''<div class="util">
<div class="wrap">
<span class="util-addr">Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · Pozuelo de Alarcón (Madrid)</span>
<span>Appointments <a class="tel" href="tel:+34913548990">+34 913 548 990</a><span class="util-hor"> · Mon–Fri, 3 pm to 9 pm</span></span>
</div>
</div>
<header class="top">
<div class="wrap">
<a class="brand" href="/en/"><strong>Dr Julio De la Morena</strong><span>Sports Medicine · Regenerative Therapies</span></a>
<nav class="menu" aria-label="Main">
<a href="/en/#conditions">Conditions</a>
<a href="/en/#treatments">Treatments</a>
<a href="/en/dr-julio-de-la-morena/">The doctor</a>
{I.menu("en", es_slug, "Language")}
<a class="btn solo-movil" href="tel:+34913548990">Book</a><a class="btn solo-escritorio" href="/en/#contact">Book an appointment</a>
</nav>
</div>
</header>'''

def footer(es_slug=""):
    links = "".join(f'<a href="/en/{p["slug"]}/">{esc(p["nav"])}</a>' for p in PAGES_EN)
    return f'''<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-col">
<strong class="foot-brand">Dr Julio De la Morena</strong>
<span>Regenerative Therapies and Sports Medicine Unit</span>
<span>Hospital Memorial Publio Cordón · Paseo de la Casa de Campo, 5 · 28223 Pozuelo de Alarcón (Madrid), Spain · <a href="{MAPA}" rel="noopener" target="_blank">Get directions</a></span>
<span>Appointments: <a class="tel" href="tel:+34913548990">+34 913 548 990</a> · Mon–Fri, 3 pm to 9 pm · Consultations in English and Spanish</span>
</div>
<nav class="foot-col foot-links" aria-label="Conditions and treatments">{links}<a href="/en/dr-julio-de-la-morena/">The doctor</a>{I.footer_links("en", es_slug)}</nav>
</div>
<div class="wrap foot-legal">
<span>Dr Julio De la Morena Garzón · Madrid Medical Council registration no. 281903698 · Specialist in Sport and Exercise Medicine</span>
<nav aria-label="Legal"><a href="/aviso-legal.html" hreflang="es">Legal notice (Spanish)</a><a href="/privacidad.html" hreflang="es">Privacy (Spanish)</a></nav>
</div>
</footer>
<nav class="cta-fija" aria-label="Quick contact"><a class="llamar" href="tel:+34913548990">Call · +34 913 548 990</a><a class="cita" href="/en/#contact">Ask for a call</a></nav>
{G.CONTADOR}'''

def head(title, desc, url, es_url, img, ld, og_type="article", extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{I.alternates(I.es_slug_from_url(es_url))}{extra}<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_GB">
{I.og_alternates("en")}
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
{header(I.es_slug_from_url(es_url))}
'''

def breadcrumb(name, url):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/en/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}

def cta():
    return f'''<div class="cta-band">
<div><h3>Would you like your case assessed?</h3><p class="ventaja">Examination and ultrasound in the same appointment: you leave with a diagnosis and a plan. First appointment with no commitment to treatment: if nothing is indicated, we tell you.</p><p>Hospital Memorial Publio Cordón · Pozuelo de Alarcón · <a class="tel" href="tel:+34913548990">+34 913 548 990</a> · Mon–Fri, 3 pm to 9 pm</p></div>
<a class="btn solo-movil" href="tel:+34913548990">Call to book</a><a class="btn solo-escritorio" href="/en/#contact">Book an appointment</a>
</div>'''

def page(p):
    url = f"{SITE}/en/{p['slug']}/"; es_url = f"{SITE}/{p['es']}/"
    atype, aname, alt_names = p["about"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url, "url": url, "name": p["seo"], "description": p["desc"],
         "inLanguage": "en", "about": {"@type": atype, "name": aname, "alternateName": alt_names},
         "audience": {"@type": "Patient"}, "lastReviewed": REVISION, "datePublished": REVISION,
         "author": DOCTOR_REF, "reviewedBy": DOCTOR_REF, "primaryImageOfPage": f"{SITE}/img/{p['img']}",
         "isPartOf": {"@id": f"{SITE}/#web"}},
        breadcrumb(p["nav"], url), G.faq_ld(p["faq"])]}
    w, h = p["img_wh"]
    secs = "\n".join(f'<h2>{esc(t)}</h2>\n{b}' for t, b in p["sections"])
    faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"])
    rel = "".join(f'<a class="rel" href="/en/{s}/"><span>{esc(BY[s]["nav"])}</span><span aria-hidden="true">→</span></a>' for s in p["related"])
    anchor = "conditions" if p["label"] == "Conditions" else "treatments"
    body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/en/">Home</a><span aria-hidden="true">/</span><a href="/en/#{anchor}">{esc(p['label'])}</a><span aria-hidden="true">/</span><span>{esc(p['nav'])}</span></nav>
<p class="label">{esc(p['label'])}</p>
<h1>{esc(p['h1'])}</h1>
<p class="answer">{esc(p['lead'])}</p>
<img class="wide" src="/img/{p['img']}" alt="{esc(p['img_alt'])}" width="{w}" height="{h}">
{secs}
<h2>Frequently asked questions</h2>
<div class="faq">
{faqs}
</div>
{cta()}
<div class="byline">
<img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy">
<p>Written and reviewed by <a href="/en/dr-julio-de-la-morena/">Dr Julio De la Morena Garzón</a>, specialist in Sport and Exercise Medicine (Madrid Medical Council no. 281903698). Last reviewed: October 2026. General information that does not replace a medical consultation.</p>
</div>
<div class="related"><p class="label">Related</p>{rel}</div>
</article>
</main>
'''
    return head(p["seo"], p["desc"], url, es_url, p["img"], ld) + body + footer(p["es"]) + "\n</body>\n</html>\n"

def about_page():
    a = ABOUT_EN; url = f"{SITE}/en/{a['slug']}/"; es_url = f"{SITE}/{a['es']}/"
    faq = [
     ("Who is Dr Julio De la Morena?", "He is a doctor specialising in Sport and Exercise Medicine, registered with the Madrid Medical Council (no. 281903698). He sees patients at the Regenerative Therapies and Sports Medicine Unit of Hospital Memorial Publio Cordón in Pozuelo de Alarcón (Madrid). He spent fourteen years with the Real Madrid CF medical services, four as first-team doctor, and is Chief Medical Officer of the Spanish Rugby Federation."),
     ("What does Dr Julio De la Morena treat?", "Osteoarthritis, tendinopathies, low back pain and sciatica, shoulder pain, sprains and muscle injuries, in athletes and in people who do no sport. He uses ultrasound in the same appointment, ultrasound-guided injections and autologous growth factors (platelet-rich plasma) when appropriate."),
     ("Does Dr De la Morena speak English?", "Yes. Consultations are available in English and Spanish."),
     ("How do I book an appointment?", f"By phone on {PHONE}, or with the contact form on drjuliodelamorena.com/en/, and we call you back."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfilePage", "@id": url, "url": url, "name": a["seo"], "inLanguage": "en",
         "mainEntity": {"@id": f"{SITE}/#julio"}, "dateModified": REVISION + "T09:00:00+02:00", "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "Person", "@id": f"{SITE}/#julio", "name": "Julio De la Morena Garzón",
         "alternateName": ["Dr Julio De la Morena", "Dr. Julio De la Morena", "Julio de la Morena"], "honorificPrefix": "Dr",
         "jobTitle": "Specialist in Sport and Exercise Medicine",
         "knowsLanguage": ["es", "en"],
         "image": f"{SITE}/img/retrato.jpg", "url": f"{SITE}/",
         "worksFor": {"@type": "Hospital", "name": "Hospital Memorial Publio Cordón", "url": "https://www.memorialpubliocordon.com/"},
         "memberOf": [{"@type": "SportsOrganization", "name": "Spanish Rugby Federation (Real Federación Española de Rugby)"}, {"@type": "Organization", "name": "Madrid Medical Council (Ilustre Colegio Oficial de Médicos de Madrid)"}],
         "knowsAbout": [p["about"][1] for p in PAGES_EN],
         "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidad de Alcalá"}, {"@type": "CollegeOrUniversity", "name": "Universidad Complutense de Madrid"}],
         "award": ["Manuel Clavel Nolla Award, Spanish National Sports Traumatology Meeting (2007)"],
         "knowsLanguage": ["es", "en"],
         "subjectOf": [
           {"@type": "VideoObject", "name": "Cómo prevenir lesiones en tendones y ligamentos", "url": "https://www.youtube.com/watch?v=FxVOJ4pY-Y4", "thumbnailUrl": "https://drjuliodelamorena.com/img/videos/tve-tendones-ligamentos.jpg", "publisher": {"@type": "Organization", "name": "Sanitas"}},
           {"@type": "VideoObject", "name": "Entrevista a Julio de la Morena y a Eduardo Vizcaíno", "url": "https://www.youtube.com/watch?v=PCEiHsOmEHU", "thumbnailUrl": "https://drjuliodelamorena.com/img/videos/esradio-entrevista.jpg", "publisher": {"@type": "Organization", "name": "esRadio"}},
           {"@type": "NewsArticle", "headline": "Tarjeta roja al sentido común", "datePublished": "2014-05-13", "publisher": {"@type": "Organization", "name": "El País"}},
           {"@type": "NewsArticle", "headline": "Una roja por salvar una vida", "datePublished": "2014-05-11", "publisher": {"@type": "Organization", "name": "Marca"}},
           {"@type": "NewsArticle", "headline": "Clamor contra Muñoz", "datePublished": "2014-05-12", "publisher": {"@type": "Organization", "name": "Diario AS"}},
           {"@type": "NewsArticle", "headline": "El Comité de Competición anula la roja al médico del Castilla", "url": "https://www.libertaddigital.com/deportes/futbol/2014-05-14/competicion-anula-la-roja-al-medico-del-castilla-1276518574/", "datePublished": "2014-05-14", "publisher": {"@type": "Organization", "name": "Libertad Digital"}}
         ],
         "identifier": {"@type": "PropertyValue", "propertyID": "Madrid Medical Council registration number", "value": "281903698"},
         "sameAs": ["https://www.instagram.com/drjuliodelamorena/", CITA]},
        breadcrumb("The doctor", url), G.faq_ld(faq)]}
    areas = "".join(f'<li><a href="/en/{p["slug"]}/">{esc(p["nav"])}</a></li>' for p in PAGES_EN)
    faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(x)}</p></details>' for q, x in faq)
    body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/en/">Home</a><span aria-hidden="true">/</span><span>The doctor</span></nav>
<p class="label">The doctor</p>
<h1>{esc(a['h1'])}</h1>
<p class="answer">Dr Julio De la Morena Garzón is a specialist in Sport and Exercise Medicine (Madrid Medical Council no. 281903698). He sees patients at the Regenerative Therapies and Sports Medicine Unit of Hospital Memorial Publio Cordón in Pozuelo de Alarcón (Madrid). He spent fourteen years with the Real Madrid CF medical services, four of them as first-team doctor, and is Chief Medical Officer of the Spanish Rugby Federation. He treats osteoarthritis, tendinopathies, back pain and musculoskeletal injuries in anyone, whether or not they play sport, with ultrasound in the same appointment and treatment without surgery whenever possible. Consultations are available in English.</p>
<img class="wide" src="/img/trayectoria.jpg" alt="Dr Julio De la Morena with the Real Madrid league trophy" width="1018" height="1024" style="aspect-ratio: 4 / 3; object-position: center 30%">
<h2>Training</h2>
<ul class="cvlist">
<li><strong>Specialist in Sport and Exercise Medicine</strong> (Spanish MIR residency) · Complutense University of Madrid (2006).</li>
<li><strong>Degree in Medicine and Surgery</strong> · University of Alcalá (1998), top of his year.</li>
<li><strong>Advanced Studies Diploma</strong> (research proficiency) · University of Alcalá (2001).</li>
<li><strong>Good Clinical Practice certification</strong> for clinical trials (ICH-GCP E6 R3) · NIDA Clinical Trials Network, National Institutes of Health (2026–2029).</li>
<li><strong>Accredited doping-control physician</strong>, Spanish Sports Council.</li>
</ul>
<h2>Career</h2>
<ul class="cvlist">
<li><strong>2026 – present · Hospital Memorial Publio Cordón</strong> (Pozuelo de Alarcón, Madrid). Regenerative Therapies and Sports Medicine Unit: diagnostic and interventional musculoskeletal ultrasound and ultrasound-guided biological therapies. Development of the hospital's advanced-therapies programme, including a clinical trial in muscle injury.</li>
<li><strong>2022 – present · Spanish Rugby Federation.</strong> Chief Medical Officer: clinical lead for the national teams; prevention, diagnosis and safe return-to-play protocols.</li>
<li><strong>2021 – 2026 · Hospital Ruber Internacional</strong> (Madrid). Sports, Regenerative and Biomechanics Medicine Unit.</li>
<li><strong>2007 – 2021 · Real Madrid CF.</strong> Fourteen years with the club's medical services: academy (2007–2013), Real Madrid Castilla (2013–2017) and first-team doctor (2017–2021).</li>
<li><strong>2019 – 2021 · GO fit Athletics.</strong> Head of medical services of a high-performance athletics club.</li>
<li><strong>2012 – 2019 · Hospital Sanitas La Moraleja</strong> (Madrid). Sports Medicine Unit.</li>
<li><strong>2006 – 2007 · Spanish Sports Council.</strong> Sports Medicine Centre: clinical care and research with elite athletes.</li>
</ul>
<h2>Teaching, research and awards</h2>
<ul class="cvlist">
<li><strong>"Manuel Clavel Nolla" Award</strong> (Spanish National Sports Traumatology Meeting, 2007) for an ultrasound study of the quadriceps tendon in elite weightlifters.</li>
<li><strong>Associate lecturer</strong> on the master's degrees in Sports Training and Nutrition and in Sports Physiotherapy · Universidad Europea de Madrid (2013–2016); contributing lecturer on the master's in Sports Traumatology · Complutense University of Madrid (2011–2012).</li>
<li><strong>Author</strong> of a book chapter on the psychological benefits of exercise in women (<em>Mujer y Deporte</em>, 2018) and co-author of papers in international journals and conference communications.</li>
<li><strong>Languages:</strong> Spanish and English (he completed his secondary education in the United Kingdom). Consultations in both languages.</li>
</ul>
<h2>Interviews and media</h2>
<div class="videos">
<a class="video" href="https://www.youtube.com/watch?v=FxVOJ4pY-Y4" target="_blank" rel="noopener"><img src="/img/videos/tve-tendones-ligamentos.jpg" alt="Dr Julio De la Morena interviewed on Spanish national television about the Achilles tendon" width="960" height="540" loading="lazy"><span class="video-t"><strong>How to prevent tendon and ligament injuries</strong><span>Television interview (La 1, Spanish public television) · Sanitas channel on YouTube (in Spanish)</span></span></a>
<a class="video" href="https://www.youtube.com/watch?v=PCEiHsOmEHU" target="_blank" rel="noopener"><img src="/img/videos/esradio-entrevista.jpg" alt="Dr Julio De la Morena interviewed on esRadio" width="960" height="540" loading="lazy"><span class="video-t"><strong>Interview on esRadio</strong><span>"Es la mañana de Federico" · YouTube (in Spanish)</span></span></a>
</div>
<h3>In the press</h3>
<p>May 2014. A Real Madrid Castilla player collapsed unconscious on the pitch after a collision. Dr De la Morena ran on to treat him without waiting for the referee's permission, secured his airway and was sent off. The Spanish sports press backed his decision and the Competition Committee overturned the sanction.</p>
<ul class="prensa">
<li><a href="https://www.libertaddigital.com/deportes/futbol/2014-05-14/competicion-anula-la-roja-al-medico-del-castilla-1276518574/" target="_blank" rel="noopener">Competition Committee overturns the red card shown to the Castilla team doctor</a><span>Libertad Digital · 14 May 2014 (in Spanish)</span></li>
<li><strong>"Tarjeta roja al sentido común" (A red card for common sense)</strong><span>El País · 13 May 2014</span></li>
<li><strong>"Clamor contra Muñoz"</strong><span>Diario AS · 12 May 2014</span></li>
<li><strong>"Una roja por salvar una vida" (A red card for saving a life)</strong><span>Marca · 11 May 2014</span></li>
<li><strong>ABC and Sport</strong><span>11 and 13 May 2014</span></li>
</ul>
<h2>How he works</h2>
<p>One-stop consultation: in a single visit the patient is examined, studied with ultrasound, diagnosed and, when appropriate, treatment begins, in coordination with interventional radiology, physiotherapy and orthopaedic surgery. Surgery is reserved for the cases that genuinely need it.</p>
<h2>What he treats</h2>
<ul class="arealist">{areas}</ul>
<h2>Frequently asked questions</h2>
<div class="faq">
{faqs}
</div>
{cta()}
</article>
</main>
'''
    return head(a["seo"], a["desc"], url, es_url, "retrato.jpg", ld) + body + footer(a["es"]) + "\n</body>\n</html>\n"

HOME_FAQ = [
 ("Do I need to be an athlete to come to the clinic?", "No. The clinic sees professional rugby, padel and football players, and also people who do no sport and have osteoarthritis, tendinopathies, back pain, sciatica or sprains."),
 ("Can knee osteoarthritis be treated without surgery?", "In many cases, yes, at least for a time. There are options between conservative treatment and a knee replacement: therapeutic exercise, weight management, ultrasound-guided injections and autologous growth factors when appropriate. Each case is assessed in clinic."),
 ("What are autologous growth factors?", "A treatment obtained from the patient's own blood, also known as platelet-rich plasma, and applied to the injured area, usually under ultrasound guidance. It is used in selected cases of osteoarthritis and tendinopathy; it is not suitable for every patient."),
 ("What is an ultrasound-guided injection?", "An injection in which the doctor sees the needle and the structure being treated on the ultrasound screen, so the treatment is placed exactly in the affected tendon or joint."),
 ("Can I be seen in English?", "Yes. Dr De la Morena sees patients in English and Spanish."),
 ("Do you accept health insurance?", "No. Consultations are private and are not billed through insurers. You are told the fee when you book, before the visit."),
 ("Do I need a referral?", "No. You can book directly."),
 ("What are the clinic hours?", "Monday to Friday, 3 pm to 9 pm, at Hospital Memorial Publio Cordón (Pozuelo de Alarcón, Madrid)."),
 ("How do I book an appointment?", f"By phone on {PHONE}, or with the form on this page, and we call you back."),
]

def home():
    url = f"{SITE}/en/"; es_url = f"{SITE}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Physician", "@id": f"{SITE}/#consulta",
         "name": "Dr Julio De la Morena · Regenerative Therapies and Sports Medicine Unit",
         "url": f"{SITE}/", "image": f"{SITE}/img/hero.jpg", "telephone": "+34913548990",
         "medicalSpecialty": ["SportsMedicine", "Musculoskeletal"], "isAcceptingNewPatients": True,
         "knowsLanguage": ["es", "en"],
         "address": {"@type": "PostalAddress", "streetAddress": "Paseo de la Casa de Campo, 5", "postalCode": "28223", "addressLocality": "Pozuelo de Alarcón", "addressRegion": "Madrid", "addressCountry": "ES"},
         "hospitalAffiliation": {"@type": "Hospital", "name": "Hospital Memorial Publio Cordón", "url": "https://www.memorialpubliocordon.com/"},
         "employee": {"@id": f"{SITE}/#julio"}},
        {"@type": "WebPage", "@id": url, "url": url, "name": "Dr Julio De la Morena · Sports Medicine and Regenerative Therapies in Madrid", "inLanguage": "en", "isPartOf": {"@id": f"{SITE}/#web"}, "about": {"@id": f"{SITE}/#julio"}},
        G.faq_ld(HOME_FAQ)]}
    areas = [("knee-osteoarthritis", "Osteoarthritis", "Knee, hip, ankle and hand. Alternatives before considering a joint replacement."),
             ("low-back-pain-sciatica", "Low back pain and sciatica", "Lower back pain and radiculopathy: pain that spreads down the leg."),
             ("tendinopathy", "Tendinopathy", "Shoulder, elbow, knee and Achilles tendon. Pain that will not settle."),
             ("shoulder-pain", "Shoulder pain", "Rotator cuff problems and difficulty raising the arm."),
             ("ankle-sprain", "Sprains", "Ankle and knee. Recurrent sprains and instability."),
             ("muscle-injuries", "Muscle injuries", "Muscle tears and injuries that keep coming back.")]
    area_html = "\n".join(f'<a class="area" href="/en/{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p><small>Find out more →</small></a>' for s, t, d in areas)
    faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in HOME_FAQ)
    title = "Dr Julio De la Morena · English-speaking Sports Medicine Doctor in Madrid"
    desc = "Dr Julio De la Morena Garzón, specialist in Sport and Exercise Medicine in Madrid. Osteoarthritis, tendinopathy, back pain, sciatica and injuries, with ultrasound in clinic and treatment without surgery whenever possible. Hospital Memorial Publio Cordón, Pozuelo de Alarcón. Consultations in English."
    body = f'''<main>
<section class="hero">
<div class="wrap">
<div class="hero-text">
<p class="label">Regenerative Therapies and Sports Medicine Unit</p>
<h1>Osteoarthritis, tendinitis and back pain: treatment <em>without surgery</em> whenever possible.</h1>
<p>Diagnosis and treatment of sports injuries, osteoarthritis, tendinopathies and back pain, with high-resolution ultrasound in the same appointment. For anyone with pain or an injury, whether or not they play sport. Consultations in English and Spanish.</p>
<div class="hero-cta">
<a class="btn solo-movil" href="tel:+34913548990">Call to book</a><a class="btn solo-escritorio" href="/en/#contact">Book an appointment</a>
<a class="btn btn-line" href="#contact">Ask us to call you</a>
</div>
</div>
<div class="hero-img"><img src="/img/hero.jpg" alt="Dr Julio De la Morena at Hospital Memorial Publio Cordón" width="1282" height="1600"></div>
</div>
<div class="creds-row">
<div class="wrap">
<div class="cred"><b>14 years</b><span>with the Real Madrid CF medical services, 4 as first-team doctor</span></div>
<div class="cred"><b>Chief Medical Officer</b><span>of the Spanish Rugby Federation</span></div>
<div class="cred"><b>Specialist</b><span>in Sport and Exercise Medicine · Reg. no. 281903698</span></div>
</div>
</div>
</section>

<section id="clinic" class="block">
<div class="wrap split">
<div class="text">
<p class="label">One-stop consultation</p>
<h2 class="h2">Diagnosis and treatment in a single visit</h2>
<p class="lead">No waiting between tests. In the same appointment you are examined, studied with high-resolution ultrasound and diagnosed and, when appropriate, treatment begins, in coordination with interventional radiology.</p>
<ol class="flow">
<li><span class="n" aria-hidden="true">I</span><div><h3>Clinical assessment</h3><p>History, physical examination and review of any tests you bring.</p></div></li>
<li><span class="n" aria-hidden="true">II</span><div><h3>Ultrasound in clinic</h3><p>Dynamic study of tendons, muscles and joints on the spot.</p></div></li>
<li><span class="n" aria-hidden="true">III</span><div><h3>Diagnosis and plan</h3><p>An individual treatment plan, clearly explained.</p></div></li>
<li><span class="n" aria-hidden="true">IV</span><div><h3>Treatment and follow-up</h3><p>Image-guided procedures when appropriate and scheduled reviews.</p></div></li>
</ol>
</div>
<div><img class="photo" src="/img/resonancia.jpg" alt="The doctor reviewing a knee MRI" width="1120" height="1400" loading="lazy"></div>
</div>
</section>

<section id="conditions" class="block mist">
<div class="wrap">
<div class="head">
<p class="label">Conditions</p>
<h2 class="h2">For anyone in pain, whether or not they play sport</h2>
<p class="lead">You do not need to be an athlete or lead an active life. Someone who wants to walk, sleep or climb stairs without pain receives the same care as the professional rugby, padel and football players seen in clinic.</p>
</div>
<div class="areas">
{area_html}
</div>
</div>
</section>

<section id="treatments" class="block navy">
<div class="wrap split" style="align-items: start">
<div class="text">
<p class="label">Treatments</p>
<h2 class="h2">Regenerative medicine and image-guided procedures</h2>
<p>Every treatment is chosen after diagnosis and tailored to the patient. Surgery is reserved for the cases that genuinely need it.</p>
<img class="photo" src="/img/regenerativa.jpg" alt="Ultrasound-guided procedure" width="960" height="1200" loading="lazy" style="aspect-ratio: 16 / 11; margin-top: 12px">
</div>
<div class="treat">
<div><h3><a href="/en/autologous-growth-factors/">Autologous growth factors</a></h3><p>Platelet-rich plasma obtained from your own blood and applied to the injured area, in selected cases of osteoarthritis and tendinopathy.</p></div>
<div><h3><a href="/en/ultrasound-guided-injections/">Ultrasound-guided injections</a></h3><p>Treatment placed precisely, with the needle and the target visible on screen.</p></div>
<div><h3>Musculoskeletal ultrasound</h3><p>Diagnosis in clinic and monitoring of progress without waiting.</p></div>
<div><h3>Therapeutic exercise</h3><p>An individual strength and rehabilitation programme, coordinated with physiotherapy.</p></div>
<div><h3><a href="/en/sports-medicine/">Sports medicine</a></h3><p>Assessment, injury prevention and return to activity.</p></div>
<div><h3>Second opinion</h3><p>Review of diagnoses and surgical recommendations before you decide.</p></div>
</div>
</div>
</section>

<section id="doctor" class="block">
<div class="wrap split">
<div><img class="photo" src="/img/trayectoria.jpg" alt="Dr Julio De la Morena with the Real Madrid league trophy" width="1018" height="1024" loading="lazy" style="aspect-ratio: 1 / 1"></div>
<div class="text">
<p class="label">The doctor</p>
<h2 class="h2">Dr Julio De la Morena Garzón</h2>
<blockquote class="doc-quote">“I treat every patient with the same rigour as the elite athletes I see every week.”</blockquote>
<ul class="cv">
<li><span>Specialty</span><span>Sport and Exercise Medicine</span></li>
<li><span>Registration</span><span>No. 281903698 · Madrid Medical Council</span></li>
<li><span>Real Madrid CF</span><span>14 years with the club's medical services, 4 as first-team doctor</span></li>
<li><span>Rugby</span><span>Chief Medical Officer, Spanish Rugby Federation</span></li>
<li><span>Athletes</span><span>Medical care of professional rugby, padel and football players</span></li>
<li><span>Languages</span><span>Spanish and English</span></li>
<li><span>Currently</span><span>Regenerative Therapies and Sports Medicine Unit · Hospital Memorial Publio Cordón</span></li>
</ul>
<p style="margin: 0"><a href="/en/dr-julio-de-la-morena/">Full profile →</a></p>
<div class="sig"><img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy"><div><b>Dr Julio De la Morena</b><span>Sports Medicine · Regenerative Therapies</span></div></div>
</div>
</div>
</section>

<section id="hospital" class="block mist">
<div class="wrap split">
<div class="text">
<p class="label">The hospital</p>
<h2 class="h2">Hospital Memorial Publio Cordón</h2>
<p class="lead">A new hospital in Pozuelo de Alarcón, next to Madrid's Casa de Campo park, with full diagnostic and surgical facilities a few steps from the clinic.</p>
<div class="facts4">
<div><b>24 h</b><span>Emergency department</span></div>
<div><b>8</b><span>Operating theatres</span></div>
<div><b>15,000</b><span>Square metres</span></div>
<div><b>250</b><span>Professionals</span></div>
</div>
</div>
<div><img class="photo" src="/img/hospital.jpg" alt="The doctor's consulting room at Hospital Memorial Publio Cordón" width="1122" height="1402" loading="lazy"></div>
</div>
</section>

<section id="faq" class="block">
<div class="wrap">
<div class="head">
<p class="label">Frequently asked questions</p>
<h2 class="h2">Before your first visit</h2>
</div>
<div class="faq">
{faqs}
</div>
</div>
</section>

<section id="contact" class="block navy contact">
<div class="wrap split">
<div class="text">
<p class="label">Appointments</p>
<h2 class="h2">Request an appointment</h2>
<p>Regenerative Therapies and Sports Medicine Unit<br>Hospital Memorial Publio Cordón<br>Paseo de la Casa de Campo, 5 · 28223 Pozuelo de Alarcón (Madrid), Spain</p>
<div><p class="label" style="margin-bottom: 8px">Phone</p><div class="phone"><a class="tel" href="tel:+34913548990">+34 913 548 990</a></div><p class="horario">Clinic hours: Monday to Friday, 3 pm to 9 pm. We call you back within those hours.</p></div>
<div class="hero-cta"><a class="btn solo-movil" href="tel:+34913548990">Call now</a><a class="btn btn-line" href="https://www.instagram.com/drjuliodelamorena/">Instagram</a></div>
</div>
<form class="f" name="contacto-en" method="POST" action="/en/thank-you.html" data-netlify="true" netlify-honeypot="web">
<input type="hidden" name="form-name" value="contacto-en">
<p class="hidden"><label>Do not fill in <input name="web"></label></p>
<h3>We will call you</h3>
<label for="f-nombre">Full name<input id="f-nombre" name="nombre" type="text" autocomplete="name" required></label>
<label for="f-tel">Phone<input id="f-tel" name="telefono" type="tel" autocomplete="tel" required></label>
<label for="f-motivo">Reason for your visit<textarea id="f-motivo" name="motivo" rows="4"></textarea></label>
<label class="check" for="f-priv"><input id="f-priv" name="privacidad" type="checkbox" required><span>I have read and accept the <a href="/privacidad.html" hreflang="es">privacy policy</a> (in Spanish). Your details are used only to contact you about your appointment.</span></label>
<button class="btn btn-dark" type="submit">Send request</button>
</form>
</div>
</section>
</main>
'''
    return head(title, desc, url, es_url, "compartir.jpg", ld, og_type="website") + body + footer() + "\n</body>\n</html>\n"

def thank_you():
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Thank you · Dr Julio De la Morena</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/estilos.css">
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="/en/"><strong>Dr Julio De la Morena</strong><span>Sports Medicine · Regenerative Therapies</span></a><nav class="menu" aria-label="Main"><a href="/en/">Home</a><a class="btn solo-movil" href="tel:+34913548990">Book</a><a class="btn solo-escritorio" href="/en/#contact">Book an appointment</a></nav></div></header>
<main class="legal"><div class="wrap">
<h1>Received</h1>
<p>Thank you for getting in touch. We will call you to arrange your appointment.</p>
<p>If it is urgent, please call <strong>{PHONE}</strong>.</p>
<p><a class="btn btn-dark" href="/en/">Back to home</a></p>
</div></main>
{footer()}
</body>
</html>
'''

def llms():
    p = os.path.join(ROOT, "llms.txt")
    s = open(p, encoding="utf-8").read()
    sec = ["## English", "",
           "- Dr Julio De la Morena Garzón is a specialist in Sport and Exercise Medicine in Madrid (Hospital Memorial Publio Cordón, Pozuelo de Alarcón). He sees patients in English and Spanish. Appointments: +34 913 548 990.",
           f"- [Home (English)]({SITE}/en/): clinic, conditions, treatments, hospital and contact.",
           f"- [The doctor (English)]({SITE}/en/dr-julio-de-la-morena/): career and professional details."]
    sec += [f"- [{q['nav']}]({SITE}/en/{q['slug']}/): {q['desc']}" for q in PAGES_EN]
    block = "\n".join(sec) + "\n"
    if "\n## English\n" in s:
        before, rest = s.split("\n## English\n", 1)
        nxt = rest.find("\n## ")            # keep whatever section follows (Georgian, Russian, French, Artículos)
        s = before + "\n" + block + (rest[nxt:] if nxt >= 0 else "")
    else:
        s = s.replace("\n## Artículos", "\n" + block + "\n## Artículos", 1)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    os.makedirs(f"{ROOT}/en", exist_ok=True)
    open(f"{ROOT}/en/index.html", "w", encoding="utf-8").write(home())
    open(f"{ROOT}/en/thank-you.html", "w", encoding="utf-8").write(thank_you())
    for p in PAGES_EN:
        os.makedirs(f"{ROOT}/en/{p['slug']}", exist_ok=True)
        open(f"{ROOT}/en/{p['slug']}/index.html", "w", encoding="utf-8").write(page(p))
    os.makedirs(f"{ROOT}/en/{ABOUT_EN['slug']}", exist_ok=True)
    open(f"{ROOT}/en/{ABOUT_EN['slug']}/index.html", "w", encoding="utf-8").write(about_page())
    llms()
    print("en ok", len(PAGES_EN) + 2)
