# is6941-ml-social-media

IS6941课程小组项目的代码仓库，聚焦机器学习在社交媒体数据分析中的应用。

### 3月21日更新

1. 爬取了完整的网易云《春日影》评论区数据，共计18061条，保存在Haruhikage_comments.txt中。

### 3月20日更新

1. 新增了对Apple Silicon的支持代码；
2. 尝试了bert-base-uncased模型，效果不佳；
3. 新增了empty_model_cache.py用于清理模型缓存；
4. 尝试了DeepSeek-R1-Distill-Llama-8B模型，效果拔群！！！

### 3月19日更新

1. 使用DeepSeek-R1-Distill-Qwen-1.5B模型进行了情感分析试验，效果不佳，有待后续改进；
2. 改进了llm_sentiment_analysis.py，取得了更好的效果。

### 3月17日更新

1. 对test_comments_data.csv进行了简单的情感分析；
2. 对Haruhikage.txt进行了简单的情感分析。

### 3月16日更新

1. 初步编写完成了对bilibili视频评论区数据的爬虫代码;
2. wdw早上7:45起床了 ^ ^ ；
3. 初步编写完成了对网易云评论区数据进行爬取的代码。

### 测试模型列表

1. DeepSeek-R1-Distill-Qwen-1.5B：[deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B · Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)
2. DeepSeek-R1-Distill-Llama-8B：[deepseek-ai/DeepSeek-R1-Distill-Llama-8B · Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)
3. bert-base-uncased：[google-bert/bert-base-uncased · Hugging Face](https://huggingface.co/google-bert/bert-base-uncased)
