# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from base64 import b64encode
from base.spider import Spider
from Crypto.PublicKey import RSA
from urllib.parse import quote_plus
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES, PKCS1_v1_5
import sys,time,json,random,hashlib,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    cache_host = {}
    def localProxy(self, params):
        if params.get('type') == 'drama':
            response = '获取域名失败'
            try:
                if params.get('from') == 'host':
                        url = params.get('url')
                        if url.startswith('http'):
                            response = self.cache_host.get(url)
                            if not(response and isinstance(response,str) and response.startswith('http')):
                                res = self.fetch(url,headers={'User-Agent': 'okhttp/3.12.1'}).json()
                                if res['domain'].startswith('http'):
                                    response =  res['domain']
                                    self.cache_host[url] = response
                elif params.get('from') == 'paramsData':
                    data = self.params_data(params)
                    response = data
                return [200, 'text/text;charset=utf-8', response]
            except Exception as e:
                return [500, 'text/text;charset=utf-8', f'处理出错: {e}']
        return None

    def params_data(self,params):
        ver_name = params.get('verName')
        ver = params.get('ver',ver_name.replace('.',''))
        app_name = params.get('AppName')
        pkg = params.get('pkg')
        public_key = params.get('publicKey').replace(' ','+')
        if not(ver and ver_name and app_name and pkg and public_key): return '请按要求传参'
        android_id = '313c3eeeb2a098a1'
        mac = '02:00:00:00:00:00'
        model = '23113RKC6C'
        manufacturer = 'Xiaomi'
        uuid = hashlib.md5(f'{android_id}{mac}{model}{manufacturer}'.encode('utf-8')).hexdigest().upper()
        timestamp = int(round(time.time() * 1000))
        random_str = self.random_str()
        cipher_aes = AES.new(b'OC1A06E197EF10CF3F6058CA7A803B5E', AES.MODE_ECB)
        sign_data = f'{timestamp}{random_str}'.encode('utf-8')
        sign_encrypted = cipher_aes.encrypt(pad(sign_data, AES.block_size))
        sign = b64encode(sign_encrypted).decode('utf-8')
        device_info = {
            'country': 'CN',
            'vName': ver_name,
            'cpuId': '',
            'young': 0,
            'facturer': manufacturer,
            'pkg': pkg,
            'uuid': uuid,
            'resolution': '900x1600',
            'mac': quote_plus(mac),
            'sig': self.rsa_encrypt(f'{timestamp}{random_str}{ver}', public_key),
            'abid': '6249',
            'model': model,
            'plat': 'android',
            'udid': uuid,
            'dpi': '240',
            'net': '1',
            'lang': 'zh',
            'random_str': random_str,
            'brand': 'Redmi',
            'timestamp': timestamp,
            'density': '3.25',
            'appName': quote_plus(app_name),
            'cpu': 'arm64-v8a',
            'chid': '10000',
            'carrier': quote_plus('移动'),
            'sig2': sign[:8],
            'sig3': sign[8:],
            '_vOsCode': '32',
            'vOs': '12',
            'vApp': ver,
            'device': '0',
            'androidID': android_id
        }
        dat = json.dumps(device_info, ensure_ascii=False, separators=(',',':'))
        key2 = b'ed5fdsgucxumegqa'
        cipher_aes2 = AES.new(key2, AES.MODE_CBC, key2)
        return cipher_aes2.encrypt(pad(dat.encode('utf-8'), AES.block_size)).hex()

    def rsa_encrypt(self, plaintext, public_key_str):
        public_key_pem = f'-----BEGIN PUBLIC KEY-----\n{public_key_str}\n-----END PUBLIC KEY-----'
        rsa_key = RSA.import_key(public_key_pem)
        cipher_rsa = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher_rsa.encrypt(plaintext.encode('utf-8'))
        return b64encode(encrypted).decode('utf-8')

    def random_str(self, length=16):
        char_array = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        result_str = ''
        i = 0
        while i < length - 1:
            c = random.choice(char_array)
            if c not in result_str:
                result_str += c
                i += 1
        return result_str + '='

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

    def playerContent(self, flag, vid, vip_flags):
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass