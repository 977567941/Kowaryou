/*
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: 'AppGet[模板]',
  lang: 'zh'
})
*/
import 'assets://js/lib/crypto-js.js';
//import '../lib/crypto-js.js';
// 全局变量
let config = {};
let _name = '';
let host = ''; // 全局host变量

let rule = {
    // 基础配置
    title: 'Appget[模板]',
    author: 'wow',
    
    // API接口配置
    homeUrl: '/api.php/Tapi.index/initV119',
    url: '/api.php/Tapi.index/typeFilterVodList',
    detailUrl: '/api.php/Tapi.index/vodDetail',
    searchUrl: '/api.php/Tapi.index/searchList',
    loginUrl: '/api.php/Tapi.index/appLogin',
    parseUrl: "/api.php/Tapi.index/vodParse",
    mineUrl: "/api.php/Tapi.index/mineInfo",
    adUrl: "/api.php/Tapi.index/watchRewardAd",
    vipUrl: "/api.php/Tapi.index/userBuyVip",
    verifyUrl: "/api.php/Tapi.verify/create?key=",
    userUrl: '/api.php/getappapi.index/userPointsLogs',
    danmuUrl: "/api.php/Tapi.index/danmuList",
    registerUrl: "/api.php/Tapi.index/appRegisterV133",
    
    // 其他配置
    timeout: 50000,
    play_parse: true,
    search_match: true,
    proxy_rule: null,
    headers: { 'User-Agent': 'okhttp/3.14.9' },
    playRegex: /\.m3u8|\.mp4|\.mkv/i,
    
    // 过滤规则
    title_remove: ['名称排除', '广告', '破解', '群'],
    line_remove: ['线路排除', '广告', '666', 'mymv'],
    line_order: ['线路排序', 'mgtv', 'qq', '官', 'ace', '1080p', 'dytt'],
    error_remove: /\/error|error\.|gitee|失败|错误|超时|异常|无效|无法|不支持|不存在|维护中/i,
    
    // API类型
    apiType: 'qijiappapi',
    
    // 解析配置
    enable_flag: true,
    parseOrder: 0
};


async function init(cfg) {
    console.log(`传入的cfg参数: 类型: ${typeof cfg}, 值: `, cfg);
    let ext = cfg.ext;
    
    // 直接使用传入的配置对象
    if (ext && typeof ext === 'object') {
        config = ext;
       // console.log(`[传入参数:]${JSON.stringify(cfg, null, 4)}`);
        const skey = cfg.skey || cfg.sourceKey || '';

        // 方法1：直接取 skey 中最后一个下划线后的部分
        const parts = skey.split('_');
        _name = parts.length > 0 ? parts[parts.length - 1] : '';
        
    } else if (ext && typeof ext === 'string') {
     //   console.log(`[传入参数:]: ${cfg}`);
        let parts = ext.split('$');
        let _host = parts[0];
        _name = decodeURIComponent(parts[1] || 'default');
        let html = await request(_host);
        let json = JSON.parse(html).AppGet;
        config = json[_name] || {};
    }
    
    // 从配置中更新过滤规则
    if (config.title_remove !== undefined) {
        rule.title_remove = Array.isArray(config.title_remove) ? config.title_remove : rule.title_remove;
    }
    if (config.line_remove !== undefined) {
        rule.line_remove = Array.isArray(config.line_remove) ? config.line_remove : rule.line_remove;
    }
    if (config.line_order !== undefined) {
        rule.line_order = Array.isArray(config.line_order) ? config.line_order : rule.line_order;
    }
    
    // 设置解析顺序
    if (config.parseOrder !== undefined) {
        rule.parseOrder = parseInt(config.parseOrder) || 0;
    }
    
    // 密钥配置
    rule.key = config.key || config.dataKey || config.datakey || '';
    rule.iv = rule.key || config.iv || config.dataIv || '';
    
    // 用户配置
    rule.username = config.username || '';
    rule.password = config.password || '';
    rule.token = config.token || ''; // 新增：支持直接配置token
    rule.lazyheader = config.lazyheader?.length ? config.lazyheader : rule.headers;
    rule.verify = /^(true|1)$/i.test(config.verify ?? 'true');
    rule.muban = config.muban || 'Appget';
    rule.enable_flag = /^(true|1)$/i.test(config.enable_flag ?? 'true');
    rule.auto_register = /^(true|1)$/i.test(config.auto_register ?? 'false');
    
    // 获取主机地址
    host = await hostJs();
    
    // 执行预处理
    await 预处理();
    
    cfg.skey = '';
    cfg.stype = '3';
}

