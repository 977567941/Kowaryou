// 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
// 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import {_, Crypto} from 'assets://js/lib/cat.js';
let host = '', key = '', iv = '', ckkey = '', ckiv = '', appConfig = {}, headers = {'User-Agent': 'Dart/2.10 (dart:io)'};

async function init(cfg) {
    try {
        let ext = {};
        if (typeof cfg.ext === 'string') {
            ext = JSON.parse(cfg.ext.trim());
        } else if (typeof cfg.ext === 'object') {
            ext = cfg.ext;
        }
        host = ext.host;
        key = ext.key;
        iv = ext.iv;
        ckkey = ext.ckkey || 'ygcnbcrvaervztmw';
        ckiv = ext.ckiv || '1212164105143708';
        if (!host.startsWith('http')) return;
        if (!/^https?:\/\/[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(:\d+)?\/?$/.test(host)) {
            const res = await req(host, { headers: headers });
            host = res.content.trim();
        }
        host = host.replace(/\/$/, '');
        if (key.length !== 16 || iv.length !== 16) {
            host = '';
            return;
        }
        const md5Sign = md5X(key + iv).toString();
        const ckData = ck_encrypt(`${host}##5483##${Date.now()}##ckzmbc`);
        const payload = {
            "sign": md5Sign,
            "ck": ckData
        };
        let initHeaders = { ...headers, 'Content-Type': "application/json" };
        const configRes = await req(`${host}/get_config`, {
            method: 'POST',
            headers: initHeaders,
            data: payload
        });
        if (configRes.content) {
            const token = sk_decrypt(configRes.content);
            if (token) {
                headers['authorization'] = 'Bearer ' + token;
            }
        }
        const appConfigRes = await req(`${host}/app/config`, { headers: headers });
        const configStr = sk_decrypt(appConfigRes.content);
        const data = JSON.parse(configStr);
        if (data.direct_link) {
            let links = data.direct_link;
            if (typeof links === 'string') {
                appConfig['direct_link'] = links.includes('|') ? links.split('|') : [links];
            }
        }
        if (data.direct_json_link) {
            let links = data.direct_json_link;
            if (typeof links === 'string') {
                appConfig['direct_json_link'] = links.includes('|') ? links.split('|') : [links];
            }
        }
        if (data.app_trans_name && Array.isArray(data.app_trans_name)) {
            appConfig['app_trans_name'] = data.app_trans_name;
        }

    } catch (e) {
        console.log('Init failed:', e);
        host = '';
    }
}

async function home(filter) {
    if (!host) return null;
    const res = await req(`${host}/sk-api/type/list`, { headers: headers });
    const decrypted = sk_decrypt(res.content);
    const data = JSON.parse(decrypted).data;
    let classes = [];
    if (data && Array.isArray(data)) {
        data.forEach(i => {
            if (_.isPlainObject(i)) {
                classes.push({type_id: i.type_id, type_name: i.type_name});
            }
        });
    }
    const filters = {};
    const tasks = classes.map(async (cls) => {
        const tid = cls.type_id;
        try {
            const fRes = await req(`${host}/sk-api/type/alltypeextend?typeId=${tid}`, { headers: headers });
            const fDecrypted = sk_decrypt(fRes.content);
            const fJson = JSON.parse(fDecrypted);
            if (fJson.code === 200 && fJson.data) {
                const fData = fJson.data;
                const typeFilters = [];
                const keys = ['class', 'area', 'lang', 'year'];
                const names = {'class': '类型', 'area': '地区', 'lang': '语言', 'year': '年份'};
                keys.forEach(k => {
                    if (fData[k]) {
                        const options = fData[k].split(',').filter(s => s && s.trim());
                        if (options.length > 0) {
                            const values = [{ n: '全部', v: '' }];
                            options.forEach(opt => { values.push({ n: opt, v: opt }); });
                            let paramKey = k;
                            if (k === 'class') paramKey = 'extendtype';
                            typeFilters.push({
                                key: paramKey,
                                name: names[k],
                                init: '',
                                value: values
                            });
                        }
                    }
                });
                typeFilters.push({
                    key: 'sort',
                    name: '排序',
                    init: 'updateTime',
                    value: [
                        { n: '最新', v: 'updateTime' },
                        { n: '人气', v: 'hot' },
                        { n: '评分', v: 'score' }
                    ]
                });
                if (typeFilters.length > 0) {
                    filters[tid] = typeFilters;
                }
            }
        } catch (e) {}
    });
    await Promise.all(tasks);
    return JSON.stringify({ class: classes, filters: filters });
}

async function homeVod() {
    const url = `${host}/sk-api/vod/list?page=1&limit=12&type=randomlikeindex&area=&lang=&year=&mtype=`;
    const res = await req(url, { headers: headers });
    const decrypted = sk_decrypt(res.content);
    const data = JSON.parse(decrypted).data;
    return JSON.stringify({ list: data });
}

async function category(tid, pg, filter, extend) {
    const sort = extend.sort || 'updateTime';
    const area = extend.area || '';
    const lang = extend.lang || '';
    const year = extend.year || '';
    const extendtype = extend.extendtype || '';
    const url = `${host}/sk-api/vod/list?typeId=${tid}&page=${pg}&limit=18&type=${sort}&area=${encodeURIComponent(area)}&lang=${encodeURIComponent(lang)}&year=${year}&mtype=&extendtype=${encodeURIComponent(extendtype)}`;
    const res = await req(url, { headers: headers });
    const decrypted = sk_decrypt(res.content);
    const data = JSON.parse(decrypted).data;
    return JSON.stringify({list: data, page: parseInt(pg)});
}

async function search(wd, quick, pg=1) {
    const url = `${host}/sk-api/search/pages?keyword=${encodeURIComponent(wd)}&page=${pg}&limit=10&typeId=-1`;
    const res = await req(url, { headers: headers });
    const decrypted = sk_decrypt(res.content);
    const data = JSON.parse(decrypted).data;
    return JSON.stringify({ list: data, page: parseInt(pg) });
}

async function detail(id) {
    const url = `${host}/sk-api/vod/one?vodId=${id}`;
    const res = await req(url, { headers: headers });
    const decrypted = sk_decrypt(res.content);
    const data = JSON.parse(decrypted).data;
    return JSON.stringify({ list: [data] });
}

async function play(flag, id, flags) {
    let jx = 0, url = '', direct_link = 0, direct_json = 0;
    const direct_json_links = appConfig['direct_json_link'] || [];
    const direct_links = appConfig['direct_link'] || [];
    for (const link of direct_json_links) {
        if (id.includes(link)) {
            direct_json = 1;
            break;
        }
    }
    for (const link of direct_links) {
        if (id.includes(link) && link.startsWith('http')) {
            direct_link = 1;
            break;
        }
    }
    if (direct_json || !direct_link || !id.startsWith('http')) {
        try {
            const apiUrl = `${host}/sk-api/vod/skjson?url=${id}&skjsonindex=0`;
            const res = await req(apiUrl, { headers: headers });
            const decrypted = sk_decrypt(res.content);
            const data = JSON.parse(decrypted).data;
            const play_url = data.url;
            if (play_url && play_url.startsWith('http')) {
                url = play_url;
            }
        } catch (e) {}
    }
    if (!url) {
        url = id;
        if (/(?:www\.iqiyi|v\.qq|v\.youku|www\.mgtv|www\.bilibili)\.com/.test(id)) {
            jx = 1;
        }
    }
    return JSON.stringify({ jx: jx, parse: 0, url: url, header: {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}});
}

function ck_encrypt(str) {
    let b64_1 = Crypto.enc.Base64.stringify(Crypto.enc.Utf8.parse(str));
    let b64_2 = Crypto.enc.Base64.stringify(Crypto.enc.Utf8.parse(b64_1));
    let keyHex = Crypto.enc.Utf8.parse(ckkey);
    let ivHex = Crypto.enc.Utf8.parse(ckiv);
    let encrypted = Crypto.AES.encrypt(b64_2, keyHex, {
        iv: ivHex,
        mode: Crypto.mode.CBC,
        padding: Crypto.pad.Pkcs7
    });
    let hex_encoded = encrypted.ciphertext.toString(Crypto.enc.Hex);
    return Crypto.enc.Base64.stringify(Crypto.enc.Utf8.parse(hex_encoded));
}

function sk_decrypt(data) {
    const prefix = 'FROMSKZZJM';
    if (data.startsWith(prefix)) {
        try {
            let encryptedHexStr = data.substring(prefix.length);
            let keyHex = Crypto.enc.Utf8.parse(key);
            let ivHex = Crypto.enc.Utf8.parse(iv);
            let encryptedBase64 = Crypto.enc.Base64.stringify(Crypto.enc.Hex.parse(encryptedHexStr));
            let decrypted = Crypto.AES.decrypt(encryptedBase64, keyHex, {
                iv: ivHex,
                mode: Crypto.mode.CBC,
                padding: Crypto.pad.Pkcs7
            });
            return decrypted.toString(Crypto.enc.Utf8);
        } catch (e) {
            return null;
        }
    } else {
        return data;
    }
}

export function __jsEvalReturn() {
    return {
        init: init,
        home: home,
        homeVod: homeVod,
        category: category,
        detail: detail,
        play: play,
        search: search
    };
}