# Vídeos diarios de las secciones

- `entradas/entrada-<día>.mp4`: entradas aprobadas (4,2 s) de cada sección: lunes «Lo que casi nadie te cuenta», martes «Cómo se diagnostica», miércoles «El ejercicio de la semana», jueves «¿Mito o verdad?», viernes «El estudio de la semana», sábado «Curiosidades del cuerpo».
- `render.py`: plantilla del vídeo completo (entrada + mitad de arriba con gráficos + abajo Julio + subtítulos + cierre fijo). Fuentes en `fonts/`, sonidos y música en `sonidos/`.
- `entradas.py` / `mezcla_entradas.py`: generan las entradas de martes a sábado con su sonido.
- `doblar.py` / `guiones.py`: doblaje con la voz clonada de Julio (ElevenLabs) a los cinco idiomas. La clave de la API no se guarda aquí.
- Cierre fijo: nombre, «Medicina Deportiva y Terapias Regenerativas», drjuliodelamorena.com, @drjuliodelamorena. Sin teléfono ni «pide cita». Sin marca de inteligencia artificial (decisión de Julio).

## Formato mejorado (auditoría nov 2026)
- Cierre con gancho: `cierre.manana("martes", "cómo se diagnostica un esguince")` cambia la frase final por «Mañana: …» antes de renderizar.
- Zona segura de Instagram: nada importante en los primeros 250 px ni en los últimos 250 px del vídeo de 1920 px (la banda de la serie, hoy en y=0-110, hay que bajarla al renderizar la tanda de la semana y comprobarlo en una captura).
- Frase gancho escrita en el primer fotograma, voz desde el segundo 0 y duración objetivo de 20-30 s.
- Año del British Medical Journal sobre la «tendinitis»: 2002 (corregido en voz.py, reel.py y render.py; hay que regenerar f2.mp3 con la nueva frase antes de usar ese vídeo).
- Vídeo PRP: la web ya lleva la nota de cautela; el vídeo con la frase «máxima recomendación» ya está suavizada en guiones.py, pero hay que volver a doblarlo (cinco idiomas) para que el vídeo publicado coincida.