async function home(filter) {
    if (!host) {
        host = await hostJs();
    }
    
    if (!host) {
        return JSON.stringify({ class: [] });
    }
    
    let url = `${host}${rule.homeUrl}`;
    let html = await request(url);
    let res = JSON.parse(html);

    if (!res.data) {
        return JSON.stringify({ class: [] });
    }
    
    const decryptedData = 解密(res.data);
    const data = JSON.parse(decryptedData);
    const type_list = data.type_list || [];
    
    const classes = [];
    const filterObj = {};
    
    const default_langs = ["国语", "粤语", "英语", "韩语", "日语"];
    const default_sorts = ["最新", "最热", "最赞"];
    const currentYear = new Date().getFullYear();
    const default_years = Array.from({ length: 10 }, (_, i) => (currentYear - i).toString());
    
    const DEFAULT_FILTERS = [
        { key: "lang", name: "语言", list: default_langs },
        { key: "year", name: "年份", list: default_years },
        { key: "sort", name: "排序", list: default_sorts }
    ];
    
    const addAllOption = (options) => [
        { n: "全部", v: "" },
        ...options.map(option => ({ n: option, v: option }))
    ];
    
    for (const item of type_list) {
        if (item.type_name ) {
            classes.push({ 
                type_name: item.type_name, 
                type_id: item.type_id 
            });
            
            if (item.type_name === "全部") {
                filterObj[item.type_id] = DEFAULT_FILTERS.map(filter => ({
                    key: filter.key,
                    name: filter.name,
                    value: addAllOption(filter.list)
                }));
            } else {
                filterObj[item.type_id] = (item.filter_type_list || []).map((it, i) => ({
                    key: it.name,
                    name: it.name,
                    value: (it.list || []).map(it1 => ({ n: it1, v: it1 }))
                }));
            }
        }
    }
    
    return JSON.stringify({
        class: classes,
        filters: filterObj
    });
}

function homeVod(params) {
    return JSON.stringify({
        list: []
    });
}

async function category(tid, pg, filter, extend) {
    if (!host) {
        return JSON.stringify({ list: [] });
    }
    
    let params = `type_id=${tid}&page=${pg || 1}`;
    
    if (extend.sort) params += `&sort=${extend.sort}`;
    if (extend.lang) params += `&lang=${extend.lang}`;
    if (extend.year) params += `&year=${extend.year}`;
    if (extend.area) params += `&area=${extend.area}`;
    if (extend.cateId) params += `&cateId=${extend.cateId}`;
    if (extend.class) params += `&class=${extend.class}`;
    const url = `${host}${rule.url}?${params}`;
    
    let html = await request(url);
    
    let res = JSON.parse(html);
    
    if (!res.data) {
        return JSON.stringify({ list: [] });
    }
    
    const html1 = 解密(res.data);
    const data = JSON.parse(html1);
    const list = data.recommend_list || [];
    
    const d = [];
    
    list.forEach(item => {
        if (!item || !item.vod_name) return;
        
        const title = item.vod_name;
        const isBadTitle = rule.title_remove && rule.title_remove.some(word =>
            new RegExp(word, 'i').test(title)
        );
        
        if (!isBadTitle) {
            d.push({
                vod_name: title,
                vod_id: item.vod_id || '',
                vod_pic: item.vod_pic || '',
                vod_remarks: item.vod_remarks || '',
            });
        }
    });
    
    return JSON.stringify({
        page: pg,
        pagecount: 99999,
        limit: 15,
        total: 99999,
        list: d
    });
}

