# coding=utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""
import re,sys,requests
from bs4 import BeautifulSoup
from base.spider import Spider
sys.path.append('..')

class Spider(Spider):
    host = 'https://www.2t58.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1'}
    session = requests.Session()
    session.headers.update(headers)

    def get_data(self,url):
        for i in range(2):
            data_ = self.session.get(url=url)
            if not(data_.status_code == 403):
                data_.encoding = 'utf-8'
                data = data_.text
                return data
        return None

    def getName(self):
        return "首页"

    def init(self, extend=''):
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
                            output += f"#{match[1]}${number}{self.host}{match[0]}"
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
            return None
        return None

    def homeContent(self, filter):
        return {"class": [{"type_id": "/list/new@play_list", "type_name": "集多🌠新歌榜"},
                            {"type_id": "/list/top@play_list", "type_name": "集多🌠TOP榜单"},
                            {"type_id": "/list/djwuqu@play_list", "type_name": "集多🌠DJ舞曲"},
                            {"type_id": "/singerlist/index/index/index/index@singer_list", "type_name": "集多🌠歌手"},
                            {"type_id": "/playtype/index@video_list", "type_name": "集多🌠歌单"},
                            {"type_id": "/radiolist/index@video_list", "type_name": "集多🌠电台"},
                            {"type_id": "/mvlist/index@video_list", "type_name": "集多🌠高清MV"}],
                 }

    def homeVideoContent(self):
        videos = []
        res = self.get_data(self.host)

        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_="ilingkuplay_list")

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:

                names = vod.find('div', class_="name")
                name = names.text.strip()

                id = names.find('a')['href']

                try:
                    pic = vod.find('img')['src']
                except (TypeError, KeyError):
                    pic = "./qyg2.png"

                remark = "集多▶️请您欣赏"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        return {'list': videos}

    def categoryContent(self, cid, pg, filter, ext):
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        fenge = cid.split("@")
        res = self.get_data(f'{self.host}{fenge[0]}/{str(page)}.html')
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_=fenge[1])

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:

                names = vod.find('div', class_="name")
                name = names.text.strip()

                id = names.find('a')['href']
                try:
                    pic = vod.find('img')['src']
                except (TypeError, KeyError):
                    pic = "./qyg2.png"

                remark = "集多▶️请您欣赏"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        return {'list': videos, 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        play_from = '集多音乐专线'
        bofang = ''

        if 'http' not in did:
            did = self.host + did

        res = self.get_data(did)
        if all(kw not in did for kw in ['singer', 'playlist', 'radio']):

            content = '集多🎉为您介绍剧情📢' + self.extract_middle_text(res,'温馨提示：','</div>', 0)

            bofang = did

            videos.append({
                "vod_id": did,
                "vod_content": content,
                "vod_play_from": play_from,
                "vod_play_url": bofang
            })
        else:
            doc = BeautifulSoup(res, "lxml")
            info = doc.find('div', class_='info').get_text(strip=True)
            soups = doc.find('div', class_="play_list")
            soup = soups.find_all('li')

            for sou in soup:
                ids = sou.find('div', class_="name")
                id = self.host + ids.find('a')['href']

                name = sou.text.strip()

                bofang = bofang + name + '$' + id + '#'

            bofang = bofang[:-1]

            videos.append({
                "vod_id": did,
                "vod_content": f'集多🎉为您介绍剧情📢\n{info}',
                "vod_play_from": play_from,
                "vod_play_url": bofang
                          })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        url = ''
        headers = {
            'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
            'referer': id
        }
        if 'song' in id:
            id = id.replace(f'{self.host}/song/', '').replace('.html', '')
            payload = {"id": id, "type": "music"}
            response = self.session.post(self.host + "/js/play.php", headers=headers, data=payload)
            if response.status_code == 200:
                response_data = response.json()
                url = response_data.get('url')

        else:
            detail = self.session.get(url=id)
            detail.encoding = "utf-8"
            res = detail.text
            url1 = self.host + self.extract_middle_text(res, "',url:'", "'", 0).replace('\\', '')
            response = self.session.get(url1, headers=headers, allow_redirects=False)
            if response.status_code == 302:
                url = response.headers['Location']

        return {"parse": 0, "playUrl": '', "url": url, "header": self.headers}

    def searchContentPage(self, key, quick, pg):
        videos = []

        if pg:
            page = int(pg)
        else:
            page = 1

        res = self.get_data(f'{self.host}/so/{key}/{str(page)}.html')
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_="play_list")

        for soup in soups:
            vods = soup.find_all('li')

            for vod in vods:

                na = vod.find("div", class_="mv")
                if na:
                    names = vod.find("div", class_="name")
                    name = names.text.strip()

                    id = na.find('a')['href']

                else:
                    names = vod.find("div", class_="name")
                    name = names.text.strip()

                    id = names.find('a')['href']

                try:
                    pic = vod.find('img')['src']
                except (TypeError, KeyError):
                    pic = "./qyg2.png"

                remark = "集多▶️请您欣赏"

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)
        return {'list': videos, 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}

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