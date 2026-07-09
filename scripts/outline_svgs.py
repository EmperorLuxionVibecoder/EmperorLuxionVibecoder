"""Convert <text> elements in the static profile SVGs to outlined <path>s.

Run locally on the Windows dev machine (needs Palatino Linotype et al.).
Keeps every non-text byte of the SVG untouched; each replaced element
carries a comment with the original string so the files stay editable.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lyra_type

ASSETS = Path(__file__).parent.parent / "assets"
DEFAULT_TARGETS = ["lyra-hero.svg", "viz-onesided.svg", "viz-recenter.svg",
                   "viz-riskoverlay.svg"]

TEXT_RE = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.DOTALL)
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


def classify(attrs: dict) -> tuple[str, str]:
    fam = attrs.get("font-family", "")
    kind = "mono" if "monospace" in fam else "sans" if "Inter" in fam else "serif"
    if attrs.get("font-style") == "italic":
        style = "italic"
    elif attrs.get("font-weight") in ("600", "700", "bold"):
        style = "bold"
    else:
        style = "regular"
    if kind != "mono" and style == "bold":
        style = "regular"  # serif 500/600 titles render regular Palatino
    return kind, style


def replace(match: re.Match) -> str:
    attrs = dict(ATTR_RE.findall(match.group(1)))
    text = html.unescape(match.group(2).strip())
    kind, style = classify(attrs)
    frag = lyra_type.svg_text(
        text,
        x=float(attrs["x"]),
        y=float(attrs["y"]),
        kind=kind,
        style=style,
        size=float(attrs["font-size"]),
        fill=attrs["fill"],
        letter_spacing=float(attrs.get("letter-spacing", 0) or 0),
        anchor=attrs.get("text-anchor", "start"),
        opacity=attrs.get("opacity"),
    )
    safe = text.replace("--", "-")
    return f"<!-- {safe} -->{frag}"


def main() -> None:
    for name in (sys.argv[1:] or DEFAULT_TARGETS):
        path = ASSETS / name
        src = path.read_text(encoding="utf-8")
        out, n = TEXT_RE.subn(replace, src)
        path.write_text(out, encoding="utf-8")
        print(f"{name}: outlined {n} text elements")


if __name__ == "__main__":
    main()
