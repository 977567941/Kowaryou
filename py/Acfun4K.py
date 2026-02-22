# coding=utf-8
# !/usr/bin/python



from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import urllib.request
import urllib.parse
import datetime
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://www.acfun.cn" #  首页 https://www.acfun.cn/

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
          }

class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def extract_nth_middle_text(self, text, start_str, end_str, n=0):

        results = []
        start_index = 0
        while True:
            start_index = text.find(start_str, start_index)
            if start_index == -1:
                break
            start_index += len(start_str)
            end_index = text.find(end_str, start_index)
            if end_index == -1:
                break
            middle_text = text[start_index:end_index].replace("\\", "")
            results.append(middle_text)

        if n < len(results) and n >= 0:
            return results[n]
        else:
            return None

    def parse_video_info(self, res, doc):

        try:
            description = self.extract_middle_text(res, "description-container'>", '<', 0)
            if not description:
                content = "为您介绍剧情📢 无简介"
            else:
                content = '为您介绍剧情📢' + description
        except Exception:
            content = "为您介绍剧情📢 无简介"

        try:
            director = self.extract_middle_text(res, "class='viewsCount'>", '<', 0)
            if not director or director.strip() == '':
                director = "无信息"
            else:
                director += "播放"
        except Exception:
            director = "无信息"

        try:
            actor = self.extract_middle_text(res, 'likeCount">', '<', 0)
            if not actor or actor.strip() == '':
                actor = "无信息"
            else:
                actor += "点赞"
        except Exception:
            actor = "无信息"

        try:
            tag_div = doc.find('div', class_="tag")
            remarks = tag_div.text.strip() if tag_div else "未知"
        except Exception:
            remarks = "未知"

        return content, director, actor, remarks

    def homeContent(self, filter):
        result = {"class": []}

        detail = requests.get(url=xurl, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        res = self.extract_middle_text(res, '番剧列表', '文章', 0)
        pattern = r'href="(.*?)">(.*?)</a>'
        matches = re.findall(pattern, res)

        skip_keywords = {r'\b动画\b', r'\b娱乐\b', r'\b生活\b', r'\b音乐\b', r'\b舞蹈·偶像\b', r'\b游戏\b', r'\b科技\b', r'\b影视\b', r'\体育\b', r'\鱼塘\b'}

        for href, title in matches:

            type_name = title
            if any(re.search(keyword, type_name) for keyword in skip_keywords):
                continue

            type_id = xurl + href

            result["class"].append({"type_id": type_id, "type_name":type_name})

        result["class"].insert(0, {"type_id": f"{xurl}/bangumilist", "type_name": "番剧"})

        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        if 'bangumilist' not in cid:
            url = f'{cid}?page={str(page)}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('div', class_="list-wrapper")

            for soup in soups:
                vods = soup.find_all('div', class_="list-content-item")

                for vod in vods:
                    names = vod.find('h1', class_="list-content-title")
                    name = names.find('a')['title']

                    id = names.find('a')['href']
                    if 'http' not in id:
                        id = xurl + id

                    pic = vod.find('img')['src']

                    try:
                        remarks = vod.find('div', class_="danmaku-mask")
                        remark = "时长 " + remarks.text.strip() if remarks else "未知"
                    except Exception:
                        remark = "未知"

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks":remark
                            }
                    videos.append(video)

        else:
            url = f'{cid}?pageNum={str(page)}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('ul', class_="ac-mod-ul")

            for soup in soups:
                vods = soup.find_all('li')

                for vod in vods:
                    names = vod.find('div', class_="ac-mod-title")
                    name = names['title']

                    ids = vod.find('a', class_="ac-mod-link")
                    id = ids['href']

                    pic = vod.find('img')['src']

                    try:
                        remark = self.extract_middle_text(str(vod), '<em>', '<', 0)
                        if not remark:
                            remark = "未知"
                    except Exception:
                        remark = "未知"

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                            }
                    videos.append(video)

        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        bofang = ''

        if 'bangumi' not in did:
            res = requests.get(url=did, headers=headerx)
            res.encoding = "utf-8"
            res = res.text
            doc = BeautifulSoup(res, "lxml")

            content, director, actor, remarks = self.parse_video_info(res, doc)

            soups = doc.find('ul', class_="scroll-div")
            if soups:
                soup = soups.find_all('li')

                for sou in soup:

                    id = sou['data-href']
                    if 'http' not in id:
                        id = xurl + id

                    name = sou['title']

                    bofang = bofang + name + '$' + id + '#'

                bofang = bofang[:-1]

                xianlu = 'Acfun专线'

            else:
                id = self.extract_middle_text(res, '"shareUrl":"', '"', 0)

                name = self.extract_middle_text(res, 'class="title"><span>', '<', 0)
                name = name.replace('#', '')
                
                bofang = name + '$' + id

                xianlu = 'Acfun专线'

            videos.append({
                "vod_id": did,
                "vod_director": director,
                "vod_actor": actor,
                "vod_remarks": remarks,
                "vod_content": content,
                "vod_play_from": xianlu,
                "vod_play_url": bofang
                         })
        else:
            res = requests.get(url=did, headers=headerx)
            res.encoding = "utf-8"
            res = res.text
            doc = BeautifulSoup(res, "lxml")

            content, director, actor, remarks = self.parse_video_info(res, doc)

            res = self.extract_middle_text(res, '"items":', "};", 0)
            data = json.loads(res)

            for sou in data:
                bangumiId = sou['bangumiId']

                itemId = sou['itemId']

                id = str(bangumiId) + '@' + str(itemId)

                name = sou.get('title', sou.get('episodeName', '未知'))

                bofang = bofang + name + '$' + id + '#'

            bofang = bofang[:-1]

            xianlu = 'Acfun专线'

            videos.append({
                "vod_id": did,
                "vod_director": director,
                "vod_actor": actor,
                "vod_remarks": remarks,
                "vod_content": content,
                "vod_play_from": xianlu,
                "vod_play_url": bofang
                          })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):

        if '@' not in id:
            detail = requests.get(url=id, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text.replace("\\", "")
            url = self.extract_middle_text(res, '[{"id":1,"url":"', '"', 0)

        else:
            fenge = id.split("@")
            url = f'{xurl}/bangumi/aa{fenge[0]}_36188_{fenge[1]}'
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text.replace("\\", "")
            url = self.extract_middle_text(res, '[{"id":1,"url":"', '"', 0)

        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, pg):
        result = {}
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        url = f'{xurl}/search?keyword={key}&pCursor={str(page)}'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        res = self.extract_nth_middle_text(res, 'bigPipe.onPageletArrive(', '</script>', n=5)
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_="search-bangumi")
        if soups:
            soup = doc.find_all('div', class_="bangumi__cover")

            for vod in soup:

                name = vod.find('img')['alt']

                id1 = self.extract_middle_text(str(vod), 'content_id":', ',', 0)
                id = f"{xurl}/bangumi/aa{id1}"

                pic = vod.find('img')['src']

                try:
                    remarks = vod.find('span', class_="episode-info")
                    remark = remarks.text.strip() if remarks else "未知"
                except Exception:
                    remark = "未知"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        else:
            soups = doc.find_all('div', class_="search-video")

            for vod in soups:

                names = vod.find('div', class_="video__main__title")
                name = names.text.strip()

                id = names.find('a')['href']
                if 'http' not in id:
                    id = xurl + id

                pic = vod.find('img')['src']

                try:
                    remarks = vod.find('span', class_="video__duration")
                    remark = "时长 " + remarks.text.strip() if remarks else "未知"
                except Exception:
                    remark = "未知"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result['list'] = videos
        result['page'] = pg
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








