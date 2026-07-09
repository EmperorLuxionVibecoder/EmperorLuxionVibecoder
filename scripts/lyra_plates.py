"""Shared frame, palette and title band for generated Lyra plates."""
from __future__ import annotations

import lyra_type

PAL = {
    "bone_top": "#FBF8F1", "bone_bot": "#ECE3D2", "ink": "#1C1813",
    "mut": "#6B6253", "soft": "#9C8E76", "bronze": "#A87F4B",
    "bronze_bright": "#C49A5E", "gold": "#C99A3A", "hair": "#E4DBCB",
}


def open_plate(w: int, h: int, grad_id: str) -> str:
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{PAL["bone_top"]}"/><stop offset="1" stop-color="{PAL["bone_bot"]}"/>
    </linearGradient>
    <radialGradient id="{grad_id}-glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{PAL["gold"]}" stop-opacity="0.42"/><stop offset="1" stop-color="{PAL["gold"]}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect x="5" y="5" width="{w - 10}" height="{h - 10}" rx="16" fill="url(#{grad_id})" stroke="{PAL["hair"]}" stroke-width="2"/>
  <rect x="15" y="15" width="{w - 30}" height="{h - 30}" rx="10" fill="none" stroke="{PAL["bronze"]}" stroke-opacity="0.22" stroke-width="1"/>'''


def title_band(w: int, kicker: str, title: str, subtitle: str,
               right_note: str | None = None) -> str:
    parts = [
        lyra_type.svg_text(kicker, 60, 58, "mono", "regular", 11,
                           PAL["soft"], letter_spacing=2.5),
        lyra_type.svg_text(title, 60, 100, "serif", "regular", 30, PAL["ink"]),
        lyra_type.svg_text(subtitle, 60, 128, "serif", "italic", 15, PAL["mut"]),
    ]
    if right_note:
        parts.append(lyra_type.svg_text(right_note, w - 60, 58, "mono", "regular",
                                        12, PAL["bronze"], letter_spacing=2,
                                        anchor="end"))
    return "\n  ".join(parts)


def footer(w: int, h: int, caption: str) -> str:
    line = (f'<line x1="60" y1="{h - 60}" x2="{w - 60}" y2="{h - 60}" '
            f'stroke="{PAL["hair"]}" stroke-width="1.5"/>')
    cap = lyra_type.svg_text(caption, w / 2, h - 36, "mono", "regular", 9.5,
                             PAL["soft"], letter_spacing=1.9, anchor="middle",
                             opacity="0.9")
    return f"{line}\n  {cap}"