async function detail(id) {
    if (!host) {
        return JSON.stringify({ list: [] });
    }
    
    const url = `${host}${rule.detailUrl}?vod_id=${id}`;
    
    let html = await request(url);
    
    let res = JSON.parse(html);
    
    if (!res.data) {
        return JSON.stringify({ list: [] });
    }
    
    const decryptedData = 解密(res.data);
    const json = JSON.parse(decryptedData);
    const vod = json.vod || {};
    const vodid = vod['vod_id'] || '';
    const playlist = json['vod_play_list'] || [];
    
    const playform = [];
    const playurls = [];
    
    playlist.forEach(item => {
        const playinfo = item.player_info || {};
        const parse = playinfo['parse'] || '';
        let form = playinfo.show || '';
        const headers = playinfo.headers || {};
        
        form = form ? form.replace(/(群号:?\d+|为防止失联请加群|失联加群|请加群)/g, '')
                    .replace(/\s+/g, ' ')
                    .replace(/\(\s*\)/g, '')
                    .trim() : form;
        
        let firstUrl = "";
        if (item.urls && item.urls.length > 0 && item.urls[0]) {
            firstUrl = item.urls[0].url || "";
        }
        
        if (firstUrl) {
            let domain = 提取域名(firstUrl);
            if (domain.length > 8) domain = domain.substring(0, 8);
            form = `${form}(${domain})`;
        }
        
        const isBadLine = rule.line_remove && rule.line_remove.some(pattern =>
            form.toLowerCase().includes(pattern.toLowerCase())
        );
        
        if (!isBadLine) {
            playform.push(form);
            
            const urls = item.urls.map((it, i) => {
                const newIt = {
                    ...it,
                    parse: parse,
                    vod_id: vodid,
                    headers: headers
                };
                return `${it.name}$${JSON.stringify(newIt)}`;
            }).join("#");
            
            playurls.push(urls);
        }
    });
    
    const sortedIndices = Array.from({length: playform.length}, (_, i) => i);
    sortedIndices.sort((a, b) => {
        const getPriority = (s) => {
            const lowerS = s.toLowerCase();
            for (let i = 0; i < rule.line_order.length; i++) {
                if (lowerS.includes(rule.line_order[i].toLowerCase())) {
                    return i;
                }
            }
            return rule.line_order.length;
        };
        return getPriority(playform[a]) - getPriority(playform[b]);
    });
    
    const sortedPlayform = sortedIndices.map(i => playform[i]);
    const sortedPlayurls = sortedIndices.map(i => playurls[i]);
    
    const vodDetail = {
        "vod_id": id,
        "vod_name": vod.vod_name || '未知',
        "vod_pic": vod.vod_pic || '',
        "type_name": vod.type_name || '',
        "vod_year": vod.vod_year || '',
        "vod_area": vod.vod_area || '',
        "vod_remarks": vod.vod_remarks || '',
        "vod_content": vod.vod_content || '暂无简介',
        "vod_play_from": sortedPlayform.join("$$$"),
        "vod_play_url": sortedPlayurls.join("$$$")
    };

    return JSON.stringify({
        list: [vodDetail]
    });
}

async function play(flag, id, flags) {
    const playData = JSON.parse(id);
    const purl = playData.url || '';
    const parse = playData.parse || '';
    const headers = playData.headers || {};
    
    if (rule.playRegex.test(purl)) {
        return JSON.stringify({ 
            parse: 0, 
            url: purl,
            header: headers
        });
    }
    
    if (parse && parse.startsWith('http')) {
        const parseApis = parse.split(',').map(api => api.trim());
        
        for (const api of parseApis) {
            const parseUrl = api.includes('url=') ? api : `${api}${api.includes('?') ? '&' : '?'}url=`;
            const fullUrl = parseUrl + encodeURIComponent(purl);
            
            const response = await request(fullUrl, { 
                headers: { ...headers, ...(rule.lazyheader || rule.headers) },
                timeout: 8000 
            });
            
            const result = JSON.parse(response);
            
            if (result.url && /^https?:\/\//i.test(result.url) && !rule.error_remove.test(result.url)) {
                return JSON.stringify({ 
                    parse: 0, 
                    url: result.url,
                    header: headers
                });
            }
        }
    }
    
    if (!parse || !parse.startsWith('http')) {
        const encryptedUrl = 加密(purl);
        const formData = `parse_api=${parse}&url=${encodeURIComponent(encryptedUrl)}`;
        const requestUrl = `${host}${rule.parseUrl}`;
        
        const html = await request(requestUrl, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/x-www-form-urlencoded', 
                ...headers, 
                ...(rule.lazyheader || rule.headers) 
            },
            body: formData,
            timeout: 5000
        });
        
        const jsonResponse = JSON.parse(html);
        const data = jsonResponse.data;
        
        if (data && !(Array.isArray(data) && !data.length)) {
            const jdata = 解密(data);
            const outerData = JSON.parse(jdata);
            const innerData = JSON.parse(outerData.json);
            
            if (innerData.url && /^https?:\/\//i.test(innerData.url)) {
                return JSON.stringify({ 
                    parse: 0, 
                    url: innerData.url, 
                    header: headers 
                });
            }
        }
    }
    
    return JSON.stringify({ 
        jx: 1,
        parse: 1, 
        url: id,
        header: headers
    });
}

