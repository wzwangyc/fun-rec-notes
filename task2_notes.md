## 学习笔记：生成式架构的基石 (Transformer & Diffusion)

### 1\. Transformer 架构：序列建模的王者

Transformer 将推荐问题建模为 **序列生成任务**，利用自注意力机制捕捉用户行为的长程依赖。

  * **核心组件：自注意力机制 (Self-Attention)**
      * **Q (Query):** 当前时刻的预测需求。
      * **K (Key):** 历史行为的索引特征。
      * **V (Value):** 历史行为的实际内容。
      * **公式:** $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$
  * **多头注意力 (Multi-Head Attention):** 类似金融中的“多因子模型”，不同头可以并行关注品牌、类别、价格等不同维度的特征。
  * **位置编码 (Positional Encoding):** 解决 Transformer 对顺序不敏感的问题。在 FinTech 场景中，**时间间隔 (Time Interval)** 的编码比绝对位置更重要。

-----

### 2\. 两种范式对比：Encoder-Decoder vs. Decoder-Only

| 维度 | Encoder-Decoder (如 T5, TIGER) | Decoder-Only (如 GPT, RecGPT) |
| :--- | :--- | :--- |
| **结构** | 双塔设计，包含交叉注意力 | 单塔设计，统一因果注意力 |
| **优势** | 擅长处理异构输入（如多模态） | 参数效率高，易于 Scaling，生态兼容性强 |
| **推荐应用** | 复杂的多任务推荐 | 序列续写、大规模预训练推荐模型 |

-----

### 3\. Diffusion 模型：迭代去噪的新视角

不同于自回归的逐个生成，Diffusion 通过从随机噪声中恢复数据来生成推荐。

  * **前向过程:** 逐渐加噪（数据 $\to$ 噪声）。
  * **反向过程:** 学习去噪（噪声 $\to$ 数据）。
  * **FinTech 应用:** 可用于金融序列的 **数据增强** 或生成更鲁棒的用户 Embedding，缓解交易数据的稀疏性。
