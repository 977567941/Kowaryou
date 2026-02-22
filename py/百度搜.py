# coding = utf-8
#!/usr/bin/python
from urllib.parse import unquote
from urllib.parse import quote
from base.spider import Spider
from bs4 import BeautifulSoup
from collections import Counter
import urllib.request
import urllib.parse
import threading
import requests
import binascii
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://ysxjjkl.souyisou.top/"

BaiduCookie = 'BDUSS=M4cjl1dTVSZFppeGIteThHZ3ktVDdhcUtGTk4xYW1QbG1wY0tnb2NKVGhGaE5wSUFBQUFBJCQAAAAAAAAAAAEAAABN9XcvZmpla2RmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOGJ62jhietoN0'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}
headerz = {
    'User-Agent': "netdisk;1.4.2;22021211RC;android-android;12;JSbridge4.4.0;jointBridge;1.1.0;",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Referer': "https://pan.baidu.com",
    'Cookie': BaiduCookie
}

pm = ''


class Spider(Spider):
    global xurl
    global headerx
    global headers
    global header

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        pass
    def homeVideoContent(self):
        pass

    def categoryContent(self, cid, pg, filter, ext):
        pass

    def detailContent(self, ids):
        result = {}
        videos = []
        play_kurl = []
        did = ids[0]
        if 'baidu' in did:
            id = 'http://sspa8.top:8100/api/vips.php?url=' + did
            res = requests.get(url=id, headers=headerz)
            kjson = res.json()
            if 'list' in kjson and kjson['list']:
                for i in kjson['list']:
                    play_urls = i['vod_play_url']
                    play_kurl = play_urls[:-1]
        videos.append({
            "vod_play_from": 'suisui',
            "vod_play_url": play_kurl
        })
        result['list'] = videos
        return result


    def playerContent(self, flag, id, vipFlags):
        result = {}
        if 'baidu' in id:
            bid = "http://sspa8.top:8100/api/vips.php?url=" + id
            res = requests.get(url=bid, headers=headerz)
            if res.status_code == 200:
                kjson = res.json()
                url = kjson['url']
                result = {}
                result["parse"] = 0
                result["playUrl"] = ''
                result["url"] = url
                result["header"] = headerz
                return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = 1
        url = f'https://ysxjjkl.souyisou.top/?search={key}'
        res = requests.get(url=url, headers=header)
        res.encoding = "utf-8"
        res = res.text
        doc = BeautifulSoup(res, 'lxml')
        soups = doc.find_all('div', class_='access-box')
        for i in soups:
            name_element = i.find('div', class_='info')
            name = name_element.get_text()
            name = ' '.join(name.split()).split('链接')[0].strip()
            id = name_element.find('a')['href']
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": 'https://pan.losfer.cn/view.php/15f16a3203e73ebfa1dab24687b78b96.png',
                "vod_remarks": '百度网盘'
            }
            videos.append(video)
        result = {'list': videos}
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result


    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None