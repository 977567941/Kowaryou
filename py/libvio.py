# coding = utf-8
# !/usr/bin/python
# 辣坤哥 2025.08.12 sharkapp第三版
import hashlib
import re,sys,uuid,json,base64,urllib3
import time
import math
from Crypto.Cipher import AES
from base.spider import Spider
from Crypto.Util.Padding import pad,unpad
from bs4 import BeautifulSoup
sys.path.append('..')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Spider(Spider):
    xurl,key,iv,init_data,search_verify = '','','','',''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.libvio.me/'
    }

    # 参考示例代码添加cookie（从浏览器获取目标站cookie，否则可能无法获取播放源）
    tx_cookie = '__51vcke__=xxx; __51vuft__=xxx; __vtins__=xxx'  # 替换为实际cookie
    cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in tx_cookie.split('; ')}


    def getName(self):
        return "首页"

    def init(self, extend):
        js1=json.loads(extend)
        self.host = js1['host']
        self.json = js1.get('json', '')


    def homeContent(self, filter):
        result = {}
        result['class'] = [
            {'type_id': 1,'type_name': '电影'},
            {'type_id': 2, 'type_name': '剧集'},
            {'type_id': 4, 'type_name': '动漫'},
            {'type_id': 15, 'type_name': '日韩剧'},
            {'type_id': 16, 'type_name': '欧美剧'}
        ]
        return result

    def homeVideoContent(self):
        videos = []
        url1 = f'{self.host}'
        response = self.fetch(url1, headers=self.headers,cookies=self.cookies, verify=False)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')  # 或'lxml'
        vod_list = soup.find('ul', class_='stui-vodlist clearfix')
        items = vod_list.find_all('li') if vod_list else []
        #print(data_p)
        for item in items:
            # 找到包含链接信息的<a>标签
            link_tag = item.find('a', class_='stui-vodlist__thumb lazyload')
            update_info_tag = item.find('span', class_='pic-text text-right')
            if link_tag:
                # 提取所需数据
                name = link_tag.get('title', '').strip()
                pic = link_tag.get('data-original', '').strip()
                vod_id = link_tag.get('href', '').strip()
                remarks = update_info_tag.get_text().strip() if update_info_tag else ""
            video = {
                "vod_id": vod_id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remarks
            }
            videos.append(video)
        return {'list': videos}

    def categoryContent(self, cid, pg, filter, ext):
        videos = []
        url = f'https://www.libvio.me/type/{cid}-{pg}.html'
        response = self.fetch(url, headers=self.headers,cookies=self.cookies,verify=False)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')  # 或'lxml'
        vod_list = soup.find('ul', class_='stui-vodlist clearfix')
        items = vod_list.find_all('li') if vod_list else []
        # print(data_p)
        for item in items:
            # 找到包含链接信息的<a>标签
            link_tag = item.find('a', class_='stui-vodlist__thumb lazyload')
            update_info_tag = item.find('span', class_='pic-text text-right')
            if link_tag:
                # 提取所需数据
                name = link_tag.get('title', '').strip()
                pic = link_tag.get('data-original', '').strip()
                vod_id = link_tag.get('href', '').strip()
                remarks = update_info_tag.get_text().strip() if update_info_tag else ""
            video = {
                "vod_id": vod_id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remarks
            }
            videos.append(video)
        return {'list': videos, 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}

    def detailContent(self, ids):
        did = ids[0]
        videos = []
        url = f'{self.host}{did}'
        response = self.fetch(url, headers=self.headers, cookies=self.cookies, verify=False)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')  # 或'lxml'
        vod_name = ""
        title_tag = soup.find('h1', class_='title')
        if title_tag:
            vod_name = title_tag.get_text(strip=True)

        # 提取演员
        vod_actor = ""
        actor_tag = soup.find('p', class_='data', string=re.compile('主演：'))
        if actor_tag:
            actor_text = actor_tag.get_text(strip=True)
            vod_actor = actor_text.replace('主演：', '').split('/')[0].strip()

        # 提取导演
        vod_director = ""
        director_tag = soup.find('p', class_='data', string=re.compile('导演：'))
        if director_tag:
            director_text = director_tag.get_text(strip=True)
            vod_director = director_text.split('导演：')[-1].split('/')[0].strip()

        # 提取简介
        vod_content = ""
        synopsis_tag = soup.find('span', class_='detail-sketch')
        if synopsis_tag:
            vod_content = synopsis_tag.get_text(strip=True)

        # 提取年份
        vod_year = ""
        year_tag = soup.find('p', class_='data', string=re.compile('年份：'))
        if year_tag:
            year_text = year_tag.get_text(strip=True)
            year_match = re.search(r'年份：(\d+)', year_text)
            if year_match:
                vod_year = year_match.group(1)

        # 提取地区
        vod_area = ""  # 注意：这里的vod_class实际上是地区信息
        region_tag = soup.find('p', class_='data', string=re.compile('地区：'))
        if region_tag:
            region_text = region_tag.get_text(strip=True)
            region_match = re.search(r'地区：([^/]+)', region_text)
            if region_match:
                vod_area = region_match.group(1).strip()

        # 提取总集数作为vod_remarks
        vod_remarks = ""
        episodes_tag = soup.find('p', class_='data', string=re.compile('总集数：'))
        if episodes_tag:
            episodes_text = episodes_tag.get_text(strip=True)
            episodes_match = re.search(r'总集数：(\d+)', episodes_text)
            if episodes_match:
                vod_remarks = f"全{episodes_match.group(1)}集"

        # 查找所有播放源容器
        play_sources = soup.find_all('div', class_='stui-vodlist__head')

        # 初始化存储播放源和播放URL的列表
        source_list = []
        url_list = []

        for source in play_sources:
            # 查找播放源名称的h3标签
            h3_tag = source.find('h3', class_='iconfont')
            if h3_tag is None:
                # 如果找不到，跳过该播放源或者使用默认名称
                continue  # 或者 source_name = "未知播放源"
            source_name = h3_tag.get_text(strip=True).replace('icon-iconfontplay2', '').strip()

            # 提取该播放源下的所有剧集
            episodes = []
            episode_tags = source.select('ul.stui-content__playlist li a')
            for ep in episode_tags:
                episode_name = ep.get_text(strip=True)
                episode_url = 'https://www.libvio.me' + ep['href']
                episodes.append(f"{episode_name}${episode_url}")

            # 如果该播放源没有剧集，跳过
            if not episodes:
                continue

            # 将同一播放源的剧集用"#"连接
            source_urls = "#".join(episodes)
            source_list.append(source_name)
            url_list.append(source_urls)

        # 拼接符合规则的格式
        play_form = "$$$".join(source_list)  # 播放源名称用$$$分隔
        play_url = "$$$".join(url_list)  # 每个播放源的剧集列表用$$$分隔

        videos.append({
            "vod_id": did,
            "vod_name": vod_name,
            "vod_actor": vod_actor,
            "vod_director": vod_director,
            "vod_content": vod_content,
            "vod_remarks": vod_remarks,
            "vod_year": vod_year+ '年',
            "vod_area": vod_area,
            "vod_play_from": play_form,
            "vod_play_url": play_url
        })
        return {'list': videos}

    def playerContent(self, flag, id, vipFlags):
        if not self.json:
            # 当 self.json 为空时
            res = {
                "parse": 1,
                "playUrl": '',
                "url": id,
                "header": {
                    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 14; 23113RK12C Build/SKQ1.231004.001)'
                }
            }
            return res
        else:
            # 构建请求URL
            url = f"{self.json}{id}"

            # 发送请求并尝试解析为JSON
            try:
                response = self.fetch(url, headers=self.headers, verify=False).json()
            except Exception as e:
                # 请求失败时返回错误信息
                return {
                    "parse": 1,
                    "playUrl": '',
                    "url": id,
                    "header": {
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 14; 23113RK12C Build/SKQ1.231004.001)'
                    },
                    "error": f"请求失败: {str(e)}"
                }

            # 检查响应中是否有有效的url字段
            if 'url' in response and response['url']:  # 添加冒号(:)
                res = {
                    "parse": 0,
                    "playUrl": '',
                    "url": response['url'],
                    "header": {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    }
                }
            else:  # 添加冒号(:)
                res = {
                    "parse": 1,
                    "playUrl": '',
                    "url": id,
                    "header": {
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 14; 23113RK12C Build/SKQ1.231004.001)'
                    }
                }
        return res

    def searchContent(self, key, quick, pg="1"):
        videos = []
        url = f'{self.host}/search/{key}----------{pg}---.html'
        response = self.fetch(url, headers=self.headers, cookies=self.cookies, verify=False)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')  # 或'lxml'
        video_items = soup.select('ul.stui-vodlist.clearfix li')

        for item in video_items:
            # 提取标题
            title_tag = item.select_one('h4.title a')
            title = title_tag['title'] if title_tag and 'title' in title_tag.attrs else title_tag.get_text(
                strip=True) if title_tag else ''

            # 提取链接
            href_tag = item.select_one('a.stui-vodlist__thumb')
            href = href_tag['href'] if href_tag and 'href' in href_tag.attrs else ''

            # 提取图片
            data_original = href_tag['data-original'] if href_tag and 'data-original' in href_tag.attrs else ''

            # 提取状态信息
            status_tag = item.select_one('span.pic-text.text-right')
            status = status_tag.get_text(strip=True) if status_tag else ''
            videos.append({
                "vod_id": href,
                "vod_name": title,
                "vod_pic": data_original,
                "vod_remarks": status
            })
        return {'list': videos, 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

