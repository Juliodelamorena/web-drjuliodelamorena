"""Configuración de cada reel para reel_i18n.py (textos traducidos, tiempos y zonas de cada rótulo)."""

L = lambda **k: k   # {"en": ..., "fr": ..., ...}

CFG = {}

# ---------------------------------------------------------------- Ecógrafo: la aguja se ve en tiempo real (11 nov 2026, 47,4 s)
CFG["ecografo"] = dict(
    f="ecografo-aguja", entrada="ecografo.mp4", dur=47.4, voz_fin=44.0, cap_fin=44.0,
    cap_y=1333, cajas=[(40, 1040), (40, 1040)],
    seg=[
        (0.0, L(
            en="Injections. Has anyone told you that you need an injection?",
            fr="Les infiltrations. On vous a dit de vous faire infiltrer ?",
            ru="Инъекции. Вам сказали, что нужно сделать инъекцию?",
            ka="ინექციები. გითხრეს, რომ ინექცია უნდა გაგიკეთონ?",
            zh="注射。有人跟你说过需要打针吗？")),
        (2.4, L(
            en="What is it? It means injecting a treatment straight into the area that hurts: a joint, a tendon, a ligament or a muscle.",
            fr="Qu'est-ce que c'est ? Il s'agit d'injecter un traitement directement dans la zone douloureuse : une articulation, un tendon, un ligament ou un muscle.",
            ru="Что это такое? Лекарство вводят прямо в то место, которое болит: в сустав, сухожилие, связку или мышцу.",
            ka="რა არის ეს? მკურნალობის საშუალება პირდაპირ იმ ადგილას შეჰყავთ, სადაც გტკივათ: სახსარში, მყესში, ლიგამენტში ან კუნთში.",
            zh="这是什么？就是把药物直接注射到疼痛的部位：关节、肌腱、韧带或肌肉。")),
        (9.5, L(
            en="What can be injected? Most often PRP, hyaluronic acid, corticosteroids and local anaesthetic; less often, bone marrow concentrate, prolotherapy or botulinum toxin.",
            fr="Que peut-on infiltrer ? Le plus souvent du PRP, de l'acide hyaluronique, des corticoïdes et de l'anesthésique local ; plus rarement, du concentré de moelle osseuse, de la prolothérapie ou de la toxine botulique.",
            ru="Что можно вводить? Чаще всего PRP, гиалуроновую кислоту, кортикостероиды и местный анестетик, а реже — концентрат костного мозга, пролотерапию или ботулотоксин.",
            ka="რისი შეყვანა შეიძლება? ყველაზე ხშირად პი-არ-პი, ჰიალურონის მჟავა, კორტიკოსტეროიდები და ადგილობრივი გაუტკივარება; უფრო იშვიათად — ძვლის ტვინის კონცენტრატი, პროლოთერაპია ან ბოტულინის ტოქსინი.",
            zh="可以注射什么？最常用的是 PRP、透明质酸、皮质类固醇和局部麻醉药；较少使用骨髓浓缩液、增生疗法或肉毒毒素。")),
        (20.7, L(
            en="Does it hurt? It feels similar to having blood drawn. It's a mild discomfort, and you walk home afterwards.",
            fr="Est-ce que ça fait mal ? C'est comparable à une prise de sang. La gêne est légère et on rentre chez soi à pied.",
            ru="Больно ли это? Похоже на забор крови. Неприятные ощущения слабые, и домой вы идёте пешком.",
            ka="გტკივათ? ეს სისხლის აღების მსგავსია. უსიამოვნო შეგრძნება მცირეა და სახლში ფეხით ბრუნდებით.",
            zh="疼吗？感觉和抽血差不多。只是轻微不适，注射后可以自己走回家。")),
        (26.6, L(
            en="How should it be done? Guided by ultrasound. With the ultrasound machine you can see the needle and the structure being treated in real time, and blood vessels and nerves are avoided.",
            fr="Comment doit-elle être réalisée ? Sous guidage échographique. Avec l'échographe, on voit en temps réel l'aiguille et la structure traitée, et on évite les vaisseaux sanguins et les nerfs.",
            ru="Как это нужно делать? Под контролем УЗИ. На экране аппарата в реальном времени видно иглу и ту структуру, которую лечат, а сосуды и нервы обходят.",
            ka="როგორ უნდა გაკეთდეს? ულტრაბგერითი კონტროლით. ექოგრაფზე რეალურ დროში ჩანს ნემსი და სტრუქტურა, რომელიც მკურნალობს, და სისხლძარღვებსა და ნერვებს გვერდს ვუვლით.",
            zh="应该怎么做？在超声引导下进行。通过超声设备，可以实时看到针头和被治疗的结构，并避开血管和神经。")),
        (35.4, L(
            en="In addition, a review of 12 randomized trials concludes that this makes the injection more precise.",
            fr="De plus, une revue de 12 essais randomisés conclut que l'infiltration est ainsi plus précise.",
            ru="Кроме того, обзор 12 рандомизированных исследований показывает, что так инъекция точнее.",
            ka="გარდა ამისა, 12 რანდომიზებული კვლევის მიმოხილვა ადასტურებს, რომ ასე ინექცია უფრო ზუსტია.",
            zh="此外，一项纳入 12 项随机试验的综述得出结论：这样注射更精准。")),
        (41.2, L(
            en="If you are going to be injected, make sure it is ultrasound-guided.",
            fr="Si on doit vous infiltrer, que ce soit sous guidage échographique.",
            ru="Если вам собираются делать инъекцию, пусть это будет под контролем УЗИ.",
            ka="თუ ინექციას გიკეთებენ, ულტრაბგერითი კონტროლით გაკეთდეს.",
            zh="如果你要接受注射，请选择超声引导。")),
    ],
    # (desde, hasta, tipo, zona de tapado (y0, y1), textos)
    titulos=[
        (0.0, 2.3, "intro", (302, 740), L(
            en=["INJECTIONS", "WHAT SHOULD YOU KNOW?"], fr=["INFILTRATIONS", "CE QU'IL FAUT SAVOIR"], ru=["ИНЪЕКЦИИ", "ЧТО НУЖНО ЗНАТЬ?"],
            ka=["ინექციები", "რა უნდა იცოდეთ?"], zh=["注射", "你需要了解什么？"])),
        (2.3, 9.5, "grande", (302, 740), L(en=["WHAT IS IT?"], fr=["QU'EST-CE QUE C'EST ?"], ru=["ЧТО ЭТО ТАКОЕ?"], ka=["რა არის ეს?"], zh=["这是什么？"])),
        (9.5, 20.6, "grande", (302, 740), L(
            en=["WHAT CAN BE", "INJECTED?"], fr=["QUE PEUT-ON", "INFILTRER ?"], ru=["ЧТО МОЖНО", "ВВОДИТЬ?"], ka=["რისი შეყვანა", "შეიძლება?"], zh=["可以注射", "什么？"])),
        (20.6, 26.5, "grande", (302, 740), L(en=["DOES IT HURT?"], fr=["ÇA FAIT MAL ?"], ru=["БОЛЬНО ЛИ ЭТО?"], ka=["გტკივათ?"], zh=["疼吗？"])),
        (26.5, 41.1, "cabecera", (302, 430), L(
            en=["HOW SHOULD IT BE DONE?"], fr=["COMMENT LA RÉALISER ?"], ru=["КАК ЭТО ДЕЛАЕТСЯ?"], ka=["როგორ უნდა გაკეთდეს?"], zh=["应该怎么做？"])),
        (41.1, 44.0, "final", (302, 740), L(
            en=["ULTRASOUND-GUIDED", "INJECTION"], fr=["INFILTRATION", "ÉCHOGUIDÉE"], ru=["ИНЪЕКЦИЯ ПОД", "КОНТРОЛЕМ УЗИ"],
            ka=["ულტრაბგერით", "კონტროლირებადი ინექცია"], zh=["超声引导", "注射"])),
    ],
    tarjeta=(44.2, 47.4, 955, 1060),
    cubre=[(44.2, 47.4, 1475, 1565)],   # línea «Próximo lunes: …» que el vídeo original deja cortada
    tarjeta_lineas=L(
        en=("Specialist in Physical Education and Sports Medicine", "Medical licence 281903698 · Hospital Memorial Publio Cordón · Madrid"),
        fr=("Spécialiste en médecine de l'éducation physique et du sport", "Médecin n° 281903698 · Hôpital Memorial Publio Cordón · Madrid"),
        ru=("Специалист по лечебной физкультуре и спортивной медицине", "Лицензия врача № 281903698 · Больница Memorial Publio Cordón · Мадрид"),
        ka=("სპეციალისტი ფიზიკური აღზრდისა და სპორტული მედიცინის დარგში", "ექიმის ლიცენზია № 281903698 · საავადმყოფო Memorial Publio Cordón · მადრიდი"),
        zh=("运动医学与体育教育专科医生", "执业医师编号 281903698 · Memorial Publio Cordón 医院 · 马德里")),
)
