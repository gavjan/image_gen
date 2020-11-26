import sys
from PIL import Image, ImageFont, ImageDraw, ImageOps

if len(sys.argv) != 3:
    print("[ERROR] passed argument error, correct usage:\n python3 image_gen.py <price> <off_tags>")
    exit(1)

passed_price = sys.argv[1]
price = passed_price
off_tags = sys.argv[2]


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except FileNotFoundError:
        print("[ERROR] file:", path, "not found")


price_font = ImageFont.truetype("assets/montserrat-bold.ttf", 36)
AMD_font = ImageFont.truetype("assets/montserrat-bold.ttf", 18)

img = read_image("input.jpg")
foreground = read_image("assets/foreground.png")
brand = read_image("brand.png").convert("RGBA")
width, height = img.size
pixels = img.load()
back_color = pixels[width - 1, 0]

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


tag_map = {
    "20_off": "assets/20_off.png",
    "50_20": "assets/50_20.png",
    "50_off": "assets/50_off.png",
    "school": "assets/school.png",
    "b_friday": "assets/b_friday.png"
}
sticker_name = ""
print(off_tags)
if off_tags in tag_map:
    sticker_name = tag_map[off_tags]
    if off_tags == "b_friday":
        print("BOZZZZZZ")
    
    sticker = read_image(sticker_name).convert("RGBA")
    sticker_size_x, sticker_size_y = sticker.size
    img.paste(im=sticker, box=(width - 1 - sticker_size_x - 2, 2), mask=sticker)


img.save('result.jpg')
