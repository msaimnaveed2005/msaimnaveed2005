from pathlib import Path


output_dir = Path("output")
text_path = output_dir / "ascii.txt"
svg_path = output_dir / "ascii.svg"

with text_path.open("r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

line_height = 11
padding = 18
height = max(1, len(lines) * line_height + padding * 2)
width = 900

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    text {{
      font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
      fill: #f5f5f5;
      letter-spacing: 0.25px;
    }}
  </style>
  <rect width="100%" height="100%" fill="#0b0d12"/>
'''

for i, line in enumerate(lines):
    svg += f'  <text x="18" y="{padding + 4 + i * line_height}">{line}</text>\n'

svg += "</svg>\n"

with svg_path.open("w", encoding="utf-8") as f:
    f.write(svg)

print(f"SVG created at {svg_path}")