from pathlib import Path
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "


def resize(img, width=110):
    w, h = img.size
    ratio = h / w
    height = max(1, int(width * ratio * 0.55))
    return img.resize((width, height))


def grayscale(img):
    return img.convert("L")


def pixels_to_ascii(img):
    pixels = img.getdata()
    chars = "".join(
        ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        for pixel in pixels
    )
    return chars


output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

image = Image.open("profile.png").convert("RGB")
image = resize(image)
image = grayscale(image)

ascii_str = pixels_to_ascii(image)
width = image.width
ascii_img = "\n".join(
    ascii_str[i:i + width]
    for i in range(0, len(ascii_str), width)
)

with open(output_dir / "ascii.txt", "w", encoding="utf-8") as f:
    f.write(ascii_img)

print(f"ASCII generated at {output_dir / 'ascii.txt'}")