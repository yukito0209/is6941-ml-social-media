# -*- coding: utf-8 -*-
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import re
import pandas as pd
import os

class AnimeSentimentAnalyzer:
    def __init__(self):
        # 模型选择(根据自己电脑的显存量力而行)
        # macbook使用统一内存架构，因此参考内存，而不是显存
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        # self.model_name = "google-bert/bert-base-uncased" # 烂

        
        # 初始化分词器和模型
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        """一般用以下代码"""
        # self.model = AutoModelForCausalLM.from_pretrained(
        #     self.model_name,
        #     trust_remote_code=True,
        #     torch_dtype=torch.bfloat16,
        #     device_map="auto",
        #     low_cpu_mem_usage=True
        # ).eval()
        """macbook用以下代码"""
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="mps" if torch.backends.mps.is_available() else "auto",
            low_cpu_mem_usage=True
        ).to('mps').eval()
        
        # 领域提示模板
        self.prompt_template = """[INST] <<SYS>>
你是观看过《BanG Dream! It's MyGO!!!!!》一千遍的资深动漫爱好者。现有200+条来自网易云的《春日影》歌曲评论，请按以下规则分析评论情感：
1. 必须用【正面/负面/中性】开头
2. 判断标准：
    - 正面：出现好评词（神曲、泪目、好听）或感动表情（😭、🎸）或善意玩梗
    - 负面：出现差评词（难听、迷惑、劝退）或负面表情（🤮）
    - 中性：其他情况
3. 示例：
    "春日影吉他solo太棒了！😭" → 正面
    "母鸡卡剧情太迷惑了" → 负面
    "周三更新吗？" → 中性
<</SYS>>

立即分析该评论：
"{comment}"
[/INST]
情感分类：【"""
        self.anime_terms = [
            '春日影', 'mygo', 'mujica', 'soyo', '祥子', 'crychic', 
            'ave mujica', '母鸡卡', '灯', '立希', '春日影事变'
        ]

    def preprocess(self, text):
        """文本清洗"""
        text = re.sub(r'\$\$\\w\+\?\$\$', '[表情]', text)
        return text[:1024]  # 控制输入长度

    def analyze(self, text):
        # 新增设备状态输出
        print(f"🔥 显存占用: {torch.mps.current_allocated_memory()/1024**2:.2f} MB" 
            if torch.backends.mps.is_available() else "⏳ CPU模式运行")

        # 前置规则覆盖
        text_lower = text.lower()
        
        # 特殊句式规则
        if any(rule in text_lower for rule in ['太好听', '神曲预定', '泪目了']):
            return "正面"
        if any(rule in text_lower for rule in ['难听死了', '劝退']):
            return "负面"
        
        # 特定组合检测
        if ('春日影' in text) and ('双吉他' in text or '为什么' in text):
            return "正面"
        if '呜呜呜' in text and ('感动' in text or '哭' in text):
            return "正面"

        """核心分析方法"""
        cleaned_text = self.preprocess(text)
        prompt = self.prompt_template.format(
            terms="、".join(self.anime_terms),
            comment=cleaned_text
        )
        """一般用以下代码"""
        # inputs = self.tokenizer(
        #     prompt,
        #     return_tensors="pt"
        # ).to(self.model.device)
        """macbook用以下代码"""
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(device)
        
        """一般用以下代码"""
        # with torch.no_grad():
        #     outputs = self.model.generate(
        #         **inputs,
        #         max_new_tokens=30,  # 限制输出长度
        #         temperature=0.9,    # 增加创造性
        #         top_k=50,
        #         num_return_sequences=1,
        #         pad_token_id=self.tokenizer.eos_token_id,
        #         eos_token_id=self.tokenizer.convert_tokens_to_ids(["<|im_end|>"])[0]
        #     )
        """macbook用以下代码"""
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=30,  # 限制输出长度
                temperature=0.9,    # 增加创造性
                top_k=50,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.convert_tokens_to_ids(["<|im_end|>"])[0],
                # MPS专属优化参数
                use_cache=True,
                do_sample=True if torch.backends.mps.is_available() else False
            )
        
        response = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
        return self._parse_response(response)

    def _parse_response(self, response):
        """增强版解析逻辑"""
        # 强制格式匹配
        if re.match(r'^正面', response):
            return "正面"
        if re.match(r'^负面', response):
            return "负面"
        
        # 表情符号检测
        emoji_rules = {
            '😭': '正面',
            '🎸': '正面',
            '🤮': '负面'
        }
        for emo, label in emoji_rules.items():
            if emo in response:
                return label
        
        # 关键词强化
        positive_keywords = {'好听', '豪听', '神曲', '泪目', '感动', '喜欢', '棒', '爽'}
        negative_keywords = {'难听', '迷惑', '劝退', '垃圾', '失望', '猎奇', '低俗', '灾难'}
        
        text = response.lower()
        if any(kw in text for kw in positive_keywords):
            return "正面"
        elif any(kw in text for kw in negative_keywords):
            return "负面"
        
        # 重复字符检测（如"呜呜呜呜"表示感动）
        if re.search(r'(.)\1{3,}', text):  # 连续4个相同字符
            return "正面" if '好' in text else "负面"
        
        return "中性"

def read_comments(file_path):
    """读取评论文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 未找到")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def display_results(results):
    """优化后的结果显示"""
    df = pd.DataFrame(results)
    
    # 情感统计
    stats = df['情感'].value_counts().reset_index()
    stats.columns = ['情感类型', '数量']
    stats['占比'] = (stats['数量'] / len(df) * 100).round(1).astype(str) + '%'
    
    # 示例展示
    samples = df.sample(5, random_state=42)
    
    # 控制台输出
    print("\n🎯 分析结果统计")
    print(stats.to_markdown(index=False, tablefmt="grid", stralign="center"))
    
    print("\n🔍 随机抽样示例")
    print(samples.to_markdown(index=False, tablefmt="grid", stralign="left"))
    
    # 保存完整结果
    df.to_csv("cloud_music/sentiment_results.csv", index=False, encoding='utf_8_sig')
    print("\n💾 完整结果已保存至 sentiment_results.csv")

if __name__ == "__main__":
    # 初始化分析器
    analyzer = AnimeSentimentAnalyzer()
    
    try:
        # 读取评论文件
        comments = read_comments("cloud_music/Haruhikage.txt")
        print(f"✅ 成功读取 {len(comments)} 条评论")
        
        # 执行分析
        results = []
        for comment in tqdm(comments, desc="分析进度", unit="条"):
            results.append({
                "评论内容": comment,
                "情感": analyzer.analyze(comment)
            })
        
        # 显示优化后的结果
        display_results(results)
        
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")