# Cambio de nombre y ajustes de portada (3 nov 2026)

The doctor has decided that on his website the treatment is no longer called "autologous growth factors"
(factores de crecimiento autólogos). From now on it is called **PRP (platelet-rich plasma)**, everywhere.

## Your job, for ONE language (given in your task)

### A. Rename the treatment in every file of your language
- First mention in a page/article/section: "PRP (<platelet-rich plasma in your language>)". Later mentions: "PRP".
  - en: PRP (platelet-rich plasma)
  - fr: PRP (plasma riche en plaquettes)
  - ru: PRP (плазма, обогащённая тромбоцитами)  — "PRP" in Latin letters; decline the explanatory noun if needed
  - ka: PRP (თრომბოციტებით მდიდარი პლაზმა)
- Rewrite each sentence so the grammar is correct (singular "PRP" vs plural "growth factors": fix verbs, articles,
  adjectives, cases). Do NOT do blind find/replace; read every sentence.
- Where the text already says "growth factors (PRP)" or "PRP / platelet-rich plasma ... growth factors", simplify so it
  is not redundant. A sentence may still explain, once, that PRP releases growth factors from the patient's own
  blood, where that is useful medical explanation (e.g. "how it works" sections, the evidence article). Do not delete
  medical content; just stop using "autologous growth factors" as the name of the treatment.
- Page titles, meta descriptions (keep ≤155 chars), nav labels, H1/H2, FAQ, JSON-LD names, image alts: all use PRP.
- Do NOT change URLs/slugs, image file names, dict keys, the Spanish slug "factores-crecimiento-autologos", or any
  `es` key that maps to the Spanish slug.
- Do NOT touch subtitle files (*.vtt): they transcribe what the doctor says in the videos.

### B. Home page and contact wording (only where your language has equivalent text)
1. Never promise "diagnosis and treatment in a single visit" as a flat promise. Use the idea:
   "A full assessment and a clear plan at the first visit; ultrasound and treatment the same day when indicated."
2. "First consultation without obligation/commitment" can be read as "free". Replace with the idea:
   "The first consultation does not commit you to treatment: if no treatment is indicated, we will tell you."
3. Callback commitment (wherever the text says "we call you back"): "We will call you back within 24 hours
   (next working day if it falls on a weekend or holiday)." Make it read nicely.
4. Where the page explains how to book by phone, add: "When you call, just say you would like an appointment with
   Dr De la Morena." (keep the doctor's name exactly "Dr De la Morena" / as your language pack already writes it).
5. Where the page describes the hospital/location (hospital section, address/"how to get there"), add one short
   phrase: the hospital has its own car park (parking).

### Files
- Pack files for your language: `herramientas/paginas_<l>.py`, `herramientas/paginas_nuevas_<l>.py`
  (for en: `paginas_en.py`, `paginas_nuevas_en.py` AND the English text inside `generar_en.py`).
- Translations: `herramientas/i18n_extra/<l>/` (ui.json, articulos/*.json, planes/*.json, galeria.json, unidad.json,
  legal.json). Skip subs/.
- Do NOT edit any other file (not generar.py, generar_i18n.py, extras.py, idiomas.py, Spanish files, other languages).

### Checks before you finish
- `python3 -c "import paginas_<l>"` etc. must import; every JSON must load.
- Run `cd herramientas && python3 comprobar_paquete.py <l>` (ka/ru/fr) — must say structure ok.
- `grep -i` your language's old terms ("growth factor", "facteurs de croissance", "факторы роста"/"факторов роста"/
  "факторами роста", "ზრდის ფაქტორ") and list any remaining occurrence with the reason it stays.
- Do NOT run the generators, do NOT commit or push.
Report: files changed, number of replacements, anything you were unsure about (max 10 lines).
