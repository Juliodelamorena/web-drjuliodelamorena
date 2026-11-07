# Vídeos diarios de las secciones

- `entradas/entrada-<día>.mp4`: entradas aprobadas (4,2 s) de cada sección: lunes «Lo que casi nadie te cuenta», martes «Cómo se diagnostica», miércoles «El ejercicio de la semana», jueves «¿Mito o verdad?», viernes «El estudio de la semana», sábado «Curiosidades del cuerpo».
- `render.py`: plantilla del vídeo completo (entrada + mitad de arriba con gráficos + abajo Julio + subtítulos + cierre fijo). Fuentes en `fonts/`, sonidos y música en `sonidos/`.
- `entradas.py` / `mezcla_entradas.py`: generan las entradas de martes a sábado con su sonido.
- `doblar.py` / `guiones.py`: doblaje con la voz clonada de Julio (ElevenLabs) a los cinco idiomas. La clave de la API no se guarda aquí.
- Cierre fijo: nombre, «Medicina Deportiva y Terapias Regenerativas», drjuliodelamorena.com, @drjuliodelamorena. Sin teléfono ni «pide cita». Sin marca de inteligencia artificial (decisión de Julio).
