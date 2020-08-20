import sys
from PIL import Image, ImageFont, ImageDraw, ImageOps

if len(sys.argv) != 3:
    print("[ERROR] passed argument error, correct usage:\n python3 image_gen.py <price> <off_tag>")
    exit(1)
# price = "stack allocated dummy string because Python can't properly allocate at runtime"
passed_price = sys.argv[1]
price = passed_price
off_tag = sys.argv[2]
print(" " + price, "[" + off_tag + "]")


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception as e:
        print("[ERROR] error opening " + path)


price_font = ImageFont.truetype("assets/montserrat-bold.ttf", 36)
AMD_font = ImageFont.truetype("assets/montserrat-bold.ttf", 18)

img = read_image("input.jpg")
foreground = read_image("assets/foreground.png")
brand = read_image("brand.png").convert("RGBA")
width, height = img.size
pixels = img.load()
back_color = pixels[width - 1, 0]

print("PASS")

img.paste(im=foreground, box=(0, 0), mask=foreground)

brand_x, brand_y = brand.size
white_back_x = 298
white_back_y = 48
size = white_back_x, white_back_y
brand.thumbnail(size, Image.ANTIALIAS)
brand_padding_x = int((white_back_x - brand_x) / 2)
img.paste(im=brand, box=(brand_padding_x, height - white_back_y - 2), mask=brand)

price_offset_x, price_offset_y = ImageDraw.Draw(img).textsize(price, price_font)
AMD_offset_x, AMD_offset_y = ImageDraw.Draw(img).textsize("AMD", AMD_font)
price_padding_x = price_offset_x + AMD_offset_x + 3 + 25
ImageDraw.Draw(img).text((width - price_padding_x, height - 50), price, (255, 255, 255), price_font)
ImageDraw.Draw(img).text((width - price_padding_x + price_offset_x + 3, height - 32), "AMD", (255, 255, 255), AMD_font)

if off_tag == "20_off":
    off_20 = read_image("assets/20_off.png").convert("RGBA")
    off_20_size_x, off_20_size_y = off_20.size
    img.paste(im=off_20, box=(width-1 - off_20_size_x, 0), mask=off_20)
elif off_tag == "20_off":
    off_50 = read_image("assets/50_20.png").convert("RGBA")
    off_50_size_x, off_50_size_y = off_50.size
    img.paste(im=off_50, box=(width - 1 - off_50_size_x, 0), mask=off_50)

img.save('result.jpg')
