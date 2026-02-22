// 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
// 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

import { load , Crypto} from 'assets://js/lib/cat.js';
let siteUrl = 'https://www.cupfox.ai';
const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'Referer': siteUrl + '/'
};

async function init(cfg) {
    try {
        if (cfg.ext) {
            siteUrl = cfg.ext;
        }
    } catch (e) {}
}

async function home(filter) {
    let classes = [];
    try {
        const res = await req(siteUrl, { headers: headers });
        const $ = load(res.content);
        $('nav.bm-item-list a').each((index, element) => {
            const $a = $(element);
            const name = $a.text().trim();
            const href = $a.attr('href');
            const match = href.match(/\/type\/(\d+)\.html/);
            if (match && match[1]) {
                classes.push({ type_id: match[1], type_name: name
                });
            }
        });
    } catch (e) {}
    return JSON.stringify({class: classes, filters: {}});
}

async function homeVod() {
    try {
        const res = await req(siteUrl, { headers: headers });
        const $ = load(res.content);
        const list = [];
        const distinct = {};
        $('.mobile-main .panel').each((i, panel) => {
            const $panel = $(panel);
            const $validTab = $panel.find('.tab-content').first();
            $validTab.find('.movie-list-item').each((_, element) => {
                const $item = $(element);
                const $a = $item.find('a').first();
                const $img = $item.find('.Lazy');
                const $note = $item.find('.movie-item-note');
                const $score = $item.find('.movie-item-score');
                const name = $a.attr('title');
                const url = $a.attr('href');
                let pic = $img.attr('data-original');
                if (pic && !pic.startsWith('http')) {
                    pic = siteUrl + pic;
                }
                let remarks = $note.text().trim();
                if (!remarks) {
                    remarks = $score.text().trim();
                }
                if (name && url && !distinct[url]) {
                    distinct[url] = 1;
                    list.push({
                        vod_id: url,
                        vod_name: name,
                        vod_pic: pic,
                        vod_remarks: remarks
                    });
                }
            });
        });
        return JSON.stringify({ list: list });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

async function category(tid, pg, filter, extend) {
    try {
        const url = `${siteUrl}/type/${tid}-${pg}.html`;
        const res = await req(url, { headers: headers });
        const $ = load(res.content);
        const list = parseList($);
        return JSON.stringify({ page: parseInt(pg), pagecount: 999,  list: list });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

async function search(wd, quick, pg) {
    try {
        let page = pg || 1;
        const url = `${siteUrl}/search/${encodeURIComponent(wd)}----------${page}---.html`;
        const res = await req(url, { headers: headers });
        const $ = load(res.content);
        const list = [];
        $('.vod-search-list .box').each((i, el) => {
            const $item = $(el);
            const $link = $item.find('a.cover-link');
            const $img = $item.find('.Lazy');
            const name = $item.find('.movie-title').text().trim();
            const id = $link.attr('href');
            let pic = $img.attr('data-original');
            if (pic && !pic.startsWith('http')) {
                pic = siteUrl + pic;
            }
            let remarks = $item.find('.movie-item-note').text().trim();
            if (!remarks) {
                remarks = $item.find('.meta.getop').text().trim();
            }
            if (name && id) {
                list.push({
                    vod_id: id,
                    vod_name: name,
                    vod_pic: pic,
                    vod_remarks: remarks
                });
            }
        });
        return JSON.stringify({page: parseInt(page), list: list});
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

async function detail(id) {
    try {
        const url = siteUrl + id;
        const res = await req(url, { headers: headers });
        const $ = load(res.content);
        const vod = {
            vod_id: id,
            vod_name: $('h1.movie-title').text().trim(),
            vod_pic: $('.poster img').attr('src'),
            vod_content: $('.summary.detailsTxt').clone().find('.ectogg').remove().end().text().trim(),
        };
        if (vod.vod_pic && !vod.vod_pic.startsWith('http')) {
            vod.vod_pic = siteUrl + vod.vod_pic;
        }
        $('.scroll-content a').each((i, el) => {
            const text = $(el).text().trim();
            if (/^\d{4}$/.test(text)) {
                vod.vod_year = text;
            }
        });
        $('.info-data').each((i, el) => {
            const text = $(el).text();
            if (text.includes('导演')) {
                vod.vod_director = $(el).find('a').map((_, a) => $(a).text()).get().join(',');
            } else if (text.includes('演员')) {
                vod.vod_actor = $(el).find('a').map((_, a) => $(a).text()).get().join(',');
            }
        });
        let playFrom = [];
        let playUrl = [];
        $('.play_source_tab .swiper-slide').each((i, el) => {
            let name = $(el).clone().children().remove().end().text().trim();
            playFrom.push(name);
        });
        $('.play_list_box').each((i, el) => {
            let urls = [];
            $(el).find('.content_playlist li a').each((j, item) => {
                let name = $(item).text().trim();
                let link = $(item).attr('href');
                urls.push(name + '$' + link);
            });
            playUrl.push(urls.join('#'));
        });
        vod.vod_play_from = playFrom.join('$$$');
        vod.vod_play_url = playUrl.join('$$$');
        return JSON.stringify({ list: [vod] });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

async function play(flag, id, flags) {
    try {
        const url = siteUrl + id;
        const res = await req(url, { headers: headers });
        const $ = load(res.content);
        let vid = '';
        const scripts = $('.player-height script');
        for (let i = 0; i < scripts.length; i++) {
            let scriptContent = $(scripts[i]).html();
            if (scriptContent && scriptContent.includes('player_aaaa')) {
                const start = scriptContent.indexOf('{');
                const end = scriptContent.lastIndexOf('}');
                if (start > -1 && end > start) {
                    const jsonStr = scriptContent.substring(start, end + 1);
                    try {
                        const playerData = JSON.parse(jsonStr);
                        if (playerData && playerData.url) {
                            vid = playerData.url;
                            break;
                        }
                    } catch (e) {}
                }
            }
        }
        if (!vid) {
            return JSON.stringify({ parse: 0, url: '' });
        }
        if (typeof getProxy !== 'function'){vid = encodeURIComponent(vid);}
        const apiRes = await req(`${siteUrl}/foxplay/api.php`, {
            method: 'post',
            headers: {
                'User-Agent': headers['User-Agent'],
                'Referer': `${siteUrl}/foxplay/muiplayer.php?vid=${vid}`,
                'Origin': siteUrl,
                'X-Requested-With': 'XMLHttpRequest'
            },
            data: { vid: vid },
            postType: 'form'
        });
        const json = JSON.parse(apiRes.content);
        if (json.code === 200 && json.data) {
            const encryptedUrl = json.data.url;
            const urlMode = json.data.urlmode;
            let realUrl = encryptedUrl;
            if (urlMode === 1) {
                realUrl = Decode1.sign(encryptedUrl);
            } else if (urlMode === 2) {
                realUrl = decode2(encryptedUrl);
            }
            return JSON.stringify({ parse: 0, url: realUrl, header: { 'User-Agent': headers['User-Agent'] } });
        }
        return JSON.stringify({ parse: 0, url: '' });
    } catch (e) {
        return JSON.stringify({ parse: 0, url: '' });
    }
}

function parseList($) {
    const list = [];
    $('.movie-list-item').each((_, element) => {
        const $item = $(element);
        const $a = $item.find('a').first();
        const $img = $item.find('.Lazy');
        const $note = $item.find('.movie-item-note');
        const $score = $item.find('.movie-item-score');
        const name = $a.attr('title');
        const url = $a.attr('href');
        let pic = $img.attr('data-original');
        if (pic && !pic.startsWith('http')) {
            pic = siteUrl + pic;
        }
        let remarks = $note.text().trim();
        if (!remarks) {
            remarks = $score.text().trim();
        }
        if (name && url) {
            list.push({
                vod_id: url,
                vod_name: name,
                vod_pic: pic,
                vod_remarks: remarks
            });
        }
    });
    return list;
}

function base64Decode(str) {
    const safeStr = str.replace(/[\r\n]/g, "");
    const words = Crypto.enc.Base64.parse(safeStr);
    return Crypto.enc.Utf8.stringify(words);
}

const Decode1 = {
    sign(encodedStr) {
        try {
            const decodedRaw = this.customStrDecode(encodedStr);
            const parts = decodedRaw.split("/");
            const mapStrB = parts[0];
            const mapStrA = parts[1];
            const path = parts.slice(2).join("/");
            const cipherMap = JSON.parse(base64Decode(mapStrA));
            const plainMap = JSON.parse(base64Decode(mapStrB));
            const decodedPath = base64Decode(path);
            return this.deString(cipherMap, plainMap, decodedPath);
        } catch (e) {
            return "";
        }
    },
    customStrDecode(str) {
        const firstDecode = base64Decode(str);
        const key = md5X('test');
        const len = key.length;
        let code = "";
        for (let i = 0; i < firstDecode.length; i++) {
            const k = i % len;
            code += String.fromCharCode(firstDecode.charCodeAt(i) ^ key.charCodeAt(k));
        }
        return base64Decode(code);
    },
    deString(cipherList, plainList, text) {
        let result = "";
        for (let i = 0; i < text.length; i++) {
            const char = text[i];
            const isAlpha = /^[a-zA-Z]+$/.test(char);
            if (isAlpha && plainList.includes(char)) {
                const index = cipherList.indexOf(char);
                if (index !== -1 && plainList[index]) {
                    result += plainList[index];
                } else {
                    result += char;
                }
            } else {
                result += char;
            }
        }
        return result;
    }
};

function decode2(encoded) {
    if (!encoded) return '';
    const dictStr = 'PXhw7UT1B0a9kQDKZsjIASmOezxYG4CHo5Jyfg2b8FLpEvRr3WtVnlqMidu6cN';
    const dictLen = dictStr.length;
    const lookup = {};
    for (let i = 0; i < dictLen; i++) {
        lookup[dictStr[i]] = dictStr[(i + 59) % dictLen];
    }
    const raw = base64Decode(encoded);
    let res = "";
    for (let i = 1; i < raw.length; i += 3) {
        const char = raw[i];
        res += (lookup[char] || char);
    }
    return res;
}

export function __jsEvalReturn() {
    return {
        init: init,
        home: home,
        homeVod: homeVod,
        category: category,
        search: search,
        detail: detail,
        play: play
    };
}