async function lazy(flag, id, flags) {
    const urlObj = JSON.parse(id);
    const purl = urlObj.url || '';
    const parse = urlObj.parse || '';
    const vodid = urlObj.vod_id || '';
    const headers = urlObj.headers || {};
    
    const PLAY_REGEX = /\.m3u8|\.mp4|\.mkv/i;
    const isPlayUrl = PLAY_REGEX.test(purl);
    const isHttpParse = parse && parse.startsWith('http');
    const parseApis = parse ? parse.split(',').map(api => api.trim()) : [];
    
    let playResult = null;
    
    if (rule.parseOrder === 1) {
        if (isHttpParse) {
            for (const api of parseApis) {
                const parseUrl = api.includes('url=') ? api : `${api}${api.includes('?') ? '&' : '?'}url=`;
                const fullUrl = parseUrl + purl;
                
                const html = await request(fullUrl, { 
                    headers: { ...headers, ...(rule.lazyheader || rule.headers) },
                    timeout: 8000 
                });
                
                const result = JSON.parse(html);
                
                const hasError = (result.url && rule.error_remove.test(result.url)) ||
                               (result.msg && rule.error_remove.test(result.msg)) ||
                               (result.content && rule.error_remove.test(result.content)) ||
                               (result.code && result.code >= 400) ||
                               result.success === false;
                
                const isValidUrl = result.url && /^https?:\/\//i.test(result.url);
                
                if (!hasError && isValidUrl) {
                    playResult = { 
                        parse: 0, 
                        url: result.url, 
                        header: headers
                    };
                    break;
                }
            }
        }
        
        if (!playResult && isPlayUrl) {
            playResult = { parse: 0, url: purl, header: headers };
        }
        
        if (!playResult && !isHttpParse && !isPlayUrl) {
            const encryptedUrl = 加密(purl);
            const formData = `parse_api=${parse}&url=${encodeURIComponent(encryptedUrl)}`;
            const requestUrl = `${host}${rule.parseUrl}`;
            
            const html = await request(requestUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/x-www-form-urlencoded', 
                    ...headers, 
                    ...(rule.lazyheader || rule.headers) 
                },
                body: formData,
                timeout: 5000
            });
            
            const jsonResponse = JSON.parse(html);
            const data = jsonResponse.data;
            
            if (data && !(Array.isArray(data) && !data.length)) {
                const jdata = 解密(data);
                const outerData = JSON.parse(jdata);
                const innerData = JSON.parse(outerData.json);
                
                const hasError = innerData.url && rule.error_remove.test(innerData.url);
                const isValidUrl = innerData.url && /^https?:\/\//i.test(innerData.url);
                
                if (innerData.url && !hasError && isValidUrl) {
                    playResult = { parse: 0, url: innerData.url, header: headers };
                }
            }
        }
        
    } else {
        if (isPlayUrl) {
            playResult = { parse: 0, url: purl, header: headers };
        }
        
        if (!playResult && isHttpParse) {
            for (const api of parseApis) {
                const parseUrl = api.includes('url=') ? api : `${api}${api.includes('?') ? '&' : '?'}url=`;
                const fullUrl = parseUrl + purl;
                
                const html = await request(fullUrl, { 
                    headers: { ...headers, ...(rule.lazyheader || rule.headers) },
                    timeout: 8000 
                });
                
                const result = JSON.parse(html);
                
                const hasError = (result.url && rule.error_remove.test(result.url)) ||
                               (result.msg && rule.error_remove.test(result.msg)) ||
                               (result.content && rule.error_remove.test(result.content)) ||
                               (result.code && result.code >= 400) ||
                               result.success === false;
                
                const isValidUrl = result.url && /^https?:\/\//i.test(result.url);
                
                if (!hasError && isValidUrl) {
                    playResult = { 
                        parse: 0, 
                        url: result.url, 
                        header: headers
                    };
                    break;
                }
            }
        }
        
        if (!playResult && !isHttpParse && !isPlayUrl) {
            const encryptedUrl = 加密(purl);
            const formData = `parse_api=${parse}&url=${encodeURIComponent(encryptedUrl)}`;
            const requestUrl = `${host}${rule.parseUrl}`;
            
            const html = await request(requestUrl, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/x-www-form-urlencoded', 
                    ...headers, 
                    ...(rule.lazyheader || rule.headers) 
                },
                body: formData,
                timeout: 5000
            });
            
            const jsonResponse = JSON.parse(html);
            const data = jsonResponse.data;
            
            if (data && !(Array.isArray(data) && !data.length)) {
                const jdata = 解密(data);
                const outerData = JSON.parse(jdata);
                const innerData = JSON.parse(outerData.json);
                
                const hasError = innerData.url && rule.error_remove.test(innerData.url);
                const isValidUrl = innerData.url && /^https?:\/\//i.test(innerData.url);
                
                if (innerData.url && !hasError && isValidUrl) {
                    playResult = { parse: 0, url: innerData.url, header: headers };
                }
            }
        }
    }
    
    if (!playResult) {
        playResult = { jx: 1, parse: 1, url: purl, header: headers };
    }
    
    return JSON.stringify({
        parse: playResult.parse,
        url: playResult.url,
        header: playResult.header,
        danmaku: ''
    });
}

