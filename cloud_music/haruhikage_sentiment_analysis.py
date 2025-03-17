import pandas as pd
import jieba
import re
from collections import defaultdict

# 专用术语预处理
anime_terms = [
    '春日影', 'mygo', 'mujica', 'soyo', '祥子', 'crychic', 
    'ave mujica', '母鸡卡', '灯', '立希', '春日影事变'
]
for term in anime_terms:
    jieba.add_word(term)

# 增强情感规则
sentiment_rules = {
    'positive': {
        'keywords': {
            '好听', '感动', '支持', '进步', '美好', '神曲', '喜欢', '天才',
            '未来可期', '拼命', '努力', '爽', '避风港', '和解', '厚实', '平滑',
            '演奏春日影', '有感觉', '豪庭', '感染力', '冰', '上头', '上瘾'
        },
        'emojis': {'😭', '😍', '🎸', '🙏🏻', '😇', '☝️', '🤓', '😂'}
    },
    'negative': {
        'keywords': {
            '破防', '猎奇', '低俗', '灾难', '痛苦', '背叛', '过家家', '错误',
            '吓人', '警告', '切割', '崩坏', '哭', '吐了', '逆天', '盒', '木柜子'
        },
        'emojis': {'🤮', '😑'}
    },
    'neutral': {
        'keywords': {
            '打卡', '建议', '键盘', '吉他', '梗', '玩梗', 
            '路人', '分析', '什么时候', '剧情', '转生', '补番'
        },
        'emojis': {'🤔', '🎹', '💔', '😡', '😨'}
    }
}

# 特殊句式模式 
patterns = {
    'positive': [
        r'太喜欢了', r'未来可期', r'哭的不能自己', r'拼命',
        r'和解', r'为什么要演奏', r'长期素食', r'soyo',
        r'全体起立', r'何时来的', r'朱元璋'
    ],
    'negative': [
        r'切割.*mujica', r'破防', r'警告', r'猎奇',
        r'低俗', r'灾难', r'过家家'
    ]
}

class AnimeSentimentAnalyzer:
    def __init__(self):
        self.negation_words = {'不', '没', '无', '非', '未', '莫'}
        
    def analyze(self, text):
        # 预处理
        text = re.sub(r'$$\\w\+?$$', '[表情]', text)
        
        # 模式匹配
        for pattern in patterns['positive']:
            if re.search(pattern, text):
                return '正面'
        for pattern in patterns['negative']:
            if re.search(pattern, text):
                return '负面'
        
        # 情感计分
        scores = defaultdict(int)
        words = jieba.lcut(text)
        
        for word in words:
            for sentiment, rule in sentiment_rules.items():
                if word in rule['keywords']:
                    scores[sentiment] += 3
                    
        # 表情符号处理
        for emoji in re.findall(r'$$表情$$', text):
            for sentiment, rule in sentiment_rules.items():
                if emoji in rule['emojis']:
                    scores[sentiment] += 3
        
        # 否定处理
        for i in range(1, len(words)):
            if words[i-1] in self.negation_words and words[i] in {'好', '喜欢', '对'}:
                scores['negative'] += 3
                
        # 特定梗处理
        if '为什么要演奏春日影' in text:
            scores['negative'] -= 2 if '开心' not in text else -3
        
        if not scores:
            return '中性'
            
        # 修改返回值部分，统一转换为中文标签
        max_sentiment = max(scores, key=scores.get)
        return {
            'positive': '正面',
            'negative': '负面',
            'neutral': '中性'
        }[max_sentiment]  # 关键修正：将英文键映射为中文标签

def read_txt_basic(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines

# 修改后的输出展示部分
if __name__ == "__main__":
    comments = read_txt_basic("cloud_music/Haruhikage.txt")
    
    analyzer = AnimeSentimentAnalyzer()
    results = []
    
    for comment in comments:
        sentiment = analyzer.analyze(comment)
        results.append({
            '评论内容': comment,
            '情感倾向': sentiment
        })
    
    df = pd.DataFrame(results)
    
    # 生成统计表格
    stats = df['情感倾向'].value_counts().reset_index()
    stats.columns = ['情感类型', '数量']
    stats['占比'] = (stats['数量'] / len(df)).round(2) * 100  # 计算百分比
    
    # 打印美化后的输出
    print("=== 情感分析结果统计 ===")
    print(stats.to_markdown(index=False, tablefmt="grid", stralign="center"))
    
    print("\n=== 示例评论分析 ===")
    sample_df = df.sample(5, random_state=42)[['评论内容', '情感倾向']]
    print(sample_df.to_markdown(index=False, tablefmt="grid", stralign="left"))