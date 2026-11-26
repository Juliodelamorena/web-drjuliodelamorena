"""Selector «¿Dónde le duele?» y aviso de segunda opinión de la portada, en los seis idiomas.

Cada zona lista las páginas de lesiones y los planes de ejercicio que existen en ese idioma
(idiomas.path_for decide si hay versión). Se usa desde generar.py (es), generar_en.py (en)
y generar_i18n.py (ka, ru, fr, zh). Sin JavaScript también funciona: cada zona es un <details>.
"""
import html
import idiomas

esc = html.escape

T = {
    "es": {"label": "¿Dónde le duele?", "h": "Elija la zona y vea qué puede ser y cómo se trata",
           "plan": "Plan de ejercicio", "so_h": "¿Le han recomendado operarse?",
           "so_p": "Antes de decidir, puede pedir una segunda opinión: se revisan sus pruebas, se explora la zona con ecografía si hace falta y se valoran las alternativas sin cirugía. Recibe un informe escrito.",
           "so_b": "Pedir una segunda opinión"},
    "en": {"label": "Where does it hurt?", "h": "Choose the area to see what it may be and how it is treated",
           "plan": "Exercise plan", "so_h": "Have you been advised to have surgery?",
           "so_p": "Before you decide, you can ask for a second opinion: your scans are reviewed, the area is examined with ultrasound if needed and non-surgical options are assessed. You receive a written report.",
           "so_b": "Ask for a second opinion"},
    "fr": {"label": "Où avez-vous mal ?", "h": "Choisissez la zone pour voir de quoi il peut s'agir et comment cela se traite",
           "plan": "Programme d'exercices", "so_h": "On vous a conseillé une opération ?",
           "so_p": "Avant de décider, vous pouvez demander un second avis : vos examens sont revus, la zone est explorée à l'échographie si besoin et les alternatives sans chirurgie sont évaluées. Vous recevez un compte rendu écrit.",
           "so_b": "Demander un second avis"},
    "ru": {"label": "Где болит?", "h": "Выберите область, чтобы узнать, что это может быть и как это лечится",
           "plan": "План упражнений", "so_h": "Вам рекомендовали операцию?",
           "so_p": "Прежде чем решать, можно получить второе мнение: врач изучит ваши исследования, при необходимости осмотрит область с помощью УЗИ и оценит варианты лечения без операции. Вы получите письменное заключение.",
           "so_b": "Получить второе мнение"},
    "ka": {"label": "სად გტკივათ?", "h": "აირჩიეთ ზონა და ნახეთ, რა შეიძლება იყოს და როგორ მკურნალობენ",
           "plan": "ვარჯიშების გეგმა", "so_h": "ოპერაციას გირჩევენ?",
           "so_p": "გადაწყვეტილების მიღებამდე შეგიძლიათ მოითხოვოთ მეორე აზრი: გადაიხედება თქვენი კვლევები, საჭიროების შემთხვევაში ზონა გამოკვლეული იქნება ულტრაბგერით და შეფასდება ქირურგიის გარეშე მკურნალობის ვარიანტები. მიიღებთ წერილობით დასკვნას.",
           "so_b": "მეორე აზრის მოთხოვნა"},
    "zh": {"label": "哪里疼？", "h": "选择部位，了解可能的原因和治疗方法",
           "plan": "锻炼计划", "so_h": "医生建议您做手术吗？",
           "so_p": "在做决定之前，您可以申请第二诊疗意见：医生会查看您的检查结果，必要时用超声检查该部位，并评估非手术方案。您将收到书面报告。",
           "so_b": "申请第二诊疗意见"},
}

