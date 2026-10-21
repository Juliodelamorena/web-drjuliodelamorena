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
