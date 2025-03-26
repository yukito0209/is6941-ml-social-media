from DrissionPage import ChromiumPage, ChromiumOptions
import time
import csv
import re

URL = input("请输入B站视频链接:")
num = int(input("请输入要爬取的页面次数:"))

# 从URL中提取BV号
bv_match = re.search(r'BV[0-9a-zA-Z]{10}', URL)
if not bv_match:
    raise ValueError("未检测到有效的BV号，请确认输入的是完整视频链接。")
bv_number = bv_match.group()

co = ChromiumOptions()
# 优化配置项
co.no_imgs(True)  # 禁用图片加载
co.no_js(True)  # 禁用JavaScript
co.set_timeouts(30)
# 创建页面对象时应用配置
page = ChromiumPage(addr_or_opts=co)
page.set.load_mode.none()

# 监听特定的网络流
page.listen.start('https://api.bilibili.com/x/v2/reply/wbi/main?')

# 访问B站页面
page.get(f'{URL}')
time.sleep(3)

# 创建CSV文件并写入标题
with open(f'bilibili\{bv_number}_comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['用户名', '性别', 'IP地址', '评论内容'])
    
    comments_buffer = []  # 批量写入缓冲区
    total_comments = 0
    empty_count = 0       # 连续空响应计数器
    
    try:
        # 修改为动态循环
        for _ in range(num):
            # 滚动加载
            page.scroll.to_bottom()
            time.sleep(1.5)
            
            # 获取响应包
            packet = page.listen.wait(timeout=10)
            if not packet:
                empty_count += 1
                if empty_count >= 10:  # 连续10次无数据则退出
                    print("连续10次未获取到新数据，提前终止")
                    break
                continue
            
            response = packet.response.body
            if not response or not isinstance(response, dict):
                print(f"收到无效响应: {type(response)}")
                continue
                
            if 'data' not in response:
                continue
                
            datas = response['data'].get('replies', [])
            if not datas:
                empty_count += 1
                if empty_count >= 10:
                    print("连续10次空数据，提前终止")
                    break
                continue
                
            empty_count = 0  # 重置计数器
            
            # 处理评论数据
            for data in datas:
                try:
                    comment = [
                        data['member'].get('uname', '匿名用户'),
                        data['member'].get('sex', '未知'),
                        data['reply_control'].get('location', '未知IP').replace('IP属地：', ''),
                        data['content'].get('message', '无内容')
                    ]
                    comments_buffer.append(comment)
                    total_comments += 1
                except KeyError as e:
                    print(f"跳过异常数据：{str(e)}")
                
                # 批量写入（每100条）
                if len(comments_buffer) >= 100:
                    writer.writerows(comments_buffer)
                    csvfile.flush()  # 确保数据写入磁盘
                    comments_buffer.clear()
                    print(f"已写入 {total_comments} 条评论")
            
            # 停止加载后续内容
            page.stop_loading()
            time.sleep(0.5)
            
        # 写入剩余数据
        if comments_buffer:
            writer.writerows(comments_buffer)
            print(f"最后写入 {len(comments_buffer)} 条评论")
            
    except Exception as e:
        print(f"发生错误：{e}")
    finally:  # 确保最终执行写入
        # 最终写入剩余数据
        if comments_buffer:
            writer.writerows(comments_buffer)
            print(f'最终补充写入 {len(comments_buffer)} 条评论')
            csvfile.flush()  # 强制刷新缓冲区
        print(f"最终爬取数量: {total_comments}")

page.close()


# from DrissionPage import ChromiumPage, ChromiumOptions
# import time
# import csv
# import re
# import random

# URL = input("请输入B站视频链接:")
# TARGET_COMMENTS = 17031  # 目标评论数

# # 从URL中提取BV号
# bv_match = re.search(r'BV[0-9a-zA-Z]{10}', URL)
# if not bv_match:
#     raise ValueError("未检测到有效的BV号，请确认输入的是完整视频链接。")
# bv_number = bv_match.group()

# # ------------------ 浏览器配置优化 ------------------
# co = ChromiumOptions()
# # 优化配置项
# co.no_imgs(True)  # 禁用图片加载
# co.no_js(True)  # 禁用JavaScript
# co.set_timeouts(30)
# # 创建页面对象时应用配置
# page = ChromiumPage(addr_or_opts=co)
# page.set.load_mode.none()

# # ------------------ 网络监听配置 ------------------
# page.listen.start('https://api.bilibili.com/x/v2/reply/wbi/main?')

# # 访问B站页面
# page.get(f'{URL}')
# time.sleep(3)  # 增加初始加载等待时间

# # 创建CSV文件
# with open(f'bilibili\{bv_number}_comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['用户名', '性别', 'IP地址', '评论内容'])
    
#     comments_buffer = []  # 批量写入缓冲区
#     total_comments = 0
#     retry_count = 0
#     max_retries = 5  # 最大重试次数
    
#     try:
#         # 动态滚动加载（改为基于数量判断）
#         while total_comments < TARGET_COMMENTS and retry_count < max_retries:
#             # 滚动加载并等待（增加滚动幅度）
#             page.scroll.down(800)  # 增大滚动幅度
#             time.sleep(random.uniform(1.2, 2.5))  # 随机延时
            
#             # 获取响应包（增加等待时间）
#             packet = page.listen.wait(timeout=15)
            
#             if not packet:
#                 retry_count += 1
#                 print(f"第 {retry_count} 次重试...")
#                 # 尝试强制加载更多
#                 page.scroll.to_bottom()
#                 time.sleep(2)
#                 continue
                
#             retry_count = 0  # 重置重试计数器
            
#             # 处理响应数据
#             response = packet.response.body
#             if 'data' not in response:
#                 continue
                
#             datas = response['data'].get('replies', [])
#             if not datas:
#                 print("检测到空数据包，可能到达底部")
#                 break
                
#             # 处理评论数据
#             for data in datas:
#                 try:
#                     comment = [
#                         data['member'].get('uname', '匿名用户'),
#                         data['member'].get('sex', '未知'),
#                         data['reply_control'].get('location', '未知IP'),
#                         data['content'].get('message', '无内容')
#                     ]
#                     comments_buffer.append(comment)
#                     total_comments += 1
#                 except KeyError as e:
#                     print(f"跳过异常数据：{str(e)}")
                
#                 # 批量写入（增大到500条/次）
#                 if len(comments_buffer) >= 500:
#                     writer.writerows(comments_buffer)
#                     csvfile.flush()
#                     comments_buffer.clear()
#                     print(f"已写入 {total_comments}/{TARGET_COMMENTS} 条评论")
            
#             # 动态调整加载频率
#             if total_comments % 2000 == 0:
#                 time.sleep(5)  # 每2000条增加等待时间
#                 page.scroll.to_bottom()  # 强制滚动到底部
                
#             # 停止加载后续内容（降低频率）
#             if random.random() < 0.3:  # 30%概率停止加载
#                 page.stop_loading()
            
#         # 写入剩余数据
#         if comments_buffer:
#             writer.writerows(comments_buffer)
            
#     except Exception as e:
#         print(f"发生错误：{str(e)}")
#     finally:
#         print(f"最终爬取数量: {total_comments}")

# page.close()