async function search(wd, quick) {
    for (let keyword of rule.title_remove) {
        if (wd.includes(keyword)) {
            return JSON.stringify({
                limit: 20,
                list: []
            });
        }
    }
    
    if (!host) {
        return JSON.stringify({ list: [] });
    }
    
    const body = `keywords=${encodeURIComponent(wd)}&type_id=0&page=1`;
    let list = [];
    
    if (rule.verify) {
        list = await 验证搜索(body);
    } else {
        const data = await request(`${host}${rule.searchUrl}`, {
            method: 'POST',
            body: body,
            headers: rule.headers
        });
        
        const json = JSON.parse(data);
        if (json.data) {
            const decryptedData = 解密(json.data);
            const searchData = JSON.parse(decryptedData);
            list = searchData.search_list || [];
        }
    }
    
    // 修改搜索匹配逻辑
    if (rule.search_match && list && list.length > 0) {
        const filteredResults = list.filter(item => {
            const title = item.vod_name || '';
            return title.toLowerCase().includes(wd.toLowerCase());
        });
        list = filteredResults;
    }
    
    const d = list.map(item => ({
        vod_name: item.vod_name || '',
        vod_id: item.vod_id || '',
        vod_pic: item.vod_pic || '',
        vod_remarks: item.vod_remarks || '搜索',
    }));

    return JSON.stringify({
        limit: 20,
        list: d
    });
}

// ==================== 核心功能函数 ====================

/**
 * 主机配置处理
 */
async function hostJs() {
    let hostUrl = config
        ? (config.host || config.hosturl || config.url || config.site || '')
        : '';
    if (!hostUrl) {
        return '';
    }
    
    let hostData = await request(hostUrl);
    if (hostData) {
        const firstLine = hostData.split('\n')[0].replace(/[\s\r]+/g, '');
        if (/^https?:\/\//i.test(firstLine)) {
            host = firstLine;
        } else {
            host = hostUrl;
        }
    } else {
        host = hostUrl;
    }
    
    if (host.endsWith('/')) {
        host = host.slice(0, -1);
    }
    
    return host;
}

/**
 * 预处理函数
 */
