"""Builds one translated version of the site (/ka/, /ru/, /fr/) from a language pack.

Usage: python3 herramientas/generar_i18n.py ka     (or ru, fr, or "all")
Pack: herramientas/paginas_<lang>.py — same structure as paginas_plantilla.py (checked by comprobar_paquete.py).
Builds /<lang>/index.html, /<lang>/<slug>/index.html, the doctor page, the thank-you page,
and refreshes the "## <Language>" section of llms.txt. Spanish and English pages get their
hreflang links from idiomas.py, so run generar.py and generar_en.py after adding a language.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as G
import idiomas as I

ROOT, SITE, FONTS, esc, REVISION, DOCTOR_REF, CITA = G.ROOT, G.SITE, G.FONTS, G.esc, G.REVISION, G.DOCTOR_REF, G.CITA
PHONE = "+34 913 548 990"
TEL = "tel:+34913548990"


class Builder:
    def __init__(self, lang):
        self.L = lang
        self.P = I.pack(lang)
        self.M, self.UI, self.H = self.P.META, self.P.UI, self.P.HOME
        self.pages = self.P.PAGES
        self.by = {p["slug"]: p for p in self.pages}
        self.base = f"/{lang}/"
        self.about_path = self.base + self.P.ABOUT["slug"] + "/"

    # ---------- helpers ----------
    def t(self, key, **kw):
        s = self.UI[key].replace("{phone}", PHONE)
        s = s.replace("{{DOCTOR_URL}}", self.about_path)
        for k, v in kw.items():
            s = s.replace("{" + k + "}", v)
        return s

    def h(self, key):
        return self.H[key].replace("{phone}", PHONE)

    def fonts(self):
        return FONTS + self.M.get("extra_fonts", "")

    def font_css(self):
        c = self.M.get("font_css", "")
        return f"<style>{c}</style>\n" if c else ""

    # ---------- chrome ----------
    def header(self, es_slug):
        UI, b = self.UI, self.base
        return f'''<div class="util">
<div class="wrap">
<span class="util-addr">{esc(UI["util_addr"])}</span>
<span>{esc(UI["util_appt"])} <a class="tel" href="{TEL}">{PHONE}</a><span class="util-hor"> · {esc(UI["util_hours"])}</span></span>
</div>
</div>
<header class="top">
<div class="wrap">
<a class="brand" href="{b}"><strong>Dr. Julio De la Morena</strong><span>{esc(UI["brand_sub"])}</span></a>
<nav class="menu" aria-label="Menu">
<a href="{b}#conditions">{esc(UI["menu_conditions"])}</a>
<a href="{b}#treatments">{esc(UI["menu_treatments"])}</a>
<a href="{self.about_path}">{esc(UI["menu_doctor"])}</a>
{I.menu(self.L, es_slug, UI["lang_menu"])}
<a class="btn" href="{b}#contact">{esc(UI["menu_write"])}</a>
</nav>
</div>
</header>'''

    def footer(self, es_slug=""):
        UI, b = self.UI, self.base
        links = "".join(f'<a href="{b}{p["slug"]}/">{esc(p["nav"])}</a>' for p in self.pages)
        return f'''<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-col">
<strong class="foot-brand">Dr. Julio De la Morena</strong>
<span>{esc(UI["foot_unit"])}</span>
<span>{esc(UI["foot_addr"])}</span>
<span>{esc(self.t("foot_appt")).replace(PHONE, f'<a class="tel" href="{TEL}">{PHONE}</a>')}</span>
</div>
<nav class="foot-col foot-links" aria-label="{esc(UI["foot_nav_label"])}">{links}<a href="{self.about_path}">{esc(UI["menu_doctor"])}</a>{I.footer_links(self.L, es_slug)}</nav>
</div>
<div class="wrap foot-legal">
<span>{esc(UI["foot_legal"])}</span>
<nav aria-label="Legal"><a href="/aviso-legal.html" hreflang="es">{esc(UI["legal_notice"])}</a><a href="/privacidad.html" hreflang="es">{esc(UI["privacy"])}</a></nav>
</div>
</footer>
<nav class="cta-fija" aria-label="{esc(UI["bar_label"])}"><a class="llamar" href="{TEL}">{esc(self.t("bar_call"))}</a><a class="cita" href="{b}#contact">{esc(UI["bar_write"])}</a></nav>'''

    def head(self, title, desc, es_slug, img, ld, og_type="article"):
        url = SITE + I.path_for(self.L, es_slug)
        return f'''<!doctype html>
<html lang="{self.L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{I.alternates(es_slug)}<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{self.M["locale"]}">
{I.og_alternates(self.L)}<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{self.fonts()}">
<link rel="stylesheet" href="/estilos.css">
{self.font_css()}<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
{self.header(es_slug)}
'''

    def breadcrumb(self, name, url):
        return {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": self.UI["crumb_home"], "item": SITE + self.base},
            {"@type": "ListItem", "position": 2, "name": name, "item": url}]}

    def cta(self, title=None):
        UI, b = self.UI, self.base
        loc = esc(self.t("cta_location")).replace(PHONE, f'<a class="tel" href="{TEL}">{PHONE}</a>')
        return f'''<div class="cta-band">
<div><h3>{esc(title or UI["cta_default"])}</h3><p class="ventaja">{esc(UI["cta_ventaja"])}</p><p>{loc}</p></div>
<a class="btn" href="{b}#contact">{esc(UI["cta_btn_write"])}</a>
</div>'''

    def contact_form(self):
        UI = self.UI
        return f'''<form class="f" name="contacto-{self.L}" method="POST" action="{self.base}{self.M["thanks"]}" data-netlify="true" netlify-honeypot="web">
<input type="hidden" name="form-name" value="contacto-{self.L}">
<p class="hidden"><label>Do not fill in <input name="web"></label></p>
<h3>{esc(UI["form_title"])}</h3>
<label for="f-nombre">{esc(UI["form_name"])}<input id="f-nombre" name="nombre" type="text" autocomplete="name" required></label>
<label for="f-email">{esc(UI["form_email"])}<input id="f-email" name="email" type="email" autocomplete="email" required></label>
<label for="f-tel">{esc(UI["form_phone"])}<input id="f-tel" name="telefono" type="tel" autocomplete="tel"></label>
<label for="f-motivo">{esc(UI["form_reason"])}<textarea id="f-motivo" name="motivo" rows="4"></textarea></label>
<label class="check" for="f-priv"><input id="f-priv" name="privacidad" type="checkbox" required><span>{UI["form_privacy"]}</span></label>
<button class="btn btn-dark" type="submit">{esc(UI["form_submit"])}</button>
</form>'''

    def second_opinion_form(self):
        UI = self.UI
        return f'''<form class="f f-line" name="segunda-opinion-{self.L}" method="POST" action="{self.base}{self.M["thanks"]}" data-netlify="true" netlify-honeypot="web"><input type="hidden" name="form-name" value="segunda-opinion-{self.L}"><p class="hidden"><label>Do not fill in <input name="web"></label></p><h3>{esc(UI["so_form_title"])}</h3><label for="so-nombre">{esc(UI["so_name"])}<input id="so-nombre" name="nombre" type="text" autocomplete="name" required></label><label for="so-email">{esc(UI["so_email"])}<input id="so-email" name="email" type="email" autocomplete="email" required></label><label for="so-tel">{esc(UI["so_phone"])}<input id="so-tel" name="telefono" type="tel" autocomplete="tel"></label><label for="so-ciudad">{esc(UI["so_city"])}<input id="so-ciudad" name="ciudad" type="text"></label><label for="so-mod">{esc(UI["so_mod"])}<select id="so-mod" name="modalidad" required><option value="">{esc(UI["so_mod_choose"])}</option><option>{esc(UI["so_mod_report"])}</option><option>{esc(UI["so_mod_video"])}</option></select></label><label for="so-caso">{esc(UI["so_case"])}<textarea id="so-caso" name="caso" rows="5" required></textarea></label><label class="check" for="so-priv"><input id="so-priv" name="privacidad" type="checkbox" required><span>{UI["so_privacy"]}</span></label><button class="btn btn-dark" type="submit">{esc(UI["so_submit"])}</button></form>'''

    # ---------- pages ----------
    def page(self, p):
        UI, b = self.UI, self.base
        url = SITE + b + p["slug"] + "/"
        atype, aname, alt_names = p["about"]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "MedicalWebPage", "@id": url, "url": url, "name": p["seo"], "description": p["desc"],
             "inLanguage": self.L, "about": {"@type": atype, "name": aname, "alternateName": alt_names},
             "audience": {"@type": "Patient"}, "lastReviewed": REVISION, "datePublished": REVISION,
             "author": DOCTOR_REF, "reviewedBy": DOCTOR_REF, "primaryImageOfPage": f"{SITE}/img/{p['img']}",
             "isPartOf": {"@id": f"{SITE}/#web"}},
            self.breadcrumb(p["nav"], url), G.faq_ld([(q, a.replace("{phone}", PHONE)) for q, a in p["faq"]])]}
        w, h = p["img_wh"]
        secs = "\n".join(f'<h2>{esc(t)}</h2>\n{body.replace("{{FORM_SEGUNDA}}", self.second_opinion_form()).replace("{phone}", PHONE)}' for t, body in p["sections"])
        faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a.replace("{phone}", PHONE))}</p></details>' for q, a in p["faq"])
        rel = "".join(f'<a class="rel" href="{b}{s}/"><span>{esc(self.by[s]["nav"])}</span><span aria-hidden="true">→</span></a>' for s in p["related"])
        anchor = "conditions" if p["label"] == self.pages[0]["label"] else "treatments"
        body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="{esc(UI["crumb_label"])}"><a href="{b}">{esc(UI["crumb_home"])}</a><span aria-hidden="true">/</span><a href="{b}#{anchor}">{esc(p['label'])}</a><span aria-hidden="true">/</span><span>{esc(p['nav'])}</span></nav>
<p class="label">{esc(p['label'])}</p>
<h1>{esc(p['h1'])}</h1>
<p class="answer">{esc(p['lead'])}</p>
<img class="wide" src="/img/{p['img']}" alt="{esc(p['img_alt'])}" width="{w}" height="{h}">
{secs}
<h2>{esc(UI["faq_title"])}</h2>
<div class="faq">
{faqs}
</div>
{self.cta(p.get("cta") or None)}
<div class="byline">
<img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy">
<p>{self.t("byline")}</p>
</div>
<div class="related"><p class="label">{esc(UI["related"])}</p>{rel}</div>
</article>
</main>
'''
        return self.head(p["seo"], p["desc"], p["es"], p["img"], ld) + body + self.footer(p["es"]) + "\n</body>\n</html>\n"

    def about_page(self):
        a, UI, b = self.P.ABOUT, self.UI, self.base
        url = SITE + self.about_path
        faq = [(q, x.replace("{phone}", PHONE)) for q, x in a["faq"]]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "ProfilePage", "@id": url, "url": url, "name": a["seo"], "inLanguage": self.L,
             "mainEntity": {"@id": f"{SITE}/#julio"}, "dateModified": REVISION + "T09:00:00+02:00", "isPartOf": {"@id": f"{SITE}/#web"}},
            {"@type": "Person", "@id": f"{SITE}/#julio", "name": "Julio De la Morena Garzón",
             "alternateName": ["Dr Julio De la Morena", "Dr. Julio De la Morena", "Julio de la Morena"], "honorificPrefix": "Dr",
             "jobTitle": "Specialist in Sport and Exercise Medicine",
             "image": f"{SITE}/img/retrato.jpg", "url": f"{SITE}/",
             "worksFor": {"@type": "Hospital", "name": "Hospital Memorial Publio Cordón", "url": "https://www.memorialpubliocordon.com/"},
             "memberOf": [{"@type": "SportsOrganization", "name": "Real Federación Española de Rugby"}, {"@type": "Organization", "name": "Ilustre Colegio Oficial de Médicos de Madrid"}],
             "knowsAbout": [p["about"][1] for p in self.pages],
             "knowsLanguage": ["es", "en"],
             "identifier": {"@type": "PropertyValue", "propertyID": "Número de colegiado", "value": "281903698"},
             "sameAs": ["https://www.instagram.com/drjuliodelamorena/", CITA]},
            self.breadcrumb(a["nav"], url), G.faq_ld(faq)]}
        areas = "".join(f'<li><a href="{b}{p["slug"]}/">{esc(p["nav"])}</a></li>' for p in self.pages)
        faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(x)}</p></details>' for q, x in faq)
        secs = "\n".join(f'<h2>{esc(t)}</h2>\n{body}' for t, body in a["sections"])
        body = f'''<main class="article">
<article class="wrap">
<nav class="crumbs" aria-label="{esc(UI["crumb_label"])}"><a href="{b}">{esc(UI["crumb_home"])}</a><span aria-hidden="true">/</span><span>{esc(a["nav"])}</span></nav>
<p class="label">{esc(a["nav"])}</p>
<h1>{esc(a['h1'])}</h1>
<p class="answer">{esc(a["answer"])}</p>
<img class="wide" src="/img/trayectoria.jpg" alt="{esc(a["img_alt"])}" width="1018" height="1024" style="aspect-ratio: 4 / 3; object-position: center 30%">
{secs}
<h2>{esc(UI["about_treats"])}</h2>
<ul class="arealist">{areas}</ul>
<h2>{esc(UI["faq_title"])}</h2>
<div class="faq">
{faqs}
</div>
{self.cta()}
</article>
</main>
'''
        return self.head(a["seo"], a["desc"], a["es"], "retrato.jpg", ld) + body + self.footer(a["es"]) + "\n</body>\n</html>\n"

    def home(self):
        H, UI, b = self.H, self.UI, self.base
        url = SITE + b
        faq = [(q, a.replace("{phone}", PHONE)) for q, a in self.P.HOME_FAQ]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Physician", "@id": f"{SITE}/#consulta",
             "name": "Dr. Julio De la Morena · Unidad de Terapias Regenerativas y Medicina Deportiva",
             "url": f"{SITE}/", "image": f"{SITE}/img/hero.jpg", "telephone": "+34913548990",
             "medicalSpecialty": ["SportsMedicine", "Musculoskeletal"], "isAcceptingNewPatients": True,
             "knowsLanguage": ["es", "en"],
             "address": {"@type": "PostalAddress", "streetAddress": "Paseo de la Casa de Campo, 5", "postalCode": "28223", "addressLocality": "Pozuelo de Alarcón", "addressRegion": "Madrid", "addressCountry": "ES"},
             "hospitalAffiliation": {"@type": "Hospital", "name": "Hospital Memorial Publio Cordón", "url": "https://www.memorialpubliocordon.com/"},
             "employee": {"@id": f"{SITE}/#julio"}},
            {"@type": "WebPage", "@id": url, "url": url, "name": H["title"], "inLanguage": self.L, "isPartOf": {"@id": f"{SITE}/#web"}, "about": {"@id": f"{SITE}/#julio"}},
            G.faq_ld(faq)]}
        creds = "\n".join(f'<div class="cred"><b>{esc(x)}</b><span>{esc(y)}</span></div>' for x, y in H["creds"])
        roman = ["I", "II", "III", "IV", "V"]
        flow = "\n".join(f'<li><span class="n" aria-hidden="true">{roman[i]}</span><div><h3>{esc(x)}</h3><p>{esc(y)}</p></div></li>' for i, (x, y) in enumerate(H["flow"]))
        abroad = "\n".join(f'<li><span class="n" aria-hidden="true">{roman[i]}</span><div><h3>{esc(x)}</h3><p>{esc(y)}</p></div></li>' for i, (x, y) in enumerate(H["abroad_steps"]))
        areas = "\n".join(f'<a class="area" href="{b}{s}/"><h3>{esc(t)}</h3><p>{esc(d)}</p><small>{esc(H["more"])}</small></a>' for s, t, d in H["areas"])
        treats = "\n".join((f'<div><h3><a href="{b}{s}/">{esc(t)}</a></h3><p>{esc(d)}</p></div>' if s else f'<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>') for s, t, d in H["treat_items"])
        cv = "\n".join(f'<li><span>{esc(k)}</span><span>{esc(v)}</span></li>' for k, v in H["doctor_cv"])
        facts = "\n".join(f'<div><b>{esc(x)}</b><span>{esc(y)}</span></div>' for x, y in H["facts"])
        faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
        body = f'''<main>
<section class="hero">
<div class="wrap">
<div class="hero-text">
<p class="label">{esc(H["hero_label"])}</p>
<h1>{H["hero_h1"]}</h1>
<p>{esc(H["hero_p"])}</p>
<div class="hero-cta">
<a class="btn" href="#contact">{esc(H["hero_btn_write"])}</a>
<a class="btn btn-line" href="{TEL}">{esc(self.h("hero_btn_call"))}</a>
</div>
</div>
<div class="hero-img"><img src="/img/hero.jpg" alt="{esc(H["hero_img_alt"])}" width="1282" height="1600"></div>
</div>
<div class="creds-row">
<div class="wrap">
{creds}
</div>
</div>
</section>

<section id="clinic" class="block">
<div class="wrap split">
<div class="text">
<p class="label">{esc(H["clinic_label"])}</p>
<h2 class="h2">{esc(H["clinic_h2"])}</h2>
<p class="lead">{esc(H["clinic_lead"])}</p>
<ol class="flow">
{flow}
</ol>
</div>
<div><img class="photo" src="/img/resonancia.jpg" alt="{esc(H["clinic_img_alt"])}" width="1120" height="1400" loading="lazy"></div>
</div>
</section>

<section id="conditions" class="block mist">
<div class="wrap">
<div class="head">
<p class="label">{esc(H["cond_label"])}</p>
<h2 class="h2">{esc(H["cond_h2"])}</h2>
<p class="lead">{esc(H["cond_lead"])}</p>
</div>
<div class="areas">
{areas}
</div>
</div>
</section>

<section id="treatments" class="block navy">
<div class="wrap split" style="align-items: start">
<div class="text">
<p class="label">{esc(H["treat_label"])}</p>
<h2 class="h2">{esc(H["treat_h2"])}</h2>
<p>{esc(H["treat_p"])}</p>
<img class="photo" src="/img/regenerativa.jpg" alt="{esc(H["treat_img_alt"])}" width="960" height="1200" loading="lazy" style="aspect-ratio: 16 / 11; margin-top: 12px">
</div>
<div class="treat">
{treats}
</div>
</div>
</section>

<section id="abroad" class="block">
<div class="wrap split">
<div class="text">
<p class="label">{esc(H["abroad_label"])}</p>
<h2 class="h2">{esc(H["abroad_h2"])}</h2>
<p class="lead">{esc(H["abroad_lead"])}</p>
<ol class="flow">
{abroad}
</ol>
<p class="nota">{esc(H["abroad_note"])}</p>
<p style="margin: 0"><a class="btn" href="#contact">{esc(H["hero_btn_write"])}</a></p>
</div>
<div><img class="photo" src="/img/consulta.jpg" alt="{esc(self.pages[3]["img_alt"])}" width="960" height="1200" loading="lazy"></div>
</div>
</section>

<section id="doctor" class="block mist">
<div class="wrap split">
<div><img class="photo" src="/img/trayectoria.jpg" alt="{esc(H["doctor_img_alt"])}" width="1018" height="1024" loading="lazy" style="aspect-ratio: 1 / 1"></div>
<div class="text">
<p class="label">{esc(H["doctor_label"])}</p>
<h2 class="h2">{esc(H["doctor_h2"])}</h2>
<blockquote class="doc-quote">{esc(H["doctor_quote"])}</blockquote>
<ul class="cv">
{cv}
</ul>
<p style="margin: 0"><a href="{self.about_path}">{esc(H["doctor_link"])}</a></p>
<div class="sig"><img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy"><div><b>Dr. Julio De la Morena</b><span>{esc(H["sig_sub"])}</span></div></div>
</div>
</div>
</section>

<section id="hospital" class="block">
<div class="wrap split">
<div class="text">
<p class="label">{esc(H["hospital_label"])}</p>
<h2 class="h2">{esc(H["hospital_h2"])}</h2>
<p class="lead">{esc(H["hospital_lead"])}</p>
<div class="facts4">
{facts}
</div>
</div>
<div><img class="photo" src="/img/hospital.jpg" alt="{esc(H["hospital_img_alt"])}" width="1122" height="1402" loading="lazy"></div>
</div>
</section>

<section id="faq" class="block mist">
<div class="wrap">
<div class="head">
<p class="label">{esc(H["faq_label"])}</p>
<h2 class="h2">{esc(H["faq_h2"])}</h2>
</div>
<div class="faq">
{faqs}
</div>
</div>
</section>

<section id="contact" class="block navy contact">
<div class="wrap split">
<div class="text">
<p class="label">{esc(H["contact_label"])}</p>
<h2 class="h2">{esc(H["contact_h2"])}</h2>
<p>{H["contact_addr"]}</p>
<div><p class="label" style="margin-bottom: 8px">{esc(H["contact_phone_label"])}</p><div class="phone"><a class="tel" href="{TEL}">{PHONE}</a></div><p class="horario">{esc(H["contact_horario"])}</p></div>
<div class="hero-cta"><a class="btn solo-movil" href="{TEL}">{esc(H["contact_btn_call"])}</a><a class="btn btn-line" href="https://www.instagram.com/drjuliodelamorena/">{esc(H["contact_instagram"])}</a></div>
</div>
{self.contact_form()}
</div>
</section>
</main>
'''
        return self.head(H["title"], H["desc"], "", "compartir.jpg", ld, og_type="website") + body + self.footer("") + "\n</body>\n</html>\n"

    def thank_you(self):
        UI, b = self.UI, self.base
        return f'''<!doctype html>
<html lang="{self.L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(UI["thanks_title"])}</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{self.fonts()}">
<link rel="stylesheet" href="/estilos.css">
{self.font_css()}</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="{b}"><strong>Dr. Julio De la Morena</strong><span>{esc(UI["brand_sub"])}</span></a><nav class="menu" aria-label="Menu"><a href="{b}">{esc(UI["crumb_home"])}</a><a class="btn" href="{b}#contact">{esc(UI["menu_write"])}</a></nav></div></header>
<main class="legal"><div class="wrap">
<h1>{esc(UI["thanks_h1"])}</h1>
<p>{esc(UI["thanks_p1"])}</p>
<p>{esc(self.t("thanks_p2")).replace(PHONE, f"<strong>{PHONE}</strong>")}</p>
<p><a class="btn btn-dark" href="{b}">{esc(UI["thanks_back"])}</a></p>
</div></main>
{self.footer("")}
</body>
</html>
'''

    def llms(self):
        p = os.path.join(ROOT, "llms.txt")
        s = open(p, encoding="utf-8").read()
        names = {"ka": "Georgian (ქართული)", "ru": "Russian (Русский)", "fr": "French (Français)"}
        heading = f"## {names.get(self.L, self.M['name'])}"
        sec = [heading, "",
               f"- {self.H['desc']}",
               f"- [Home ({self.M['name']})]({SITE}{self.base})",
               f"- [{self.P.ABOUT['nav']}]({SITE}{self.about_path}): {self.P.ABOUT['desc']}"]
        sec += [f"- [{q['nav']}]({SITE}{self.base}{q['slug']}/): {q['desc']}" for q in self.pages]
        block = "\n".join(sec) + "\n"
        marker = "\n" + heading + "\n"
        if marker in s:
            before, rest = s.split(marker, 1)
            nxt = rest.find("\n## ")
            after = rest[nxt:] if nxt >= 0 else ""
            s = before + "\n" + block + after
        else:
            s = s.replace("\n## Artículos", "\n" + block + "\n## Artículos", 1)
        open(p, "w", encoding="utf-8").write(s)

    def build(self):
        d = os.path.join(ROOT, self.L)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(self.home())
        open(os.path.join(d, self.M["thanks"]), "w", encoding="utf-8").write(self.thank_you())
        for p in self.pages:
            os.makedirs(os.path.join(d, p["slug"]), exist_ok=True)
            open(os.path.join(d, p["slug"], "index.html"), "w", encoding="utf-8").write(self.page(p))
        os.makedirs(os.path.join(d, self.P.ABOUT["slug"]), exist_ok=True)
        open(os.path.join(d, self.P.ABOUT["slug"], "index.html"), "w", encoding="utf-8").write(self.about_page())
        self.llms()
        print(self.L, "ok", len(self.pages) + 2)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    for code in (I.PACKS if arg == "all" else [arg]):
        Builder(code).build()
