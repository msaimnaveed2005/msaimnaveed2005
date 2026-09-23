from pathlib import Path
from xml.sax.saxutils import escape


output_dir = Path("output")
text_path = output_dir / "ascii.txt"
svg_path = output_dir / "ascii.svg"

with text_path.open("r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

line_height = 15
padding = 14
char_width = 7.74
font_size = 12.9
width = 620
height = max(1, len(lines) * line_height + padding * 2)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .portrait {{
      font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
      font-size: {font_size}px;
      fill: #6e7681;
      letter-spacing: 0;
    }}
    .cursor {{
      fill: #6e7681;
    }}
    @media (prefers-color-scheme: dark) {{
      .portrait, .cursor {{
        fill: #c9d1d9;
      }}
    }}
  </style>
'''

for i, line in enumerate(lines):
    y = padding + 4 + i * line_height
    safe_line = escape(line)
    reveal_width = max(char_width, len(line) * char_width)
    x = max(padding, (width - reveal_width) / 2)
    begin = i * 0.09
    end = begin + 0.09
    clip_id = f"row{i}"
    svg += f'''  <clipPath id="{clip_id}">
    <rect x="{x:.1f}" y="{y - line_height + 1}" width="0" height="{line_height}">
      <animate attributeName="width" from="0" to="{reveal_width:.1f}" begin="{begin:.2f}s" dur="0.09s" fill="freeze"/>
    </rect>
  </clipPath>
  <g clip-path="url(#{clip_id})">
    <text x="{x:.1f}" y="{y}" xml:space="preserve" class="portrait">{safe_line}</text>
  </g>
  <rect x="{x:.1f}" y="{y - line_height + 1}" width="4" height="{line_height - 1}" class="cursor" opacity="0">
    <animate attributeName="x" from="{x:.1f}" to="{x + reveal_width:.1f}" begin="{begin:.2f}s" dur="0.09s" fill="freeze"/>
    <set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>
    <set attributeName="opacity" to="0" begin="{end:.2f}s"/>
  </rect>
'''

svg += "</svg>\n"

with svg_path.open("w", encoding="utf-8") as f:
    f.write(svg)

print(f"SVG created at {svg_path}")