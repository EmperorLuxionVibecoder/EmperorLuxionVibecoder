import svgwrite
from svgwrite import cm, mm

def generate_wip_card():
    # Solana/Cyberpunk Palette
    COLORS = {
        "bg": "#0D1117",
        "border": "#30363d",
        "green": "#14F195",
        "purple": "#9945FF",
        "text": "#c9d1d9",
        "subtext": "#8b949e",
        "highlight": "rgba(20, 241, 149, 0.1)"
    }

    dwg = svgwrite.Drawing('wip.svg', size=('500px', '220px'))
    
    # Fonts
    dwg.defs.add(dwg.style("""
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        .text { font-family: 'Fira Code', monospace; fill: #c9d1d9; font-size: 14px; }
        .label { fill: #8b949e; font-size: 12px; }
        .header { fill: #14F195; font-size: 16px; font-weight: bold; }
        .status { fill: #9945FF; font-size: 12px; font-weight: bold; }
        
        /* Glitch Animation for Header */
        @keyframes glitch {
            0% { transform: translate(0) }
            20% { transform: translate(-2px, 2px) }
            40% { transform: translate(-2px, -2px) }
            60% { transform: translate(2px, 2px) }
            80% { transform: translate(2px, -2px) }
            100% { transform: translate(0) }
        }
        .glitch-text { animation: glitch 3s infinite; }
        
        /* Blink Animation for Progress */
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        .blinking { animation: blink 1.5s infinite; }
        
        /* Scanline Animation */
        @keyframes scan {
            from { transform: translateY(-100%); }
            to { transform: translateY(200%); }
        }
        .scanline {
            animation: scan 4s linear infinite;
        }
    """))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=10, ry=10, fill=COLORS['bg'], stroke=COLORS['border'], stroke_width=1))
    
    # Scanline Overlay (masked)
    mask = dwg.defs.add(dwg.mask(id="scan-mask"))
    mask.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill="white", rx=10, ry=10))
    
    scan_group = dwg.add(dwg.g(mask="url(#scan-mask)", opacity=0.05))
    scan_group.add(dwg.rect(insert=(0, 0), size=('100%', '20%'), fill=COLORS['green'], class_="scanline"))

    # Header
    dwg.add(dwg.text("ACTIVE_DIRECTIVES // WORK_QUEUE", insert=(20, 35), class_="text header"))
    
    # Decoration Line
    dwg.add(dwg.line(start=(20, 50), end=(480, 50), stroke=COLORS['purple'], stroke_width=2))

    # Projects
    projects = [
        {"id": "ALPHA_SCANNER", "status": "BUILDING...", "class": "Analytics", "icon": "🕵️‍♂️"},
        {"id": "CIPHER_OWL_DAO", "status": "BUILDING...", "class": "Governance", "icon": "🦉"},
        {"id": "THE_CIPHERVERSE", "status": "BUILDING...", "class": "Metaverse",  "icon": "🌌"}
    ]

    y_pos = 80
    for proj in projects:
        # Row Background Highlight
        # dwg.add(dwg.rect(insert=(20, y_pos - 15), size=('460', '30'), rx=5, fill=COLORS['highlight']))
        
        # Project Name
        dwg.add(dwg.text(f"[{proj['id']}]", insert=(30, y_pos), class_="text", style="font-weight: bold;"))
        
        # Class/Icon
        dwg.add(dwg.text(f"{proj['icon']} {proj['class']}", insert=(230, y_pos), class_="text label"))
        
        # Status
        status_group = dwg.add(dwg.g(class_="blinking"))
        status_group.add(dwg.text(f"[{proj['status']}]", insert=(380, y_pos), class_="status"))
        
        y_pos += 45

    # Footer decoration
    dwg.add(dwg.rect(insert=(20, 190), size=(10, 10), fill=COLORS['green']))
    dwg.add(dwg.rect(insert=(35, 190), size=(10, 10), fill=COLORS['purple']))
    dwg.add(dwg.text("SYS.ONLINE", insert=(60, 200), class_="label", style="font-size: 10px;"))

    dwg.save()

if __name__ == '__main__':
    generate_wip_card()
