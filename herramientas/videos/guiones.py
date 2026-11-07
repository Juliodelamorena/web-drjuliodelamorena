A, M = "ambiente", "musica"
def codo(f): return {"fondo": A, "frases": list(zip([1.9, 4.65, 10.0, 15.0, 19.8, 26.2], f))}
def rod(f): return {"fondo": A, "frases": list(zip([0.0, 4.95, 8.0, 10.4, 15.7, 24.4], f))}
def uni(f): return {"fondo": M, "frases": list(zip([0.3, 4.2, 8.1, 12.0, 15.3, 19.9, 23.5, 26.8], f))}
GUIONES = {
 "en": {
  "codo-de-padel": codo(["Does your elbow hurt after playing padel?",
    "It's an overload of the forearm tendons, and rest alone won't cure it.",
    "First I examine the elbow and do an ultrasound to see the tendons.",
    "Then, exercise, and checking your racket and technique.",
    "And if it doesn't improve, autologous growth factors guided by ultrasound: what's called PRP.",
    "Book your assessment with me, in Pozuelo, Madrid."]),
  "terapias-regenerativas": rod(["Months of knee pain, and they're already talking about a replacement?",
    "In many cases, there's a step before that.",
    "PRP: platelet-rich plasma.",
    "Autologous growth factors, obtained from your own blood.",
    "Always guided by ultrasound, together with an interventional radiologist, and with an exercise plan.",
    "Book your assessment with Doctor Julio De la Morena, at Hospital Memorial Publio Cordón, in Pozuelo, Madrid."]),
  "unidad": uni(["This is my clinic: Hospital Memorial Publio Cordón, in Pozuelo, Madrid.",
    "A brand-new hospital, designed for your comfort.",
    "Spacious, calm areas.",
    "The Regenerative Therapies and Sports Medicine Unit.",
    "Here I listen to you, examine you and explain what is going on.",
    "Ultrasound in the same visit, with no need for another appointment.",
    "Ultrasound-guided treatments, to reach the exact spot.",
    "Doctor Julio De la Morena: fourteen years with Real Madrid's medical services."]),
 },
 "fr": {
  "codo-de-padel": codo(["Mal au coude après le padel ?",
    "C'est une surcharge des tendons de l'avant-bras, et le repos seul ne suffit pas à guérir.",
    "J'examine d'abord le coude et je fais une échographie pour voir les tendons.",
    "Ensuite, de l'exercice, et revoir la raquette et la technique.",
    "Et sinon, des facteurs de croissance autologues guidés par échographie : ce qu'on appelle le PRP.",
    "Demandez votre bilan avec moi, à Pozuelo, Madrid."]),
  "terapias-regenerativas": rod(["Mal au genou depuis des mois, et on vous parle déjà de prothèse ?",
    "Souvent, il existe une étape avant.",
    "Le PRP : plasma riche en plaquettes.",
    "Des facteurs de croissance autologues, obtenus à partir de votre propre sang.",
    "Toujours guidé par échographie, avec un radiologue interventionnel, et avec un programme d'exercices.",
    "Demandez votre bilan avec le docteur Julio De la Morena, à l'Hôpital Memorial Publio Cordón, à Pozuelo, Madrid."]),
  "unidad": uni(["Voici ma consultation : l'Hôpital Memorial Publio Cordón, à Pozuelo, Madrid.",
    "Un hôpital tout neuf, pensé pour votre confort.",
    "Des espaces vastes et calmes.",
    "L'Unité de thérapies régénératives et de médecine du sport.",
    "Ici, je vous écoute, je vous examine et je vous explique ce qui se passe.",
    "L'échographie pendant la consultation, sans autre rendez-vous.",
    "Des traitements guidés par échographie, pour atteindre le point exact.",
    "Docteur Julio De la Morena : quatorze ans au service médical du Real Madrid."]),
 },
 "ru": {
  "codo-de-padel": codo(["Болит локоть после игры в падел?",
    "Это перегрузка сухожилий предплечья, и одним покоем она не лечится.",
    "Сначала я осматриваю локоть и делаю ультразвуковое исследование, чтобы увидеть сухожилия.",
    "Затем — упражнения, проверка ракетки и техники.",
    "А если улучшения нет — аутологичные факторы роста под контролем ультразвука: то, что называют пэ-эр-пэ.",
    "Запишитесь ко мне на приём, в Посуэло, Мадрид."]),
  "terapias-regenerativas": rod(["Колено болит уже много месяцев, и Вам уже говорят об эндопротезе?",
    "Во многих случаях есть шаг до этого.",
    "Пэ-эр-пэ: плазма, обогащённая тромбоцитами.",
    "Аутологичные факторы роста, полученные из Вашей же крови.",
    "Всегда под контролем ультразвука, вместе с интервенционным радиологом и с планом упражнений.",
    "Запишитесь на приём к доктору Хулио де ла Морене, в госпиталь Мемориал Публио Кордон, в Посуэло, Мадрид."]),
  "unidad": uni(["Так выглядит мой кабинет: госпиталь Мемориал Публио Кордон, в Посуэло, Мадрид.",
    "Новая современная больница, созданная для Вашего комфорта.",
    "Просторные и спокойные залы.",
    "Отделение регенеративной терапии и спортивной медицины.",
    "Здесь я выслушаю и осмотрю Вас и объясню, что происходит.",
    "Ультразвук прямо на приёме, без отдельной записи.",
    "Лечение под контролем ультразвука, точно в нужную точку.",
    "Доктор Хулио де ла Морена: четырнадцать лет в медицинской службе «Реал Мадрида»."]),
 },
 "es": {
  "unidad": uni(["Así es mi consulta: el Hospital Memorial Publio Cordón, en Pozuelo, Madrid.",
    "Un hospital nuevo, pensado para su comodidad.",
    "Espacios amplios y tranquilos.",
    "La Unidad de Terapias Regenerativas y Medicina Deportiva.",
    "Aquí le escucho, le exploro y le explico qué le pasa.",
    "Ecografía en la misma consulta, sin esperar a otra cita.",
    "Tratamientos guiados por ecografía, para llegar al punto exacto.",
    "Doctor Julio De la Morena: catorce años en los servicios médicos del Real Madrid."]),
 },
}

