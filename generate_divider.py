import svgwrite
import math

def generate_divider():
    # Solana/Netrunner Palette
    COLORS = {
        "bg": "#0D1117",
        "purple": "#9945FF",
        "green": "#14F195",
        "cyan": "#00F0FF"
    }

    width = 800
    height = 50
    dwg = svgwrite.Drawing('divider.svg', size=(width, height))

    # Background (Transparent usually better for dividers, but we'll use dark matching fill or none)
    # dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill=COLORS['bg']))

    # Wave Generation
    # We'll generate a "digital" looking wave
    points = []
    steps = 100
    for i in range(steps + 1):
        x = (width / steps) * i
        # Combine sine waves for a "beat" pattern
        y = height/2 + (math.sin(i * 0.2) * 15 * math.sin(i * 0.05))
        points.append((x, y))

    # Gradient Definition
    grad = dwg.defs.add(dwg.linearGradient(id="waveGrad", x1="0%", y1="0%", x2="100%", y2="0%"))
    grad.add_stop_color(0, COLORS['green'])
    grad.add_stop_color(0.5, COLORS['purple'])
    grad.add_stop_color(1, COLORS['cyan'])

    # Draw the Path
    path_data = "M " + " L ".join([f"{p[0]},{p[1]}" for p in points])
    dwg.add(dwg.path(d=path_data, stroke="url(#waveGrad)", stroke_width=3, fill="none"))
    
    # Add some "digital particles"
    for i in range(0, steps, 10):
        if i % 20 == 0:
            x = (width / steps) * i
            y = height/2 + (math.sin(i * 0.2) * 15 * math.sin(i * 0.05))
            dwg.add(dwg.circle(center=(x, y), r=2, fill=COLORS['cyan']))

    dwg.save()

if __name__ == '__main__':
    generate_divider()
