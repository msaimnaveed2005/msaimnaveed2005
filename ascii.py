from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ASCII_CHARS = "@%#*+=-:.` "
ASCII_WIDTH = 90


def crop_to_subject(img):
    width, height = img.size
    margin = int(width * 0.08)
    return img.crop((margin, 0, width - margin, height))


def remove_flat_background(img):
    pixels = img.load()
    background = (158, 158, 158)
    for y in range(img.height):
        for x in range(img.width):
            red, green, blue = pixels[x, y]
            distance = max(
                abs(red - background[0]),
                abs(green - background[1]),
                abs(blue - background[2]),
            )
            if distance <= 10:
                pixels[x, y] = (255, 255, 255)
    return img


def resize(img, width=ASCII_WIDTH):
    w, h = img.size
    ratio = h / w
    height = max(1, int(width * ratio * 0.55))
    return img.resize((width, height), Image.Resampling.LANCZOS)


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
image = crop_to_subject(image)
image = remove_flat_background(image)
image = grayscale(resize(image))
image = ImageOps.autocontrast(image, cutoff=2)
image = ImageEnhance.Contrast(image).enhance(1.35)
image = image.point(lambda value: int(255 * (value / 255) ** 1.35))

ascii_str = pixels_to_ascii(image)
width = image.width
ascii_img = "\n".join(
    ascii_str[i:i + width].rstrip()
    for i in range(0, len(ascii_str), width)
)

with open(output_dir / "ascii.txt", "w", encoding="utf-8") as f:
    f.write(ascii_img)

print(f"ASCII generated at {output_dir / 'ascii.txt'}")