T_PRP = [0.2, 3.2, 9.8, 16.4, 23.0, 29.6, 36.2, 42.8, 49.5, 54.5]
def prp(f): return {"fondo": M, "frases": list(zip(T_PRP, f))}
GUIONES["es"]["prp-evidencia"] = prp([
 "¿Funciona el PRP? Esto dice la literatura médica.",
 "Rodilla. Un consenso europeo lo considera apropiado en casos seleccionados de artrosis leve y moderada.",
 "En artrosis de rodilla, varios estudios muestran menos dolor y mejor función al año que con ácido hialurónico.",
 "Hombro. En la tendinopatía del manguito rotador, los resultados publicados son favorables y sin problemas de seguridad a largo plazo.",
 "Espalda. En el dolor lumbar, menos dolor y menos discapacidad hasta seis meses.",
 "Cadera. En la tendinopatía glútea, mejoría clara en el ochenta y dos por ciento, frente al cincuenta y siete con corticoide.",
 "Codo de tenista. El corticoide alivia antes, pero el PRP da mejores resultados a los seis meses.",
 "Pie. En la fascitis plantar, algunos estudios muestran más alivio del dolor que con corticoide o placebo.",
 "Los resultados varían según la lesión y la persona, y el PRP no sirve en todos los casos. Le valoramos para saber si es lo indicado en el suyo.",
 "Doctor Julio De la Morena, en Pozuelo, Madrid. Pida cita."])
GUIONES["en"]["prp-evidencia"] = prp([
 "Does PRP work? Here's what the medical literature says.",
 "Knee. The European consensus gives PRP its strongest recommendation for mild and moderate osteoarthritis.",
 "In knee osteoarthritis, PRP works better than hyaluronic acid: less pain and better function at one year.",
 "Shoulder. In rotator cuff tendinopathy, it is effective and safe in the long term.",
 "Lower back. In low back pain, less pain and less disability for up to six months.",
 "Hip. In gluteal tendinopathy, clear improvement in eighty-two percent, compared with fifty-seven with a corticosteroid.",
 "Tennis elbow. The corticosteroid works faster, but PRP gives better results at six months.",
 "Foot. In plantar fasciitis, more pain relief than a corticosteroid or a placebo.",
 "PRP is backed by science. We'll assess whether it's right for you.",
 "Doctor Julio De la Morena, in Pozuelo, Madrid. Book your appointment."])
GUIONES["fr"]["prp-evidencia"] = prp([
 "Le PRP, ça marche ? Voici ce que dit la littérature médicale.",
 "Genou. Le consensus européen donne au PRP sa plus forte recommandation dans l'arthrose légère et modérée.",
 "Dans l'arthrose du genou, le PRP est plus efficace que l'acide hyaluronique : moins de douleur et une meilleure fonction à un an.",
 "Épaule. Dans la tendinopathie de la coiffe des rotateurs, il est efficace et sûr à long terme.",
 "Dos. Dans la lombalgie, moins de douleur et moins d'incapacité jusqu'à six mois.",
 "Hanche. Dans la tendinopathie glutéale, une nette amélioration dans quatre-vingt-deux pour cent des cas, contre cinquante-sept avec un corticoïde.",
 "Coude du tennis. Le corticoïde soulage plus vite, mais le PRP donne de meilleurs résultats à six mois.",
 "Pied. Dans la fasciite plantaire, plus de soulagement que le corticoïde et que le placebo.",
 "Le PRP est validé par la science. Nous évaluons s'il est indiqué dans votre cas.",
 "Docteur Julio De la Morena, à Pozuelo, Madrid. Prenez rendez-vous."])
