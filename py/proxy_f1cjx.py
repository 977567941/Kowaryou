# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
from Crypto.Util.Padding import unpad
import re,sys,time,json,base64,hashlib,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    def localProxy(self, params):
        try:
            if params.get('type') == 'f1cjx':
                data =  self.szy_jx(params)
            else:
                data = '请按要求传参'
            return [200, 'text/json;charset=utf-8', data]
        except Exception:
            data = self.json_encode({"code": "400", "success": "0", "msg": "处理出错"})
            return [400, 'text/json;charset=utf-8', data]

    def szy_jx(self, params):
        v = params.get('v')
        if not v:  return '链接为空'
        timeout = params.get('timeout') or 10
        host = params.get('domain') or 'https://f1c.cc'
        key = params.get('key') or 'LXFMQW7294RBTE10'
        iv = params.get('iv') or 'Y9D2H6Z5K81NRC3P'
        md5_salt = params.get('md5Salt') or '123456789'
        timestamp = int(time.time())
        md5_key = hashlib.md5(f'{md5_salt}{v}{timestamp}'.encode('utf-8')).hexdigest()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "origin": host,
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }
        body = {"url": v, "time": timestamp, "key": md5_key}
        try:
            data = self.post(f"{host}/p/api.php", data=body, headers=headers, timeout=timeout, verify=False, allow_redirects=True).json()
        except Exception:
            return '请求或解析失败'
        data.pop('user-agent', None)
        encrypted_url = data.get("url", "")
        if not encrypted_url:
            return self.json_encode({"code": "404", "success": "0", "msg": "解析失败", "from_url": v})
        try:
            encrypted_bytes = base64.b64decode(encrypted_url)
            cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
            decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
            url2 = decrypted_bytes.decode("utf-8")
        except Exception:
            return self.json_encode({"code": "-1", "success": "0", "msg": "解析失败", "from_url": v})
        url_pattern = re.compile(r"^https?://", re.IGNORECASE)
        if not (url_pattern.match(url2) or url2 == v):
            return self.json_encode({"code": "-2", "success": "0", "msg": "解析失败", "from_url": v})
        data['url'] = url2
        return self.arr2json(v, data)

    def arr2json(self, v, data):
        remove_key = ['type', 'ip', 'player', 'From', 'From_Url']
        for key in remove_key:
            data.pop(key, None)
        if re.match(r'^https://(?:m|www)\.bilibili\.com/', v, re.I):
            if 'Referer' not in data:
                data['Referer'] = 'https://www.bilibili.com/'
            if 'User-Agent' not in data:
                data[
                    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        elif re.match(r'^https://(?:m|www)\.mgtv\.com/', v, re.I):
            if 'User-Agent' not in data or data.get(
                    'User-Agent') == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36':
                data['User-Agent'] = 'MGDS/Android/2.0.5'
        data['from'] = v
        return self.json_encode(data)

    def no_parse(self, params):
        v = params.get('v')
        play_from = params.get('from')
        play_prefix = params.get('prefix')
        play_include = params.get('include')
        if not isinstance(v, str) or not v:
            return False
        if not any([play_from, play_prefix, play_include]): return False
        play_from_map = {
            'qq': 'qq.com',
            'qiyi': 'iqiyi.com',
            'youku': 'youku.com',
            'mgtv': 'mgtv.com',
            'bili': 'bilibili.com'
        }

        def split_param(param):
            if isinstance(param, str):
                return [p.strip() for p in param.split(',') if p.strip()]
            return []

        is_all = False
        if play_from == 'all':
            is_all = any(domain in v for domain in play_from_map.values())
        is_from = False
        if not is_all:
            from_parts = split_param(play_from)
            if from_parts: is_from = any(
                (domain := play_from_map.get(key)) is not None and domain in v for key in from_parts)
        is_prefix = False
        prefix_parts = split_param(play_prefix)
        if prefix_parts:
            is_prefix = any(v.startswith(prefix) for prefix in prefix_parts)
        is_include = False
        include_parts = split_param(play_include)
        if include_parts:
            is_include = any(inc in v for inc in include_parts)
        final_result = is_all or is_from or is_prefix or is_include
        return not final_result

    def json_encode(self,arr):
        return json.dumps(arr, ensure_ascii=False, indent=2)

    def init(self, extend=''):
        pass

    def homeContent(self, filter):
        pass

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        pass

    def searchContent(self, key, quick, pg='1'):
        pass

    def detailContent(self, ids):
        pass

    def playerContent(self, flag, id, vipflags):
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass