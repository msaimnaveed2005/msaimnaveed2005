from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

RAMP = " .`:-=+*cs#%@"
COLS = 90
ROW_RATIO = 0.48
CURVE = 1.7
# Tight portrait crop around the hair, face, neck, and upper shoulders.
FACE_CROP = (100, 160, 840, 1240)


def prepare(path):
    source = Image.open(path).convert("RGBA")
    source = source.crop(FACE_CROP)
    cutout = remove(source)
    alpha = np.array(cutout.getchannel("A"))

    white = Image.new("RGBA", cutout.size, (255, 255, 255, 255))
    gray = np.array(Image.alpha_composite(white, cutout).convert("L"))
    gray = cv2.bilateralFilter(gray, 11, 50, 50)
    gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
    gray = (255.0 * (gray / 255.0) ** CURVE).astype("uint8")
    gray[alpha < 20] = 255
    return Image.fromarray(gray)


def to_ascii(image):
    width, height = image.size
    rows = max(1, int(COLS * (height / width) * ROW_RATIO))
    image = image.resize((COLS, rows), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    result = []
    for row in range(rows):
        result.append("".join(
            RAMP[min(len(RAMP) - 1,
                     int((1 - pixels[row * COLS + col] / 255.0) * len(RAMP)))]
            for col in range(COLS)
        ).rstrip())
    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    return result


output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
lines = to_ascii(prepare("profile.png"))
(output_dir / "ascii.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"ASCII generated at {output_dir / 'ascii.txt'}: {len(lines)} rows")
