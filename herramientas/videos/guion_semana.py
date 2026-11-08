# Guiones de martes a sábado (semana del 10 al 14 de noviembre de 2026).
# voz = texto que se locuta (números en letra); sub = subtítulo en pantalla.
# panel = lista de (tipo, y, texto, fuente, color, aparece_en_s[, tachado_en_s]); tipos: t texto, x texto tachado.
DIAS = {
"martes": {
 "banda": "LOS MARTES DE…  CÓMO SE DIAGNOSTICA", "gancho": "no sale en la radiografía", "cierre": "el ejercicio para el Aquiles",
 "frases": [
  {"voz": "El esguince de tobillo… no se ve en una radiografía.", "sub": "El esguince de tobillo… no se ve en una radiografía.",
   "panel": [("t", 400, "ESGUINCE", "K", "W", 0), ("t", 560, "¿en la radiografía?", "S", "G", 1.0)]},
  {"voz": "La radiografía sirve para descartar una fractura. El ligamento no aparece en ella.", "sub": "La radiografía sirve para descartar una fractura. El ligamento no aparece en ella.",
   "panel": [("t", 300, "RADIOGRAFÍA", "K2", "W", 0), ("t", 440, "descarta fracturas", "S", "S", 1.2), ("t", 540, "el ligamento no se ve", "SUB", "G", 3.0)]},
  {"voz": "El diagnóstico empieza con la exploración: dónde duele, cómo se mueve el tobillo y si hay inestabilidad.", "sub": "El diagnóstico empieza con la exploración: dónde duele, cómo se mueve el tobillo y si hay inestabilidad.",
   "panel": [("t", 250, "EXPLORACIÓN", "K2", "W", 0), ("t", 420, "dónde duele", "SUB", "S", 1.0), ("t", 510, "cómo se mueve", "SUB", "S", 2.2), ("t", 600, "si hay inestabilidad", "SUB", "G", 3.6)]},
  {"voz": "Y la ecografía permite ver el ligamento, compararlo con el otro tobillo y estudiarlo en movimiento.", "sub": "Y la ecografía permite ver el ligamento, compararlo con el otro tobillo y estudiarlo en movimiento.",
   "panel": [("t", 280, "ECOGRAFÍA", "K2", "W", 0), ("t", 440, "ve el ligamento", "SUB", "G", 1.0), ("t", 530, "lo compara con el otro tobillo", "S", "S", 2.6), ("t", 610, "y lo estudia en movimiento", "S", "S", 4.2)]},
  {"voz": "Si el tobillo sigue fallando meses después, merece un nuevo estudio: puede haber un ligamento que no cicatrizó bien.", "sub": "Si el tobillo sigue fallando meses después, merece un nuevo estudio: puede haber un ligamento que no cicatrizó bien.",
   "panel": [("t", 280, "¿SIGUE FALLANDO?", "K2", "W", 0), ("t", 440, "vuelve a estudiarlo", "SUB", "G", 1.6), ("t", 540, "puede haber un ligamento sin cicatrizar", "S", "S", 3.6)]},
 ]},
"miercoles": {
 "banda": "LOS MIÉRCOLES DE…  EL EJERCICIO DE LA SEMANA", "gancho": "para el tendón de Aquiles", "cierre": "¿hielo o calor?",
 "frases": [
  {"voz": "Si te duele el tendón de Aquiles… este es el ejercicio.", "sub": "Si te duele el tendón de Aquiles… este es el ejercicio.",
   "panel": [("t", 400, "AQUILES", "K", "W", 0), ("t", 560, "el ejercicio", "S", "G", 1.0)]},
  {"voz": "Se llama carga excéntrica. Subes a la punta de los pies con las dos piernas, y bajas despacio solo con la pierna que duele.", "sub": "Se llama carga excéntrica. Subes a la punta de los pies con las dos piernas, y bajas despacio solo con la pierna que duele.",
   "panel": [("t", 250, "CARGA EXCÉNTRICA", "K2", "W", 0), ("t", 430, "SUBES con las dos piernas", "SUB", "S", 2.0), ("t", 540, "BAJAS despacio con la que duele", "SUB", "G", 5.0)]},
  {"voz": "Tres series de quince repeticiones, dos veces al día, durante doce semanas.", "sub": "Tres series de 15 repeticiones, dos veces al día, durante 12 semanas.",
   "panel": [("t", 280, "3 × 15", "K", "W", 0), ("t", 470, "dos veces al día", "SUB", "S", 1.6), ("t", 570, "12 semanas", "SUB", "G", 3.0)]},
  {"voz": "Es normal notar molestia, pero tolerable. Si el dolor es fuerte, o notas un golpe y no puedes ponerte de puntillas, consulta.", "sub": "Es normal notar molestia, pero tolerable. Si el dolor es fuerte, o notas un golpe y no puedes ponerte de puntillas, consulta.",
   "panel": [("t", 260, "MOLESTIA LEVE", "K2", "W", 0), ("t", 420, "es normal", "SUB", "S", 1.0), ("t", 520, "dolor fuerte o golpe seco:", "SUB", "R", 4.2), ("t", 600, "consulta", "SUB", "G", 5.4)]},
  {"voz": "Es un ejercicio sencillo. Lo que lo hace funcionar es la dosis… y la constancia.", "sub": "Es un ejercicio sencillo. Lo que lo hace funcionar es la dosis… y la constancia.",
   "panel": [("t", 330, "LA DOSIS", "K", "W", 0), ("t", 500, "y la constancia", "SUB", "G", 2.2)]},
 ]},
"jueves": {
 "banda": "LOS JUEVES DE…  ¿MITO O VERDAD?", "gancho": "¿el hielo cura?", "cierre": "el estudio del menisco",
 "frases": [
  {"voz": "Mito o verdad: el hielo cura las lesiones.", "sub": "Mito o verdad: el hielo cura las lesiones.",
   "panel": [("t", 400, "HIELO", "K", "W", 0), ("t", 560, "¿cura las lesiones?", "S", "G", 1.0)]},
  {"voz": "Mito. El hielo adormece y alivia el dolor un rato, pero no hay pruebas de que acelere la recuperación.", "sub": "Mito. El hielo adormece y alivia el dolor un rato, pero no hay pruebas de que acelere la recuperación.",
   "panel": [("t", 280, "MITO", "K", "R", 0), ("t", 450, "adormece y alivia el dolor", "S", "S", 1.6), ("t", 540, "no acelera la recuperación", "SUB", "G", 4.0)]},
  {"voz": "En dos mil diecinueve, el British Journal of Sports Medicine cuestionó el uso rutinario del hielo.", "sub": "En 2019, el British Journal of Sports Medicine cuestionó el uso rutinario del hielo.",
   "panel": [("t", 250, "British Journal of Sports Medicine · 2019", "S", "G", 0), ("t", 380, "HIELO", "K2", "W", 0.6), ("t", 500, "uso rutinario, en duda", "SUB", "S", 2.6)]},
  {"voz": "El calor relaja la musculatura: va bien en una contractura o un dolor crónico, no en una lesión reciente con hinchazón.", "sub": "El calor relaja la musculatura: va bien en una contractura o un dolor crónico, no en una lesión reciente con hinchazón.",
   "panel": [("t", 250, "CALOR", "K2", "W", 0), ("t", 420, "sí: contractura, dolor crónico", "SUB", "G", 2.4), ("t", 520, "no: lesión reciente con hinchazón", "SUB", "R", 4.6)]},
  {"voz": "Lo que más ayuda a recuperar es volver a moverse de forma progresiva, no el frío ni el calor.", "sub": "Lo que más ayuda a recuperar es volver a moverse de forma progresiva, no el frío ni el calor.",
   "panel": [("t", 300, "MOVERSE", "K", "G", 0), ("t", 480, "de forma progresiva", "SUB", "S", 1.8)]},
 ]},
"viernes": {
 "banda": "LOS VIERNES DE…  EL ESTUDIO DE LA SEMANA", "gancho": "operación simulada", "cierre": "¿por qué crujen las rodillas?",
 "frases": [
  {"voz": "A unos pacientes los operaron… y a otros les simularon la operación.", "sub": "A unos pacientes los operaron… y a otros les simularon la operación.",
   "panel": [("t", 400, "OPERACIÓN", "K2", "W", 0), ("t", 560, "¿o simulacro?", "S", "G", 1.2)]},
  {"voz": "En dos mil trece, en Finlandia, ciento cuarenta y seis pacientes con rotura degenerativa de menisco entraron al quirófano.", "sub": "En 2013, en Finlandia, 146 pacientes con rotura degenerativa de menisco entraron al quirófano.",
   "panel": [("t", 250, "FINLANDIA · 2013", "S", "G", 0), ("t", 340, "146", "K", "W", 0.8), ("t", 500, "pacientes con rotura de menisco", "SUB", "S", 1.8)]},
  {"voz": "A unos los operaron. A otros les simularon la operación, y no sabían cuál les tocó.", "sub": "A unos los operaron. A otros les simularon la operación, y no sabían cuál les tocó.",
   "panel": [("t", 280, "operación real", "SUB", "W", 0.4), ("t", 380, "operación simulada", "SUB", "G", 1.8), ("t", 500, "nadie sabía cuál le tocaba", "S", "S", 3.4)]},
  {"voz": "Un año después, la mejoría en dolor y en función de la rodilla fue la misma en los dos grupos.", "sub": "Un año después, la mejoría en dolor y en función de la rodilla fue la misma en los dos grupos.",
   "panel": [("t", 300, "12 MESES", "K", "W", 0), ("t", 480, "misma mejoría", "SUB", "G", 1.8), ("t", 570, "en los dos grupos", "S", "S", 3.2)]},
  {"voz": "Lo publicó el New England Journal of Medicine. Antes de operar, hay que valorar bien cada caso.", "sub": "Lo publicó el New England Journal of Medicine. Antes de operar, hay que valorar bien cada caso.",
   "panel": [("t", 250, "New England Journal of Medicine", "S", "G", 0), ("t", 360, "ANTES DE OPERAR", "K2", "W", 1.8), ("t", 520, "valorar bien cada caso", "SUB", "S", 3.4)]},
 ]},
"sabado": {
 "banda": "LOS SÁBADOS DE…  CURIOSIDADES DEL CUERPO", "gancho": "no tiene por qué ser desgaste", "cierre_frase": "Nos vemos el lunes",
 "frases": [
  {"voz": "¿Te crujen las rodillas? No tiene por qué ser desgaste.", "sub": "¿Te crujen las rodillas? No tiene por qué ser desgaste.",
   "panel": [("t", 400, "CRUJIDO", "K", "W", 0), ("t", 560, "de rodilla", "S", "G", 1.0)]},
  {"voz": "A ese ruido se le llama crepitación. Puede deberse a burbujas de gas en el líquido de la articulación, o a tendones que rozan al moverse.", "sub": "A ese ruido se le llama crepitación. Puede deberse a burbujas de gas en el líquido de la articulación, o a tendones que rozan al moverse.",
   "panel": [("t", 250, "CREPITACIÓN", "K2", "W", 0), ("t", 430, "burbujas de gas", "SUB", "G", 3.2), ("t", 520, "tendones que rozan", "SUB", "S", 6.2)]},
  {"voz": "Si no duele, no se hincha y la rodilla no se bloquea, casi siempre es inofensivo.", "sub": "Si no duele, no se hincha y la rodilla no se bloquea, casi siempre es inofensivo.",
   "panel": [("t", 250, "sin dolor", "SUB", "S", 0.4), ("t", 340, "sin hinchazón", "SUB", "S", 1.4), ("t", 430, "sin bloqueos", "SUB", "S", 2.4), ("t", 560, "casi siempre inofensivo", "SUB", "G", 3.8)]},
  {"voz": "Cuidado cuando el crujido viene con dolor, con hinchazón, o con sensación de bloqueo o de que la rodilla falla.", "sub": "Cuidado cuando el crujido viene con dolor, con hinchazón, o con sensación de bloqueo o de que la rodilla falla.",
   "panel": [("t", 250, "CONSULTA SI…", "K2", "R", 0), ("t", 430, "dolor · hinchazón", "SUB", "S", 1.8), ("t", 520, "bloqueo · la rodilla falla", "SUB", "S", 3.6)]},
  {"voz": "Y lo que mejor cuida la rodilla es moverla… y fortalecer los músculos que la rodean.", "sub": "Y lo que mejor cuida la rodilla es moverla… y fortalecer los músculos que la rodean.",
   "panel": [("t", 300, "MOVERLA", "K", "W", 0), ("t", 480, "y fortalecerla", "SUB", "G", 2.2)]},
 ]},
}
