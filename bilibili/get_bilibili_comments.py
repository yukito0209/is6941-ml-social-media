"""爬取教程: BV1K9Hse8EwM"""
import json
import requests
import csv
import hashlib
import time
from urllib.parse import quote


def get_w_rid(wts, next_page):
    # 进行编码处理
    pagination_str = quote(next_page)
    """w_rid加密参数"""
    l = [
        "mode=3",
        "oid=114122112894260",
        f"pagination_str={pagination_str}",
        "plat=1",
        "type=1",
        "web_location=1315875",
        f"wts={wts}",
    ]
    y = '&'.join(l)
    string = y + "ea1db124af3c7062474693fa704f4ff8"
    MD5 = hashlib.md5()
    MD5.update(string.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid


def get_content(offset):
    """发送请求"""
    # 模拟浏览器
    headers = {
        # cookie 用户信息，常用于检测是否有登录账号
        "cookie":"buvid3=76550049-7B82-1351-870E-2A105ECA321786255infoc; b_nut=1725417186; _uuid=A3CAC957-B12F-9CC5-AD35-F64485FBC15786793infoc; buvid_fp=4235616ab8b322cee0e65cda370d8b34; enable_web_push=DISABLE; buvid4=F03F1FB6-4814-9659-C35E-AD0B5DEDB9DD89399-024090402-CbRgJ8QwFMXqgF38lY3bEA%3D%3D; rpdid=|(~k|)lulu~0J'u~klRu~kJJ; header_theme_version=CLOSE; hit-dyn-v2=1; LIVE_BUVID=AUTO7517254458155360; CURRENT_BLACKGAP=0; DedeUserID=13845177; DedeUserID__ckMd5=714fb4a37a578788; CURRENT_QUALITY=120; match_float_version=ENABLE; is-2022-channel=1; go-back-dyn=0; enable_feed_channel=ENABLE; share_source_origin=WEIXIN; fingerprint=a803961d0a51b8d12fe2190505f5847f; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIxMDA3MTIsImlhdCI6MTc0MTg0MTQ1MiwicGx0IjotMX0.Q2Vsm2d8SOXK24Xkkv88qveLPkUh4PfDvWgUnhAAGLk; bili_ticket_expires=1742100652; bsource=search_bing; SESSDATA=76c4b5c5%2C1757479660%2Cba870%2A32CjBeUI3WQ0WXpPP-DKrdmAdzMeFOvBfwNdAd2yrAP4VFdM8JAuVLgH7d6-_9gFgmhdISVmtjajNZOHNZaWtGcE5DLTRHUDIyUWRmbHVFbnpLSUFENjhaX1V4Z3Q2MjRJOXo1Tlphdnp1cWJJYUxrNWFNak04cWFXbWcwdTZSUjR3MXhGVDk1TV9nIIEC; bili_jct=d4065519616409a73277e7e41ab0a0ca; sid=8502w2b3; home_feed_column=5; browser_resolution=2560-1317; PVID=3; b_lsid=59EF7A3E_1959B2E7C29; bp_t_offset_13845177=1044663194599030784; CURRENT_FNVAL=4048",
        # user-agent 用户代理，表示浏览器的基本身份信息
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
    }
    # 请求网址
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    pagination_str = '{"offset": %s}'% offset
    # 获取当前时间戳
    wts = int(time.time())
    # 获取加密参数
    w_rid = get_w_rid(wts=wts, next_page=pagination_str)
    # 查询参数
    data = {
        'oid': '114122112894260',
        'type': '1',
        'mode': '3',
        'pagination_str': pagination_str,
        'plat': '1',
        'web_location': '1315875',
        'w_rid': w_rid,
        'wts': wts,
    }
    # 发送请求
    response = requests.get(url=url, params=data, headers=headers)

    """获取数据"""
    # 获取响应的json数据
    json_data = response.json()

    """解析数据"""
    # 字典取值，提取评论信息所在的replies列表
    replies = json_data['data']['replies']
    # for循环遍历，提取列表中的元素
    for index in replies:
        # 提取具体的评论区内容
        dict = {
            '昵称': index['member']['uname'],
            '性别': index['member']['sex'],
            '地区': index['reply_control']['location'].replace('IP属地：', ''),
            '评论': index['content']['message']
        }
        print(dict)
        """保存数据"""
        csv_writer.writerow(dict)
    # 获取下一页请求参数
    next_page = json_data['data']['cursor']['pagination_reply']['next_offset']
    next_offset = json.dumps(next_page)
    return next_offset


if __name__ == '__main__':
    # 创建CSV文件
    f = open(file='bilibili\\test_comments_data.csv', mode='w', encoding='utf-8-sig', newline='')
    # 字典写入方法
    csv_writer = csv.DictWriter(f, fieldnames=['昵称', '性别', '地区', '评论'])
    # 写入表头
    csv_writer.writeheader()
    offset = '""'
    for page in range(1, 21):
        offset = get_content(offset=offset)