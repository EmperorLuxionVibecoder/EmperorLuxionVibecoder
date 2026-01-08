import svgwrite

def generate_stats_card():
    # Solana/Netrunner Palette
    COLORS = {
        "bg": "#0D1117",
        "border": "#30363d",
        "green": "#14F195",
        "purple": "#9945FF",
        "cyan": "#00F0FF",
        "red": "#FF003C",
        "text": "#c9d1d9",
        "label": "#8b949e",
        "bar_bg": "#21262d"
    }

    width = 500
    height = 300
    dwg = svgwrite.Drawing('stats.svg', size=(width, height))

    # Styles
    dwg.defs.add(dwg.style(f"""
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        .text {{ font-family: 'Fira Code', monospace; fill: {COLORS['text']}; font-size: 14px; }}
        .label {{ font-family: 'Fira Code', monospace; fill: {COLORS['label']}; font-size: 12px; }}
        .value {{ font-family: 'Fira Code', monospace; fill: {COLORS['green']}; font-size: 12px; font-weight: bold; }}
        .header {{ font-family: 'Fira Code', monospace; fill: {COLORS['purple']}; font-size: 16px; font-weight: bold; }}
        .bar-bg {{ fill: {COLORS['bar_bg']}; }}
        .bar-fill {{ fill: {COLORS['cyan']}; }}
        .bar-fill-secondary {{ fill: {COLORS['green']}; }}
    """))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=10, ry=10, fill=COLORS['bg'], stroke=COLORS['border'], stroke_width=1))

    # Header
    dwg.add(dwg.text("OPERATIVE_STATS // SKILL_TREE", insert=(20, 35), class_="header"))
    dwg.add(dwg.line(start=(20, 50), end=(width-20, 50), stroke=COLORS['purple'], stroke_width=2))

    # Stats Data (Hardcoded based on recent data)
    stats = [
        {"name": "Total Commits", "value": "369+", "max": 1000, "color": COLORS['green']},
        {"name": "PRs Reviewed", "value": "0", "max": 10, "color": COLORS['green']},
        {"name": "Issues Opened", "value": "1", "max": 10, "color": COLORS['green']},
    ]

    # Languages Data (Based on screenshot)
    langs = [
        {"name": "JavaScript", "percent": 43.25, "color": "#f1e05a"},
        {"name": "PHP", "percent": 18.19, "color": "#4F5D95"},
        {"name": "CSS", "percent": 14.73, "color": "#563d7c"},
        {"name": "Python", "percent": 9.11, "color": "#3572A5"},
        {"name": "HTML", "percent": 8.59, "color": "#e34c26"},
    ]

    # --- Section 1: Core Metrics ---
    y = 80
    x_col1 = 20
    
    dwg.add(dwg.text(">> CORE_METRICS", insert=(x_col1, y), class_="label", style=f"fill:{COLORS['cyan']}"))
    y += 20

    for stat in stats:
        # Label
        dwg.add(dwg.text(f"{stat['name']}:", insert=(x_col1, y), class_="text"))
        # Value
        dwg.add(dwg.text(stat['value'], insert=(x_col1 + 130, y), class_="value", style=f"fill:{stat['color']}"))
        y += 20
    
    # --- Section 2: Language Proficiency ---
    y = 80
    x_col2 = 250
    dwg.add(dwg.text(">> NEURAL_LANGUAGES", insert=(x_col2, y), class_="label", style=f"fill:{COLORS['cyan']}"))
    y += 25

    bar_width = 200
    bar_height = 10

    for lang in langs:
        # Label and Percent
        dwg.add(dwg.text(lang['name'], insert=(x_col2, y-5), class_="label"))
        dwg.add(dwg.text(f"{lang['percent']}%", insert=(x_col2 + bar_width, y-5), class_="label", text_anchor="end"))
        
        # Bar Background
        dwg.add(dwg.rect(insert=(x_col2, y), size=(bar_width, bar_height), rx=3, ry=3, class_="bar-bg"))
        
        # Bar Fill
        fill_width = (lang['percent'] / 100) * bar_width
        dwg.add(dwg.rect(insert=(x_col2, y), size=(fill_width, bar_height), rx=3, ry=3, fill=lang['color']))
        
        y += 35

    # Footer / Decor
    dwg.add(dwg.text("STATUS: ONLINE", insert=(20, height-15), class_="label", style=f"fill:{COLORS['green']}; font-size:10px;"))
    dwg.add(dwg.text("SYNC: MANUAL", insert=(width-20, height-15), class_="label", text_anchor="end", style="font-size:10px;"))

    dwg.save()

if __name__ == '__main__':
    generate_stats_card()