GUIONES["ru"]["prp-evidencia"] = prp([
 "Работает ли пэ-эр-пэ? Вот что говорит медицинская литература.",
 "Колено. Европейский консенсус даёт пэ-эр-пэ высшую рекомендацию при лёгком и умеренном артрозе.",
 "При артрозе колена пэ-эр-пэ эффективнее гиалуроновой кислоты: меньше боли и лучше функция через год.",
 "Плечо. При тендинопатии вращательной манжеты — эффективно и безопасно в долгосрочной перспективе.",
 "Спина. При боли в пояснице — меньше боли и ограничений до шести месяцев.",
 "Бедро. При тендинопатии ягодичных мышц — явное улучшение у восьмидесяти двух процентов, против пятидесяти семи с кортикостероидом.",
 "Локоть теннисиста. Кортикостероид помогает быстрее, но пэ-эр-пэ даёт лучший результат через шесть месяцев.",
 "Стопа. При подошвенном фасциите — больше облегчения, чем от кортикостероида и плацебо.",
 "У пэ-эр-пэ есть научное обоснование. Мы оценим, подходит ли оно в Вашем случае.",
 "Доктор Хулио де ла Морена, Посуэло, Мадрид. Запишитесь на приём."])
GUIONES.setdefault("ka", {})["prp-evidencia"] = prp([
 "მუშაობს თუ არა პი-არ-პი? აი, რას ამბობს სამედიცინო ლიტერატურა.",
 "მუხლი. ევროპული კონსენსუსი პი-არ-პის უმაღლეს რეკომენდაციას აძლევს მსუბუქი და ზომიერი ართროზის დროს.",
 "მუხლის ართროზის დროს პი-არ-პი ჰიალურონის მჟავაზე ეფექტურია: ნაკლები ტკივილი და უკეთესი ფუნქცია ერთ წელიწადში.",
 "მხარი. როტატორული მანჟეტის ტენდინოპათიის დროს ეფექტური და უსაფრთხოა ხანგრძლივად.",
 "წელი. წელის ტკივილის დროს ნაკლები ტკივილი და შეზღუდვა ექვს თვემდე.",
 "თეძო. დუნდულოს ტენდინოპათიის დროს აშკარა გაუმჯობესება ოთხმოცდაორ პროცენტში, კორტიკოსტეროიდით კი ორმოცდათჩვიდმეტში.",
 "ჩოგბურთელის იდაყვი. კორტიკოსტეროიდი უფრო სწრაფად შველის, მაგრამ ექვს თვეში პი-არ-პის უკეთესი შედეგი აქვს.",
 "ტერფი. ტერფის ფასციიტის დროს მეტი შვება, ვიდრე კორტიკოსტეროიდით ან პლაცებოთი.",
 "პი-არ-პის მეცნიერული საფუძველი აქვს. შეგაფასებთ, გჭირდებათ თუ არა.",
 "ექიმი ხულიო დე ლა მორენა, პოსუელო, მადრიდი. ჩაეწერეთ."])

import copy
GUIONES["es_ig"] = copy.deepcopy(GUIONES["es"])
def _tu(nombre, cambios):
    fr = GUIONES["es_ig"][nombre]["frases"]
    GUIONES["es_ig"][nombre]["frases"] = [(t, cambios.get(x, x)) for t, x in fr]
_tu("unidad", {"Un hospital nuevo, pensado para su comodidad.": "Un hospital nuevo, pensado para tu comodidad.",
               "Aquí le escucho, le exploro y le explico qué le pasa.": "Aquí te escucho, te exploro y te explico qué te pasa."})
_tu("prp-evidencia", {"Los resultados varían según la lesión y la persona, y el PRP no sirve en todos los casos. Le valoramos para saber si es lo indicado en el suyo.": "El PRP tiene respaldo científico. Te valoramos para saber si es lo indicado en tu caso.",
                      "Doctor Julio De la Morena, en Pozuelo, Madrid. Pida cita.": "Doctor Julio De la Morena, en Pozuelo, Madrid. Pide cita."})
