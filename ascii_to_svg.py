with open("output/ascii.txt") as f:
    lines = f.readlines()

svg = """
<svg xmlns="http://www.w3.org/2000/svg"
width="1000"
height="800">

<style>
text{
font-family:monospace;
font-size:10px;
fill:white;
}
</style>

<rect width="100%" height="100%" fill="black"/>

"""

y = 20

for line in lines:
    svg += f'<text x="10" y="{y}">{line}</text>'
    y += 10

svg += "</svg>"

with open("output/ascii.svg","w") as f:
    f.write(svg)

print("SVG created")