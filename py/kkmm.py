import json, base64
from html.parser import HTMLParser
from gmssl import sm4
import requests


class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []

    def handle_data(self, data):
        self._text.append(data)

    def get_text(self):
        return ''.join(self._text)


def html2text(html_str):
    extractor = _HTMLTextExtractor()
    extractor.feed(html_str)
    return extractor.get_text()


def format_json(data):
    try:
        parsed_data = json.loads(data)
        # 格式化输出（4空格缩进，保留中文）
        return json.dumps(parsed_data, ensure_ascii=False, sort_keys=False, indent=4)
    except json.JSONDecodeError:
        return data
    except Exception:
        return data


def clean_item(item, keep_keys=None, remove_keys=None):
    """清理字典项：保留/移除指定键，处理字符串HTML转义"""
    for key in list(item.keys()):
        if remove_keys and key in remove_keys:
            item.pop(key)
            continue
        if keep_keys and key not in keep_keys:
            item.pop(key)
            continue
        if isinstance(item.get(key), str):
            item[key] = html2text(item[key])


def get_data(payload, path='/api/app.php'):
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; U; Android 12; zh-cn; xiaomi) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
        'Accept-Encoding': "gzip",
        'accept-language': "zh-CN,zh;q=0.8",
        'cache-control': "no-cache"
    }

    response = requests.post(f'https://s.kumao.vip{path}', data=payload, headers=headers).text

    try:
        # 移除引号后转16进制字节
        encrypted_data = bytes.fromhex(response.replace('"', ''))
        sm4_crypt = sm4.CryptSM4()
        sm4_crypt.set_key(bytes.fromhex('621170111cbe54c18f6f4ef65e935e93'), sm4.SM4_DECRYPT)
        decrypted_data = sm4_crypt.crypt_ecb(encrypted_data).rstrip(b'\x00')
        data = decrypted_data.decode('utf-8')
    except Exception:
        print('解密失败')
        return None

    try:
        parsed_data = json.loads(data)
        return parsed_data['appInfoList'] if 'appInfoList' in parsed_data else parsed_data
    except Exception:
        print('列表获取失败')
        print(format_json(data))
        return None


def base64_encode(data):
    return base64.b64encode(str(data).encode('utf-8')).decode('utf-8')

def alls(page=1):
    res = get_data({'page': base64_encode(page), 'type': base64_encode(1)})
    keep_keys = {'appid', 'name', 'content', 'size', 'category'}
    for item in res:
        clean_item(item, keep_keys=keep_keys)
    return res

def recently_updated(page=1):
    res = get_data({'page': base64_encode(page), 'type': base64_encode(0)})
    keep_keys = {'appid', 'name', 'content', 'size', 'category'}
    for item in res:
        clean_item(item, keep_keys=keep_keys)
    return res


def search(key, page=1):
    res = get_data({'content': base64_encode(key), 'page': base64_encode(page), 'type': base64_encode('search_result')})
    keep_keys = {'appid', 'name', 'content', 'size', 'category'}
    for item in res:
        clean_item(item, keep_keys=keep_keys)
    return res


def detail(app_id):
    res = get_data({'appid': base64_encode(app_id), 'email': ''}, '/api/app_tali.php')
    remove_keys = {'icon', 'img'}
    for item in res['appDetails']:
        clean_item(item, remove_keys=remove_keys)
    for item in res['reCommendApp']:
        clean_item(item, remove_keys=remove_keys)
    return res


# 最近更新
# res = recently_updated()
'''
[{
	'name': '鲸鱼视频(1.1.0)最新去广告纯净版',    # 文件名称
	'content': '',   # 简介，可能为空
	'appid': '03393',   # 文件id，用于访问详情函数(detail)
	'size': '60',    # 文件大小（单位MB）
	'category': '网络采集'  # 来源
}, {
	'name': '曼波动漫(1.1.9)去广告动漫追番软件',
	'content': '',
	'appid': '02755',
	'size': '40',    # 文件大小（单位MB）
	'category': '网络采集'
}]
'''
# print(res)

# 搜索
# res = search('影视')
'''
[{
	'name': '夏杰语音TV(4.3.4.9)电视端语音AI输入，强大的AI语音功能',    # 文件名
	'content': '一款电视端全功能智能语音服务软件，支持AI大模型，集语音输入/手机输入、语音换台、语音音乐/K歌、语音搜索电影电视剧、语音故事/相声/评书、语音智能家居、语音智能问答、古诗词/成语、语音点餐/订票/酒店、航班/火车票、天气、周边搜索/导航等30多类功能于一体，支持海量影视、音乐、菜谱、电视频道的搜索与控制，让您的生活更智慧、方便、快捷！',     # 简介，可能为空
	'appid': '03102',    # 文件id，用于访问详情函数(detail)
	'size': '7.5',    # 文件大小（单位MB）
	'category': '网络采集'
}, {
	'name': '云视听虎电竞(2.4.0)电视版虎牙游戏和影视直播',
	'content': '',
	'appid': '02792',
	'size': '24',
	'category': '网络采集'
}]
'''
# print(res)

# 全部文件。参数为页数,返回结果与 最近更新recently_updated函数格式一致
res = alls()
# print(res)

# 详情
# res = detail('02820')
'''
{
	'code': 0,
	'msg': '获取成功',
	'appDetails': [{
		'name': '动漫共和国(1.0.0.7)最新去广告v2版',  # 文件名
		'content': '',
		'appid': '02820',
		'mem': 'false',
		'size': '59',  # 文件大小（单位MB）
		'wes': 169519,
		'time': '1761435405',
		'comment_num': '34',
		'link': 'https://pan.lanzoum.com/iqyg737mc3wf|https://pan.lanzn.com/iqyg737mc3wf', # link地址中 | 为分割符合，多地址，可能存在重复地址或空地址（需要去掉）
		'colle': 'false',
		'category': '网络采集'
	}],
	'reCommendApp': [{  # reCommendApp是相关APP推荐，没有link地址，需要访问详情才可获取link地址
		'name': '拾光视频(2.1.0)最新去广告纯净版',
		'content': '',
		'appid': '02793', # appid是访问详情函数的标识符
		'mem': 'false',
		'size': '66',  # 文件大小（单位MB）
		'time': '1761354929',  # 时间（时间戳格式）
		'category': '网络采集'   # 来源
	}, {
		'name': '漫画台(3.4.6)高级版海量漫画免费阅读',
		'content': '',
		'appid': '02671',
		'mem': 'false',
		'size': '74',
		'time': '1761783790',
		'category': '网络采集'
	}],
	'appComments': [{   # APP评论，可能为空
		'id': '2247',  #用户id
		'username': 'liao15274178619@qq.com',    # 用户名
		'content': '咋又用不了了',   # 评论内容
		'appid': '2820',      
		'sendtime': '1760589680',  # 发送时间（时间戳格式）
		'replies': [{
			'reply': None,    # 回复内容（可能为空）
			'reply_time': None  # 回复时间（可能为空，时间戳格式）
		}]
	}, {
		'id': '2254',
		'username': 'come_0308@qq.com',
		'content': '闪退进不去',
		'appid': '2820',
		'sendtime': '1760800114',
		'replies': [{
			'reply': None,
			'reply_time': None
		}]
	}]
}
'''
print(res)