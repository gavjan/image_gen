import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError


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


def fetch(session, job):
    if re.search(r"(jpg|jpeg|png|jfif|webp)$", job['url']):
        download_image(job['url'], f"input/{job['img_name']}")
        return job
    else:
        with session.get(job['url']) as response:
            job['data'] = response.text
            if response.status_code != 200:
                print("FAILURE::{0}".format(job['url']))
            return job


async def get_data_asynchronous(jobs, callback):
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            session.headers = {'User-Agent': 'Mozilla/5.0'}
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, job)
                )
                for job in jobs
            ]
            for response in await asyncio.gather(*tasks):
                callback(response)


def async_get(jobs, callback):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(jobs, callback))
    loop.run_until_complete(future)


# Example
def main():
    jobs = [
        {'url': "https://topsale.am/img/prodpic/8072cb8b65b1e1be3bab8177HWIZK7L._AC_UX625_.jpg",
         'arg': 1},
        {'url': "https://topsale.am/img/prodpic/912c69a66e4ad596304471EM8dMmr6L._AC_UX625_.jpg",
         'arg': 2}
    ]

    def callback(job):
        f = open(f"input/{job['arg']}.jpg", "wb")
        f.write(str.encode(job['data']))
        f.close()

    async_get(jobs, callback)


# main()
