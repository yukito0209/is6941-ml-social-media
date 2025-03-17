import pandas as pd
import jieba
from collections import defaultdict

# 加载数据
def load_comments(csv_path):
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='gbk')
    
    # 数据清洗
    df['评论'] = df['评论'].str.replace(r'$$\\w\+?\_?\\d\+$$', '[表情]', regex=True)  # 统一特殊表情符号
    return df

# 情感分析增强模块
class SentimentAnalyzer:
    def __init__(self):
        self.lexicon = self._load_lexicon()
        self.sentiment_map = {
            'positive': {'权重': 1.2, 'keywords': {
                '[支持]', '[doge]', '致敬', '坚持', '启发', '伟大', '专业', '感谢',
                '有用', '支持', '理解', '学习', '庆幸', '有帮助', '喜欢', '致敬'
            }},
            'negative': {'权重': 1.5, 'keywords': {
                '[无语]', '[大哭]', '猎奇', '炸裂', '恶心', '后悔', '封了', '骂',
                '骗', '编造', '不理解', '危险', '痛苦', '伤害', '变态', '异常'
            }},
            'neutral': {'权重': 1.0, 'keywords': {
                '[笑哭]', '🤓', '第一次', '是不是', '怎么', '可能', '感觉',
                '建议', '讨论', '疑问', '思考', '分析', '猜测'
            }}
        }
        self.negation_words = {'不', '没', '无', '非', '未', '莫'}  # 否定词列表
        
        # 修正分词词典加载方式
        for sentiment in self.sentiment_map.values():
            for word in sentiment['keywords']:  # 遍历每个关键词
                jieba.add_word(word)  # 正确的方法调用

    def _load_lexicon(self):
        """加载B站专用情感词典"""
        lexicon = defaultdict(set)
        lexicon.update({
            'positive': {'yyds', '破防了', '泪目', '三连'},
            'negative': {'蚌埠住了', '下头', '寄', '典急孝'},
            'neutral': {'谜语人', '钝角', '典', '孝'}
        })
        return lexicon

    def _contains_negation(self, words, index):
        """检查否定修饰 (处理类似"不专业"的情况)"""
        return index > 0 and words[index-1] in self.negation_words

    def analyze(self, text):
        words = list(jieba.cut(text))
        scores = defaultdict(float)

        for i, word in enumerate(words):
            for sentiment, data in self.sentiment_map.items():
                if word in data['keywords']:
                    modifier = 0.5 if self._contains_negation(words, i) else 1.0
                    scores[sentiment] += data['权重'] * modifier
            # 处理B站专用词汇
            for sentiment, terms in self.lexicon.items():
                if word in terms:
                    scores[sentiment] += 1.0

        # 特殊表情符号处理
        if '[表情]' in text:
            scores['neutral'] += 1.2

        if not scores:
            return '中性'
        
        max_sentiment = max(scores, key=scores.get)
        return '正面' if max_sentiment == 'positive' else \
               '负面' if max_sentiment == 'negative' else '中性'

# 使用示例
if __name__ == "__main__":
    # 加载数据
    comments_df = load_comments("bilibili/test_comments_data.csv")
    
    # 初始化分析器
    analyzer = SentimentAnalyzer()
    
    # 执行分析
    comments_df['情感'] = comments_df['评论'].apply(analyzer.analyze)
    
    # 保存结果
    # comments_df.to_csv("bilibili/analyzed_comments.csv", index=False, encoding='utf-8-sig')
    
    # 生成分析报告
    report = comments_df['情感'].value_counts(normalize=True).apply(lambda x: f"{x:.1%}")
    print(f"\n情感分布分析：\n{report.to_markdown()}")