import sys
price = "stack allocated dummy string because Python can't properly allocate at runtime"
passed_price = sys.argv[1]
price = passed_price
print(" " + price)

from PIL import Image, ImageFont, ImageDraw, ImageOps


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
back_color = pixels[width-1,0]

print("PASS")

img.paste(im=foreground, box=(0,0), mask=foreground)

brand_x, brand_y = brand.size
white_back_x = 298
white_back_y = 48
size = white_back_x, white_back_y
brand.thumbnail(size, Image.ANTIALIAS)
brand_padding_x = int((white_back_x - brand_x)/2)
img.paste(im=brand, box=(brand_padding_x, height - white_back_y - 2), mask=brand)

price_offset_x, price_offset_y = ImageDraw.Draw(img).textsize(price, price_font)
AMD_offset_x, AMD_offset_y = ImageDraw.Draw(img).textsize("AMD", AMD_font)
price_padding_x = price_offset_x + AMD_offset_x + 3 + 25
ImageDraw.Draw(img).text((width - price_padding_x, height - 50), price, (255, 255, 255), price_font)
ImageDraw.Draw(img).text((width - price_padding_x + price_offset_x + 3, height - 32), "AMD", (255, 255, 255), AMD_font)

img.save('result.png')
