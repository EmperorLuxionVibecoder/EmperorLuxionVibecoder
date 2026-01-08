import svgwrite
import math

def create_hex_node():
    """Option 1: The Neural Hex - Abstract geometric node"""
    name = "avatar_hex_node.svg"
    dwg = svgwrite.Drawing(name, size=('400px', '400px'))
    
    # Palette
    bg = "#0D1117"
    green = "#14F195"
    purple = "#9945FF"
    cyan = "#00F0FF"
    
    # Background Circle
    dwg.add(dwg.circle(center=(200, 200), r=200, fill=bg))
    
    # Outer Ring
    dwg.add(dwg.circle(center=(200, 200), r=190, fill="none", stroke=purple, stroke_width=8, stroke_dasharray="40,20"))
    
    # Inner Hexagon logic
    def hexagon(cx, cy, r, **kwargs):
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            x = cx + r * math.cos(angle_rad)
            y = cy + r * math.sin(angle_rad)
            points.append((x, y))
        return dwg.polygon(points, **kwargs)

    # Glowing Hexagons
    dwg.add(hexagon(200, 200, 100, fill="none", stroke=green, stroke_width=6, opacity=0.8))
    dwg.add(hexagon(200, 200, 80, fill="none", stroke=cyan, stroke_width=4, opacity=0.6))
    dwg.add(hexagon(200, 200, 40, fill=green, opacity=0.9))
    
    # Connecting Lines (Circuitry)
    lines = dwg.add(dwg.g(stroke=purple, stroke_width=3, opacity=0.6))
    for i in range(6):
        angle = 60 * i - 30
        rad = math.radians(angle)
        x1 = 200 + 100 * math.cos(rad)
        y1 = 200 + 100 * math.sin(rad)
        x2 = 200 + 190 * math.cos(rad)
        y2 = 200 + 190 * math.sin(rad)
        lines.add(dwg.line((x1, y1), (x2, y2)))

    dwg.save()
    print(f"Generated {name}")

def create_glitch_monogram():
    """Option 2: The Vibecoder Glitch - Monogram EV"""
    name = "avatar_glitch_mono.svg"
    dwg = svgwrite.Drawing(name, size=('400px', '400px'))
    
    bg = "#0D1117"
    green = "#14F195"
    purple = "#9945FF"
    
    dwg.defs.add(dwg.style("""
        @import url('https://fonts.googleapis.com/css2?family=Rubik+Glitch&display=swap');
        .text { font-family: 'Rubik Glitch', monospace; font-size: 200px; font-weight: bold; anchor: middle; }
    """))
    
    # Background
    dwg.add(dwg.rect(insert=(0,0), size=('100%', '100%'), fill=bg))
    
    # Glitch Layers
    # Red Offset
    dwg.add(dwg.text("EV", insert=(55, 270), fill="#FF003C", opacity=0.7, class_="text"))
    # Cyan Offset
    dwg.add(dwg.text("EV", insert=(45, 270), fill="#00F0FF", opacity=0.7, class_="text"))
    # Main Text
    dwg.add(dwg.text("EV", insert=(50, 270), fill="white", class_="text"))
    
    # Scanlines
    scan = dwg.add(dwg.g(stroke="black", stroke_width=2, opacity=0.3))
    for y in range(0, 400, 8):
        scan.add(dwg.line((0, y), (400, y)))
        
    # Border
    dwg.add(dwg.rect(insert=(10,10), size=(380, 380), fill="none", stroke=green, stroke_width=10))

    dwg.save()
    print(f"Generated {name}")

def create_cyber_eye():
    """Option 3: The Netrunner Eye"""
    name = "avatar_cyber_eye.svg"
    dwg = svgwrite.Drawing(name, size=('400px', '400px'))
    
    bg = "#000000"
    green = "#14F195"
    purple = "#9945FF"
    
    dwg.add(dwg.circle(center=(200, 200), r=200, fill=bg))
    
    # Iris
    dwg.add(dwg.circle(center=(200, 200), r=90, fill="none", stroke=purple, stroke_width=15))
    dwg.add(dwg.circle(center=(200, 200), r=70, fill=green))
    
    # Pupil
    dwg.add(dwg.circle(center=(200, 200), r=30, fill="#000"))
    # Glint
    dwg.add(dwg.circle(center=(180, 180), r=10, fill="white", opacity=0.9))
    
    # Crosshairs / HUD
    hud = dwg.add(dwg.g(stroke=green, stroke_width=2))
    hud.add(dwg.line((50, 200), (100, 200)))
    hud.add(dwg.line((300, 200), (350, 200)))
    hud.add(dwg.line((200, 50), (200, 100)))
    hud.add(dwg.line((200, 300), (200, 350)))
    
    # Data rings
    dwg.add(dwg.circle(center=(200, 200), r=140, fill="none", stroke=purple, stroke_width=2, stroke_dasharray="10,10"))

    dwg.save()
    print(f"Generated {name}")

if __name__ == "__main__":
    create_hex_node()
    create_glitch_monogram()
    create_cyber_eye()
