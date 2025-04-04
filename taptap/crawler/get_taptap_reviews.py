from DrissionPage import ChromiumPage, ChromiumOptions
import time
import csv
import re
from datetime import datetime
import random
import json

# 配置参数
TARGET_APP_ID = '224267'
CSV_HEADERS = [
    'review_id', 'score', 'device', 'spent', 'played_spent',
    'ups', 'downs', 'funnies', 'comments_count', 'created_time',
    'updated_time', 'content_text', 'author_id', 'author_name',
    'app_id', 'app_identifier', 'app_title'
]

# 浏览器配置增强
co = ChromiumOptions()
co.no_imgs(True)
co.no_js(False)  # 部分动态加载需要JS支持
co.set_timeouts(30, 30, 30)
co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
co.set_paths(browser_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')

# 初始化页面对象
page = ChromiumPage(addr_or_opts=co)
page.set.load_mode.none()

# 监听多个可能的API端点（修正正则表达式）
# page.listen.start(r'https://www\.taptap\.cn/webapiv2/review/(v1/detail|v2/list|v2/list-by-app\?)')
page.listen.start('https://www.taptap.cn/webapiv2/review/v2/list-by-app?')

# 访问目标页面
page.get(f'https://www.taptap.cn/app/{TARGET_APP_ID}/review')
time.sleep(8)  # 延长初始加载等待时间

# CSV文件初始化
with open(f'taptap_reviews_{TARGET_APP_ID}.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(CSV_HEADERS)
    
    comments_buffer = []
    total_comments = 0
    retry_count = 0
    max_retries = 5

    try:
        while retry_count < max_retries:
            # 渐进式滚动（优化滚动策略）
            for _ in range(random.randint(3, 5)):
                page.scroll.down(random.randint(700, 1200))
                time.sleep(random.uniform(1.5, 2.8))
                page.scroll.up(200)  # 模拟真实用户回滚行为
                time.sleep(random.uniform(0.5, 1.2))
            
            # 获取数据包（使用正确参数）
            packet = page.listen.wait(timeout=15)
            
            if packet is not None:
                print('-' * 50)
                print(f"捕获到有效请求: {packet.request.url}")
                print(f"状态码: {packet.response.status_code}")
                
                try:
                    # 解析JSON响应
                    response = json.loads(packet.response.body)
                    
                    # 处理不同API版本的数据结构
                    if 'v2/list' in packet.request.url:
                        data_key = 'list'
                    elif 'v1/detail' in packet.request.url:
                        data_key = 'data'
                    else:
                        print("未知API端点，跳过处理")
                        continue
                        
                    reviews = response.get('data', {}).get(data_key, [])
                    
                    if not reviews:
                        print("未获取到评论数据，可能到达页面底部")
                        retry_count += 1
                        continue
                        
                    # 处理评论数据
                    for review in reviews:
                        try:
                            # 数据清洗
                            device = review.get('device') or review.get('reply_control', {}).get('device', '')
                            
                            row = [
                                review['id'],
                                review['score'],
                                device,
                                review.get('spent', 0),
                                review.get('played_spent', 0),
                                review['ups'],
                                review['downs'],
                                review['funnies'],
                                review['comments'],
                                datetime.fromtimestamp(review['created_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                datetime.fromtimestamp(review['updated_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                review.get('contents', {}).get('text', '').replace('\u003cbr /\u003e', '\n'),
                                review.get('author', {}).get('id'),
                                review.get('author', {}).get('name'),
                                review.get('app', {}).get('id'),
                                review.get('app', {}).get('identifier'),
                                review.get('app', {}).get('title')
                            ]
                            comments_buffer.append(row)
                            total_comments += 1
                        except KeyError as e:
                            print(f"数据字段缺失: {str(e)}")
                            continue
                            
                    # 批量写入
                    if comments_buffer:
                        writer.writerows(comments_buffer)
                        csvfile.flush()
                        print(f"成功写入 {len(comments_buffer)} 条评论")
                        comments_buffer.clear()
                        retry_count = 0  # 重置重试计数器
                        
                except json.JSONDecodeError:
                    print("响应不是有效的JSON格式")
                except Exception as e:
                    print(f"数据处理异常: {str(e)}")
            else:
                print("未捕获到新数据包，重试计数:", retry_count)
                retry_count += 1
                time.sleep(3)
                
    except Exception as e:
        print(f"主流程异常: {str(e)}")
    finally:
        # 安全关闭浏览器
        try:
            page.quit()
        except Exception as e:
            print(f"关闭浏览器异常: {str(e)}")
        
        # 写入剩余数据
        if comments_buffer:
            writer.writerows(comments_buffer)
        print(f"采集完成，总计评论数：{total_comments}")