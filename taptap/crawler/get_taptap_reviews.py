import requests
import csv
import time
import random
from datetime import datetime

app_id = 221561 # 游戏ID
output_file = "maple_story_m.csv" # 保存的CSV表名
total_required = 1000  # 需要爬取的评论总数
per_page = 10  # 每页评论数量

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": f"https://www.taptap.cn/app/{app_id}/review",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "X-UA": "V=1&PN=WebApp&LANG=zh_CN&VN_CODE=102&LOC=CN&PLT=PC&DS=Android&UID=54fa6ab5-f962-4201-b631-57afcca4e8dc&OS=Windows&OSV=10&DT=PC",
    "Connection": "keep-alive"
}

def fetch_reviews():
    collected = 0
    page = 1
    session = requests.Session()
    
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "用户ID", "用户名", "评分", "评论内容", 
            "点赞数", "发布时间", "设备型号"
        ])

        while collected < total_required:
            current_ts = int(time.time() * 1000)
            
            params = {
                "app_id": app_id,
                "sort": "new", # 评论排序方式 hot/new
                "from": (page - 1) * per_page + 1,
                "limit": per_page,
                "stage_type": 2,
                "X-UA": headers["X-UA"],
                "_ts": current_ts,
                "session_id": "221d8b7a-dfb9-411f-9006-7a26aadac1b1"
            }

            try:
                time.sleep(random.uniform(2, 4))
                
                response = session.get(
                    "https://www.taptap.cn/webapiv2/review/v2/list-by-app",
                    params=params,
                    headers=headers,
                    timeout=15
                )
                
                print(f"请求参数：{params}")
                print(f"响应状态码：{response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except Exception as e:
                        print(f"JSON解析失败：{str(e)}")
                        print(f"响应内容：{response.text[:200]}")
                        break

                    items = data.get("data", {}).get("list", [])
                    
                    if not items:
                        print("没有更多评论了")
                        break

                    for item in items:
                        moment = item.get("moment", {})
                        review = moment.get("review", {})
                        author = moment.get("author", {}).get("user", {})
                        stat = moment.get("stat", {})
                        
                        # 解析评论内容
                        contents = review.get("contents", {})
                        content_text = contents.get("text", contents.get("raw_text", ""))
                        
                        # 解析设备信息
                        device = moment.get("device", "未提供")
                        
                        writer.writerow([
                            author.get("id"),
                            author.get("name"),
                            review.get("score"),
                            content_text.replace("\n", " "),
                            stat.get("ups"),  # 使用moment的点赞数
                            datetime.fromtimestamp(moment.get("created_time", 0)).strftime("%Y-%m-%d %H:%M"),
                            device,
                        ])

                    collected += len(items)
                    print(f"成功获取 {len(items)} 条，累计 {collected} 条")
                    page += 1
                else:
                    print(f"请求失败详情：{response.text[:200]}")
                    break

            except Exception as e:
                print(f"请求异常：{str(e)}")
                break

    print(f"\n完成！共爬取 {collected} 条评论")

if __name__ == "__main__":
    fetch_reviews()