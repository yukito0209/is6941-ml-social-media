# is6941-ml-social-media

IS6941课程小组项目的代码仓库，聚焦机器学习在社交媒体数据分析中的应用。

### 已经实验的预训练语言模型

1. [google-bert/bert-base-chinese · Hugging Face](https://huggingface.co/google-bert/bert-base-chinese)
2. [hfl/chinese-roberta-wwm-ext · Hugging Face](https://huggingface.co/hfl/chinese-roberta-wwm-ext)
3. [IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment · Hugging Face](https://huggingface.co/IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment)
4. [uer/gpt2-chinese-cluecorpussmall · Hugging Face](https://huggingface.co/uer/gpt2-chinese-cluecorpussmall)

### 4月8日更新

1. 尝试了CatBoost方法和一些预训练语言模型；
2. 对数据集进行了描述性分析。

### 4月7日更新

1. 完成了一些传统方法的分析流程，写了一点报告；
2. 做了一些集成学习方法的尝试。

### 4月5日更新

1. 尝试编写了爬取TapTap评论区数据的代码，大失败；
2. 发现一篇文章：[使用fiddler对手机APP进行抓包_fiddler抓包手机app-CSDN博客](https://blog.csdn.net/xyz846/article/details/78963245)，以及GitHub仓库：[sariel-black/taptap_emotion_analyse: TAPTAP游戏评论的文本挖掘，包括APP爬虫、数据清洗、pyecharts可视化、pytorch框架下LSTM模型情感分析](https://github.com/sariel-black/taptap_emotion_analyse/tree/master)和[guderian110/taptap_review_inexcel: 通过xlwings实现对taptap评论的拉取，存储、情感分析、词云&amp;可视化](https://github.com/guderian110/taptap_review_inexcel)，睡醒再试；
3. 不用试了，成功了！
4. 爬取了40款游戏的最新评论数据，每款1000条，共40000条。

### 3月31日更新

1. 尝试了使用「知网Hownet情感词典」进行无监督情感分类，整了一半突然不想整了。

### 3月26日更新

1. 原来的get_bilibili_comments.py代码有些问题，且不易使用，重新写了更方便使用的new_get_bilibili_comments.py替代；
2. 使用new_get_bilibili_comments.py爬取了BV1dZwLeKEzG视频下的评论区数据，共计8800条，保存为BV1dZwLeKEzG_comments.csv；
3. new_get_bilibili_comments.py爬取时，最后的小于100条数量的评论无法保存，有待后续改进；
4. 修复了3中提到的bug，不过爬取的评论总数变成8364条了（？）；
5. 对BV1dZwLeKEzG_comments.csv做了初步的数据清洗，清洗后文件存放在analysis\data\cleaned_BV1dZwLeKEzG_comments.csv；
6. 使用DeepSeek-R1-Distill-Llama-8B对cleaned_BV1dZwLeKEzG_comments.csv进行了分析尝试，代码参见：analysis\basic_algorithm\Llama_analysis.py；
7. 布什，为什么分类结果全是同一类？？？

### 3月25日更新

1. 尝试了对小红书搜索结果的爬取，尚未成功。

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

### 计划爬取的视频

1. 【IGN】Switch 2公布预告：https://www.bilibili.com/video/BV1dZwLeKEzG/?spm_id_from=333.337.search-card.all.click&vd_source=04ece31a501c42b11a4a13b2d069946b
