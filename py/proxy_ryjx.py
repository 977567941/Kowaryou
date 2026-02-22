# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from Crypto.Cipher import AES
from base.spider import Spider
from Crypto.Util.Padding import unpad
from urllib.parse import unquote_plus
import re,sys,time,json,base64,hashlib,urllib3
from Crypto.Util.number import bytes_to_long,long_to_bytes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class DecryptShijie:
    def __call__(self, str_data, z=False):
        return self.decrypt(str_data, z)

    @staticmethod
    def decrypt(str_data, z=False):
        if not str_data:
            return None if z else str_data
        trim_str = str_data.strip()
        if trim_str.lower().startswith('<!doctype html') or trim_str.lower().startswith('<html'):
            return None if z else str_data
        try:
            json_obj = json.loads(str_data)
            if json_obj.get('code') != 1 or json_obj.get('msg') in ['退出成功', '热搜词库']:
                return None if z else str_data
        except Exception:
            pass
        clean_str = str_data.replace('"', '').replace('\\/', '/')
        prefix = ''
        if clean_str.startswith('lvdou+'):
            prefix = 'lvdou+'
        elif clean_str.startswith('lvDou+'):
            prefix = 'lvDou+'
        data_after_prefix = clean_str[len(prefix):] if prefix else clean_str
        if len(data_after_prefix) <= 32: return None if z else clean_str
        main_key = data_after_prefix[:32]
        if len(main_key) != 32 or not main_key.isalnum(): return None if z else clean_str
        encrypted_data = data_after_prefix[32:]
        return DecryptShijie.core_decrypt(main_key, encrypted_data, z, clean_str)

    @staticmethod
    def core_decrypt(main_key, encrypted_data, z, origin_str):
        if not encrypted_data.strip() or not DecryptShijie.is_valid_base64(encrypted_data):
            return None if z else origin_str
        try:
            decrypted_raw = DecryptShijie.aes_decrypt(encrypted_data, main_key)
            if not decrypted_raw or not decrypted_raw.strip():
                return None if z else origin_str
        except Exception:
            return None if z else origin_str

        try:
            return DecryptShijie.de_obfuscate(decrypted_raw)
        except Exception:
            return decrypted_raw

    @staticmethod
    def aes_decrypt(encrypted_data, main_key):
        key_hash = hashlib.sha256((main_key + 'encryption_key_salt_2024').encode()).digest()
        iv_hash = hashlib.sha256((main_key + 'iv_salt_2024').encode()).digest()[:16]
        if len(key_hash) != 32 or len(iv_hash) != 16: raise ValueError
        cipher = AES.new(key_hash, AES.MODE_CBC, iv_hash)
        decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
        return decrypted.decode()

    @staticmethod
    def de_obfuscate(data):
        try:
            json_obj = json.loads(data)
        except Exception:
            return data
        if '_f' not in json_obj or not isinstance(json_obj['_f'], dict): return data
        field_map = json_obj['_f']
        required_fields = ['data', 'timestamp', 'checksum']
        if not all(field in field_map for field in required_fields): return data
        if not all(field in json_obj for field in [field_map['data'], field_map['timestamp'], field_map['checksum']]): return data
        encoded_data = json_obj[field_map['data']]
        if not DecryptShijie.is_valid_base64(encoded_data): return data
        try:
            decoded_data = base64.b64decode(encoded_data)
        except Exception:
            return data
        return decoded_data.decode()

    @staticmethod
    def is_valid_base64(s):
        if not s or len(s) % 4 != 0:
            return False
        try:
            if re.match(r'^[A-Za-z0-9+/]*={0,2}$', s):
                base64.b64decode(s, validate=True)
                return True
        except Exception:
            pass
        return False

