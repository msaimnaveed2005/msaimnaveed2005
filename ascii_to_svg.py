import base64
from pathlib import Path
from xml.sax.saxutils import escape

output_dir = Path("output")
font_path = Path("scripts/fonts/jbmono-ramp.woff2")
lines = (output_dir / "ascii.txt").read_text(encoding="utf-8").splitlines()

FONT_SIZE = 12.9
CHAR_W = 7.74
LINE_H = 15
PAD = 14
WIDTH = int(90 * CHAR_W + PAD * 2)
HEIGHT = len(lines) * LINE_H + PAD * 2
font_b64 = base64.b64encode(font_path.read_bytes()).decode("ascii")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="JBMono,ui-monospace,monospace">
<style>@font-face{{font-family:JBMono;font-style:normal;font-weight:400;font-display:block;src:url(data:font/woff2;base64,{font_b64}) format("woff2")}}.a{{fill:#6e7681}}@media(prefers-color-scheme:dark){{.a{{fill:#c9d1d9}}}}</style>'''

for index, line in enumerate(lines):
    y = PAD + index * LINE_H
    safe = escape(line)
    line_width = max(CHAR_W, len(line) * CHAR_W)
    begin = index * 0.09
    end = (index + 1) * 0.09
    clip_id = f"row{index}"
    svg += f'''<clipPath id="{clip_id}"><rect x="{PAD}" y="{y}" width="0" height="{LINE_H}"><animate attributeName="width" from="0" to="{line_width:.1f}" begin="{begin:.2f}s" dur="0.09s" fill="freeze"/></rect></clipPath><g clip-path="url(#{clip_id})"><text xml:space="preserve" x="{PAD}" y="{y + 11.2:.1f}" class="a" font-size="{FONT_SIZE}">{safe}</text></g><rect y="{y + 1}" width="6" height="12" class="a" opacity="0"><animate attributeName="x" from="{PAD}" to="{PAD + line_width:.1f}" begin="{begin:.2f}s" dur="0.09s" fill="freeze"/><set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/><set attributeName="opacity" to="0" begin="{end:.2f}s"/></rect>'''

svg += "</svg>\n"
(output_dir / "ascii.svg").write_text(svg, encoding="utf-8")
print(f"SVG created at {output_dir / 'ascii.svg'}")
