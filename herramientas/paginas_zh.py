# -*- coding: utf-8 -*-
"""Paquete del chino simplificado (/zh/). Textos en zh_src/p*.py; estructura y valores no textuales de paginas_plantilla.py."""
import copy, importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paginas_plantilla as T
from zh_src import p1, p2, p3, p4, p5, p6

META = {
 "lang": "zh", "locale": "zh_CN", "name": "中文", "thanks": "xiexie.html",
 "extra_fonts": "&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@500;700",
 "font_css": ":root{--display:'Cormorant Garamond','Noto Serif SC','Songti SC',serif;--body:'Manrope','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif}",
}
SLUGS = dict(T.SLUGS)

_TEXT = {}
for m in (p1, p2, p3, p6): _TEXT.update(m.T)
_TEXT.update(p4.T)

PAGES = []
for src in T.PAGES:
    d = copy.deepcopy(src)
    tx = _TEXT[d["slug"]]
    for k, v in tx.items():
        d[k] = v
    PAGES.append(d)

UI = p4.UI
HOME = p5.HOME
HOME_FAQ = p5.HOME_FAQ
ABOUT = dict(copy.deepcopy(T.ABOUT))
ABOUT.update(p5.ABOUT)
