from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError
import re
import os
from image_gen import gen_image
from cairosvg import svg2png
from async_get import async_get


def assert_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)


def file_exists(filename):
    return os.path.exists(filename)


def download_image(url, file_name, attempt=1):
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    if not is_ascii(url):
        for x in url:
            if not is_ascii(x):
                url = url.replace(x, quote(x))

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        web_byte = urlopen(req).read()
        f = open(file_name, "wb")
        f.write(web_byte)
        f.close()
        return True
    except HTTPError as err:
        if err.code == 503 and attempt < 5:
            return download_image(url, file_name, attempt + 1)
        else:
            return False


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
    f = open(name, "r")
    svg2png(bytestring=f.read(), write_to=f"{name[:-4]}.png")
    f.close()


def do_prod(job):
    link, html, save_path = job['url'], job['data'], job['save_path']
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
    download_image(img_link, f"input/{img_name}")

    gen_image(f"input/{img_name}", f"{save_path}/{img_name}", price, brand, off_tags)


def do_individual(links):
    jobs = []
    assert_folder("results")
    for link in links:
        jobs.append({
            'url': link,
            'save_path': "results"
        })
    async_get(jobs, do_prod)


def start():
    links = [
        "https://topsale.am/product/adidas-originals-top-ten-rb-sneaker/16365/",
        "https://topsale.am/product/adidas-originals-top-ten-rb-sneaker/16365/",
        "https://topsale.am/product/adidas-originals-top-ten-rb-sneaker/16365/",
        "https://topsale.am/product/jack-and-jones-jorbendt-padded-jacket/16360/",
        "https://topsale.am/product/jack-and-jones-jorbendt-padded-jacket/16360/",
        "https://topsale.am/product/jack-and-jones-jorbendt-padded-jacket/16360/",
        "https://topsale.am/product/puma-rebound-playoff-sl-sneakers/16324/",
        "https://topsale.am/product/puma-rebound-playoff-sl-sneakers/16324/"
    ]
    do_individual(links)


if __name__ == '__main__':
    start()
