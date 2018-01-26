#!/usr/bin/env python
# coding=utf-8

import os
import urllib
import json
import re

import requests
from lxml import etree
import fire


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}


def list_page(url):
    print('crawling : %s' % url)
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    vkeys = html.xpath('//*[@class="phimage"]/div/a/@href')
    gif_keys = html.xpath('//*[@class="phimage"]/div/a/img/@data-mediabook')
    _list = []
    for i in range(len(vkeys)):
        item = {}
        item['vkey'] = vkeys[i].split('=')[-1]
        item['gif_url'] = gif_keys[i]
        _list.append(item)
        try:
            if 'ph' in item['vkey']:
                downloadImageFile(item['gif_url'], item['vkey'])
        except Exception as err:
            print(err)


def downloadImageFile(imgUrl, name):
    path = 'webm/%s.webm' % name
    tem = os.path.exists(path)
    if tem:
        print('this webm file had been downloaded :: %s' % name)
        return
    print("downloading webm file :: ", name)
    r = requests.get(imgUrl, stream=True)
    with open('webm/%s.webm' % name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()


def req_detail_page(url):
    s = requests.Session()
    resp = s.get(url, headers=headers)
    html = etree.HTML(resp.content)
    title = ''.join(html.xpath('//h1//text()')).strip()

    js = html.xpath('//*[@id="player"]/script/text()')[0]
    tem = re.findall('var\s+\w+\s+=\s+(.*);\s+var player_mp4_seek', js)[-1]
    con = json.loads(tem)
    for _dict in con['mediaDefinitions']:
        if 'quality' in _dict.keys() and _dict.get('videoUrl'):
            print(_dict.get('quality'), _dict.get('videoUrl'))
            try:
                downloadvideo(_dict.get('videoUrl'), title)
                break
            except Exception as err:
                print(err)


def downloadvideo(url, title):
    tem = os.path.exists('mp4/%s.mp4' % title)
    if tem:
        print('this mp4 file had been downloaded :: %s' % title)
        return
    urllib.request.urlretrieve(url, 'mp4/%s.mp4' % title)
    print('download video success :: %s %s' % (url, title))


def run(_arg=None):
    paths = ['webm', 'mp4']
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
    if _arg=='webm':
        urls = ['https://www.pornhub.com/video?o=tr',
                'https://www.pornhub.com/video?o=ht']
        for url in urls:
            try:
                list_page(url)
            except Exception as err:
                print(err)
    elif _arg=='mp4':
        with open('download.txt', 'r') as file:
            keys = list(set(file.readlines()))
        for key in keys:
            url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % key.strip()
            print(url)
            req_detail_page(url)
    else:
        _str = """
tips:
    python crawler.py run webm 
        - 下载热门页面的缩略图，路径为webm文件夹下

    python crawler.py run mp4
        - 将下载的webm文件对应的以ph开头的文件名逐行写在download.txt中，运行该命令
        """
        print(_str)
    print('finish !')


if __name__ == '__main__':
    fire.Fire()