async function 预处理() {
    if (!host) {
        console.log(`[预处理] 主机地址为空`);
        return false;
    }
    
    console.log(`[预处理] 开始预处理，主机: ${host}`);
    console.log(`[预处理] 配置名称: ${_name || 'default'}`);
    
    rule.apiType = await 检测API类型(host);
    console.log(`[预处理] 检测到API类型: ${rule.apiType || '未知'}`);
    
    if (!rule.apiType) {
        rule.apiType = rule.muban === 'Appget' ? 'getappapi' : 'qijiappapi';
        console.log(`[预处理] 使用默认API类型: ${rule.apiType}`);
    }
    
    const API_PATHS = [
        'url', 'searchUrl', 'detailUrl', 'homeUrl', 'parseUrl', 'danmuUrl',
        'mineUrl', 'adUrl', 'vipUrl', 'loginUrl', 'verifyUrl', 'userUrl', 'registerUrl'
    ];
    
    API_PATHS.forEach(path => {
        if (rule[path]) {
            rule[path] = rule[path].replace(/Tapi/g, rule.apiType);
        }
    });
    
    let loginSuccess = false;
    
    // 优先使用直接配置的token
    if (rule.token) {
        rule.headers['app-user-token'] = rule.token;
        loginSuccess = true;
        console.log('使用配置的token登录');
    }
    // 如果配置了用户名密码，尝试登录获取token
    else if (rule.username && rule.password) {
        console.log('尝试使用配置的用户名密码登录');
        loginSuccess = await 用户登录();
        if (loginSuccess) {
            console.log('登录成功');
        } else {
            console.log('登录失败');
        }
    }
    
    if (!loginSuccess && rule.auto_register) {
        console.log('开始自动注册新账号');
        const registerSuccess = await 用户注册();
        if (registerSuccess) {
            console.log('使用新注册账号登录');
            loginSuccess = await 用户登录();
            
            if (loginSuccess) {
                await 检查并处理VIP功能();
            }
        } else {
            console.log('自动注册失败');
        }
    }
    
    if (loginSuccess) {
        setTimeout(() => {
            执行预处理循环().catch(() => {});
        }, 1000);
    }
    
    return true;
}

/**
 * API类型检测
 */
async function 检测API类型(hostUrl) {
    const TEST_APIS = [
        '/api.php/getappapi.index/mineInfo',
        '/api.php/qijiappapi.index/mineInfo'
    ];
    
    for (const api of TEST_APIS) {
        const testUrl = `${hostUrl}${api}`;
        const res = await request(testUrl, { timeout: 5000 });
        
        if (res.trim().startsWith('<')) continue;
        
        let jsonRes = JSON.parse(res);
        
        if (jsonRes.code !== undefined) {
            const apiType = api.includes('getappapi') ? 'getappapi' : 'qijiappapi';
            return apiType;
        }
    }
    
    return 'qijiappapi';
}

/**
 * 检查并处理VIP功能
 */
async function 检查并处理VIP功能() {
    const userInfo = await 获取用户信息();
    if (userInfo && userInfo.user_points > 0) {
        console.log(`[VIP检查] 用户积分: ${userInfo.user_points}`);
        await 处理VIP功能();
        return true;
    } else {
        console.log(`[VIP检查] 用户积分不足或未登录`);
    }
    return false;
}

/**
 * 处理广告功能
 */
async function 处理广告功能() {
    const deviceId = 生成设备ID();
    const body = JSON.stringify({ "uuid": deviceId });
    
    const randomDelay = Math.floor(Math.random() * 1000) + 1000;
    await new Promise(resolve => setTimeout(resolve, randomDelay));
    
    const requestHeaders = {
        ...rule.headers,
        "Content-Type": "application/json",
    };
    
    const response = await request(`${host}${rule.adUrl}`, {
        method: 'POST',
        headers: requestHeaders,
        body: JSON.stringify({ "data": 加密(body) }),
        timeout: 15000
    });
    
    const result = JSON.parse(response);
    
    if (result.code === 1) {
        console.log(`[广告处理] 成功观看广告`);
        return true;
    } else {
        return false;
    }
}

/**
 * 处理VIP功能
 */
