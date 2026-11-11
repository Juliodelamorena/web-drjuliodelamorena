# -*- coding: utf-8 -*-
"""Utilidades para generar los artículos en chino a partir de la versión inglesa (estructura, imágenes, enlaces) + textos chinos."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(os.path.dirname(D), "i18n_extra")

def tags(s): return sorted(re.findall(r"</?[a-z0-9]+", s))

def build(slug, tx, vid=None):
    en = json.load(open(os.path.join(EX, "en", "articulos", slug + ".json"), encoding="utf-8"))
    out = dict(en)
    for k in ("categoria", "titulo", "resumen", "descripcion", "entradilla", "imagen_alt", "temas"):
        out[k] = tx[k]
    secs = []
    assert len(tx["secciones"]) == len(en["secciones"]), (slug, "secciones")
    for (et, eh), (zt, zh) in zip(en["secciones"], tx["secciones"]):
        if zh is None:       # sección de vídeo: se deriva del HTML inglés
            zh = eh.replace(".en.", ".zh.").replace('"inLanguage": "en"', '"inLanguage": "zh"')
            for a, b in (vid or {}).items():
                assert a in zh, (slug, a)
                zh = zh.replace(a, b)
        assert tags(eh) == tags(zh), (slug, et, tags(eh), tags(zh))
        secs.append([zt, zh])
    out["secciones"] = secs
    assert len(tx["faq"]) == len(en["faq"]), (slug, "faq")
    out["faq"] = [list(f) for f in tx["faq"]]
    json.dump(out, open(os.path.join(EX, "zh", "articulos", slug + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", slug)
