# -*- coding: utf-8 -*-
# by @嗷呜
# 基于原作者修改
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import re,sys,json,base64
from Crypto.Cipher import AES
from urllib.parse import urljoin
from Crypto.Util.Padding import unpad
from base.spider import Spider
sys.path.append('..')

class Spider(Spider):
    headers,host,cmskey,raw_play_url = {'User-Agent': 'okhttp/4.12.0'},'','',0

    def init(self, extend=''):
        if extend.startswith('http'):
         self.host=extend
        else:
            ext = json.loads(extend)
            self.host = ext['host']
            self.cmskey = ext.get('cmskey')
            raw_play_url = ext.get('RawPlayUrl')
            if raw_play_url == 1: self.raw_play_url = 1

    def homeVideoContent(self):
        data=self.fetch(f"{self.host}/api.php/app/index_video?token=",headers=self.headers).json()
        videos=[]
        for item in data['list']:videos.extend(item['vlist'])
        return {'list':videos}

    def homeContent(self, filter):
        data = self.fetch(f"{self.host}/api.php/app/nav?token=",headers=self.headers).json()
        keys = ["class", "area", "lang", "year", "letter", "by", "sort"]
        filters = {}
        classes = []
        for item in data['list']:
            has_non_empty_field = False
            jsontype_extend = item["type_extend"]
            classes.append({"type_name": item["type_name"], "type_id": item["type_id"]})
            for key in keys:
                if key in jsontype_extend and jsontype_extend[key].strip() != "":
                    has_non_empty_field = True
                    break
            if has_non_empty_field:
                filters[str(item["type_id"])] = []
            for dkey in jsontype_extend:
                if dkey in keys and jsontype_extend[dkey].strip() != "":
                    values = jsontype_extend[dkey].split(",")
                    value_array = [{"n": value.strip(), "v": value.strip()} for value in values if value.strip() != ""]
                    filters[str(item["type_id"])].append({"key": dkey, "name": dkey, "value": value_array})
        return {"class": classes, "filters": filters}

    def categoryContent(self, tid, pg, filter, extend):
        params = {'tid':tid,'class':extend.get('class',''),'area':extend.get('area',''),'lang':extend.get('lang',''),'year':extend.get('year',''),'limit':'18','pg':pg}
        data=self.fetch(f"{self.host}/api.php/app/video",params=params,headers=self.headers).json()
        return data

    def searchContent(self, key, quick, pg="1"):
        data=self.fetch(f"{self.host}/api.php/app/search?text={key}&pg={pg}",headers=self.headers).json()
        videos=data['list']
        for item in data['list']:
            item.pop('type', None)
        return {'list':videos,'page':pg}

    def detailContent(self, ids):
        data=self.fetch(f"{self.host}/api.php/app/video_detail?id={ids[0]}",headers=self.headers).json()['data']
        show,paly_urls = [],[]
        for i in data['vod_url_with_player']:
            urls = i['url'].split('#')
            urls2 = []
            for j in urls:
                if j:
                    url = j.split('$',1)
                    urls2.append(f"{url[0]}${self.lvdou(url[1])}")
            paly_urls.append('#'.join(urls2))
            show.append(f"{i['name']}{i['code']}")
        data.pop('vod_url_with_player')
        data['vod_play_from'] = '$$$'.join(show)
        data['vod_play_url'] = '$$$'.join(paly_urls)
        return  {'list':[data]}

    def playerContent(self, flag, video_id, vipFlags):
        jx = 0
        if self.check_paly_url(video_id):
            if self.raw_play_url == 1:
                video_id = self.raw_url(video_id)
        elif re.search(r'(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com', video_id):
            jx = 1
        return {'jx': jx, 'playUrl': '', 'parse': 0, 'url': video_id, 'header': self.headers}

    def lvdou(self, text):
        key = self.cmskey[:16].encode("utf-8")
        iv = self.cmskey[-16:].encode("utf-8")
        original_text = text
        url_prefix = "lvdou+"
        if original_text.startswith(url_prefix):
            ciphertext_b64 = original_text[len(url_prefix):]
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                ct_bytes = base64.b64decode(ciphertext_b64)
                pt_bytes = cipher.decrypt(ct_bytes)
                return unpad(pt_bytes, AES.block_size).decode('utf-8')
            except Exception:
                return original_text
        else:
            return original_text

    def raw_url(self,original_url):
        try:
            response = self.fetch(original_url,allow_redirects=False,stream=True,timeout=20)
            if 300 <= response.status_code < 400:
                redirect_location = response.headers.get('Location')
                if redirect_location:
                    real_url = urljoin(original_url, redirect_location)
                    return real_url
            return original_url
        except Exception:
            return original_url

    def check_paly_url(self,content):
        pattern = r"https?://.*(?:\.(?:avi|wmv|wmp|wm|asf|mpg|mpeg|mpe|m1v|m2v|mpv2|mp2v|ts|tp|tpr|trp|vob|ifo|ogm|ogv|mp4|m4v|m4p|m4b|3gp|3gpp|3g2|3gp2|mkv|rm|ram|rmvb|rpm|flv|mov|qt|nsv|dpg|m2ts|m2t|mts|dvr-ms|k3g|skm|evo|nsr|amv|divx|webm|wtv|f4v|mxf)|[\w\-_]+\.lyyytv\.cn\/.)"
        regex = re.compile(pattern, re.IGNORECASE | re.VERBOSE)
        return regex.search(content) is not None

    def getName(self):
        pass

    def localProxy(self, param):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

if __name__ == "__main__":
    sp = Spider()
    formatJo = sp.init(
        '''        
        {
            "host": "http://cmsmytv.lyyytv.cn",
            "cmskey": "z0afJ9wfCMEuLwDMJCFHwFQmaxCzC5zM",
            "RawPlayUrl": 1
        }
        '''
    )  # 初始化
    # formatJo = sp.homeContent(False) # 筛选分类(首页 可选)
    # formatJo = sp.homeVideoContent() # (首页 可选)
    # formatJo = sp.searchContent("仙逆",False,'1') # 搜索
    # formatJo = sp.categoryContent('20', '1', False, {}) # 分类
    # formatJo = sp.detailContent(['74080']) # 详情
    # formatJo = sp.playerContent("","http://yh4kjx.lyyytv.cn/d/ty/12489192151422919/01_4K.mp4",{}) # 播放
    # formatJo = sp.localProxy({"":""}) # 代理
    print(formatJo)

'''        
{
    "host": "http://cmsmytv.lyyytv.cn",
    "cmskey": "z0afJ9wfCMEuLwDMJCFHwFQmaxCzC5zM",
    "RawPlayUrl": 1
}
'''