# (slug español, {idioma: texto}); los planes llevan el prefijo "planes/"
ZONAS = [
    ({"es": "Hombro", "en": "Shoulder", "fr": "Épaule", "ru": "Плечо", "ka": "მხარი", "zh": "肩部"}, [
        ("hombro-doloroso", {"es": "Hombro doloroso y manguito rotador", "en": "Shoulder pain and rotator cuff", "fr": "Épaule douloureuse et coiffe des rotateurs", "ru": "Боль в плече и вращательная манжета", "ka": "მხრის ტკივილი და მბრუნავი მანჟეტი", "zh": "肩痛与肩袖"}),
        ("hombro-congelado", {"es": "Hombro congelado (capsulitis)"}),
        ("planes/capsulitis-hombro-congelado", {"es": "Hombro congelado", "en": "Frozen shoulder", "fr": "Épaule gelée", "ru": "Замороженное плечо", "ka": "გაყინული მხარი", "zh": "冻结肩"}),
        ("planes/manguito-rotador-subescapular", {"es": "Manguito rotador"}),
        ("planes/artritis-hombro-bursitis", {"es": "Artritis de hombro y bursitis"}),
        ("planes/hombro-cintura-escapular", {"es": "Fortalecimiento del hombro"}),
    ]),
    ({"es": "Codo", "en": "Elbow", "fr": "Coude", "ru": "Локоть", "ka": "იდაყვი", "zh": "肘部"}, [
        ("codo-de-tenista", {"es": "Codo de tenista y de pádel", "en": "Tennis elbow", "fr": "Épicondylite (coude du tennisman)", "ru": "Локоть теннисиста", "ka": "ჩოგბურთელის იდაყვი", "zh": "网球肘"}),
        ("planes/epicondilitis-codo-de-tenista", {"es": "Codo de tenista"}),
        ("planes/epitrocleitis-codo-de-golfista", {"es": "Codo de golfista"}),
    ]),
    ({"es": "Espalda", "en": "Back", "fr": "Dos", "ru": "Спина", "ka": "ზურგი", "zh": "背部"}, [
        ("lumbalgia-ciatica", {"es": "Lumbalgia y ciática", "en": "Low back pain and sciatica", "fr": "Lombalgie et sciatique", "ru": "Боль в пояснице и ишиас", "ka": "წელის ტკივილი და იშიასი", "zh": "腰痛与坐骨神经痛"}),
        ("planes/ciatica-radiculopatia-l5", {"es": "Ciática y estabilidad lumbar"}),
    ]),
    ({"es": "Cadera e ingle", "en": "Hip and groin", "fr": "Hanche et aine", "ru": "Бедро и пах", "ka": "მენჯ-ბარძაყი და საზარდული", "zh": "髋部与腹股沟"}, [
        ("artrosis-cadera", {"es": "Artrosis de cadera", "en": "Hip osteoarthritis", "fr": "Arthrose de la hanche", "ru": "Артроз тазобедренного сустава", "ka": "მენჯ-ბარძაყის სახსრის ართროზი", "zh": "髋关节骨关节炎"}),
        ("trocanteritis", {"es": "Dolor lateral de cadera (trocanteritis)"}),
        ("pubalgia", {"es": "Pubalgia", "en": "Groin pain", "fr": "Pubalgie", "ru": "Пубалгия", "ka": "პუბალგია", "zh": "耻骨痛"}),
        ("planes/coxartrosis-artrosis-de-cadera", {"es": "Artrosis de cadera"}),
        ("planes/tendinopatia-glutea-trocanteritis", {"es": "Trocanteritis"}),
    ]),
    ({"es": "Rodilla", "en": "Knee", "fr": "Genou", "ru": "Колено", "ka": "მუხლი", "zh": "膝部"}, [
        ("artrosis-rodilla", {"es": "Artrosis de rodilla", "en": "Knee osteoarthritis", "fr": "Arthrose du genou", "ru": "Артроз коленного сустава", "ka": "მუხლის ართროზი", "zh": "膝骨关节炎"}),
        ("prp-rodilla", {"es": "PRP (plasma rico en plaquetas) en la rodilla"}),
        ("rotura-menisco", {"es": "Rotura de menisco", "en": "Meniscus tear", "fr": "Déchirure du ménisque", "ru": "Разрыв мениска", "ka": "მენისკის გახევა", "zh": "半月板撕裂"}),
        ("tendinitis-rotuliana", {"es": "Tendinitis rotuliana", "en": "Patellar tendinopathy", "fr": "Tendinopathie rotulienne", "ru": "Тендинит надколенника", "ka": "კვირისთავის მყესის ტენდინიტი", "zh": "髌腱病"}),
        ("planes/condropatia-rotuliana", {"es": "Condropatía rotuliana"}),
        ("planes/osgood-schlatter", {"es": "Osgood-Schlatter"}),
    ]),
    ({"es": "Tobillo y pie", "en": "Ankle and foot", "fr": "Cheville et pied", "ru": "Голеностоп и стопа", "ka": "კოჭი და ტერფი", "zh": "踝部与足部"}, [
        ("esguince-tobillo", {"es": "Esguince de tobillo", "en": "Ankle sprain", "fr": "Entorse de la cheville", "ru": "Растяжение голеностопа", "ka": "კოჭის დაჭიმულობა", "zh": "踝关节扭伤"}),
        ("tendinitis-aquiles", {"es": "Tendinitis de Aquiles", "en": "Achilles tendinopathy", "fr": "Tendinopathie d'Achille", "ru": "Тендинит ахиллова сухожилия", "ka": "აქილევსის მყესის ტენდინიტი", "zh": "跟腱病"}),
        ("fascitis-plantar", {"es": "Fascitis plantar", "en": "Plantar fasciitis", "fr": "Fasciite plantaire", "ru": "Подошвенный фасциит", "ka": "ტერფის ფასციიტი", "zh": "足底筋膜炎"}),
    ]),
    ({"es": "Músculo", "en": "Muscle", "fr": "Muscle", "ru": "Мышцы", "ka": "კუნთი", "zh": "肌肉"}, [
        ("lesiones-musculares", {"es": "Lesiones musculares", "en": "Muscle injuries", "fr": "Lésions musculaires", "ru": "Мышечные травмы", "ka": "კუნთის დაზიანებები", "zh": "肌肉损伤"}),
        ("planes/rotura-isquiotibiales", {"es": "Rotura de isquiotibiales"}),
    ]),
    ({"es": "Todo el cuerpo", "en": "Whole body", "fr": "Tout le corps", "ru": "Всё тело", "ka": "მთელი სხეული", "zh": "全身"}, [
        ("medicina-deportiva", {"es": "Médico deportivo en Pozuelo", "en": "Sports medicine", "fr": "Médecine du sport", "ru": "Спортивная медицина", "ka": "სპორტული მედიცინა", "zh": "运动医学"}),
        ("planes/cuerpo-completo", {"es": "Cuerpo completo", "en": "Whole body", "fr": "Corps entier", "ru": "Всё тело", "ka": "მთელი სხეული", "zh": "全身"}),
    ]),
]


