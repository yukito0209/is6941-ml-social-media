import pandas as pd
import numpy as np
import re
import emoji
import jieba

# ================== 预处理函数 ==================
def process_comment(text, stopwords):
    if pd.isna(text):
        return ""
    
    # 1. HTML标签处理
    text = re.sub(r'<[^>]+>', ' ', str(text))
    
    # 2. Emoji转换
    text = emoji.demojize(text, delimiters=(" ", " "))
    
    # 3. 特殊字符处理
    text = re.sub(r'[^\w\u4e00-\u9fff\s]', ' ', text)
    text = re.sub(r'(\!|\?|\.|\,)\1+', r'\1', text)
    
    # 4. 中文分词
    words = jieba.cut(text, cut_all=False)
    
    # 5. 停用词过滤
    filtered = [word.strip() for word in words if word.strip() and word not in stopwords]
    
    return ' '.join(filtered).strip()
    # return text

# ================== 主处理流程 ==================
def main():
    # 1. 加载停用词表
    stopwords_path = r"D:\GitHubRepos\is6941-ml-social-media\taptap\analytics\stopwords\stopwords_hit.txt"
    try:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = set([line.strip() for line in f if line.strip()])
        print(f"成功加载停用词数量：{len(stopwords)}")
    except Exception as e:
        print(f"停用词加载失败：{str(e)}")
        stopwords = set()  # 回退为空集合

    # 2. 读取原始数据
    df = pd.read_csv(r"D:\GitHubRepos\is6941-ml-social-media\taptap\data\integrated\taptap_reviews.csv")
    
    # 3. 基础清洗
    df['用户名'] = df['用户名'].fillna('未知用户').str.strip()
    df['点赞数'] = df['点赞数'].fillna(0).astype(np.int64)
    df['评分'] = df['评分'].clip(1, 5)
    df['设备型号'] = df['设备型号'].replace('未提供', 'unknown')
    
    # 4. 处理评论内容
    df['评论内容'] = df['评论内容'].apply(lambda x: process_comment(x, stopwords))
    
    # 5. 列名标准化
    column_mapping = {
        '用户ID': 'user_id',
        '用户名': 'username',
        '评分': 'rating',
        '评论内容': 'review_content',
        '点赞数': 'likes',
        '发布时间': 'publish_time',
        '设备型号': 'device_model',
        '游戏名称': 'game_name',
    }
    df = df.rename(columns=column_mapping)

    # 新增步骤：添加情感二分类列
    df['sentiment'] = np.where(df['rating'].between(1, 2), 0, 1)  # 1-2分=0，3-5分=1
    # 删除列: 'username', 'review_content' 中缺少数据的行
    df = df.dropna(subset=['username', 'review_content'])
    
    # 6. 最终处理
    df['publish_time'] = pd.to_datetime(
        df['publish_time'], 
        format='mixed',  # 自动识别多種格式
        dayfirst=False,   # 月份在前（默认MM/DD格式）
        errors='coerce'   # 将解析失败设为NaT
    )
    df = df.drop_duplicates(subset=['user_id', 'publish_time'])
    df = df.reset_index(drop=True)
    
    # 7. 保存结果
    df.to_csv(r"D:\GitHubRepos\is6941-ml-social-media\taptap\data\integrated\cleaned_taptap_reviews.csv", encoding='utf-8-sig', index=False)
    
    # 打印处理示例
    print("\n处理前后示例对比：")
    sample = df[['review_content']].head(3)
    print(sample.to_string(index=False))
    # 在处理后添加检查
    print(f"处理后缺失值数量：{df['review_content'].isna().sum()}")
    print(f"非字符串类型数量：{df['review_content'].apply(type).ne(str).sum()}")

if __name__ == "__main__":
    main()