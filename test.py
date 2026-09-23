from PIL import Image

img = Image.open("profile.png")

print(img.size)
print(img.mode)