def _nombre(code, slug, txt):
    """Nombre de la página en ese idioma: el del menú del paquete o el del plan traducido; si no, el de la tabla."""
    import json, os
    if code == "es":
        return txt.get("es")
    if slug.startswith("planes/"):
        f = os.path.join(idiomas.EXTRA_DIR, code, "planes", slug[7:] + ".json")
        return json.load(open(f, encoding="utf-8")).get("corto") if os.path.isfile(f) else None
    pk = idiomas.pack(code)
    for q in (getattr(pk, "PAGES_EN", None) or getattr(pk, "PAGES", [])):
        if q.get("es") == slug:
            return q["nav"]
    return txt.get(code)


def selector(code):
    t = T[code]
    zonas = []
    for nombres, items in ZONAS:
        lis = []
        for slug, txt in items:
            p = idiomas.path_for(code, slug)
            nombre = _nombre(code, slug, txt) if p else None
            if not nombre:
                continue
            es_plan = slug.startswith("planes/")
            etiqueta = f'<span class="zona-tipo">{esc(t["plan"])}</span>' if es_plan else ""
            lis.append(f'<li><a href="{p}">{etiqueta}{esc(nombre)}</a></li>')
        if lis:
            zonas.append(f'<details class="zona"><summary>{esc(nombres[code])}</summary><ul>{"".join(lis)}</ul></details>')
    return (f'<div class="zonas" id="donde-duele"><p class="label">{esc(t["label"])}</p>'
            f'<p class="zonas-h">{esc(t["h"])}</p><div class="zonas-grid">{"".join(zonas)}</div></div>')


def segunda_opinion(code):
    t = T[code]
    p = idiomas.path_for(code, "segunda-opinion")
    if not p:
        return ""
    return (f'<div class="so-band"><div><h3>{esc(t["so_h"])}</h3><p>{esc(t["so_p"])}</p></div>'
            f'<a class="btn" href="{p}">{esc(t["so_b"])}</a></div>')
