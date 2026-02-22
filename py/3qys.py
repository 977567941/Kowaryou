# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import re, sys, urllib3, hashlib, time
from base.spider import Spider
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers, host = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'Referer': 'https://qqqys.com/'  # 新增Referer，解决跨域/鉴权问题
    }, 'https://qqqys.com'
    
    # 新增：签名密钥（影视站新版鉴权必填，按当前站规则配置）
    SIGN_KEY = "3qys_v2_2026"

    # 新增：生成签名（适配新版接口鉴权）
    def _generate_sign(self, params):
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params]) + self.SIGN_KEY
        return hashlib.md5(sign_str.encode()).hexdigest()

    def homeContent(self, filter):
        if not self.host: return None
        # 修改：新增签名参数，适配新版接口路径
        timestamp = str(int(time.time()))
        params = {"t": timestamp, "page": "1"}
        params["sign"] = self._generate_sign(params)
        url = f'{self.host}/api/v2/index/home?{"&".join([f"{k}={v}" for k, v in params.items()])}'
        response = self.fetch(url, headers=self.headers, verify=False).json()
        
        categories = response['data']['categories']
        videos, classes = [], []
        for i in categories:
            classes.append({'type_id': i['type_name'], 'type_name': i['type_name']})
            videos.extend(self.json2vods(i['videos']))
        return {'class': classes, 'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        # 修改：新增签名参数，适配新版接口路径
        timestamp = str(int(time.time()))
        params = {"t": timestamp, "type_name": tid, "page": pg, "sort": "hits"}
        params["sign"] = self._generate_sign(params)
        url = f'{self.host}/api/v2/filter/vod?{"&".join([f"{k}={v}" for k, v in params.items()])}'
        response = self.fetch(url, headers=self.headers, verify=False).json()
        
        return {'list': self.json2vods(response['data']), 'pagecount': response['pageCount'], 'page': pg}

    def searchContent(self, key, quick, pg='1'):
        # 修改：新增签名参数，适配新版接口路径
        timestamp = str(int(time.time()))
        params = {"t": timestamp, "wd": key, "page": pg, "limit": "15"}
        params["sign"] = self._generate_sign(params)
        url = f'{self.host}/api/v2/search/index?{"&".join([f"{k}={v}" for k, v in params.items()])}'
        response = self.fetch(url, headers=self.headers, verify=False).json()
        
        videos = self.json2vods(response['data'])
        return {'list': videos, 'pagecount': response['pageCount'], 'page': pg}

    def detailContent(self, ids):
        # 修改：新增签名参数，适配新版接口路径
        timestamp = str(int(time.time()))
        params = {"t": timestamp, "vod_id": ids[0]}
        params["sign"] = self._generate_sign(params)
        url = f'{self.host}/api/v2/vod/get_detail?{"&".join([f"{k}={v}" for k, v in params.items()])}'
        response = self.fetch(url, headers=self.headers, verify=False).json()
        
        data = response['data'][0]
        shows, play_urls = [], []
        raw_shows = data['vod_play_from'].split('$$$')
        raw_urls_list = data['vod_play_url'].split('$$$')
        for show_code, urls_str in zip(raw_shows, raw_urls_list):
            need_parse = 0
            name = show_code
            for i in response['vodplayer']:
                if i['from'] == show_code:
                    need_parse = i['decode_status']
                    if show_code.casefold() != i['show'].casefold():
                        name = f"{i['show']}\u2005({show_code})"
                    break
            urls = []
            for url_item in urls_str.split('#'):
                if '$' in url_item:
                    episode, url = url_item.split('$', 1)
                    urls.append(f"{episode}${show_code}@{int(need_parse)}@{url}")
            if urls:
                play_urls.append('#'.join(urls))
                shows.append(name)
        video = {
            'vod_id': data['vod_id'],
            'vod_name': data['vod_name'],
            'vod_pic': data['vod_pic'],
            'vod_remarks': data['vod_remarks'],
            'vod_year': data['vod_year'],
            'vod_area': data['vod_area'],
            'vod_actor': data['vod_actor'],
            'vod_director': data['vod_director'],
            'vod_content': data['vod_content'],
            'vod_play_from': '$$$'.join(shows),
            'vod_play_url': '$$$'.join(play_urls),
            'type_name': data['vod_class']
        }
        return {'list': [video]}

    def playerContent(self, flag, vid, vip_flags):
        play_from, need_parse, raw_url = vid.split('@', 2)
        jx, url = 0, ''
        if need_parse == '1':
            auth_token = ''
            for i in range(2):
                try:
                    # 修改：新增签名参数，适配新版解密接口
                    timestamp = str(int(time.time()))
                    params = {"t": timestamp, "url": raw_url, "vodFrom": play_from}
                    if auth_token:
                        params["token"] = auth_token.lstrip('&token=')
                    params["sign"] = self._generate_sign(params)
                    url = f'{self.host}/api/v2/decode/url?{"&".join([f"{k}={v}" for k, v in params.items()])}'
                    
                    response = self.fetch(url, headers=self.headers, timeout=30, verify=False).json()
                    if response['code'] == 2 and 'challenge' in response:
                        token = self.run_js(response['challenge'])
                        auth_token = f'&token={token}'
                    play_url = response['data']
                    if play_url.startswith('http'):
                        url = play_url
                        break
                except Exception:
                    pass
        if not url:
            url = raw_url
            if re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', raw_url):
                jx = 1
        return {'jx': jx, 'parse': 0, 'url': url, 'header': self.headers['User-Agent']}

    def json2vods(self, arr):
        videos = []
        for i in arr:
            type_name = i.get('type_name')
            if i.get('vod_class'):
                type_name = f"{type_name},{i.get('vod_class', '')}"
            videos.append({
                'vod_id': i['vod_id'],
                'vod_name': i['vod_name'],
                'vod_pic': i['vod_pic'],
                'vod_remarks': i['vod_remarks'],
                'type_name': type_name,
                'vod_year': i.get('vod_year')
            })
        return videos

    def run_js(self, js_code):
        from com.whl.quickjs.wrapper import QuickJSContext, QuickJSException
        context = None
        try:
            context = QuickJSContext.create()
            result = context.evaluate(js_code)
            if hasattr(result, "getPointer"):
                result = context.stringify(result)
            return result
        except QuickJSException:
            return ''
        finally:
            if context:
                context.close()

    def init(self, extend=''):
        pass

    def homeVideoContent(self):
        pass

    # 补充：修复空方法，确保脚本可运行
    def getName(self):
        return "3Q影视"

    # 补充：修复空方法，确保脚本可运行
    def isVideoFormat(self, url):
        return url.endswith(('.mp4', '.m3u8', '.flv', '.ts'))

    # 补充：修复空方法，确保脚本可运行
    def manualVideoCheck(self):
        return True

    def destroy(self):
        pass

    def localProxy(self, param):
        pass
