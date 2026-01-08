import svgwrite

def generate_signature_card():
    # Solana/Netrunner Palette
    COLORS = {
        "text": "#c9d1d9",
        "comment": "#8b949e",
        "green": "#14F195",
        "purple": "#9945FF",
        "cyan": "#00F0FF",
        "dim": "#484f58"
    }

    width = 500
    height = 120
    dwg = svgwrite.Drawing('signature.svg', size=(width, height))

    # Styles
    dwg.defs.add(dwg.style(f"""
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        .text {{ font-family: 'Fira Code', monospace; fill: {COLORS['text']}; font-size: 12px; }}
        .dim {{ font-family: 'Fira Code', monospace; fill: {COLORS['comment']}; font-size: 12px; }}
        .enc {{ font-family: 'Fira Code', monospace; fill: {COLORS['green']}; font-size: 12px; }}
        .header {{ font-family: 'Fira Code', monospace; fill: {COLORS['purple']}; font-size: 12px; font-weight: bold; }}
    """))

    # No background rect -> transparent clean look, or maybe a very subtle border?
    # User asked for "clean". Let's do no background, just text, centered-ish.
    
    x = 10
    y = 20
    line_height = 20

    # Line 1
    dwg.add(dwg.text("-----BEGIN PGP SIGNATURE-----", insert=(x, y), class_="header"))
    y += line_height

    # Line 2
    dwg.add(dwg.text("Version: GnuPG v2.0.22 (GNU/Linux)", insert=(x, y), class_="dim"))
    y += line_height * 1.5

    # Line 3 (The block)
    dwg.add(dwg.text("iQEcBAEBAgAGBQJS2O+LAAoJE...[ENCRYPTED_BLOCK]...Ende", insert=(x, y), class_="enc"))
    y += line_height * 1.5

    # Line 4
    dwg.add(dwg.text("-----END PGP SIGNATURE-----", insert=(x, y), class_="header"))

    dwg.save()

if __name__ == '__main__':
    generate_signature_card()
