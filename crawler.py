#!/usr/bin/env python
# coding=utf-8

import os
import urllib
import json
import re

import gevent
import requests
from lxml import etree
import fire

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}


def list_page(url):
    print('crawling : %s' % url)
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    vkeys = html.xpath('//*[@class="phimage"]/div/a/@href')
    gif_keys = html.xpath('//*[@class="phimage"]/div/a/img/@data-mediabook')
    jobs = []
    for i in range(len(vkeys)):
        item = {}
        item['vkey'] = vkeys[i].split('=')[-1]
        item['gif_url'] = gif_keys[i]
        try:
            if 'ph' in item['vkey']:
                jobs.append(gevent.spawn(download, item['gif_url'], item['vkey'], 'webm'))
        except Exception as err:
            print(err)
    gevent.joinall(jobs, timeout=2)


def detail_page(url):
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
                download(_dict.get('videoUrl'), title, 'mp4')
                break    #如下载了较高分辨率的视频 就跳出循环
            except Exception as err:
                print(err)


def download(url, name, filetype):
    filepath = '%s/%s.%s' % (filetype, name, filetype)
    if os.path.exists(filepath):
        print('this file had been downloaded :: %s' % (filepath))
        return
    urllib.request.urlretrieve(url, '%s' % (filepath))
    print('download success :: %s' % (filepath))


def run(_arg=None):
    paths = ['webm', 'mp4']
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
    if _arg == 'webm':
        # 这是只放了两个分类链接 如需添加 请移步 https://www.pornhub.com/categories
        urls = ['https://www.pornhub.com/video?o=tr', 'https://www.pornhub.com/video?o=ht']
        jobs = [gevent.spawn(list_page, url) for url in urls]
        gevent.joinall(jobs)
    if _arg == 'link':
        path = 'webm'
        dir = os.listdir(path)  # dir是目录下的全部文件
        fopen = open('download.txt', 'w')
        for d in dir:
            string = d + '\n'  # 换行
            new_string = string.replace('.webm', '')  # 删掉后缀
            fopen.write(new_string)
        fopen.close()
    elif _arg == 'mp4':
        with open('download.txt', 'r') as file:
            keys = list(set(file.readlines()))
        jobs = []
        for key in keys:
            url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % key.strip()
            print(url)
            jobs.append(gevent.spawn(detail_page, url))
        gevent.joinall(jobs, timeout=2)
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