class Spider(Spider):
    headers = {'User-Agent': 'okhttp/4.12.0'}

    def localProxy(self, params):
        try:
            if params.get('type') == 'ryjx':
                data =  self.ry_jx(params)
            elif params.get('type') == 'ryccjx':
                data =  self.cc_jx(params)
            else:
                data = '请按要求传参'
            return [200, 'text/json;charset=utf-8', data]
        except Exception:
            data = self.json_encode({"code": "400", "success": "0", "msg": "处理出错"})
            return [400, 'text/json;charset=utf-8', data]

    def ry_jx(self, params):
        error_msg = self.json_encode({"code": "400", "success": "0", "msg": "URL或API为空"})
        try:
            v = params['v']
            api = unquote_plus(params['api'])
            if not (v and api.startswith('http')):
                return error_msg
        except Exception:
            return error_msg
        if self.no_parse(params):
            return self.json_encode({"code": "-0", "success": "0", "msg": "链接不支持"})
        retry = int(params.get('retry', 0))
        timeout = params.get('timeout')
        msg,data2 = None,None
        for i in range(retry+1):
            msg,data2 = None,None
            try:
                data = self.fetch(f'{api}{v}', headers=self.headers, timeout=timeout or 20, verify=False).json()
            except Exception:
                msg = self.json_encode({"code": "-1", "success": "0", "msg": "请求或json解析失败"})
                continue
            dat_vurl = data.get('url', '')
            if not dat_vurl:
                return self.json_encode(data)
            video_url = self.common_decrypt(dat_vurl)
            if not self.is_valid_url(video_url) or video_url == v:
                msg = self.json_encode({"code": "-3", "success": "0", "msg": "解密或解析失败"})
                continue
            if re.match(r'^https?://.*/api/index/Video/\?.*&act=ZhiBaiQq[0-9]*\.m3u8$', video_url, flags=re.IGNORECASE) or video_url == 'https://kjjsaas-sh.oss-cn-shanghai.aliyuncs.com/u/3401405881/20240818-936952-fc31b16575e80a7562cdb1f81a39c6b0.mp4':
                msg = self.json_encode({"code": "-4", "success": "0", "msg": "解析结果为无效地址"})
                continue
            data['url'] = video_url
            if 'url' in data:
                return self.arr2json(v, data)
            data2 = self.json_encode(data)
        return msg or data2 or self.json_encode({"code": "-5", "success": "0", "msg": "解析失败"})

    def cc_jx(self, params):
        v = params.get('v')
        if not v: return '链接为空'
        api = unquote_plus(params.get('api'))
        if not api: return 'api为空'
        if 'act=jxjm' not in api:
            return 'api不支持'
        appkey = params.get('appkey')
        if not appkey: return 'appkey为空'
        key = params.get('key')
        if not key: return 'key为空'
        timeout = params.get('timeout')
        if self.no_parse(params):
            return self.json_encode({"code": "-0", "success": "0", "msg": "链接不支持"})
        timestamp = str(int(time.time()))
        jx_api, line_id = api.split('id=',1)
        payload = {
            'url': v, 'id': str(line_id), 't': timestamp,
            'sign': hashlib.md5(f'url={v}&id={line_id}&t={timestamp}&{appkey}'.encode('utf-8')).hexdigest()
        }
        headers = {
            'User-Agent': 'okhttp/3.12.11',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        try:
            response = self.post(f'{jx_api}url={v}&app=10000', data=payload, headers=headers, verify=False, timeout=timeout or 10).text
        except Exception as e:
            return self.json_encode({"code": "-1","success": "0","msg": "请求失败", "error": str(e)})

        try:
            data = json.loads(self.cc_decrypt(response, key))
        except Exception as e:
            return self.json_encode({"code": "-1", "success": "0", "msg": "解密或解析失败", "error": str(e), 'raw_data': response})
        if 'url' in data:
            return self.arr2json(v, data)
        return self.json_encode(data)

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

    def common_decrypt(self, dat_vurl):
        if re.match(r'^https?://baidu\.con/', dat_vurl, re.I):
            if dat_vurl.count(':') > 2:
                result = self.ui9_decode(dat_vurl)
                if result: return result
            result = self.decode(dat_vurl)
            if result and self.is_valid_url(result): return result
            if result:
                result = self.ld_xor(result)
                if result: return result
            result = self.ld_xor(dat_vurl)
            if result: return result
            result = self.yd_xor(dat_vurl)
            if result: return result
        elif 'https://vod.baidu.com/' in dat_vurl:
            result = self.ld_xor(dat_vurl)
            if result: return result
        elif '6max.con' in dat_vurl:
            result = self.yd2(dat_vurl)
            if result: return result
        elif 'lvDou+' in dat_vurl:
            result = DecryptShijie()(dat_vurl)
            if result: return result
        elif dat_vurl.startswith('https://vod-parses.baidu.com/'):
            result = self.ui8(dat_vurl)
            if result: return result
        return None

    def ui9_decode(self, input_str):
        try:
            cleaned_input = re.sub(r'https://baidu\.con/|lvDou\+', '', input_str)
            if cleaned_input.count(':') < 2: return None
            parts = cleaned_input.split(':', 3)
            if len(parts) < 4: return None
            _, key, iv, data_part = parts
            cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
            decrypted = unpad(cipher.decrypt(base64.b64decode(data_part)), AES.block_size)
            return decrypted.decode()
        except Exception:
            return None

    def decode(self, d):
        original_d = d
        try:
            while re.match(r'^https?://baidu\.con/', d, re.I):
                data = re.sub(r'^https?://baidu\.con/', '', d, flags=re.I)
                if len(data) < 16:
                    return None
                key = data[:16].encode()
                encrypted_data = data[16:]
                cipher = AES.new(key, AES.MODE_CBC, key)
                decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
                d = decrypted.decode()
            return d if d != original_d else None
        except Exception:
            return None

    def ld_xor(self, d):
        if not d: return None
        original_d = d
        try:
            if 'https://baidu.con/' in d or 'https://vod.baidu.com/' in d or d.startswith('2423'):
                d = d.replace('https://baidu.con/', '').replace('https://vod.baidu.com/', '')
                if d.startswith("2423"): d = d[6:]
                substring = str(int(time.time()))[:8]
                decoded = base64.b64decode(d)
                sb = ''
                length = len(substring)
                length2 = len(decoded)
                for i in range(length2):
                    sb += chr(decoded[i] ^ ord(substring[i % length]))
                d = base64.b64decode(sb).decode()
            return d if d != original_d else None
        except Exception:
            return None

    def yd_xor(self, d):
        if not d or 'baidu.con/' not in d: return None
        try:
            parts = d.split('baidu.con/', 1)
            if len(parts) < 2: return None
            encoded_part = parts[1]
            decoded = base64.b64decode(encoded_part)
            split_parts = decoded.split(b'|', 1)
            if len(split_parts) != 2: return None
            str2, str3 = split_parts
            key = 'k3yM@$k2024'
            key_length = len(key)
            sb2 = ''
            for i in range(len(str2)):
                char = chr(str2[i] ^ ord(key[i % key_length]))
                sb2 += char
            sb3 = ''
            sb2_length = len(sb2)
            if sb2_length == 0: return None
            for i2 in range(len(str3)):
                pos1 = (i2 + 5) % sb2_length
                pos2 = i2 % sb2_length
                xor_value = (ord(sb2[pos1]) + ord(sb2[pos2])) % 256
                char = chr(str3[i2] ^ xor_value)
                sb3 += char
            return sb3
        except Exception:
            return None

    def yd2(self, d):
        if not d or '6max.con' not in d: return None
        try:
            data = d.replace('https://6max.con/', '')
            if len(data) < 16: return None
            key = data[:16][::-1]
            encrypted_data = data[16:]
            cipher = AES.new(key.encode(), AES.MODE_CBC, key.encode())
            decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
            return decrypted.decode()
        except Exception:
            return None

    def cc_decrypt(self, data, key):
        cipher = AES.new(key[:16].encode('utf-8'), AES.MODE_CBC, key[-16:].encode('utf-8'))
        decrypted = unpad(cipher.decrypt(base64.b64decode(data)), AES.block_size)
        return decrypted.decode('utf-8')

    def ui8_key(self, data):
        def remove_padding(data_bytes):
            if len(data_bytes) > 10 and data_bytes[0:2] == b'\x00\x02':
                separator_index = -1
                for i in range(2, len(data_bytes)):
                    if data_bytes[i] == 0x00:
                        separator_index = i
                        break
                if separator_index != -1 and separator_index >= 10:
                    return data_bytes[separator_index + 1:]
            if len(data_bytes) > 10 and data_bytes[0:2] == b'\x00\x01':
                separator_index = data_bytes.find(b'\x00', 2)
                if separator_index != -1:
                    return data_bytes[separator_index + 1:]
            leading_zeros = 0
            for i, byte in enumerate(data_bytes):
                if byte == 0x00:
                    leading_zeros += 1
                else:
                    break
            if 4 < leading_zeros < len(data_bytes) - 4:
                return data_bytes[leading_zeros:]
            return data_bytes

        try:
            ciphertext = base64.b64decode(data)
            e = 65537
            key_size = 256
            n = 21079562076490917015219587480852512299132282846588972509613626067512096161389328018952967457235862130835563213420479656634103575049300097161679204081658154497272581125245352803881834652019229809107820308002912749854520391970510245623300240009991722378306164668314002824501199929254049911331868110702469664803250702178374575823923934377743766444104491434605938939890181211241005585699358654598872394352374955459144334648826707577459995980217087014729507004998084715621911009102107688390105352539795259098849457413742825469024104523030276553490595865329453646012415093918163886593950079624681378051572920908409755103897
            if len(ciphertext) > key_size: raise ValueError
            data_int = bytes_to_long(ciphertext)
            if data_int >= n: raise ValueError
            result_bytes = long_to_bytes(pow(data_int, e, n))
            if len(result_bytes) < key_size:
                padding_length = key_size - len(result_bytes)
                result_bytes = b'\x00' * padding_length + result_bytes
            cleaned_bytes = remove_padding(result_bytes)
            try:
                result = cleaned_bytes.decode('utf-8')
                return result
            except UnicodeDecodeError:
                printable_bytes = bytes(b for b in cleaned_bytes if 32 <= b <= 126)
                if printable_bytes:
                    try:
                        return printable_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        return None
                return None
        except Exception:
            raise ValueError

    def ui8(self, data):
        try:
            if not data: return None
            processed = data.replace('https://vod-parses.baidu.com/', '').replace('"', '')
            parts = processed.split('81238', 1)
            if len(parts) < 2 or not parts[1]: return None
            aes_encrypted_part = parts[0]
            rsa_encrypted_part = parts[1]
            rsa_decrypted = self.ui8_key(rsa_encrypted_part)
            aes_key_iv = rsa_decrypted.split('|', 1)
            if len(aes_key_iv) < 2: return None
            aes_key = aes_key_iv[0].encode('utf-8')
            aes_iv = aes_key_iv[1].encode('utf-8')
            if len(aes_key) != 16 or len(aes_iv) != 16: raise ValueError
            aes_encrypted_bytes = base64.b64decode(aes_encrypted_part)
            cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
            decrypted_padded = cipher.decrypt(aes_encrypted_bytes)
            decrypted = unpad(decrypted_padded, AES.block_size).decode('utf-8')
            return decrypted.strip('"')
        except Exception:
            return None

    def is_valid_url(self, url):
        """验证是否为有效的URL"""
        if not url or url == 'null':
            return False
        return re.match(r'https?://.*', url, re.I) is not None

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