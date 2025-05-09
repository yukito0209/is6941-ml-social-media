好的，这是第 6 部分“性能评估 (Assessment of Performance)”的示例内容：

---

### **6. 性能评估 (Assessment of Performance)**

本章旨在客观、量化地评估在第5部分中构建的情感分析模型的性能。我们采用了机器学习领域标准的评估指标，并在独立的测试数据集上对模型进行了严格测试，以衡量其在预测未知TapTap评论情感时的准确性和鲁棒性。

* **6.1 评估指标 (Performance Metrics)**

  为全面评估模型的分类性能，我们选用了以下常用的评估指标：

  * **准确率 (Accuracy)**: 模型预测正确的样本数占总样本数的比例。计算公式为 \( \frac{TP+TN}{TP+TN+FP+FN} \)。它提供了模型整体性能的一个直观度量。
  * **精确率 (Precision)**: 在所有被模型预测为正类（Positive, 即正面情感）的样本中，实际为正类的比例。计算公式为 \( \frac{TP}{TP+FP} \)。高精确率意味着模型预测为正面的评论确实是正面的，这对于需要确保正面反馈质量的应用场景很重要。
  * **召回率 (Recall / Sensitivity)**: 在所有实际为正类的样本中，被模型成功预测为正类的比例。计算公式为 \( \frac{TP}{TP+FN} \)。高召回率意味着模型能找出尽可能多的实际正面评论，这对于不希望漏掉任何正面反馈的场景很重要。（同样适用于负面类别，评估找出负面评论的能力）。
  * **F1 分数 (F1-Score)**: 精确率和召回率的调和平均数，计算公式为 \( 2 \times \frac{Precision \times Recall}{Precision + Recall} \)。它综合了精确率和召回率的表现，尤其适用于类别分布可能不均衡的情况，是衡量模型综合性能的常用指标。
  * **混淆矩阵 (Confusion Matrix)**: 一个表格，用于可视化模型预测结果与实际标签之间的关系，包含真正例 (TP)、真负例 (TN)、假正例 (FP) 和假负例 (FN) 的数量。它为深入分析模型的错误类型提供了基础。
  * **宏平均 (Macro Average)** 与 **加权平均 (Weighted Average)**: 对于多类别（或二分类）任务，这些平均指标用于汇总各类别上的Precision, Recall, F1-Score。宏平均平等对待所有类别，加权平均则考虑了各类别样本数量的不平衡性。
* **6.2 模型性能结果 (Model Performance Results)**

  所有性能评估均在预留的**测试集**上进行，该测试集数据未参与任何模型的训练或验证过程。

  * **基模型性能 (Base Model Performance)**:
    我们首先评估了作为Stacking集成基础的三个核心基模型的性能。结果总结如下表所示（详细分类报告及混淆矩阵见附录9.2及PPT第22-24页）：

    | 模型 (Model)      | 准确率 (Accuracy) | 精确率 (Weighted Avg Precision) | 召回率 (Weighted Avg Recall) | F1分数 (Weighted Avg F1-Score) | 参考 (Reference) |
    | :---------------- | :---------------- | :------------------------------ | :--------------------------- | :----------------------------- | :--------------- |
    | XGBoost           | 0.83              | 0.83                            | 0.83                         | 0.83                           | PPT Slide 22     |
    | CatBoost          | 0.83              | 0.83                            | 0.83                         | 0.83                           | PPT Slide 23     |
    | BERT-base-Chinese | 0.84              | 0.84                            | 0.84                         | 0.84                           | PPT Slide 24     |

    初步结果显示，BERT-base-Chinese 作为预训练语言模型，在单模型中表现最佳，准确率达到84%。XGBoost和CatBoost作为强大的梯度提升模型，也取得了相当不错的性能，准确率均为83%。
  * **最终Stacking模型性能 (Final Stacking Model Performance)**:
    应用Stacking集成策略后，最终模型的性能得到了显著提升。其在测试集上的表现如下（详细分类报告及混淆矩阵见附录9.2及PPT第25页）：

    | 模型 (Model)                | 准确率 (Accuracy) | 精确率 (Weighted Avg Precision) | 召回率 (Weighted Avg Recall) | F1分数 (Weighted Avg F1-Score) | 参考 (Reference) |
    | :-------------------------- | :---------------- | :------------------------------ | :--------------------------- | :----------------------------- | :--------------- |
    | **Stacking Ensemble** | **0.86**    | **0.86**                  | **0.86**               | **0.86**                 | PPT Slide 25     |

    最终的Stacking集成模型在所有主要指标上均达到了 **86%** 的水平。
* **6.3 性能对比与讨论 (Performance Comparison and Discussion)**

  通过对比最终Stacking模型与表现最佳的单一基模型（BERT-base-Chinese），我们可以清晰地看到集成学习带来的优势（参考PPT第26页）：

  * **准确率提升**: Stacking模型的准确率达到了 **86%**，相较于BERT-base-Chinese的84%，实现了 **2个百分点** 的绝对提升（相对提升约 2.4%）。
  * **综合性能提升**: 不仅是准确率，Stacking模型在加权平均的精确率、召回率和F1分数上也均优于BERT-base-Chinese（均为0.86 vs 0.84）。这表明集成模型在整体预测的准确性（Precision）和完整性（Recall）之间取得了更好的平衡。
  * **有效性验证**: 性能的提升验证了我们采用Stacking策略的有效性。通过智能地结合XGBoost、CatBoost和BERT这三种不同类型模型的预测能力，集成模型成功地超越了任何单一模型的性能上限，展现了更强的泛化能力和预测鲁棒性。这对于处理复杂多变的TapTap用户评论数据至关重要。
* **6.4 性能评估说明 (Performance Assessment Note)**

  根据课程要求特此说明：**本部分的评分基于性能评估内容的完整性和合理性，而非模型达到的具体性能分数。**

---
