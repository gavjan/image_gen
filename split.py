import sys
price = "stack allocated dummy string because Python can't allocate at runtime"
passed_price = sys.argv[1]
price = passed_price
print(" " + price)

from PIL import Image, ImageFont, ImageDraw, ImageOps
import math

def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception as e:
        print("[ERROR] error opening " + path)

def color_distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2

    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

price_font = ImageFont.truetype("assets/sans-serif.ttf", 50)
AMD_font = ImageFont.truetype("assets/sans-serif.ttf", 25)

# --------
img = read_image("input.jpg")
logo = read_image("assets/logo.png")
brand = read_image("brand.png").convert("RGBA")
original_img_x, original_img_y = img.size
pixels = img.load()

back_color = pixels[original_img_x-1,0]
left_border = -1
right_border = original_img_x-1
possible_border_left = True
possible_border_right = True
for x in range(original_img_x):
    possible_border = True
    for y in range(original_img_y):
        if color_distance(pixels[x, y], back_color) > 25.0:
            possible_border = False
    if possible_border_left:
        if possible_border:
            left_border+=1
        else:
            possible_border_left = False
    elif possible_border_right:
        if possible_border:
            right_border = x
            possible_border_right = False

# # Border Debug
# for y in range(original_img_y):
#     pixels[left_border, y] = (255, 0, 0)
# for y in range(original_img_y):
#     pixels[right_border, y] = (255, 0, 0)
# img.save('debug.png')

img_padding = int((original_img_x/2 - (right_border - left_border))/2)
right_border+=img_padding
left_border-=img_padding
# Move image to left
new_width = right_border - left_border
for y in range(original_img_y):
    for x in range(new_width):
        pixels[x, y] = pixels[left_border+x,y]

# Fill Right Red Color
for y in range(original_img_y):
    for x in range(original_img_x - new_width):
        pixels[x+new_width,y] = (255, 77, 92)



# Brand
brand_padding_y = 20
brand_padding_x = 10
brand_size_x, brand_size_y = brand.size

brand_back_x = brand_size_x + brand_padding_x + 20
brand_back_y = brand_size_y + brand_padding_y
for y in range(brand_back_y):
    for x in range(brand_back_x):
        pixels[original_img_x-1 - x,brand_padding_y + y] = back_color

img.paste(im=brand, box=(original_img_x-1 - brand_size_x - brand_padding_x, brand_padding_y+5), mask=brand)

# Price Text

price_padding_y = brand_size_y + brand_padding_y + 70

x_offset, y_offset = ImageDraw.Draw(img).textsize(price, price_font)
amd_offset_x, amd_offset_y = ImageDraw.Draw(img).textsize("AMD", AMD_font)
text_x = new_width + (original_img_x - new_width - x_offset - amd_offset_x - 5)/2
text_y = price_padding_y + 10

for y in range(y_offset + 20):
    for x in range(original_img_x - new_width):
        pixels[new_width + x,price_padding_y + y] = (0,0,0)

ImageDraw.Draw(img).text((text_x, text_y), price, (241, 233, 229), price_font)
ImageDraw.Draw(img).text((text_x + (x_offset+5), text_y+20), "AMD", (241, 233, 229), AMD_font)


# Logo
logo_size_x,logo_size_y = logo.size
logo_back_y = logo_size_y + 20
logo_back_x = logo_size_x + 30
logo_offset_y = 20
logo_offset_x = 20
for y in range(logo_back_y):
    for x in range(logo_back_x + 10):
        pixels[original_img_x-1 - x,original_img_y - y - logo_offset_y] = back_color
logo_x = original_img_x - logo_size_x - logo_offset_x
logo_y = original_img_y - logo_size_y - logo_offset_y
img.paste(im=logo, box=(logo_x, logo_y-10), mask=logo)

img.save('last.png')
img.save('result.png')
print("PASS")
