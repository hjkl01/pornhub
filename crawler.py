#!/usr/bin/env python

import os
import re

import js2py
import requests
from lxml import etree
from clint.textui import progress
import fire
from loguru import logger

logger.add(
    "logs/%s.log" % __file__.rstrip(".py"),
    format="{time:MM-DD HH:mm:ss} {level} {message}",
)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}
proxies = {}

# 如果代理不稳定，不推荐使用
# local proxy service
# proxies example:
proxies = {
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080",
}


def list_page(url):
    logger.info("crawling : %s" % url)
    resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
    html = etree.HTML(resp.text)

    buff = '//*[@class="phimage"]/a/'
    names = html.xpath(f"{buff}@href")
    urls = html.xpath(f"{buff}img/@data-mediabook")
    for i in range(len(urls)):
        try:
            url = urls[i]
            name = re.findall("=ph(\w+)", names[i])[-1]
            logger.info(f"{url} {name}")
            download(url, name, "webm")
        except Exception as err:
            logger.error(err)


def detail_page(url):
    s = requests.Session()
    resp = s.get(url, headers=headers, proxies=proxies, verify=False)
    html = etree.HTML(resp.content)

    title = "".join(html.xpath("//h1//text()")).strip()
    logger.info(title)

    js_temp = html.xpath("//script/text()")
    for j in js_temp:
        if "flashvars" in j:
            videoUrl = exeJs(j)
            # logger.debug(videoUrl)
            download(videoUrl, title, "mp4")
            continue


def exeJs(js):
    flashvars = re.findall("flashvars_\d+", js)[0]
    js = "".join(js.split("\n\t")[:-5]).strip()
    # logger.debug(js)
    # logger.debug(flashvars)
    res = js2py.eval_js(js + flashvars)
    # logger.debug(res)
    if res.quality_720p:
        return res.quality_720p
    elif res.quality_480p:
        return res.quality_480p
    elif res.quality_240p:
        return res.quality_240p
    else:
        logger.error("parse url error")


def download(url, name, filetype):
    logger.info(f"{url} {name} {filetype}")
    filepath = "%s/%s.%s" % (filetype, name, filetype)
    if os.path.exists(filepath):
        logger.info("this file had been downloaded :: %s" % filepath)
        return
    else:
        response = requests.get(url, headers=headers, proxies=proxies, stream=True)
        with open(filepath, "wb") as file:
            total_length = int(response.headers.get("content-length"))
            for ch in progress.bar(
                response.iter_content(chunk_size=2391975),
                expected_size=(total_length / 1024) + 1,
            ):
                if ch:
                    file.write(ch)

        # from tqdm import tqdm
        # with open(filepath, "wb") as handle:
        #     for data in tqdm(response.iter_content()):
        #         handle.write(data)

        # rep = requests.get(url, headers=headers, proxies=proxies)
        # with open(filepath, 'wb') as file:
        #     file.write(rep.content)
        # urllib.request.urlretrieve(url, '%s' % filepath)
        logger.info("download success :: %s" % filepath)


def run(_arg=None):
    paths = ["webm", "mp4"]
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
    if _arg == "webm":
        # https://www.pornhub.com/categories
        urls = [
            # "https://www.pornhub.com/video?o=tr",
            # "https://www.pornhub.com/video?o=ht",
            # "https://www.pornhub.com/video?o=mv",
            "https://www.pornhub.com/video",
        ]
        for url in urls:
            list_page(url)
    elif _arg == "mp4":
        with open("download.txt", "r") as file:
            keys = list(set(file.readlines()))
        logger.info(keys)
        keys += [d.strip(".webm") for d in os.listdir("webm/")]
        for key in keys:
            if not key.strip():
                continue
            url = "https://www.pornhub.com/view_video.php?viewkey=ph%s" % key.strip()
            logger.info("url: {}", url)
            detail_page(url)
    else:
        _str = """
tips:
    python crawler.py webm
        - 下载热门页面的缩略图，路径为webm文件夹下

    python crawler.py mp4
        - 该命令会下载webm文件下对应的mp4文件
        - 也可以将目标地址写入download.txt中
        """
        logger.info(_str)
        return
    logger.info("finish !")


if __name__ == "__main__":
    fire.Fire(run)
