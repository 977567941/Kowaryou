# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
import re,sys,time,json,base64,urllib3
from Crypto.Util.Padding import pad,unpad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    key = ''

    def localProxy(self, params):
        if params.get('type') == 'getjx':
            try:
                data =  self.jx(params)
                return [200, 'text/json;charset=utf-8', data]
            except:
                data = self.json_encode({"code": "400", "success": "0", "msg": "处理出错"})
                return [400, 'text/json;charset=utf-8', data]
        return None

    def jx(self, params):
        v = params.get('v')
        if not v: return '链接为空'
        domain = params.get('domain')
        if not domain: return 'host为空'
        parse_api = params.get('parse')
        if not parse_api: return 'parse为空'
        self.key = params.get('key')
        if not self.key: return 'key为空'
        get = params.get('get')
        get_type = 'qiji' if get == '2' else 'get'
        play_from = params.get('from')
        play_prefix = params.get('prefix')
        play_include = params.get('include')
        play_from_map = {
            'qq': 'qq.com',
            'qiyi': 'iqiyi.com',
            'youku': 'youku.com',
            'mgtv': 'mgtv.com',
            'bili': 'bilibili.com'
        }
        if play_from or play_prefix or play_include:
            play_from_parts = play_from.split(',') if isinstance(play_from, str) and play_from else []
            play_prefix_parts = play_prefix.split(',') if isinstance(play_prefix, str) and play_prefix else []
            play_include_parts = play_include.split(',') if isinstance(play_include, str) and play_include else []
            is_play_from_all = (play_from == 'all' and any(item in v for item in play_from_map.values() if item))
            is_play_from = (play_from_parts and any((value := play_from_map.get(key.strip())) is not None and value in v for key in play_from_parts))
            is_play_prefix = (play_prefix_parts and any(v.startswith(prefix.strip()) for prefix in play_prefix_parts if prefix.strip()))
            is_play_include = (play_include_parts and any(inc.strip() in v for inc in play_include_parts if inc is not None and inc.strip() != ''))
            if not (is_play_from_all or is_play_from or is_play_prefix or is_play_include):
                return self.json_encode({"code": "-0", "success": "0", "msg": "不支持的地址"})
        current_time = str(int(time.time()))
        headers = {
            'User-Agent': 'okhttp/3.14.9',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
            'app-version-code': '207',
            'app-ui-mode': 'light',
            'app-api-verify-time': current_time,
            'app-api-verify-sign': self.encrypt(current_time),
        }
        post_data = {'parse_api': parse_api, 'url': self.encrypt(v), 'token': ''}

        try:
            response = self.post(f"{domain}/api.php/{get_type}appapi.index/vodParse", headers=headers, data=post_data, timeout=30, verify=False).json()
        except Exception:
            return self.json_encode({"code": "-1","success": "0","msg": "请求或json解析失败"})
        try:
            data = json.loads(self.decrypt(response['data']))
            data = json.loads(data['json'])
        except Exception:
            return self.json_encode({"code": "-1", "success": "0", "msg": "解密失败或解析失败"})
        if 'url' not in data:
            return self.json_encode({"code":"404","msg":"解析失败","from":v,"server_data":data})
        data.pop('From', None)
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

    def encrypt(self, data):
        key = self.key
        if len(key) > 16:
            key = key[:16]
        elif len(key) < 16:
            key = key.ljust(16, '\0')
        iv = key if len(key) >= 16 else key.ljust(16, '\0')
        data = pad(data.encode('utf-8'), AES.block_size)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, data):
        key = self.key
        if len(key) > 16:
            key = key[:16]
        elif len(key) < 16:
            key = key.ljust(16, '\0')
        iv = key if len(key) >= 16 else key.ljust(16, '\0')
        data = base64.b64decode(data)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        decrypted = cipher.decrypt(data)
        decrypted = unpad(decrypted, AES.block_size)
        return decrypted.decode('utf-8')

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