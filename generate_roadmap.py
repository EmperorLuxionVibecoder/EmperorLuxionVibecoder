import svgwrite

def generate_roadmap_card():
    # Solana/Netrunner Palette
    COLORS = {
        "bg": "#0D1117",
        "border": "#30363d",
        "green": "#14F195",
        "purple": "#9945FF",
        "cyan": "#00F0FF",
        "text": "#c9d1d9",
        "label": "#8b949e",
        "dim": "#484f58"
    }

    width = 600
    height = 400
    dwg = svgwrite.Drawing('roadmap.svg', size=(width, height))

    # Styles
    dwg.defs.add(dwg.style(f"""
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        .text {{ font-family: 'Fira Code', monospace; fill: {COLORS['text']}; font-size: 12px; }}
        .header {{ font-family: 'Fira Code', monospace; fill: {COLORS['green']}; font-size: 16px; font-weight: bold; }}
        .phase-title {{ font-family: 'Fira Code', monospace; fill: {COLORS['purple']}; font-size: 14px; font-weight: bold; }}
        .status-done {{ fill: {COLORS['green']}; }}
        .status-wip {{ fill: {COLORS['cyan']}; }}
        .status-todo {{ fill: {COLORS['dim']}; }}
    """))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=10, ry=10, fill=COLORS['bg'], stroke=COLORS['border'], stroke_width=1))

    # Header
    dwg.add(dwg.text("STRATEGIC_ROADMAP // PRD_V1.0", insert=(20, 35), class_="header"))
    dwg.add(dwg.line(start=(20, 50), end=(width-20, 50), stroke=COLORS['green'], stroke_width=2))

    # Phases
    phases = [
        {
            "title": "PHASE_1: CORE_INFRASTRUCTURE [Q1]",
            "items": [
                {"name": "Establish GitHub Presence", "status": "done"},
                {"name": "Define Brand Identity (Netrunner)", "status": "done"},
                {"name": "Deploy Portfolio Skeletons", "status": "done"}
            ]
        },
        {
            "title": "PHASE_2: ASSET_GENERATION [Q2]",
            "items": [
                {"name": "Automate Metrics (Python/Actions)", "status": "done"},
                {"name": "Create Static SVG Assets", "status": "done"},
                {"name": "Launch 'CipherLabs' Components", "status": "wip"}
            ]
        },
        {
            "title": "PHASE_3: DECENTRALIZED_APPS [Q3-Q4]",
            "items": [
                {"name": "Solana Smart Contract Integration", "status": "todo"},
                {"name": "Deploy DApp Frontend", "status": "todo"},
                {"name": "Audit & Security Review", "status": "todo"}
            ]
        }
    ]

    y = 80
    x = 30

    for phase in phases:
        # Phase Connector Line
        dwg.add(dwg.line(start=(20, y-10), end=(20, y + len(phase['items'])*25 + 20), stroke=COLORS['dim'], stroke_width=1, stroke_dasharray="4,4"))
        
        # Phase Title
        dwg.add(dwg.text(phase['title'], insert=(x, y), class_="phase-title"))
        y += 25

        # Items
        for item in phase['items']:
            # Status Indicator
            if item['status'] == 'done':
                indicator_char = "[X]"
                style_class = "status-done"
            elif item['status'] == 'wip':
                indicator_char = "[/]"
                style_class = "status-wip"
            else:
                indicator_char = "[ ]"
                style_class = "status-todo"
            
            dwg.add(dwg.text(f"{indicator_char} {item['name']}", insert=(x + 10, y), class_="text"))
            y += 25
        
        y += 15 # Gap between phases

    # PRD Sidebar (Visual Flavor)
    sidebar_x = 420
    dwg.add(dwg.line(start=(sidebar_x, 60), end=(sidebar_x, height-20), stroke=COLORS['border'], stroke_width=1))
    
    dwg.add(dwg.text(">> PRD_SUMMARY", insert=(sidebar_x + 10, 80), class_="text", style=f"fill:{COLORS['cyan']}; font-weight:bold;"))
    
    prd_items = [
        "ROLE: Full Stack Engineer",
        "FOCUS: Blockchain/Solana",
        "EXP: 5+ Years",
        "SecLevel: RED_TEAM",
        "Availability: REMOTE"
    ]
    
    py = 110
    for item in prd_items:
         dwg.add(dwg.text(item, insert=(sidebar_x + 10, py), class_="text", style="font-size:10px;"))
         py += 20
         
    # Stamp
    dwg.add(dwg.rect(insert=(sidebar_x + 10, py+20), size=(100, 30), fill="none", stroke=COLORS['green'], stroke_width=2, rx=5))
    dwg.add(dwg.text("APPROVED", insert=(sidebar_x + 25, py+40), class_="header", style=f"font-size:14px; fill:{COLORS['green']}"))

    dwg.save()

if __name__ == '__main__':
    generate_roadmap_card()
