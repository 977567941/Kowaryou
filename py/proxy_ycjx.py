# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from urllib.parse import urlparse
from Crypto.Cipher import AES, ARC4
from base.spider import Spider
from Crypto.Util.Padding import unpad
import re,sys,time,json,base64,hashlib,urllib3,binascii
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    jx_api = ''

    def localProxy(self, params):
        if params.get('type') == 'ycjx':
            try:
                data =  self.jx(params)
                return [200, 'text/json;charset=utf-8', data]
            except Exception:
                data = self.json_encode({"code": "400", "success": "0", "msg": "处理出错"})
                return [400, 'text/json;charset=utf-8', data]
        return None

    def jx(self,params):
        error_msg = self.json_encode({"code": "400", "success": "0", "msg": "URL或API为空"})
        v = params.get('v')
        if not v: return error_msg
        if self.no_parse(params):
            return self.json_encode({"code": "-0", "success": "0", "msg": "链接不支持"})
        timeout = params.get('timeout') or 15

        app_key = 'HaTN33Xsne48P7HfhyQCajKsGFExSP2p'
        url = 'http://192.140.163.42:6199/api/index?parsesId=29&appid=10004&pay='
        key = self.domain(url)

        headers = {
          'User-Agent': 'okhttp/3.12.11',
          'Connection': 'Keep-Alive',
          'Accept-Encoding': 'gzip',
          'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        if self.jx_api:
            response2 = self.fetch(f'{self.jx_api}{v}', headers=headers, timeout=timeout, verify=False).json()
            return self.arr2json(v, response2)
        else:
            timestamp = str(int(time.time()))
            payload = {'t': timestamp, 'sign': hashlib.md5(f'pay&t={timestamp}&{app_key}'.encode('utf-8')).hexdigest()}
            response = self.post(url, data=payload, headers=headers, timeout=timeout, verify=False).text
            try:
                data = json.loads(response)
            except Exception:
                data = json.loads(self.rc4_decrypt(response,key))
            try:
                analysis = data['msg']['analysis']
                if not isinstance(analysis,list): ValueError()
            except Exception:
                return '获取analysis失败'
            res = ''
            for i in analysis:
                try:
                    if i['encry'] == 'n' and i['url'].startswith('http'):
                        response2 = self.fetch(f"{i['url']}{v}", headers=headers, timeout=timeout, verify=False).json()
                        if response2['url'].startswith('http'):
                            self.jx_api = i['url']
                            res = self.arr2json(v, response2)
                            break
                except Exception:
                    continue
            if not res: return '解析失败'
        return res

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
            if from_parts: is_from = any((domain := play_from_map.get(key)) is not None and domain in v for key in from_parts)
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

    def cc_decrypt(self, data, key):
        cipher = AES.new(key[:16].encode('utf-8'), AES.MODE_CBC, key[-16:].encode('utf-8'))
        decrypted = unpad(cipher.decrypt(base64.b64decode(data)), AES.block_size)
        return decrypted.decode('utf-8')

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

    def rc4_decrypt(self, ciphertext_hex, key):
        key_bytes = key.encode('utf-8')
        ciphertext_bytes = binascii.unhexlify(ciphertext_hex)
        cipher = ARC4.new(key_bytes)
        plaintext_bytes = cipher.decrypt(ciphertext_bytes)
        return plaintext_bytes.decode('utf-8')

    def domain(self, url):
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            if not domain:
                parsed_url = urlparse(f"http://{url}")
                domain = parsed_url.netloc
                if not domain: domain = ""
            if "." not in domain: return ""
            return domain
        except Exception:
            return ""

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