"""春日影 (MyGO!!!!! ver.) 评论区采集"""
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Edge()
driver.get('https://music.163.com/#/song?id=2097486090')
# 切换到嵌套网页中
driver.switch_to.frame(0)

# 要抓几页就循环几次
for page in range(10):
    time.sleep(2)
    # 下拉页面到页面底部
    js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight'
    driver.execute_script(js)
    # css选择器，根据标签属性提取内容 --> []表示没有提取到元素
    list = driver.find_elements(By.CSS_SELECTOR, '.itm') # --> 返回对象
    for li in list:
        content = li.find_element(By.CSS_SELECTOR, '.cnt').text
        new_content = re.findall('：(.*)', content)[0]
        print(new_content)
        with open('cloud_music\\Haruhikage.txt', mode='a', encoding='utf-8') as f:
            f.write(new_content)
            f.write('\n')
    driver.find_element(By.CSS_SELECTOR, '.znxt').click()