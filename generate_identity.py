import svgwrite
from svgwrite import cm, mm

def create_identity_card():
    # Solana/Netrunner Palette (Consistent with wip.svg)
    COLORS = {
        "bg": "#0D1117",
        "border": "#30363d",     # Darker border for consistency
        "accent": "#9945FF",     # Purple
        "text": "#c9d1d9",
        "key": "#00F0FF",        # Cyan
        "val": "#14F195",        # Green
        "comment": "#8b949e"
    }
    
    width = 600
    height = 340
    
    dwg = svgwrite.Drawing('identity.svg', size=(width, height))
    
    # Embedded Fonts & CSS Animations
    dwg.defs.add(dwg.style(f"""
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        
        .bg {{ fill: {COLORS['bg']}; stroke: {COLORS['border']}; stroke-width: 1; }}
        .header-bg {{ fill: #161b22; }}
        
        .code {{ font-family: 'Fira Code', monospace; font-size: 14px; }}
        .key {{ fill: {COLORS['key']}; }}
        .val {{ fill: {COLORS['val']}; }}
        .str {{ fill: {COLORS['text']}; }}
        .bracket {{ fill: {COLORS['text']}; font-weight: bold; }}
        
        .title {{ font-family: 'Fira Code', monospace; font-size: 14px; fill: {COLORS['comment']}; }}
        
        /* Animations */
        @keyframes glitch {{
            0% {{ transform: translate(0) }}
            20% {{ transform: translate(-1px, 1px) }}
            40% {{ transform: translate(-1px, -1px) }}
            60% {{ transform: translate(1px, 1px) }}
            80% {{ transform: translate(1px, -1px) }}
            100% {{ transform: translate(0) }}
        }}
        .glitch-text {{ animation: glitch 4s infinite; }}
        
        @keyframes fade {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        .fading {{ animation: fade 2s infinite; }}
    """))
    
    # 1. Main Container
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=10, ry=10, class_="bg"))
    
    # 2. Header Bar
    dwg.add(dwg.rect(insert=(1, 1), size=(width-2, 40), rx=10, ry=10, class_="header-bg"))

    dwg.add(dwg.rect(insert=(1, 30), size=(width-2, 12), fill="#161b22")) # Flatten bottom
    
    # Traffic Lights
    dwg.add(dwg.circle(center=(25, 20), r=6, fill="#FF5F56", opacity=0.8))
    dwg.add(dwg.circle(center=(45, 20), r=6, fill="#FFBD2E", opacity=0.8))
    dwg.add(dwg.circle(center=(65, 20), r=6, fill="#27C93F", opacity=0.8))
    
    # Title
    dwg.add(dwg.text("IDENTITY_LOG.json", insert=(width/2, 25), text_anchor="middle", class_="title"))

    # 4. Code Content
    content = dwg.add(dwg.g(class_="code", style="transform: translate(30px, 70px)"))
    
    # Helper to create lines
    def add_line(y, parts):
        """ parts is list of (text, class) """
        row = dwg.g(style=f"transform: translateY({y}px)")
        x = 0
        for text, cls in parts:
            t = dwg.text(text, insert=(x, 0), class_=cls)
            row.add(t)
            # Estimate width (rough approx for monospace 14px ~ 8.4px width)
            x += len(text) * 8.5 
        content.add(row)

    # Simplified key-value construction
    lines_data = [
        [("{", "bracket")],
        [('  "user"', "key"), (": ", "str"), ('"EmperorLuxion"', "val"), (",", "str")],
        [('  "class"', "key"), (": ", "str"), ('"Solana Netrunner"', "val"), (",", "str")],
        [('  "faction"', "key"), (": ", "str"), ('"CipherLabs"', "val"), (",", "str")],
        [('  "status"', "key"), (": ", "str"), ('"BUILDING_ON_CHAIN"', "val"), (",", "str")],
        [('  "location"', "key"), (": ", "str"), ('"ENCRYPTED_NODE_01"', "val"), (",", "str")],
        [('  "modules"', "key"), (": [", "bracket")],
        [('    "Smart Contracts"', "val"), (",", "str")],
        [('    "DeFi Protocols"', "val"), (",", "str")],
        [('    "Red Team Ops"', "val")],
        [("  ]", "bracket")],
        [("}", "bracket")]
    ]
    
    y = 0
    for line in lines_data:
        add_line(y, line)
        y += 22

    dwg.save()

if __name__ == '__main__':
    create_identity_card()
