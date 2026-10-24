# Cómo se mantiene esta web

Web estática del Dr. Julio De la Morena Garzón (drjuliodelamorena.com), publicada en Netlify desde la rama `main`. Cada `git push` la publica en un minuto.

## Reglas de contenido (obligatorias)
- Trato de usted al lector. Tono de clínica privada, sobrio.
- Código de Deontología Médica: sin precios, sin testimonios ni pacientes reconocibles, sin famosos como reclamo, sin prometer resultados ("siempre que sea posible", "en casos seleccionados", "cuando está indicado").
- La terapia biológica se llama "factores de crecimiento autólogos" (se puede mencionar "plasma rico en plaquetas" como sinónimo de búsqueda).
- Nada de diapositivas ni apartados de "señales de alarma" de alteraciones urinarias.
- La web se dirige a cualquier persona, haga deporte o no; los deportistas de élite solo como prueba de nivel.
- Ilustraciones anatómicas siempre propias; nunca dibujos sacados de internet ni retocados.
- Cada texto empieza con una respuesta directa (qué es, cómo se trata, quién lo trata y dónde) y termina con preguntas frecuentes reales.

## Artículos del blog
1. Crear `herramientas/articulos/<slug>.json` con: slug, fecha (AAAA-MM-DD), categoria, titulo, resumen (1 frase), descripcion (meta, unos 155 caracteres), entradilla (respuesta directa de 60-90 palabras que nombre al Dr. Julio De la Morena y el Hospital Memorial Publio Cordón en Pozuelo de Alarcón), imagen (archivo en `img/`), imagen_wh [ancho, alto], imagen_alt, temas [enfermedades], secciones [[título, html], ...], faq [[pregunta, respuesta], ...], relacionadas [slugs de páginas de especialidad].
2. `python3 herramientas/articulos.py` regenera el artículo, la página /blog/, los 3 últimos artículos de la portada, `sitemap.xml` y `llms.txt`.
3. Comprobar que los JSON-LD son válidos y hacer commit y push.

Slugs de páginas de especialidad: artrosis-rodilla, lumbalgia-ciatica, tendinopatias, hombro-doloroso, esguince-tobillo, lesiones-musculares, factores-crecimiento-autologos, infiltraciones-ecoguiadas, medicina-deportiva, segunda-opinion.

## Páginas de especialidad
Texto en `herramientas/paginas.py`; se regeneran con `python3 herramientas/generar.py`.

## Planes de ejercicio
Origen: planes genéricos de Julio en Google Drive, carpeta "01 Clinica y pacientes/PROGRAMAS DE EJERCICIOS VIP" (los que llevan "(generico)" o sin nombre de paciente). Nunca publicar planes con nombre de paciente.
1. Pasar el plan a `herramientas/planes/<slug>.json` (ver capsulitis-hombro-congelado.json): se respeta su texto y su trato de tú; se quitan los campos de paciente y la marca IMRAD.
2. Fotos opcionales en `img/planes/<slug>/<n>.jpg` (n = número de ejercicio en orden), a 760 px.
3. `python3 herramientas/planes.py` y después `python3 herramientas/articulos.py` (actualiza el sitemap).

## Versión en inglés (/en/)

- Contenido en `herramientas/paginas_en.py`; se genera con `python3 herramientas/generar_en.py`.
- Orden al regenerar todo: `generar.py`, `generar_en.py`, `articulos.py`, `planes.py`.
- Cada página española con pareja en inglés lleva enlaces hreflang (es, en, x-default) y el enlace "English" en la cabecera; la tabla de parejas es `SLUG_ES_TO_EN`.
- Al añadir una página nueva en español, añadir su traducción en `paginas_en.py` y su pareja en `SLUG_ES_TO_EN`.
- La segunda opinión todavía no tiene versión en inglés.

## Captación (24 oct 2026)
- Teléfono siempre pulsable (`<a class="tel" href="tel:+34913548990">`) y barra fija en el móvil (`.cta-fija`, la añade `footer()` en generar.py y generar_en.py; index.html y blog/lumbalgia-5-cosas.html la llevan a mano).
- Horario de consulta: lunes a viernes, de 15:00 a 21:00. Aparece en la barra superior, el contacto, el pie, las preguntas frecuentes y el JSON-LD (openingHoursSpecification).
- Portada: bloque "¿Es su caso?" (#caso) y botón principal a la cita online del hospital; el formulario queda como "Prefiero que me llamen" y pide la zona que duele.
- Cada página de paginas.py lleva `"cta"`: una pregunta específica para el cierre, más la ventaja (exploración y ecografía en la misma consulta; primera consulta sin compromiso).
- Sin seguros: la consulta es privada. Está en las preguntas frecuentes (es/en). Sin precios en la web.
