# -*- coding: utf-8 -*-
import torch
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, pipeline
import pandas as pd
import re
import os

class WindowsBatchAnalyzer:
    def __init__(self):
        # 使用量化模型降低显存占用
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

        # 初始化模型
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        # 量化配置优化
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,  # 显式指定计算类型
            bnb_4bit_quant_type="nf4",  # 使用最新量化格式
            bnb_4bit_use_double_quant=True  # 启用二次量化
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            torch_dtype=torch.float16,  # 保持数据类型一致
            quantization_config=quantization_config,  # 替换旧参数
            low_cpu_mem_usage=True,
            max_memory={0: "28GiB"}
        )

        # 批处理优化参数
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            batch_size=32  # 根据显存调整
        )

        # 优化后的模板
        self.prompt_template = """[INST] <<SYS>>
作为资深产品分析师，请严格按以下标准分类评论：

【正面】需满足以下任一条件：
✓ 明确购买意向："必买/首发/已预购"等
✓ 积极评价："太棒了/值得入手"等
✓ 示例："存钱等发售！" "画质提升明显"

【负面】需满足以下任一条件：
✗ 价格抱怨："太贵/不值/割韭菜"等
✗ 质量问题："做工差/性能拉胯"等
✓ 示例："价格劝退" "joycon又漂移"

【中性】无明确情感倾向：
• 参数讨论："CPU频率/TFLOPS数值"
• 普通提问："什么时候发售"
<</SYS>>

请分析该评论（保持原始表述）：
「{comment}」

只需输出【正面/中性/负面】：
[/INST] 【"""

    def batch_analyze(self, texts):
        # 批量预处理
        cleaned = [self._clean_text(t) for t in texts]
        prompts = [self.prompt_template.format(comment=t[:512]) for t in cleaned]
        
        # 批量生成（Windows优化参数）
        outputs = self.pipeline(
            prompts,
            max_new_tokens=20,
            temperature=0.7,
            top_k=40,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            num_return_sequences=1
        )
        
        return [self._parse(o[0]['generated_text']) for o in outputs]

    def _clean_text(self, text):
        # Windows路径兼容处理
        return re.sub(r'($$.\*?$$|\\n|\\r)', '', text)

    def _parse(self, generated_text):
        # 高效解析逻辑
        if "购买意愿" in generated_text:
            return "购买意愿"
        if "负面评价" in generated_text:
            return "负面评价"
        return "中性讨论"

def windows_optimized_analysis(csv_path):
    # 路径兼容处理
    df = pd.read_csv(csv_path, engine='python')
    
    # 分批处理防止内存溢出
    analyzer = WindowsBatchAnalyzer()
    batch_size = 32
    
    results = []
    for i in range(0, len(df), batch_size):
        batch = df['评论内容'].iloc[i:i+batch_size].tolist()
        batch_results = analyzer.batch_analyze(batch)
        results.extend(batch_results)
        print(f"进度: {min(i+batch_size, len(df))}/{len(df)}")
    
    df['情感分类'] = results

    def display_statistics(df):
        # 统计各分类数量
        stats = df['情感分类'].value_counts().reset_index()
        stats.columns = ['分类', '数量']
        
        # 计算百分比
        total = len(df)
        stats['占比'] = (stats['数量'] / total * 100).round(1).astype(str) + '%'
        
        # 打印统计表格
        print("\n📊 情感分布统计:")
        print(stats.to_markdown(index=False, tablefmt="grid", stralign="center"))
        
        # 打印随机样本
        print("\n🔍 随机抽样示例:")
        sample = df.sample(5, random_state=42)[['评论内容', '情感分类']]
        print(sample.to_markdown(index=False, tablefmt="grid", stralign="left"))

    # 执行统计展示
    display_statistics(df)

    save_path = os.path.normpath(r"D:\\GitHubRepos\\is6941-ml-social-media\\analysis\\results\\comment_results.csv")
    df.to_csv(save_path, index=False, encoding='utf_8_sig')

if __name__ == "__main__":
    csv_path = os.path.normpath(r"analysis\data\\cleaned_BV1dZwLeKEzG_comments.csv")
    windows_optimized_analysis(csv_path)