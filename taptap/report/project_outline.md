# 报告大纲

## 摘要

## 1 引言

建议添加更多介绍TapTap的内容，体现商业价值，参考链接：

* [关于我们 | TapTap 发现好游戏](https://www.taptap.cn/about-us)
* [TapTap（易玩（上海）网络科技有限公司开发的游戏社区）_百度百科](https://baike.baidu.com/item/Taptap/20623110)
* [TapTap - 维基百科，自由的百科全书](https://zh.wikipedia.org/zh-cn/TapTap)
* [AP202408301639654381.pdf](https://testtoo1.oss-cn-hangzhou.aliyuncs.com/eastmoney_pdf/AP202408301639654381.pdf)
* [关于心动 - 心动](https://www.xd.com/about-us/?lang=zh)

In the mobile gaming ecosystem, TapTap, as a leading global gaming community and distribution platform, hosts user reviews that reflect direct player feedback on game quality and offer critical insights into market demand and user experience. However, game reviews are often characterized by short text length, informal language (e.g., slang like "肝爆" [grinding] or "氪金" [pay-to-win]), and implicit sentiment expressions, posing challenges for traditional sentiment analysis methods (e.g., lexicon-based rule models) that struggle with limited classification accuracy and generalization capabilities.

While prior studies have attempted to improve sentiment analysis using machine learning models (e.g., LR, KNN, SVM) or deep learning models (e.g., LSTM, CNN), there remains a lack of systematic comparison and optimization of pre-trained language models and ensemble strategies in the context of game reviews. Furthermore, most existing research relies on small-scale datasets (The largest known dataset currently includes fewer than 5,000 reviews.) and fails to address the unique linguistic characteristics of Chinese game reviews.

To address these challenges, this study proposes the following solutions:

- **Dataset Construction:** A large-scale Chinese game review dataset (40 games × 1,000 reviews, totally 40,000 reviews) is curated, covering diverse game genres and user expression patterns.
- **Model Comparison:** Four categories of models are rigorously evaluated, including lexicon-based methods, machine learning models, deep learning architectures, and pre-trained language models.
- **Ensemble Optimization:** A cross-validation-driven ensemble voting mechanism is designed to combine top-performing models, overcoming the limitations of single-model approaches.

The key innovations of this work include:

- **Data Contribution:** The first large-scale, fine-grained annotated Chinese sentiment analysis dataset tailored for TapTap game reviews.
- **Methodological Advancements:** Integration of cutting-edge pre-trained models  and lightweight models to balance accuracy and computational efficiency.
- **Strategic Breakthrough:** A dynamic weighted voting mechanism that achieves a great accuracy improvement over the best single model.

This research not only provides an efficient sentiment analysis tool for game developers and operators but also offers empirical insights into the application of multi-model ensemble optimization in natural language processing tasks.

## 2 数据采集与预处理 Data Collection and Preprocessing

### 2.1 数据采集 Data Collectioon

The user review data utilized in this study was systematically collected from the official TapTap gaming platform. Employing a multi-criteria selection framework that integrated platform ranking positions, review volume metrics, and game popularity indices, we identified 40 representative game titles. For each selected game, custom web crawlers were developed to extract the most recent 1,000 user reviews, capturing seven key data dimensions: unique user identifier, username, numerical rating score, textual review content, like counts, review publication timestamp, and device model information. Through systematic data aggregation and validation processes, this methodology yielded a comprehensive raw dataset comprising 40,000 distinct user reviews, establishing a robust foundation for subsequent analytical investigations.

The 40 games selected are listed below (arranged by the first letter of the English name):

| 序号 |            英文名            |           中文名           | 序号 |           英文名           |      中文名      |
| :--: | :---------------------------: | :------------------------: | :--: | :-------------------------: | :--------------: |
|  01  |       7 Years From Now       |      我在7年后等着你      |  21  |           Justice           |      逆水寒      |
|  02  |         Aether Gazer         |          深空之眼          |  22  |       Light and Night       |    光与夜之恋    |
|  03  |           Arknights           |          明日方舟          |  23  |     Love and Deepspace     |     恋与深空     |
|  04  |           Azur Lane           |          碧蓝航线          |  24  |  Minecraft: Pocket Edition  | 我的世界：移动版 |
|  05  | BanG Dream! Girls Band Party! | BanG Dream! 少女乐团派对！ |  25  |          Muse Dash          |     喵斯快跑     |
|  06  |         Blue Archive         |          蔚蓝档案          |  26  |     Naraka: Bladepoint     |     永劫无间     |
|  07  |           Cytus II           |      音乐世界赛特斯2      |  27  |           Naruto           |     火影忍者     |
|  08  |          Dead Cells          |          死亡细胞          |  28  |           Onmyoji           |      阴阳师      |
|  09  |          Delta Force          |         三角洲行动         |  29  |           Phigros           |     菲格罗斯     |
|  10  |          Eggy Party          |          蛋仔派对          |  30  |        Reverse:1999        |  重返未来：1999  |
|  11  |       Fate/Grand Order       |       命运-冠位指定       |  31  |         Sausage Man         |     香肠派对     |
|  12  |        Game for Peace        |          和平精英          |  32  | Sky: Children of the Light |      光·遇      |
|  13  |        Genshin Impact        |            原神            |  33  | Snowbreak: Containment Zone |     尘白禁区     |
|  14  |     GRAY RAVEN：PUNISHING     |         战双帕弥什         |  34  |         Soul Knight         |     元气骑士     |
|  15  |        Honkai Impact 3        |           崩坏3           |  35  |      Teamfight Tactics      |    金铲铲之战    |
|  16  |       Honkai: Star Rail       |       崩坏：星穹铁道       |  36  |       Tears of Themis       |    未定事件簿    |
|  17  |        Honor of Kings        |          王者荣耀          |  37  |          Terraria          |     泰拉瑞亚     |
|  18  |             ICEY             |            艾希            |  38  |      WHERE WINDS MEET      |    燕云十六声    |
|  19  |          Identity Ⅴ          |          第五人格          |  39  |       Wuthering Waves       |       鸣潮       |
|  20  |        Infinity Nikki        |          无限暖暖          |  40  |      Zenless Zone Zero      |      绝区零      |

### 2.2 数据清洗 Data Cleaning

- 这部分清洗出了两个CSV文件，taptap\data\integrated\cleaned_taptap_reviews.csv是一般方法用的，taptap\data\integrated\lm_cleaned_taptap_reviews.csv是专门给预训练语言模型用的；
- 它们的主要区别在于前者对评论内容进行了分词处理，并去除了emoji表情。

### 2.3 最终数据集 Final Dataset

## 3 方法论与模型设计

### 3.1 基于情感词典的模型——基线模型

### 3.2 传统机器学习模型

#### 3.2.1 逻辑回归

#### 3.2.2 KNN

#### 3.2.3 决策树

#### 3.2.4 支持向量机 SVM

#### 3.2.5 Boosting集成学习

### 3.3 传统深度学习模型

#### 3.3.1 卷积神经网络 CNN

#### 3.3.2 双向长短时记忆网络 BiLSTM

### 3.4 预训练语言模型

### 3.5 Stacking集成

- 基模型：XGBoost、CatBoost和bert-base-chinese预训练语言模型；
- 元模型：Logistic Regression；
- 完整的notebook文件代码蔚为壮观，参见：taptap\analytics\ensemble_voting\enhanced_ensemble_voting.ipynb。

## 4 结果与分析

## 5 总结与展望

## 参考文献
