import svgwrite
import math

def generate_stats_card():
    # Theme: Solana Netrunner
    COLORS = {
        "bg": "#0D1117",
        "border": "#30363d",
        "green": "#14F195",
        "purple": "#9945FF",     
        "cyan": "#00F0FF",
        "red": "#FF003C",
        "text": "#e6edf3",
        "dim_text": "#8b949e",
        "bar_bg": "#21262d",
        "grid": "#1a1f26"
    }

    width = 850
    height = 420
    # Ensure asset directory exists or save to relative path correctly
    dwg = svgwrite.Drawing('assets/stats.svg', size=(width, height))

    # CSS Styles for that cyberpunk feel
    dwg.defs.add(dwg.style(f"""
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        .bg {{ fill: {COLORS['bg']}; stroke: {COLORS['border']}; stroke-width: 1; }}
        .header {{ font-family: 'JetBrains Mono', monospace; fill: {COLORS['green']}; font-size: 20px; font-weight: bold; letter-spacing: 2px; }}
        .subheader {{ font-family: 'JetBrains Mono', monospace; fill: {COLORS['purple']}; font-size: 14px; font-weight: bold; letter-spacing: 1px; }}
        .text {{ font-family: 'JetBrains Mono', monospace; fill: {COLORS['text']}; font-size: 13px; }}
        .label {{ font-family: 'JetBrains Mono', monospace; fill: {COLORS['dim_text']}; font-size: 11px; }}
        .stat-value {{ font-family: 'JetBrains Mono', monospace; fill: {COLORS['cyan']}; font-size: 14px; font-weight: bold; }}
        .radar-poly {{ fill: {COLORS['purple']}; fill-opacity: 0.2; stroke: {COLORS['purple']}; stroke-width: 2; }}
        .radar-grid {{ fill: none; stroke: {COLORS['grid']}; stroke-width: 1; stroke-dasharray: 4 2; }}
        .hex-bg {{ fill: {COLORS['bar_bg']}; stroke: {COLORS['border']}; stroke-width: 1; }}
    """))

    # 1. Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=12, ry=12, class_="bg"))
    
    # Grid Pattern (Decoration)
    pattern = dwg.defs.add(dwg.pattern(id="grid_pat", size=(40, 40), patternUnits="userSpaceOnUse"))
    pattern.add(dwg.path(d="M 40 0 L 0 0 0 40", stroke=COLORS['grid'], stroke_width=0.5, fill="none"))
    dwg.add(dwg.rect(insert=(0,0), size=("100%", "100%"), fill="url(#grid_pat)", fill_opacity=0.3))

    # 2. Header
    dwg.add(dwg.text(">> SYSTEM_OVERRIDE // OPERATIVE_PROFILE", insert=(30, 40), class_="header"))
    dwg.add(dwg.line(start=(30, 55), end=(width-30, 55), stroke=COLORS['green'], stroke_width=1, stroke_opacity=0.5))

    # 3. Create Hexagon Radar Chart (Left Side)
    radar_center = (200, 240)
    radar_radius = 110
    
    # Skills: Blockchain, Frontend, Backend, Security, AI, Cloud
    skills = [
        ("BLOCKCHAIN", 0.95),  # High
        ("FRONTEND", 0.90),
        ("BACKEND", 0.85),
        ("SECURITY", 0.80),
        ("AI / ML", 0.75),
        ("CLOUD", 0.70)
    ]
    
    # Draw Radar Grid
    num_vars = len(skills)
    angle_step = 2 * math.pi / num_vars
    
    # Concentric rings
    for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
        points = []
        for i in range(num_vars):
            angle = i * angle_step - math.pi/2
            x = radar_center[0] + radar_radius * r * math.cos(angle)
            y = radar_center[1] + radar_radius * r * math.sin(angle)
            points.append((x, y))
        dwg.add(dwg.polygon(points=points, class_="radar-grid"))

    # Draw Data Polygon
    data_points = []
    for i, (name, score) in enumerate(skills):
        angle = i * angle_step - math.pi/2
        x = radar_center[0] + radar_radius * score * math.cos(angle)
        y = radar_center[1] + radar_radius * score * math.sin(angle)
        data_points.append((x, y))
        
        # Labels
        lx = radar_center[0] + (radar_radius + 25) * math.cos(angle)
        ly = radar_center[1] + (radar_radius + 15) * math.sin(angle)
        
        anchor = "middle"
        if lx < radar_center[0] - 20: anchor = "end"
        if lx > radar_center[0] + 20: anchor = "start"
        
        dwg.add(dwg.text(name, insert=(lx, ly), class_="label", style=f"fill:{COLORS['cyan']}; font-weight:bold", text_anchor=anchor, dominant_baseline="middle"))

    dwg.add(dwg.polygon(points=data_points, class_="radar-poly"))
    # Add points
    for p in data_points:
         dwg.add(dwg.circle(center=p, r=3, fill=COLORS['green']))

    dwg.add(dwg.text("MASTERY_VECTORS", insert=(radar_center[0], radar_center[1] + radar_radius + 50), class_="subheader", text_anchor="middle"))


    # 4. Tech Stack Details (Right Side)
    # Split into columns
    
    col1_x = 420
    col2_x = 640
    start_y = 100
    
    # Column 1: Core Stats & Languages
    dwg.add(dwg.text(">> CORE_METRICS", insert=(col1_x, 85), class_="subheader"))
    
    core_stats = [
        ("Total Commits", "420+", COLORS['green']),
        ("Projects", "12", COLORS['green']),
        ("Years Active", "4", COLORS['purple']),
        ("PRs Reviewed", "42", COLORS['cyan'])
    ]
    
    y = start_y
    for label, val, color in core_stats:
        dwg.add(dwg.text(f"{label}:", insert=(col1_x, y), class_="label"))
        dwg.add(dwg.text(val, insert=(col1_x + 120, y), class_="stat-value", style=f"fill:{color}"))
        y += 25
        
    y += 20
    dwg.add(dwg.text(">> NEURAL_LINKS", insert=(col1_x, y), class_="subheader"))
    y += 25
    
    langs = [
        ("TypeScript", 0.90, "#3178C6"),
        ("Rust", 0.85, "#DEA584"),
        ("Python", 0.80, "#3572A5"),
        ("Solidity", 0.70, "#AA6746")
    ]
    
    bar_w = 140
    bar_h = 6
    for name, pct, col in langs:
        dwg.add(dwg.text(name, insert=(col1_x, y), class_="text", style="font-size:11px"))
        # Bg
        dwg.add(dwg.rect(insert=(col1_x + 75, y-6), size=(bar_w, bar_h), fill=COLORS['bar_bg'], rx=2))
        # Fill
        dwg.add(dwg.rect(insert=(col1_x + 75, y-6), size=(bar_w * pct, bar_h), fill=col, rx=2))
        y += 20


    # Column 2: Recent Tech (Based on user Resume update)
    dwg.add(dwg.text(">> ACTIVE_MODULES", insert=(col2_x, 85), class_="subheader"))
    
    modules = [
        "Next.js / React",
        "Solana / Anchor",
        "Node.js / Express",
        "Docker / K8s",
        "Terraform",
        "PyTorch / AI"
    ]
    
    y = start_y
    for mod in modules:
        # Tech decoration like a terminal line
        dwg.add(dwg.text("> ", insert=(col2_x, y), class_="label", style=f"fill:{COLORS['green']}"))
        dwg.add(dwg.text(mod, insert=(col2_x + 15, y), class_="text"))
        y += 25

    # 5. Bottom Status Bar
    dwg.add(dwg.line(start=(30, height-40), end=(width-30, height-40), stroke=COLORS['border'], stroke_width=1))
    
    dwg.add(dwg.text("STATUS: ONLINE", insert=(30, height-20), class_="label", style=f"fill:{COLORS['green']}"))
    dwg.add(dwg.text("ENCRYPTION: AES-256-GCM", insert=(width/2, height-20), class_="label", text_anchor="middle"))
    dwg.add(dwg.text("VERSION: v2.4.0-alpha", insert=(width-30, height-20), class_="label", text_anchor="end", style=f"fill:{COLORS['purple']}"))

    dwg.save()

if __name__ == '__main__':
    generate_stats_card()
