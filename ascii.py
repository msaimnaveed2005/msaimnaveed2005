from PIL import Image

ASCII_CHARS = "@%#*+=-:. "

def resize(img, width=100):
    w, h = img.size
    ratio = h / w
    height = int(width * ratio * 0.55)
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

image = Image.open("profile.png").convert("RGB")

image = resize(image)
image = grayscale(image)

ascii_str = pixels_to_ascii(image)

width = image.width

ascii_img = "\n".join(
    ascii_str[i:i+width]
    for i in range(0, len(ascii_str), width)
)

with open("output/ascii.txt", "w") as f:
    f.write(ascii_img)

print("ASCII generated.")