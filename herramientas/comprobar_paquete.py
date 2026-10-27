"""Checks that a language pack (paginas_<lang>.py) has the same structure as paginas_plantilla.py.

Usage: python3 herramientas/comprobar_paquete.py ka
"""
import importlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paginas_plantilla as T

lang = sys.argv[1]
P = importlib.import_module(f"paginas_{lang}")
errs = []

def same_keys(a, b, where):
    if set(a) != set(b):
        errs.append(f"{where}: keys differ: missing {set(a) - set(b)} extra {set(b) - set(a)}")

def tags(s):
    return re.findall(r"</?[a-z0-9]+", s) + re.findall(r"\{\{[A-Z_]+\}\}|\{phone\}", s)

def same_tags(a, b, where):
    if sorted(tags(a)) != sorted(tags(b)):
        errs.append(f"{where}: HTML tags/tokens differ\n   template: {sorted(tags(a))}\n   pack:     {sorted(tags(b))}")

def not_english(s, where):
    if lang != "fr" and re.search(r"\b(the|and|with|without|pain|knee)\b", s):
        errs.append(f"{where}: looks untranslated: {s[:70]!r}")

# META
same_keys(T.META, P.META, "META")
if P.META["lang"] != lang: errs.append("META.lang must be " + lang)
# SLUGS
same_keys(T.SLUGS, P.SLUGS, "SLUGS")
for k, v in P.SLUGS.items():
    if not re.fullmatch(r"[a-z0-9-]*", v): errs.append(f"SLUGS[{k}]: slug must be lowercase ASCII with hyphens: {v}")
# PAGES
if len(T.PAGES) != len(P.PAGES): errs.append(f"PAGES: {len(T.PAGES)} expected, {len(P.PAGES)} found")
slugs = {p["slug"] for p in P.PAGES}
for t, p in zip(T.PAGES, P.PAGES):
    w = f"PAGES[{t['slug']}]"
    same_keys(t, p, w)
    if p.get("es") != t["es"]: errs.append(f"{w}: 'es' must be {t['es']}")
    if P.SLUGS.get(t["es"]) != p.get("slug"): errs.append(f"{w}: slug {p.get('slug')} must equal SLUGS[{t['es']}]")
    for k in ("img", "img_wh", "label"):
        pass
    if p["img"] != t["img"] or tuple(p["img_wh"]) != tuple(t["img_wh"]): errs.append(f"{w}: img/img_wh changed")
    if p["about"][0] != t["about"][0]: errs.append(f"{w}: about type changed")
    if len(p["sections"]) != len(t["sections"]): errs.append(f"{w}: sections count")
    for (tt, tb), (pt, pb) in zip(t["sections"], p["sections"]):
        same_tags(tb, pb, f"{w} section {tt!r}")
        not_english(pb, f"{w} section {tt!r}")
    if len(p["faq"]) != len(t["faq"]): errs.append(f"{w}: faq count")
    for s in p["related"]:
        if s not in slugs: errs.append(f"{w}: related slug {s} not in this pack's slugs")
    rel_es = [T.SLUGS and k for k in t["related"]]
    for a, b in zip(t["related"], p["related"]):
        es_of = {v: k for k, v in T.SLUGS.items()}[a]
        if P.SLUGS[es_of] != b: errs.append(f"{w}: related must be [{', '.join(P.SLUGS[{v: k for k, v in T.SLUGS.items()}[x]] for x in t['related'])}]")
        break
    not_english(p["lead"], f"{w} lead")
# UI
same_keys(T.UI, P.UI, "UI")
for k in T.UI:
    if k in P.UI: same_tags(T.UI[k], P.UI[k], f"UI[{k}]")
# HOME
same_keys(T.HOME, P.HOME, "HOME")
for k in ("creds", "flow", "areas", "treat_items", "abroad_steps", "doctor_cv", "facts"):
    if k in P.HOME and len(P.HOME[k]) != len(T.HOME[k]): errs.append(f"HOME[{k}]: length")
for s, _, _ in P.HOME.get("areas", []):
    if s not in slugs: errs.append(f"HOME.areas: slug {s} not in pack")
for s, _, _ in P.HOME.get("treat_items", []):
    if s and s not in slugs: errs.append(f"HOME.treat_items: slug {s} not in pack")
for k in ("hero_h1", "contact_addr", "hero_btn_call"):
    if k in P.HOME: same_tags(T.HOME[k], P.HOME[k], f"HOME[{k}]")
if len(P.HOME_FAQ) != len(T.HOME_FAQ): errs.append("HOME_FAQ: length")
# ABOUT
same_keys(T.ABOUT, P.ABOUT, "ABOUT")
if len(P.ABOUT["sections"]) != len(T.ABOUT["sections"]): errs.append("ABOUT.sections: length")
for (tt, tb), (pt, pb) in zip(T.ABOUT["sections"], P.ABOUT["sections"]):
    same_tags(tb, pb, f"ABOUT section {tt!r}")
if len(P.ABOUT["faq"]) != len(T.ABOUT["faq"]): errs.append("ABOUT.faq: length")
if P.ABOUT["slug"] != P.SLUGS["dr-julio-de-la-morena"]: errs.append("ABOUT.slug must equal SLUGS['dr-julio-de-la-morena']")

print("\n".join(errs) if errs else f"paginas_{lang}.py: structure ok")
sys.exit(1 if errs else 0)
