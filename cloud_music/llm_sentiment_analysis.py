# -*- coding: utf-8 -*-
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import re

class AnimeSentimentAnalyzer:
    def __init__(self):
        # 模型配置
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 特殊参数（关键修复）
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True  # 必须添加此参数
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,  # 必须添加此参数
            torch_dtype=torch.bfloat16,  # 量化优化
            device_map="auto"  # 自动设备分配
        ).eval()
        
        # 领域提示模板
        self.prompt_template = """[INST] <<SYS>>
你是一个动漫音乐评论分析专家，请对以下内容进行情感分析：
1. 识别评论中的专业术语：{terms}
2. 判断情感倾向（正面/负面/中性）
3. 简要说明理由
<</SYS>>

评论内容：{comment} [/INST]
"""
        self.anime_terms = [
            '春日影', 'mygo', 'mujica', 'soyo', '祥子', 'crychic', 
            'ave mujica', '母鸡卡', '灯', '立希', '春日影事变'
        ]

    def preprocess(self, text):
        """文本清洗"""
        text = re.sub(r'\$\$\\w\+\?\$\$', '[表情]', text)
        return text[:512]  # 控制输入长度

    def analyze(self, text):
        """核心分析方法"""
        # 预处理
        cleaned_text = self.preprocess(text)
        
        # 构建提示词
        prompt = self.prompt_template.format(
            terms="、".join(self.anime_terms),
            comment=cleaned_text
        )
        
        # 生成配置
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)
        
        # 生成参数
        generate_kwargs = {
            "max_new_tokens": 50,
            "do_sample": False,
            "temperature": 0.3,
            "repetition_penalty": 1.1
        }
        
        # 执行推理
        with torch.no_grad():
            outputs = self.model.generate(**inputs, **generate_kwargs)
        
        # 解析结果
        response = self.tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
        
        # 提取情感标签（关键解析逻辑）
        if "正面" in response:
            return "正面"
        elif "负面" in response:
            return "负面"
        else:
            return "中性"

# 使用示例
if __name__ == "__main__":
    # 初始化分析器
    analyzer = AnimeSentimentAnalyzer()
    
    # 测试评论
    test_comments = [
        "春日影这首曲子太神了，听得我泪流满面😭",
        "母鸡卡的剧情发展有点迷，编剧在想什么？",
        "为什么要演奏春日影！这简直是灾难！"
    ]
    
    # 执行分析
    results = []
    for comment in tqdm(test_comments):
        results.append({
            "评论": comment,
            "情感": analyzer.analyze(comment)
        })
    
    # 打印结果
    import pandas as pd
    print(pd.DataFrame(results).to_markdown(index=False))