# Translation brief (one language per agent)

Website of Dr Julio De la Morena, sports-medicine doctor (Hospital Memorial Publio Cordón, Pozuelo de Alarcón, Madrid).
Translate Spanish source content into TARGET language and write files under
/home/claude/web-drjuliodelamorena/herramientas/i18n_extra/<lang>/ (lang = en, ka, ru or fr).

Style: match the existing pack /home/claude/web-drjuliodelamorena/herramientas/paginas_<lang>.py (for en: paginas_en.py) —
same terminology, polite form, how the doctor's name/hospital are written. "factores de crecimiento autólogos" = the term that
pack uses (main term); never mention monocytes. Medically accurate, natural, no prices, no testimonials, no promised results.
Keep phone "913 548 990" (en/ka/ru/fr: "+34 913 548 990"). Keep proper names (Hospital Memorial Publio Cordón, Endoret, Stryker).

Files to produce (same JSON structure/keys as the Spanish source, UTF-8, valid JSON, ensure_ascii False):

1. ui.json  — translate every value of i18n_extra/es/ui.json. Keep the keys. Keep placeholders {n} {t} {f} {d} {month} {y} and the
   <strong> tag. "months" = 12 month names. "date_format" = natural date pattern in the language using {d} {month} {y}.
   video_caption_* must say the video is in Spanish with subtitles in the TARGET language.
2. legal.json — translate the two HTML strings of i18n_extra/es/legal.json (keep every HTML tag; keep the NIF and registration
   numbers; Spanish law names may stay in Spanish followed by a short translation; "Agencia Española de Protección de Datos" keep name).
3. galeria.json — translate "titulo" and, for each photo, items [1] (alt text) and [2] (caption). Keep item [0] (file name).
4. articulos/<slug>.json — for each JSON in herramientas/articulos/ EXCEPT lumbalgia-5-cosas.json: same keys; translate
   categoria, titulo, resumen, descripcion (≤155 chars), entradilla, imagen_alt, temas (list), secciones (list of [title, html]),
   faq (list of [q, a]). Keep slug, fecha, imagen, imagen_wh, relacionadas EXACTLY. In section HTML keep every tag and attribute
   exactly (including href values — do NOT change links); translate only text, and keep cited paper titles/journal names as they are.
   ALSO lumbalgia-5-cosas: the Spanish article is hand-written HTML in /home/claude/web-drjuliodelamorena/blog/lumbalgia-5-cosas.html.
   Create articulos/lumbalgia-5-cosas.json in the same structure as the other articles (keys: slug, fecha, categoria, titulo, resumen,
   descripcion, entradilla, imagen, imagen_wh, imagen_alt, temas, secciones, faq, relacionadas) using the metadata of
   herramientas/articulos/lumbalgia-5-cosas.json, the article body of that HTML (lead paragraph → entradilla, each <h2> block → a
   section; its FAQ if any → faq), relacionadas = ["lumbalgia-ciatica","segunda-opinion"]. Keep its images/figures HTML as is.
5. planes/capsulitis-hombro-congelado.json — translate every text field of herramientas/planes/capsulitis-hombro-congelado.json
   (titulo, corto, zona, descripcion ≤155, intro, regla, elegir_fase, antes, fases[*].nombre/cuando/texto/ejercicios[*][0..3],
   evitar, complementario, consultar, normal). Keep slug, fecha, relacionadas and list lengths/structure exactly.
   Phase names keep the "·" separator pattern ("Phase 1 · ...").
6. subs/terapias-regenerativas.vtt and subs/codo-de-padel.vtt — translate the cue text of i18n_extra/es/subs/*.vtt. Keep WEBVTT
   header, every timing line and cue count exactly; max 2 lines per cue, short lines (≤ 32 characters each if possible).
   These are subtitles of Spanish speech, keep meaning faithful.

Validate when done: every JSON loads; for articles and plan, sorted HTML tag lists of each section equal the Spanish ones;
VTT has the same number of cues and identical timings. Reply only "done" plus any real concern.
