import sys
price = sys.argv[1]

from PIL import Image, ImageFont, ImageDraw, ImageOps


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception as e:
        print(e)




img = read_image("input.jpg")
logo = read_image("logo.png")


img = ImageOps.expand(img, 100, 'white')

width, height = img.size
x_offset, y_offset = ImageDraw.Draw(img).textsize(price, ImageFont.truetype("sans-serif.ttf", 60))
ImageDraw.Draw(img).text((width - 320, height - 100), price, (205, 92, 92), ImageFont.truetype("sans-serif.ttf", 60))

img2 = img
ImageDraw.Draw(img2).text((width - 320 + (x_offset+10), height - 70), "AMD", (205, 92, 92), ImageFont.truetype("sans-serif.ttf", 30))

img.paste(logo, (25, 25), logo)


img.save('result.png')

# img_arr = np.array(img)
# result = Image.fromarray(img_arr)
