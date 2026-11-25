"""Design tokens + text-to-outline helpers shared by build_assets.py and activity.py."""
from pathlib import Path
import re
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path(__file__).resolve().parent / ".fonts"
FONT_URLS = {
    "InterTight.ttf": "https://github.com/google/fonts/raw/main/ofl/intertight/InterTight%5Bwght%5D.ttf",
    "JetBrainsMono.ttf": "https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}

THEMES = {
    "dark": dict(
        bg="#140809", surface="#1B0B0E", line="#3B1A20", wine="#6E1423",
        bordeaux="#8E2433", accent="#C9A27E", text="#F3E7E2", muted="#A68E89",
        faint="#6E5854",
        heat=["#261316", "#4E1722", "#7A1A2B", "#A8344A", "#C9A27E"],
    ),
    "light": dict(
        bg="#F6F0EC", surface="#FBF7F4", line="#E4D3CD", wine="#7A1626",
        bordeaux="#9A2A3A", accent="#9C7450", text="#2A0F14", muted="#76605C",
        faint="#B49F99",
        heat=["#EDE3DE", "#E6BFC3", "#C77380", "#8E2433", "#5A0E1B"],
    ),
}


def _num(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Font:
    _cache = {}

    def __init__(self, file, wght):
        path = FONT_DIR / file
        if not path.exists():
            FONT_DIR.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(FONT_URLS[file], path)
        f = instantiateVariableFont(TTFont(path), {"wght": wght})
        self.gs = f.getGlyphSet()
        self.cmap = f.getBestCmap()
        self.upm = f["head"].unitsPerEm
        self.hmtx = f["hmtx"]
        self.key = ("s" if file.startswith("Inter") else "m") + str(wght)

    @classmethod
    def get(cls, file, wght):
        key = (file, wght)
        if key not in cls._cache:
            cls._cache[key] = cls(file, wght)
        return cls._cache[key]

    def _glyph(self, ch):
        return self.cmap.get(ord(ch)) or self.cmap.get(ord("?"))

    def width(self, text, size, ls=0.0):
        s = size / self.upm
        w = sum(self.hmtx[self._glyph(c)][0] * s for c in text)
        return w + ls * max(len(text) - 1, 0)

    def uses(self, text, x, y, size, ls=0.0, anchor="start"):
        s = size / self.upm
        w = self.width(text, size, ls)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        out, cx = [], x
        for c in text:
            g = self._glyph(c)
            gid = self.key + re.sub(r"[^A-Za-z0-9]", "_", g)
            if gid not in DEFS:
                pen = SVGPathPen(self.gs, ntos=lambda v: str(round(v)))
                self.gs[g].draw(pen)
                DEFS[gid] = pen.getCommands()
            if DEFS[gid]:
                out.append(f'<use href="#{gid}" transform="translate({_num(cx)} {_num(y)}) scale({s:.4g} {-s:.4g})"/>')
            cx += self.hmtx[g][0] * s + ls
        return "".join(out)


DEFS = {}


def sans(w=400):
    return Font.get("InterTight.ttf", w)


def mono(w=500):
    return Font.get("JetBrainsMono.ttf", w)


def text(font, s, x, y, size, fill, ls=0.0, anchor="start", extra=""):
    return f'<g fill="{fill}"{extra}>{font.uses(s, x, y, size, ls, anchor)}</g>'


def wrap(font, s, size, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if font.width(trial, size) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def svg(w, h, body, label):
    defs = "".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items())
    DEFS.clear()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
        f"<title>{label}</title><defs>{defs}</defs>{body}</svg>\n"
    )


def write_pair(name, build):
    for theme, t in THEMES.items():
        out = ROOT / "assets" / f"{name}-{theme}.svg"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(t), encoding="utf-8")