async function 处理VIP功能() {
    const vipPlans = [
        { index: 2, days: 30, name: "30天VIP" },
        { index: 1, days: 7, name: "7天VIP" },
        { index: 0, days: 1, name: "1天VIP" }
    ];
    
    for (const plan of vipPlans) {
        console.log(`[VIP处理] 尝试购买 ${plan.name}`);
        
        const response = await request(`${host}${rule.vipUrl}`, {
            method: 'POST',
            headers: rule.headers,
            body: `index=${plan.index}`,
        });
        
        const vipResult = JSON.parse(response);
        
        if (vipResult.code === 1) {
            console.log(`[VIP处理] ${plan.name} 购买成功`);
            
            // 获取更新后的用户信息
            const userInfo = await 获取用户信息();
            if (userInfo && userInfo.user) {
                console.log(`[用户登录] 用户积分: ${userInfo.user.user_points || 0}`);
                console.log(`[用户登录] VIP状态: ${userInfo.user.vip_days > 0 ? 'VIP用户' : '普通用户'}`);
                if (userInfo.user.vip_days > 0) {
                    console.log(`[用户登录] VIP剩余天数: ${Math.floor(userInfo.user.vip_days)}天`);
                }
            }
            
            return true;
        } 
        
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    return false;
}

/**
 * 用户登录函数
 */
async function 用户登录() {
    console.log(`[用户登录] 尝试登录用户: ${rule.username}`);
    
    const passwordEncoded = encodeURIComponent(rule.password);
    const usernameEncoded = encodeURIComponent(rule.username);
    const formData = `password=${passwordEncoded}&user_name=${usernameEncoded}`;
    const loginUrl = `${host}${rule.loginUrl}?${formData}`;
    
    const response = await request(loginUrl);
    const jsonResponse = JSON.parse(response);
    
    if (jsonResponse.code === 1 && jsonResponse.data) {
        const userInfo = JSON.parse(解密(jsonResponse.data));
        const token = userInfo.user?.auth_token || '';
        
        if (token) {
            rule.headers['app-user-token'] = token;
            
            console.log(`[用户登录] 登录成功！`);
            console.log(`[用户登录] 配置标识: ${_name || '未知'}`);
            console.log(`[用户登录] 主机地址: ${host}`);
            console.log(`[用户登录] 用户积分: ${userInfo.user?.user_points || 0}`);
            console.log(`[用户登录] VIP状态: ${userInfo.user?.vip_days > 0 ? 'VIP用户' : '普通用户'}`);
            
            if (userInfo.user?.vip_days > 0) {
                console.log(`[用户登录] VIP剩余天数: ${Math.floor(userInfo.user.vip_days)}天`);
            }
            
            return true;
        } 
    } else {
        console.log(`[用户登录] 登录失败: ${jsonResponse.msg || '未知错误'}`);
        return false;
    }
    return false;
}

/**
 * 用户注册函数
 */
async function 用户注册() {
    const randomUsername = 生成随机账号();
    const randomPassword = 生成随机密码();
    
    console.log(`[用户注册] 生成账号: ${randomUsername}`);
    
    const registerData = {
        'password': randomPassword,
        'user_name': randomUsername,
        'code': '',
        'invite_code': 'akitqv',
        'is_emulator': 0
    };
    
    const encryptedData = 加密(JSON.stringify(registerData));
    const formData = `data=${encodeURIComponent(encryptedData)}`;
    
    const response = await request(`${host}${rule.registerUrl}`, {
        method: 'POST',
        headers: {
            ...rule.headers,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
    });
    
    const jsonResponse = JSON.parse(response);
    
    if (jsonResponse.code === 1) {
        rule.username = randomUsername;
        rule.password = randomPassword;
        
        // 打印注册成功的账号信息
        console.log('注册成功！');
        console.log('用户名:', randomUsername);
        console.log('密码:', randomPassword);
        console.log('请保存好账号信息，下次启动时可在配置中使用');
        
        return true;
    } else {
        console.log('注册失败:', jsonResponse.msg || '未知错误');
        return false;
    }
}

/**
 * 加密函数
 */
function 加密(word) {
    if (!rule.key || !word) return word;
    
    const key = CryptoJS.enc.Utf8.parse(rule.key);
    const iv = CryptoJS.enc.Utf8.parse(rule.iv);
    const srcs = CryptoJS.enc.Utf8.parse(word);
    
    const encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    
    return encrypted.toString(CryptoJS.enc.base64);
}

/**
 * 解密函数
 */
function 解密(word) {
    if (!rule.key || !word) return word;
    
    const key = CryptoJS.enc.Utf8.parse(rule.key);
    const iv = CryptoJS.enc.Utf8.parse(rule.iv);
    
    const decrypted = CryptoJS.AES.decrypt(word, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });

    return decrypted.toString(CryptoJS.enc.Utf8);
}

/**
 * 生成设备ID
 */
function 生成设备ID() {
    const randomBytes = CryptoJS.lib.WordArray.random(17);
    return randomBytes.toString(CryptoJS.enc.Hex).substring(0, 33);
}

/**
 * 验证搜索
 */
async function 验证搜索(body, maxAttempts = 3) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        const key = 生成UUID();
        
        const data = await request(`${host}${rule.searchUrl}`, {
            method: 'POST',
            headers: rule.headers,
            body: `${body}&key=${key}`,
            timeout: 5000
        });
        
        const json = JSON.parse(data);
        if (json.code === 1 && json.data) {
            return JSON.parse(解密(json.data)).search_list || [];
        }
    }
    
    return [];
}

