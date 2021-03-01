from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError
import re
import os
from image_gen import gen_image
from async_get import async_get
from async_get import download_image

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import glob


def assert_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)


def file_exists(filename):
    return os.path.exists(filename)


def load_page(url, attempt=1):
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    if not is_ascii(url):
        for x in url:
            if not is_ascii(x):
                url = url.replace(x, quote(x))

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        web_byte = urlopen(req).read()
    except HTTPError as err:
        if err.code == 503:
            return load_page(url, attempt + 1) if attempt < 5 else soup("", "html.parser")
        return soup("", "html.parser")

    webpage = web_byte.decode('utf-8')
    page = soup(webpage, "html.parser")
    return page


def load_to_cache(link, name):
    assert_folder(".cache")
    if not file_exists(f".cache/{name}"):
        download_image(link, f".cache/{name}")


def download_tags(tag_links):
    del_len = len("topsale.am/img/")
    tags = []
    for link in tag_links:
        tag_name = re.search(r"topsale\.am/img/.*", link).group()[del_len:]

        load_to_cache(link, tag_name)

        tags.append(tag_name)
    return tags


def svg_to_png(name):
    drawing = svg2rlg(name)
    renderPM.drawToFile(drawing, f"{name[:-4]}.png", fmt="PNG")


def rm_rf(name):
    for f in glob.glob(f"{name}/*"):
        if os.path.isdir(f):
            rm_rf(f)
            os.rmdir(f)
        else:
            os.remove(f)


def do_prod(job):
    link, html, save_path, todo = job['url'], job['data'], job['save_path'], job['todo']
    print(link)
    page_soup = soup(html, "html.parser")
    prod_html = page_soup.find("div", {"class": "details-block"})
    if not prod_html:
        return

    # Image Link
    prod_html = prod_html.div.div.div
    image_html = prod_html.find("div", {"class": "carousel-inner"})
    img_link = image_html.find("div", {"class": ["item", "active"]}).a.img["src"]

    # Price
    price = prod_html.find("span", {"class": "regular"}).decode_contents()
    price = re.search(r"[0-9,]+", price).group()

    # Brand
    brand_link = prod_html.find("div", {"class": "product-brnd-logo"}).img["src"]
    del_len = len("topsale.am/img/brands/")
    brand = re.search(r"topsale\.am/img/brands/.*", brand_link).group()[del_len:]
    load_to_cache(brand_link, brand)
    if brand[-4:] == ".svg":
        if not file_exists(f".cache/{brand[:-4]}.png"):
            svg_to_png(f".cache/{brand}")
        brand = f"{brand[:-4]}.png"

    # off_tags
    tag_links = []
    labels = prod_html.find_all("span", {"class": "customlabel"})
    if labels:
        for label in labels:
            tag_links.append(label.img["src"])
    off_tags = download_tags(tag_links)

    # Get image file name
    del_len = len("topsale.am/img/prodpic/")
    img_name = re.search(r"topsale\.am/img/prodpic/.*", img_link).group()[del_len:]

    todo.append({
        "url": img_link,
        "img_name": img_name,
        "save_path": save_path,
        "price": price,
        "brand": brand,
        "off_tags": off_tags.copy()
    })


def print_json(_json, intend="", comma=False, left_bracket=True):
    if isinstance(_json, list):
        if left_bracket:
            print(intend + "[")

        for i in range(len(_json)):
            print_json(_json[i], intend + "\t", comma=(i < len(_json) - 1))
        print(intend + "]")
        return

    def colored(color, text):
        return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(color[0], color[1], color[2], text)

    green = [0, 255, 0]
    cyan = [0, 255, 255]
    if left_bracket:
        print(intend + "{")
    i = 0
    for key in _json:
        val = _json[key]
        if isinstance(_json[key], dict):
            print(f"{intend}\t{colored(green, key)}: {'{'}")
            print_json(_json[key], intend + "\t", left_bracket=False, comma=(i < len(_json) - 1))
        elif isinstance(_json[key], list):
            print(f"{intend}\t{colored(green, key)}: {'['}")
            print_json(_json[key], intend + "\t", left_bracket=False, comma=(i < len(_json) - 1))
        else:
            if isinstance(_json[key], str):
                val = f"\"{val}\"".replace("\n", "\\n")
            val_comma = "," if i < len(_json) - 1 else ""
            print(f"{intend}\t{colored(green, key)}: {colored(cyan, val)}{val_comma}")
        i += 1
    print(intend + "}" + ("," if comma else ""))


def do_links(links, save_path):
    jobs = []
    todo = []
    for link in links:
        jobs.append({
            'url': link,
            'save_path': save_path,
            'todo': todo
        })
    async_get(jobs, do_prod)

    def download_and_edit(job):
        print(job["url"])
        img_name = job["img_name"]
        _save_path = job["save_path"]
        price = job["price"]
        brand = job["brand"]
        off_tags = job["off_tags"]

        gen_image(f"input/{img_name}", f"{_save_path}/{img_name}", price, brand, off_tags)

    async_get(todo, download_and_edit)


def get_all_cats():
    home = load_page("https://topsale.am/")

    categories = home.find("div", {"class": "categorylist"}).ul
    categories = categories.find_all("li", {"class": ["swiper-slide", "item menu-element"]})[:-1]

    all_cats = {}

    # TODO: Delete me
    categories = categories[:1]

    for cat in categories:
        main_cat_name = cat.a.decode_contents().strip()
        all_cats[main_cat_name] = []
        sub_cats = cat.div.ul.find_all("li", {})

        # TODO: Delete me
        sub_cats = sub_cats[:1]
        for sub_cat in sub_cats:
            all_cats[main_cat_name].append({
                "sub_category": sub_cat.a.decode_contents().strip(),
                "link": sub_cat.a["href"]
            })

    return all_cats


def do_sub_category(category, sub_cat):
    sub_cat_name, link = sub_cat["sub_category"], sub_cat["link"]

    page = load_page(link)
    page = page.find("div", {"class": "row"})
    list_items = page.find_all("div", {"class": "listitem"})

    prod_links = []
    for list_item in list_items:
        prod_link = list_item.find("a", {"class": "prod-item-img"})['href']
        prod_link = re.sub(r"[\n\r]", "", prod_link)
        prod_links.append(prod_link)

    do_links(prod_links, f"results/{category}/{sub_cat['sub_category']}")


def start():
    assert_folder("results")
    rm_rf("results")
    rm_rf("input")

    all_cats = get_all_cats()
    for cat in all_cats:
        os.makedirs(f"results/{cat}")
        for sub_cat in all_cats[cat]:
            os.makedirs(f"results/{cat}/{sub_cat['sub_category']}")
            do_sub_category(cat, sub_cat)

    rm_rf("input")


if __name__ == '__main__':
    start()
