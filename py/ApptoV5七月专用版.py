# -*- coding: utf-8 -*-
# 七月专用版 Spider
import sys, uuid, json
from base.spider import Spider
sys.path.append('..')


class Spider(Spider):
    local_uuid = ''
    config = ''
    parsing_config = []
    headers = {
        'User-Agent': "Dart/2.19 (dart:io)",
        'Accept-Encoding': "gzip",
        'appto-local-uuid': ''
    }
    account = ''
    password = ''
    token = ''

    def init(self, extend=""):
        try:
            self.host = extend.get('host','').strip() if isinstance(extend, dict) else str(extend).strip()
            self.account = extend.get('account','') if isinstance(extend, dict) else ''
            self.password = extend.get('password','') if isinstance(extend, dict) else ''
            self.token = extend.get('token','') if isinstance(extend, dict) else ''
            if not self.host.startswith('http'):
                return {}
            
            # 生成唯一 uuid 并更新 headers
            self.local_uuid = str(uuid.uuid4())
            self.headers['appto-local-uuid'] = self.local_uuid
            
            # 获取配置
            response = self.fetch(self._with_auth(f'{self.host}/apptov5/v1/config/get?p=android&__platform=android')).json()
            config = response['data']
            self.config = config

            # 解析解析配置
            parsing_conf = config['get_parsing']['lists']
            parsing_config = {}
            for i in parsing_conf:
                if len(i['config']) != 0:
                    label = [j['label'] for j in i['config'] if j['type']=='json']
                    parsing_config[i['key']] = label
            self.parsing_config = parsing_config

        except Exception as e:
            print(f'初始化异常：{e}')
            return {}

    # 给 URL 自动加上账号/密码/token
    def _with_auth(self, url):
        if self.account or self.password or self.token:
            params = {}
            if self.account: params['account'] = self.account
            if self.password: params['password'] = self.password
            if self.token: params['token'] = self.token
            # 自动拼接 URL
            sep = '&' if '?' in url else '?'
            auth_str = '&'.join([f'{k}={v}' for k,v in params.items()])
            url = f'{url}{sep}{auth_str}'
        return url

    # 图片地址修复
    def fix_pic(self, url):
        if url and url.startswith('mac://'):
            return url.replace('mac://','http://',1)
        return url

    # 详情内容
    def detailContent(self, ids):
        response = self.fetch(self._with_auth(f"{self.host}/apptov5/v1/vod/getVod?id={ids[0]}"), headers=self.headers).json()
        data = response['data']
        vod_play_url = ''
        vod_play_from = ''
        for i in data['vod_play_list']:
            play_url = ''
            for j in i['urls']:
                play_url += f"{j['name']}${i['player_info']['from']}@{j['url']}#"
            vod_play_from += i['player_info']['from'] + '$$$'
            vod_play_url += play_url.rstrip('#') + '$$$'
        vod_play_url = vod_play_url.rstrip('$$$')
        vod_play_from = vod_play_from.rstrip('$$$')

        # vod_remarks格式化
        vod_remarks = '|'.join(filter(None, [
            data.get('vod_remarks',''),
            str(data.get('vod_year','')),
            data.get('vod_area',''),
            ','.join(data.get('vod_type', []))
        ]))

        videos = [{
            'vod_id': data.get('vod_id'),
            'vod_name': data.get('vod_name'),
            'vod_content': data.get('vod_content'),
            'vod_remarks': vod_remarks,
            'vod_director': data.get('vod_director'),
            'vod_actor': data.get('vod_actor'),
            'vod_year': data.get('vod_year'),
            'vod_area': data.get('vod_area'),
            'vod_play_from': vod_play_from,
            'vod_play_url': vod_play_url
        }]
        return {'list': videos}

    # 搜索内容
    def searchContent(self, key, quick, pg='1'):
        url = self._with_auth(f"{self.host}/apptov5/v1/search/lists?wd={key}&page={pg}&type=&__platform=android")
        response = self.fetch(url, headers=self.headers).json()
        data = response['data']['data']
        for i in data:
            i['vod_pic'] = self.fix_pic(i.get('vod_pic',''))
        return {'list': data, 'page': pg, 'total': response['data']['total']}

    # 播放内容解析
    def playerContent(self, flag, id, vipflags):
        default_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        parsing_config = self.parsing_config
        parts = id.split('@')
        if len(parts) != 2:
            return {'parse': 0, 'url': id, 'header': {'User-Agent': default_ua}}
        playfrom, rawurl = parts
        label_list = parsing_config.get(playfrom)
        if not label_list:
            return {'parse': 0, 'url': rawurl, 'header': {'User-Agent': default_ua}}
        # 解析
        for label in label_list:
            try:
                response = self.post(
                    self._with_auth(f"{self.host}/apptov5/v1/parsing/proxy?__platform=android"),
                    data={'play_url': rawurl, 'label': label, 'key': playfrom},
                    headers=self.headers
                ).json()
            except Exception:
                continue
            data = response.get('data') or {}
            url = data.get('url')
            if url:
                ua = data.get('UA') or data.get('UserAgent') or default_ua
                return {'parse': 0, 'url': url, 'header': {'User-Agent': ua}}
        return {'parse': 1, 'url': rawurl, 'header': {'User-Agent': default_ua}}

    # 首页分类
    def homeContent(self, filter):
        config = self.config
        if not config:
            return {}
        home_cate = config['get_home_cate']
        classes = []
        for i in home_cate:
            classes.append({'type_id': i['cate'], 'type_name': i['title']})
        return {'class': classes}

    # 首页视频
    def homeVideoContent(self):
        response = self.fetch(self._with_auth(f'{self.host}/apptov5/v1/home/data?id=1&mold=1&__platform=android'), headers=self.headers).json()
        data = response['data']
        vod_list = []
        for i in data['sections']:
            for j in i['items']:
                vod_list.append({
                    "vod_id": j.get('vod_id'),
                    "vod_name": j.get('vod_name'),
                    "vod_pic": self.fix_pic(j.get('vod_pic','')),
                    "vod_remarks": j.get('vod_remarks')
                })
        return {'list': vod_list}

    # 分类内容
    def categoryContent(self, tid, pg, filter, extend):
        url = f"{self.host}/apptov5/v1/vod/lists?area={extend.get('area','')}&lang={extend.get('lang','')}&year={extend.get('year','')}&order={extend.get('sort','time')}&type_id={tid}&type_name=&page={pg}&pageSize=21&__platform=android"
        response = self.fetch(self._with_auth(url), headers=self.headers).json()
        data = response['data']
        data2 = data['data']
        for i in data2:
            i['vod_pic'] = self.fix_pic(i.get('vod_pic',''))
        return {'list': data2, 'page': pg, 'total': data['total']}

    # 保留空方法兼容
    def getName(self): pass
    def isVideoFormat(self, url): pass
    def manualVideoCheck(self): pass
    def destroy(self):
        self.config = None
        self.parsing_config = []
    def localProxy(self, param): return param
