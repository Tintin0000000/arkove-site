#!/usr/bin/env python3
"""
Logo « Épargne malin » : génère les SVG (lettres vectorisées, aucune police requise).

    python3 brand/logo.py        # écrit brand/*.svg ; brand/export.mjs en fait des PNG

Idée : l'accent aigu du « é » devient une flèche qui monte (l'argent qui grandit),
le tout frappé dans une pièce. Typo : Instrument Serif (SIL OFL), comme les vidéos.
"""
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"

INK, BG = "#f3eee4", "#0d0c0a"
INK_LIGHT, BG_LIGHT = "#171310", "#f3eee4"
GOLD_DEFS = """<linearGradient id="gold" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="#f6d690"/><stop offset="0.55" stop-color="#e2b467"/><stop offset="1" stop-color="#b98436"/>
    </linearGradient>"""


class Font:
    def __init__(self, name):
        self.tt = TTFont(FONTS / name)
        self.upm = self.tt["head"].unitsPerEm
        self.hbfont = hb.Font(hb.Face(_sfnt(FONTS / name)))
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        return [(self.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def path(self, text, size, x, y):
        """Chemin SVG du texte, ligne de base en (x, y), taille en px. Renvoie (d, largeur, bbox)."""
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        bp = BoundsPen(self.gs)
        cx = 0
        for name, adv, xo, yo in self.shape(text):
            t = (s, 0, 0, -s, x + (cx + xo) * s, y - yo * s)
            self.gs[name].draw(TransformPen(pen, t))
            self.gs[name].draw(TransformPen(bp, t))
            cx += adv
        return pen.getCommands(), cx * s, bp.bounds


def _sfnt(path):
    """Police décompressée en TTF (harfbuzz ne lit pas le WOFF2)."""
    import io
    tt = TTFont(path)
    tt.flavor = None
    out = io.BytesIO()
    tt.save(out)
    return out.getvalue()


SERIF = Font("InstrumentSerif-Regular.woff2")
ITALIC = Font("InstrumentSerif-Italic.woff2")


def arrow(x0, y0, x1, y1, w, color="url(#gold)"):
    """Accent-flèche de (x0, y0) vers (x1, y1), pointe au bout."""
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    h = w * 2.1
    p1 = (x1 - h * math.cos(a - 0.62), y1 - h * math.sin(a - 0.62))
    p2 = (x1 - h * math.cos(a + 0.62), y1 - h * math.sin(a + 0.62))
    return (f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f} M{p1[0]:.1f} {p1[1]:.1f} L{x1:.1f} {y1:.1f} L{p2[0]:.1f} {p2[1]:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def e_with_arrow(font, size, x, y, color, arrow_color="url(#gold)"):
    """Le « é » du logo : un e de la police + l'accent-flèche dessiné."""
    d, adv, (xmin, ymin, xmax, ymax) = font.path("e", size, x, y)
    w = size * (0.062 if font is ITALIC else 0.055)
    cx = (xmin + xmax) / 2 + size * 0.06                    # léger décalage pour l'italique
    top = ymin - size * 0.07
    x0, y0 = cx - size * 0.10, top
    x1, y1 = cx + size * 0.13, top - size * 0.21
    return f'<path d="{d}" fill="{color}"/>' + arrow(x0, y0, x1, y1, w, arrow_color), adv, (xmin, y1 - w, xmax, ymax)


def coin(cx, cy, r, glyph_color="url(#gold)", bg=True):
    """L'icône : une pièce frappée d'un é-flèche."""
    size = r * 2.05
    # On centre le « é » (e + flèche) dans la pièce.
    _, _, (x0, y0, x1, y1) = e_with_arrow(ITALIC, size, 0, 0, glyph_color)
    dx, dy = cx - (x0 + x1) / 2, cy - (y0 + y1) / 2 + r * 0.02
    e, _, _ = e_with_arrow(ITALIC, size, dx, dy, glyph_color)
    face = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#face)"/>' if bg else ""
    return f"""{face}
    <circle cx="{cx}" cy="{cy}" r="{r - r * 0.022}" fill="none" stroke="url(#gold)" stroke-width="{r * 0.044:.1f}"/>
    <circle cx="{cx}" cy="{cy}" r="{r * 0.9:.1f}" fill="none" stroke="#e8c27a" stroke-opacity="0.28" stroke-width="{r * 0.008:.1f}" stroke-dasharray="{r * 0.012:.1f} {r * 0.028:.1f}"/>
    {e}"""


def avatar_flat(fill, ink, ring):
    """Avatar à fond plein (or ou crème) : é-flèche et anneau d'une seule couleur, très lisible en petit."""
    cx = cy = 512
    r = 468
    size = r * 2.05
    _, _, (x0, y0, x1, y1) = e_with_arrow(ITALIC, size, 0, 0, ink, ink)
    dx, dy = cx - (x0 + x1) / 2, cy - (y0 + y1) / 2 + r * 0.02
    e, _, _ = e_with_arrow(ITALIC, size, dx, dy, ink, ink)
    return (f'<rect width="1024" height="1024" fill="{fill}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - r * 0.022:.1f}" fill="none" stroke="{ring}" stroke-width="{r * 0.03:.1f}"/>' + e)


def defs():
    return f"""<defs>
    {GOLD_DEFS}
    <radialGradient id="face" cx="0.4" cy="0.35" r="0.75">
      <stop offset="0" stop-color="#2a241c"/><stop offset="1" stop-color="#110f0c"/>
    </radialGradient>
  </defs>"""


def svg(w, h, body, bg=None):
    back = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n  {defs()}\n  {back}\n  {body}\n</svg>\n'


def wordmark(x, y, size, ink, gold="url(#gold)"):
    """« épargne malin » sur une ligne, ligne de base en y. Renvoie (svg, largeur)."""
    e, adv, _ = e_with_arrow(SERIF, size, x, y, ink, gold)
    d1, w1, _ = SERIF.path("pargne", size, x + adv, y)
    gap = size * 0.24
    d2, w2, _ = ITALIC.path("malin", size, x + adv + w1 + gap, y)
    return e + f'<path d="{d1}" fill="{ink}"/><path d="{d2}" fill="{gold}"/>', adv + w1 + gap + w2


def build():
    out = {}
    # 1. Avatar TikTok / Instagram : carré plein, la pièce au centre (l'appli recadre en rond).
    out["avatar.svg"] = svg(1024, 1024, coin(512, 512, 468), bg=BG)
    # Variantes à fond plein : se détachent mieux dans le mode sombre de TikTok.
    out["avatar-or.svg"] = svg(1024, 1024, avatar_flat("url(#gold)", "#171310", "#171310"))
    out["avatar-creme.svg"] = svg(1024, 1024, avatar_flat("#f3eee4", "#171310", "#b98436"))
    # 2. Icône seule, fond transparent.
    out["icone.svg"] = svg(1024, 1024, coin(512, 512, 500))
    # 3. Logo horizontal (fond sombre et fond clair).
    for name, ink, bg in (("logo-horizontal.svg", INK, BG), ("logo-horizontal-clair.svg", INK_LIGHT, BG_LIGHT)):
        H, size = 400, 210
        wm, ww = wordmark(0, 0, size, ink)
        W = int(60 + 280 + 50 + ww + 70)
        body = coin(60 + 140, H / 2, 140) + f'<g transform="translate({60 + 280 + 50} {H / 2 + size * 0.24:.1f})">{wm}</g>'
        out[name] = svg(W, H, body, bg=bg)
    # 4. Logo empilé (bannières, miniatures).
    H, size = 1000, 190
    wm, ww = wordmark(0, 0, size, INK)
    W = int(max(ww + 160, 1000))
    body = coin(W / 2, 330, 250) + f'<g transform="translate({(W - ww) / 2:.1f} {780})">{wm}</g>'
    out["logo-empile.svg"] = svg(W, H, body, bg=BG)
    # 5. Filigrane pour les vidéos : blanc cassé semi-opaque, fond transparent.
    wm, ww = wordmark(0, 0, 120, INK, gold="#e8c27a")
    out["filigrane.svg"] = svg(int(ww + 40), 200, f'<g opacity="0.85" transform="translate(20 140)">{wm}</g>')

    for name, content in out.items():
        (HERE / name).write_text(content, encoding="utf-8")
        print("✓", name)


if __name__ == "__main__":
    build()
