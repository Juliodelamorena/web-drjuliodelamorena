"""Planes de ejercicio para pacientes, pensados para el móvil.

Uso: crear herramientas/planes/<slug>.json y ejecutar  python3 herramientas/planes.py
Genera planes/<slug>/index.html y la página planes/index.html.
Fotos opcionales: img/planes/<slug>/<n>.jpg (n = número de ejercicio, 1, 2, 3...).
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as G
from paginas import PAGES

ROOT, SITE, esc = G.ROOT, G.SITE, G.esc

SCRIPT = """<script>
(function(){
  var key='plan:'+location.pathname, done={};
  try{done=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}
  var boxes=document.querySelectorAll('.ex input[type=checkbox]');
  function count(){var n=0;boxes.forEach(function(b){if(b.checked)n++});
    document.querySelectorAll('[data-cuenta]').forEach(function(el){el.textContent=n+' de '+boxes.length+' hechos hoy'});}
  var hoy=new Date().toISOString().slice(0,10);
  if(done._dia!==hoy){done={_dia:hoy}}
  boxes.forEach(function(b){b.checked=!!done[b.id];b.addEventListener('change',function(){done[b.id]=b.checked;try{localStorage.setItem(key,JSON.stringify(done))}catch(e){}count();});});
  count();
  var tabs=document.querySelectorAll('.tab'),panes=document.querySelectorAll('.pane');
  tabs.forEach(function(t,i){t.addEventListener('click',function(){tabs.forEach(function(x){x.setAttribute('aria-selected','false')});panes.forEach(function(p){p.hidden=true});t.setAttribute('aria-selected','true');panes[i].hidden=false;try{localStorage.setItem(key+':fase',i)}catch(e){}});});
  try{var f=localStorage.getItem(key+':fase');if(f!==null&&tabs[f])tabs[f].click()}catch(e){}
  var pr=document.getElementById('imprimir');if(pr)pr.addEventListener('click',function(){panes.forEach(function(p){p.hidden=false});window.print();});
  window.addEventListener('afterprint',function(){var s=document.querySelector('.tab[aria-selected=true]');if(s)s.click();});
})();
</script>"""


def plan(p):
    url = f"{SITE}/planes/{p['slug']}/"
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
    fases_txt = "".join(f"<li><strong>{esc(a)}.</strong> {esc(b)}</li>" for a, b in p["elegir_fase"])
    antes = "".join(f"<li><strong>{esc(a)}.</strong> {esc(b)}</li>" for a, b in p["antes"])
    evitar = "".join(f"<li>{esc(x)}</li>" for x in p["evitar"])
    consultar = "".join(f"<li>{esc(x)}</li>" for x in p["consultar"])
    intro = "".join(f"<p>{esc(x)}</p>" for x in p["intro"])
    by = {q["slug"]: q for q in PAGES}
    rel = "".join(f'<a class="rel" href="/{s}/"><span>{esc(by[s]["nav"])}</span><span aria-hidden="true">→</span></a>' for s in p.get("relacionadas", []) if s in by)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url, "url": url, "name": p["titulo"], "description": p["descripcion"],
         "inLanguage": "es-ES", "lastReviewed": p["fecha"], "audience": {"@type": "Patient"},
         "about": {"@type": "MedicalCondition", "name": p["corto"]},
         "mainEntity": {"@type": "ExercisePlan", "name": p["titulo"], "activityFrequency": "Diaria, según la fase"},
         "author": G.DOCTOR_REF, "reviewedBy": G.DOCTOR_REF, "isPartOf": {"@id": f"{SITE}/#web"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Planes de ejercicio", "item": f"{SITE}/planes/"},
            {"@type": "ListItem", "position": 3, "name": p["corto"], "item": url}]}]}
    body = f'''<main class="article plan">
<article class="wrap">
<nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a><span aria-hidden="true">/</span><a href="/planes/">Planes de ejercicio</a><span aria-hidden="true">/</span><span>{esc(p['zona'])}</span></nav>
<p class="label">Plan de ejercicio · {esc(p['zona'])}</p>
<h1>{esc(p['titulo'])}</h1>
<div class="aviso"><strong>Plan orientativo.</strong> No sustituye una valoración médica ni el criterio de tu fisioterapeuta. Si el dolor aumenta de forma clara, para y consulta.</div>
<details class="bloque"><summary>Por qué este plan</summary>{intro}</details>
<div class="regla"><p class="label">La regla de oro</p><p>{esc(p['regla'])}</p></div>
<details class="bloque"><summary>¿En qué fase estás?</summary><p>Elige la fase por cómo está hoy el hombro, no por el tiempo que llevas.</p><ul>{fases_txt}</ul></details>
<details class="bloque"><summary>Antes de empezar</summary><ul>{antes}</ul></details>
<div class="plan-bar"><div class="tabs" role="tablist">{"".join(tabs)}</div><span class="cuenta" data-cuenta></span></div>
{"".join(panes)}
<details class="bloque"><summary>Qué evitar</summary><ul>{evitar}</ul></details>
<details class="bloque"><summary>Tratamiento complementario</summary><p>{esc(p['complementario'])}</p></details>
<div class="box"><h3>Cuándo consultar antes de la revisión</h3><ul>{consultar}</ul><p style="margin-top:12px">{esc(p['normal'])}</p></div>
<p class="no-print"><button class="btn btn-dark" id="imprimir" type="button">Imprimir o guardar en PDF</button></p>
<div class="cta-band no-print"><div><h3>¿No mejora como esperabas?</h3><p>Solicita una revisión · Hospital Memorial Publio Cordón · <a class="tel" href="tel:+34913548990">913 548 990</a> · lunes a viernes, de 15:00 a 21:00</p></div><a class="btn solo-movil" href="tel:+34913548990">Llamar para pedir cita</a><a class="btn solo-escritorio" href="/#contacto">Pedir cita</a></div>
<div class="byline"><img src="/img/retrato.jpg" alt="" width="480" height="480" loading="lazy"><p>Plan elaborado por el <a href="/dr-julio-de-la-morena/">Dr. Julio De la Morena Garzón</a>, especialista en Medicina de la Educación Física y del Deporte (colegiado nº 281903698), Unidad de Terapias Regenerativas y Medicina Deportiva del Hospital Memorial Publio Cordón.</p></div>
<div class="related no-print">{('<p class="label">Relacionado</p>' + rel) if rel else ''}</div>
</article>
</main>
{SCRIPT}
'''
    return G.head(p["titulo"] + " · Dr. Julio De la Morena", p["descripcion"], url, "retrato.jpg", ld) + body + G.footer() + "\n</body>\n</html>\n"


def indice(planes):
    url = f"{SITE}/planes/"
    cards = "\n".join(f'<a class="card" href="/planes/{p["slug"]}/"><span class="meta">{esc(p["zona"])}</span><h3>{esc(p["corto"])}</h3><p>{esc(str(sum(len(f["ejercicios"]) for f in p["fases"])))} ejercicios en {len(p["fases"])} fases · pensado para el móvil</p></a>' for p in planes)
    body = f'''<main class="block"><div class="wrap">
<div class="head"><p class="label">Planes de ejercicio</p><h1 class="h2">Planes de ejercicio para casa</h1>
<p class="lead">Planes por fases elaborados por el Dr. Julio De la Morena para sus pacientes. Ábrelos en el móvil, marca los ejercicios que vas haciendo cada día o imprímelos. Son orientativos: no sustituyen una valoración.</p></div>
<div class="cards">{cards}</div></div></main>
'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "url": url, "name": "Planes de ejercicio del Dr. Julio De la Morena", "inLanguage": "es-ES", "author": G.DOCTOR_REF}
    return G.head("Planes de ejercicio · Dr. Julio De la Morena", "Planes de ejercicio por fases para casa, pensados para el móvil: capsulitis, lumbalgia y más. Dr. Julio De la Morena, Hospital Memorial Publio Cordón.", url, "retrato.jpg", ld) + body + G.footer() + "\n</body>\n</html>\n"


def cargar():
    ps = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(os.path.dirname(__file__), "planes", "*.json"))]
    return sorted(ps, key=lambda p: (p["zona"], p["corto"]))


if __name__ == "__main__":
    ps = cargar()
    for p in ps:
        d = os.path.join(ROOT, "planes", p["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(plan(p))
    open(os.path.join(ROOT, "planes", "index.html"), "w", encoding="utf-8").write(indice(ps))
    print("planes:", len(ps))
