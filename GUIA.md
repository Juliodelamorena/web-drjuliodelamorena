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
- Cada página española con pareja en otro idioma lleva enlaces hreflang (es, en, ka, ru, fr, x-default) y el menú de idiomas en la cabecera (`idiomas.py`); la tabla de parejas inglesas es `SLUG_ES_TO_EN`.
- Al añadir una página nueva en español, añadir su traducción en `paginas_en.py` y su pareja en `SLUG_ES_TO_EN`.
- La segunda opinión todavía no tiene versión en inglés (sí en georgiano, ruso y francés).

## Versiones en georgiano, ruso y francés (/ka/, /ru/, /fr/)

- Pensadas para pacientes que vienen desde fuera (muchos desde Georgia): portada con apartado "pacientes del extranjero", página del doctor, las nueve páginas de patologías y tratamientos y la segunda opinión a distancia con su formulario (`segunda-opinion-<idioma>`); formulario de contacto `contacto-<idioma>`. Página de gracias: `/ka/madloba.html`, `/ru/spasibo.html`, `/fr/merci.html`.
- Contenido en `herramientas/paginas_ka.py`, `paginas_ru.py`, `paginas_fr.py` (misma estructura que `paginas_plantilla.py`, que es la plantilla en inglés). Comprobar la estructura con `python3 herramientas/comprobar_paquete.py ka`. Generar con `python3 herramientas/generar_i18n.py all` (o `ka`, `ru`, `fr`).
- Orden al regenerar todo: `generar_i18n.py all`, `generar.py`, `generar_en.py`, `articulos.py`, `planes.py` (los dos primeros ponen el hreflang de cinco idiomas en las páginas españolas e inglesas; `articulos.py` mete los idiomas en el sitemap).
- `herramientas/idiomas.py` es el registro común: parejas de slugs por idioma, enlaces hreflang, menú desplegable de idiomas (`<details class="lang-menu">`, sin JavaScript) y enlaces de idioma del pie. `index.html` lleva el menú y el hreflang a mano.
- En estos idiomas el botón principal es "escríbanos" (formulario), no "llamar": la recepción del hospital atiende en español e inglés. En los textos se dice que puede escribirse en su idioma y que se responde en su idioma (Julio responde con ayuda de Claude), y que la consulta es en español o inglés (que vengan acompañados si no hablan ninguno). Nada de precios ni promesas.
- El nombre del doctor va en alfabeto latino en marca, títulos SEO y descripciones, y transliterado en el cuerpo del texto (ხულიო დე ლა მორენა / Хулио де ла Морена). "Factores de crecimiento autólogos" es el término principal; "plasma rico en plaquetas" solo como sinónimo entre paréntesis.
- Georgiano: las fuentes Manrope y Cormorant no tienen alfabeto georgiano; el paquete `paginas_ka.py` añade Noto Sans Georgian y Noto Serif Georgian (`META["extra_fonts"]` y `META["font_css"]`).
- Pendiente: que un paciente georgiano de confianza revise la versión georgiana antes de difundirla.

## Captación (24 oct 2026)
- Teléfono siempre pulsable (`<a class="tel" href="tel:+34913548990">`) y barra fija en el móvil (`.cta-fija`, la añade `footer()` en generar.py y generar_en.py; index.html y blog/lumbalgia-5-cosas.html la llevan a mano).
- Horario de consulta: lunes a viernes, de 15:00 a 21:00. Aparece en la barra superior, el contacto, el pie, las preguntas frecuentes y el JSON-LD (openingHoursSpecification).
- La ficha del Memorial NO tiene cita online (su "Pedir cita" lleva a una página de contacto con el teléfono). Por eso todos los botones de cita llaman por teléfono en el móvil (`.btn.solo-movil`, tel:) y en escritorio van a /#contacto (`.btn.solo-escritorio`). La barra fija: "Llamar" (tel:) y "Que me llamen" (/#contacto). No enlazar la ficha del hospital como si fuera cita online.
- Portada: bloque "¿Es su caso?" (#caso); el formulario es "Prefiero que me llamen" y pide la zona que duele.
- Cada página de paginas.py lleva `"cta"`: una pregunta específica para el cierre, más la ventaja (exploración y ecografía en la misma consulta; primera consulta sin compromiso).
- Sin seguros: la consulta es privada. Está en las preguntas frecuentes (es/en). Sin precios en la web.

## Dosier de prensa de mayo de 2014
- Los recortes (ABC, AS 11 y 12, El País, Marca, Sport) están en /home/claude/kit/prensa2014/ (copia del móvil de Julio). Son páginas de periódico con derechos: NO se publican en la web; solo se citan cabecera, fecha y titular, y se enlaza Libertad Digital. No nombrar al jugador en la web.
- Netlify (plan gratuito) agotó los créditos de publicación el 24 oct 2026: los cambios desde el commit 8aa9765 quedan pendientes hasta que se renueven (o se amplíe el plan). Agrupar cambios y publicar como mucho una vez al día.
