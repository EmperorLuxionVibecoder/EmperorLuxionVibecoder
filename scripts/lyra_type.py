"""Shared typography for Lyra Systems plates.

Display text in the profile SVGs is outlined to vector paths so every
viewer sees the same letterforms regardless of OS fonts. Outlining uses
local system fonts (Palatino Linotype / Segoe UI / Consolas on the
Windows dev machine); results are cached in scripts/type_cache.json and
committed, so CI (ubuntu, none of those fonts) reproduces the exact same
paths. A string missing from the cache falls back to a <text> element
with a robust font stack rather than failing the build.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from fontTools.misc.transform import Transform
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    _HAVE_FONTTOOLS = True
except ImportError:  # CI without fontTools still works via the cache
    _HAVE_FONTTOOLS = False

FONT_DIR = Path(os.environ.get("SYSTEMROOT", r"C:\Windows")) / "Fonts"
CACHE_PATH = Path(__file__).parent / "type_cache.json"

# (family kind, style) -> font file. Palatino Linotype is the serif the
# live site falls back to (and what the approved mockup rendered in).
FONTS = {
    ("serif", "regular"): "pala.ttf",
    ("serif", "bold"): "palab.ttf",
    ("serif", "italic"): "palai.ttf",
    ("sans", "regular"): "segoeui.ttf",
    ("mono", "regular"): "consola.ttf",
    ("mono", "bold"): "consolab.ttf",
}

MONO_STACK = "ui-monospace,'SF Mono','Cascadia Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SERIF_STACK = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
SANS_STACK = "'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"
STACKS = {"serif": SERIF_STACK, "sans": SANS_STACK, "mono": MONO_STACK}

_font_cache: dict = {}
_type_cache: dict | None = None


def _load_font(kind: str, style: str):
    key = (kind, style)
    if key not in _font_cache:
        font = TTFont(FONT_DIR / FONTS[key])
        upm = font["head"].unitsPerEm
        cmap = font.getBestCmap()
        glyphset = font.getGlyphSet()
        hmtx = font["hmtx"]
        kern: dict = {}
        if "kern" in font:
            try:
                for table in font["kern"].kernTables:
                    kern.update(table.kernTable)
            except Exception:
                pass
        _font_cache[key] = (upm, cmap, glyphset, hmtx, kern)
    return _font_cache[key]


def shape(text: str, kind: str, style: str, size: float,
          letter_spacing: float = 0.0) -> tuple[str, float]:
    """Outline `text` at origin (x=0, baseline y=0). Returns (path_d, width)."""
    upm, cmap, glyphset, hmtx, kern = _load_font(kind, style)
    scale = size / upm
    x = 0.0
    parts: list[str] = []
    prev = None
    for ch in text:
        cp = ord(ch)
        if cp == 0xA0:  # non-breaking space renders as a space
            cp = 0x20
        gname = cmap.get(cp) or cmap.get(0x20)
        if prev is not None:
            x += kern.get((prev, gname), 0) * scale + letter_spacing
        pen = SVGPathPen(glyphset, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        glyphset[gname].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += hmtx[gname][0] * scale
        prev = gname
    return " ".join(parts), x


def _cache() -> dict:
    global _type_cache
    if _type_cache is None:
        if CACHE_PATH.exists():
            _type_cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        else:
            _type_cache = {}
    return _type_cache


def _cache_key(text: str, kind: str, style: str, size: float, spacing: float) -> str:
    return f"{kind}|{style}|{size}|{spacing}|{text}"


def _fonts_available() -> bool:
    return _HAVE_FONTTOOLS and all((FONT_DIR / f).exists() for f in FONTS.values())


def shaped(text: str, kind: str, style: str, size: float,
           letter_spacing: float = 0.0) -> tuple[str, float] | None:
    """Cache-backed shape(). Returns (path_d, width) or None when the
    string is uncached and fonts are unavailable (CI with a new string)."""
    key = _cache_key(text, kind, style, size, letter_spacing)
    cache = _cache()
    if key in cache:
        entry = cache[key]
        return entry["d"], entry["w"]
    if not _fonts_available():
        return None
    d, w = shape(text, kind, style, size, letter_spacing)
    w = round(w, 2)
    cache[key] = {"d": d, "w": w}
    CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=0, sort_keys=True),
        encoding="utf-8")
    return d, w


def svg_text(text: str, x: float, y: float, kind: str, style: str, size: float,
             fill: str, letter_spacing: float = 0.0, anchor: str = "start",
             opacity: str | None = None) -> str:
    """An SVG fragment for `text`: outlined <path> when possible, else a
    <text> element on a resilient font stack."""
    res = shaped(text, kind, style, size, letter_spacing)
    op = f' opacity="{opacity}"' if opacity else ""
    if res is None:
        anch = f' text-anchor="{anchor}"' if anchor != "start" else ""
        stylea = ' font-style="italic"' if style == "italic" else ""
        weight = ' font-weight="600"' if style == "bold" else ""
        ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
        return (f'<text x="{x}" y="{y}" font-family="{STACKS[kind]}" '
                f'font-size="{size}"{ls}{stylea}{weight}{anch} fill="{fill}"{op}>'
                f'{text}</text>')
    d, w = res
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    return (f'<path transform="translate({round(x, 2)} {round(y, 2)})" '
            f'd="{d}" fill="{fill}"{op}/>')
