import sys
price = "stack allocated dummy string because Python can't allocate at runtime"
passed_price = sys.argv[1]
price = passed_price
print("got price: " + price)

from PIL import Image, ImageFont, ImageDraw, ImageOps


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception as e:
        print("[ERROR] error opening " + path)


price_font = ImageFont.truetype("assets/sans-serif.ttf", 60)
AMD_font = ImageFont.truetype("assets/sans-serif.ttf", 30)

img = read_image("input.jpg")
logo = read_image("assets/logo.png")
brand = read_image("brand.png").convert("RGBA")

img_new = ImageOps.expand(image=img, border=100, fill='white')
img = img_new

width, height = img.size
print("PASS")
x_offset, y_offset = ImageDraw.Draw(img).textsize(price, price_font)

ImageDraw.Draw(img).text((width - 320, height - 100), price, (205, 92, 92), price_font)

ImageDraw.Draw(img).text((width - 320 + (x_offset+10), height - 70), "AMD", (205, 92, 92), AMD_font)

img.paste(im=logo, box=(25, 25), mask=logo)
brand_x, brand_y = brand.size
img.paste(im=brand, box=(width - 25 - brand_x, 25), mask=brand)



img.save('result.png')
