import time
from DrissionPage import WebPage
from DrissionPage.common import Actions


# 开启浏览器（必须使用Chrome浏览器）
wp = WebPage()
ac = Actions(wp)
wp.ele('xpath://div[@class="search-icon"]').click()
info = []
# wp.get('https://www.xiaohongshu.com/')
wp.listen.start(['web/v1/search/notes', 'api/sns/web/v1/feed'])

for page in range(10):
    packet = wp.listen.wait()
    print(packet.response.body)
    for i in range(0, len(wp.eles('xpath://a[@class="cover ld mask"]'))):
        temp = wp.eles('xpath://a[@class="cover ld mask"]')[i]
        if temp.attr('href') not in info:
            info.append(temp.attr('href'))
            temp.click()
            pack = wp.listen.wait()
            print(pack.response.body)
            wp.ele('xpath://div[@class="close close-mask-dark"]').click()
            time.sleep(1)