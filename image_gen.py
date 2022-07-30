from PIL import Image, ImageFont, ImageDraw
import re


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except FileNotFoundError:
        print("[ERROR] file:", path, "not found")


def gen_image(input_img, output_img, price, brand, off_tags):
    price_font = ImageFont.truetype("assets/montserrat-bold.ttf", 36)
    AMD_font = ImageFont.truetype("assets/montserrat-bold.ttf", 18)

    img = read_image(input_img)
    foreground = read_image("assets/foreground.png")

    brand_exists = brand != ""
    brand = f".cache/{brand}"
    if brand_exists:
        brand = read_image(brand).convert("RGBA")
    width, height = img.size

    img.paste(im=foreground, box=(0, 0), mask=foreground)

    brand_x, brand_y = brand.size if brand_exists else (0, 0)
    white_back_x = 298
    white_back_y = 48
    size = white_back_x, white_back_y
    if brand_exists:
        brand.thumbnail(size, Image.ANTIALIAS)
    brand_padding_x = int((white_back_x - brand_x) / 2)
    if brand_exists:
        img.paste(im=brand, box=(brand_padding_x, height - white_back_y - 2), mask=brand)

    price_offset_x, price_offset_y = ImageDraw.Draw(img).textsize(price, price_font)
    AMD_offset_x, AMD_offset_y = ImageDraw.Draw(img).textsize("AMD", AMD_font)
    price_padding_x = price_offset_x + AMD_offset_x + 3 + 25
    ImageDraw.Draw(img).text((width - price_padding_x, height - 50), price, (255, 255, 255), price_font)
    ImageDraw.Draw(img).text((width - price_padding_x + price_offset_x + 3, height - 32), "AMD", (255, 255, 255),
                             AMD_font)

    for tag in off_tags:
        tag = f".cache/{tag}"
        sticker = read_image(tag).convert("RGBA")
        sticker = sticker.resize((100, 100))

        sticker_size_x, sticker_size_y = sticker.size
        img.paste(im=sticker, box=(width - 1 - sticker_size_x - 2, 2), mask=sticker)

    img.save(re.sub(r"(\.jpeg|\.png|\.webp|\.jfif)$", ".jpg", output_img))
