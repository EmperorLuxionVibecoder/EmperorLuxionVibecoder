"""Generate assets/register.svg — the operator log extract.

Renders the most recent entries from data/register.json as a ledger plate.
With no synced data it renders an honest AWAITING FIRST SYNC state — the
register never shows invented entries.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lyra_type
from lyra_plates import PAL, footer, open_plate, title_band

ROOT = Path(__file__).parent.parent
W, H = 1200, 520
MAX_ROWS = 9

COLS = [("TIME UTC", 60), ("AGENT", 300), ("ACTION", 490),
        ("VENUE", 730), ("NOTE", 950)]


def row(entry: dict, y: float) -> str:
    fields = [
        (entry.get("t", ""), 60, PAL["soft"]),
        (entry.get("agent", "").upper(), 300, PAL["ink"]),
        (entry.get("action", "").upper(), 490, PAL["bronze"]),
        (entry.get("venue", "").upper(), 730, PAL["soft"]),
        (entry.get("note", ""), 950, PAL["soft"]),
    ]
    parts = []
    for text, x, fill in fields:
        if text:
            parts.append(lyra_type.svg_text(text, x, y, "mono", "regular", 12,
                                            fill, letter_spacing=1.2))
    return "\n  ".join(parts)


def main() -> None:
    data = json.loads((ROOT / "data" / "register.json").read_text(encoding="utf-8"))
    entries = data.get("entries", [])[:MAX_ROWS]
    synced = data.get("synced")

    right = f"SYNC: {synced[:10]}" if synced else "SYNC: PENDING"

    svg = [open_plate(W, H, "reg")]
    svg.append("  " + title_band(
        W, "LYRA SYSTEMS · OPERATOR LOG", "The register",
        "Every action the system takes is written down. The most recent entries appear here.",
        right))

    if entries:
        for name, x in COLS:
            svg.append("  " + lyra_type.svg_text(name, x, 172, "mono", "regular",
                                                 10.5, PAL["soft"], letter_spacing=2))
        svg.append(f'  <line x1="60" y1="186" x2="{W - 60}" y2="186" '
                   f'stroke="{PAL["hair"]}" stroke-width="1.5"/>')
        y = 214
        for entry in entries:
            svg.append("  " + row(entry, y))
            y += 27
    else:
        svg.append("  " + lyra_type.svg_text(
            "AWAITING FIRST SYNC", W / 2, 280, "mono", "regular", 14,
            PAL["ink"], letter_spacing=3.5, anchor="middle"))
        svg.append("  " + lyra_type.svg_text(
            "The register updates daily from the operator log. Entries appear once the sync is live.",
            W / 2, 312, "serif", "italic", 14.5, PAL["mut"], anchor="middle"))

    svg.append("  " + footer(W, H, "OPERATOR LOG EXTRACT · ACTIONS ONLY · NOT A PERFORMANCE RECORD"))
    svg.append("</svg>\n")

    out = ROOT / "assets" / "register.svg"
    out.write_text("\n".join(svg), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(entries)} entries, sync={synced or 'pending'})")


if __name__ == "__main__":
    main()
