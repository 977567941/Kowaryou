# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
from urllib.parse import quote_plus
from Crypto.Util.Padding import unpad
import re,sys,time,json,base64,hashlib,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    def localProxy(self, params):
        if params.get('type') == 'jx':
            try:
                return [200, 'text/json;charset=utf-8', self.jx(params)]
            except Exception as e:
                data = self.json_encode({"code": "400", "success": "0", "msg": "处理出错", "error": str(e)})
                return [400, 'text/json;charset=utf-8', data]
        return None

    def jx(self, params):
        error_msg = self.json_encode({"code": "400", "success": "0", "msg": "URL或API为空"})
        try:
            v = params['v']
            if not v: return error_msg
        except Exception:
            return error_msg
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
            is_play_from = (play_from_parts and any(
                (value := play_from_map.get(key.strip())) is not None and value in v for key in play_from_parts))
            is_play_prefix = (play_prefix_parts and any(
                v.startswith(prefix.strip()) for prefix in play_prefix_parts if prefix.strip()))
            is_play_include = (play_include_parts and any(
                inc.strip() in v for inc in play_include_parts if inc is not None and inc.strip() != ''))
            if not (is_play_from_all or is_play_from or is_play_prefix or is_play_include):
                return self.json_encode({"code": "-0", "success": "0", "msg": "不支持的地址"})
        def_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
        }
        qy_headers = {**def_headers, 'origin': 'https://www.iqiyi.com', 'referer': 'https://www.iqiyi.com/', 'sec-fetch-site': 'same-site'}
        response = self.fetch(f'https://data.video.iqiyi.com/v.f4v?random={int(time.time() * 1000)}', headers=qy_headers).json()
        res_time = response['time']
        url = quote_plus(v)
        key = self.sign(self.md5(f'{res_time}{url}'))
        payload = {'ua': '0', 'url': url, 'time': res_time, 'key': key, 'token': self.encrypt(key), 'area': response['t']}
        xm_headers = {**def_headers, 'Accept': 'application/json, text/javascript, */*; q=0.01', 'origin': 'https://jx.xmflv.cc', 'sec-fetch-site': 'cross-site'}
        data = ''
        api_num = 1
        for api in ['https://202.189.8.170/Api.js', 'https://cache.hls.one/Api.js']:
            try:
                response = self.post(api, data=payload, headers=xm_headers, timeout=10).json()
                if response.get('code') == 200:
                    data = response.get('data')
                    api_num += 1
                    break
            except Exception:
                continue
        if not data:
            return self.json_encode({"code": "-1", "success": "0", "msg": "请求API失败", "from": v})
        try:
            data2 = self.decrypt(data)
        except  Exception:
            return self.json_encode({"code": "-2", "success": "0", "msg": "解密失败", "from": v})
        data3 = {**response, **json.loads(data2)}
        for key in ['data', 'dmid', 'next', 'listapi', 'ggdmapi']: data3.pop(key, None)
        vid = data3.get('url', '')
        if not vid.startswith('http') or vid == 'https://kjjsaas-sh.oss-cn-shanghai.aliyuncs.com/u/3401405881/20240818-936952-fc31b16575e80a7562cdb1f81a39c6b0.mp4':
            return self.json_encode({"code": "-3", "success": "0", "msg": "解析失败", "from": v})
        if re.match(r'^https://(?:m|www)\.bilibili\.com/', v, re.I):
            if 'Referer' not in data3:
                data3['Referer'] = 'https://www.bilibili.com/'
            if 'User-Agent' not in data3:
                data3['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        elif re.match(r'^https://(?:m|www)\.mgtv\.com/', v, re.I):
            if 'User-Agent' not in data or data3.get('User-Agent') == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36':
                data3['User-Agent'] = 'MGDS/Android/2.0.5'
        elif 'User-Agent' not in data:
            data3['User-Agent'] = def_headers['User-Agent']
        data3['from'] = v
        data3['api'] = api_num
        return self.json_encode(data3)

    def sign(self, data):
        key = self.md5(data).encode('utf-8')
        data = data.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, b'OrSrAd8RtISPnooc')
        block_size = AES.block_size
        padding_length = block_size - (len(data) % block_size)
        if padding_length == block_size:
            padding_length = 0
        padded_data = data + b'\x00' * padding_length
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')

    def encrypt(self, text):
        if not text or not isinstance(text, str) or text.strip() == '': return None
        key = b'm7EgOccP4xSeyjwQ'
        key_length = len(key)
        text_bytes = text.encode('utf-8')
        data_length = len(text_bytes)
        aligned_length = ((data_length + 15) // 16) * 16
        aligned_buffer = bytearray(aligned_length)
        aligned_buffer[:data_length] = text_bytes
        if data_length < aligned_length:
            aligned_buffer[data_length] = 0x80
        encrypted_buffer = bytearray(aligned_length)
        for i in range(aligned_length):
            key_byte = key[i % key_length]
            encrypted_buffer[i] = aligned_buffer[i] ^ key_byte
        return base64.b64encode(bytes(encrypted_buffer)).decode('ascii')

    def decrypt(self, encrypted_data):
        cipher = AES.new(b'4zYgSAsEAUS6YAud', AES.MODE_CBC, b'ppa7qtR4McCIMCX4')
        decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
        return decrypted.decode('utf-8')

    def md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def json_encode(self, arr):
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