/**
 * 生成UUID
 */
function 生成UUID() {
    const randomBytes = CryptoJS.lib.WordArray.random(16);
    const hexString = randomBytes.toString(CryptoJS.enc.Hex);
    
    return (
        hexString.substr(0, 8) + "-" +
        hexString.substr(8, 4) + "-" +
        "4" + hexString.substr(12, 3) + "-" +
        (parseInt(hexString.substr(16, 1), 16) & 0x3 | 0x8).toString(16) +
        hexString.substr(17, 3) + "-" +
        hexString.substr(20, 12)
    );
}

/**
 * 提取域名
 */
function 提取域名(url) {
    if (!url) return "";
    
    const cleanUrl = url.replace(/^(https?:\/\/)?/, '');
    const domainPart = cleanUrl.split('/')[0];
    
    if (domainPart.includes('-')) {
        return domainPart.split('-')[0];
    }
    
    if (domainPart.includes('.')) {
        const dotParts = domainPart.split('.');
        if (dotParts.length > 2) {
            return dotParts[dotParts.length - 2];
        } else if (dotParts.length === 2) {
            return dotParts[0];
        }
    }
    
    return domainPart;
}

/**
 * 生成随机账号
 */
function 生成随机账号() {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let username = '';
    const length = 8 + Math.floor(Math.random() * 4);
    
    for (let i = 0; i < length; i++) {
        username += chars[Math.floor(Math.random() * chars.length)];
    }
    return 'user' + username;
}

/**
 * 生成随机密码
 */
function 生成随机密码() {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let password = '';
    const length = 8 + Math.floor(Math.random() * 4);
    
    for (let i = 0; i < length; i++) {
        password += chars[Math.floor(Math.random() * chars.length)];
    }
    return password;
}

/**
 * 获取用户信息
 */
async function 获取用户信息() {
    const response = await request(`${host}${rule.userUrl}`, {
        method: 'POST',
        headers: rule.headers
    });
    
    const jsonData = JSON.parse(response);
    if (jsonData.data) {
        const decryptedData = 解密(jsonData.data);
        const userInfo = JSON.parse(decryptedData);
        return userInfo;
    }
    return null;
}

/**
 * 执行预处理循环
 */
async function 执行预处理循环() {
    const userInfo = await 获取用户信息();
    const userPoints = userInfo.user_points || 0;
    const remainWatchTimes = userInfo.remain_watch_times || 0;

    console.log(`[预处理循环] 用户积分: ${userPoints}, 可观看广告次数: ${remainWatchTimes}`);

    if (userPoints > 0) {
        console.log(`[预处理循环] 有积分 ${userPoints}，尝试购买VIP`);
        await 处理VIP功能();
    }
    
    if (remainWatchTimes > 0) {
        console.log(`[预处理循环] 开始处理广告，剩余 ${remainWatchTimes} 次`);
        let successCount = 0;
        
        for (let i = 0; i < remainWatchTimes; i++) {
            console.log(`[预处理循环] 处理第 ${i+1}/${remainWatchTimes} 次广告`);
            const adResult = await 处理广告功能();
            if (adResult) {
                successCount++;
            }
            
            if (i < remainWatchTimes - 1) {
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }
        
        console.log(`[预处理循环] 广告处理完成，成功 ${successCount}/${remainWatchTimes} 次`);
        
        if (successCount > 0) {
            console.log(`[预处理循环] 获取更新后的用户信息`);
            const updatedUserInfo = await 获取用户信息();
            if (updatedUserInfo && updatedUserInfo.user_points > 0) {
                console.log(`[预处理循环] 更新后积分: ${updatedUserInfo.user_points}，再次尝试购买VIP`);
                await 处理VIP功能();
            }
        }
    }
}

async function request(url, obj) {
    if (!obj) {
        obj = {
            headers: rule.headers,
        }
    }
    return (await req(url, obj)).content;
}

// 导出函数对象
export function __jsEvalReturn() {
    return {
        init: init,
        home: home,
        homeVod: homeVod,
        category: category,
        detail: detail,
        play: play,
        lazy: lazy,
        search: search
    };
}