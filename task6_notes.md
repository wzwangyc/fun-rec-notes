## 学习笔记：HSTU 的工程演进与 GenRank 革命

### 1. 寻找生成式推荐的本质
通过在数千亿真实日志上的实验，小红书团队确定了生成式推荐的核心竞争力：

* **自回归机制是灵魂：** 使用 Causal Mask 强制模型学习行为的因果结构，能有效抑制模型对稀疏特征（如长尾 ID）的死记硬背。如果允许双向 Attention，模型会学到虚假的未来关联，导致性能下降。
* **User-level 组织的价值：** 相比单样本训练，序列化组织更多是带来了工程上的便利，例如更高的训练吞吐量和更容易实现的 KV Caching。



### 2. Action-Oriented：序列长度的减半革命
HSTU 的交织建模 $[x_0, a_0, x_1, a_1]$ 导致序列极长，计算开销巨大。GenRank 提出将行为（Action）作为主体，物品（Item）作为属性融合：

* **融合逻辑：** 将物品 Embedding $\phi(x_i)$ 与行为 Embedding $\phi(a_i)$ 直接相加。
* **计算收益：** 序列长度减半，Attention 计算量直接下降 75%，训练速度提升约 80%。
* **信息对齐：** 在 Token 级别完成交互，减轻了 Attention 层的建模负担。



### 3. 位置与时间：从 $O(N^2)$ 到 $O(N)$
为了解决相对注意力偏置（RAB）带来的内存带宽瓶颈，GenRank 重新定义了时空编码方案：

###### 绝对信息编码 (Lightweight Embeddings)
采用三套 $O(N)$ 复杂度的 Embedding 叠加：
* **Position Embeddings:** 记录序列索引。
* **Request Index Embeddings:** 区分用户不同的打开 App 频次（Session 边界）。
* **Pre-Request Time Embeddings:** 捕捉跨请求的时间间隔，实现自适应衰减。

###### 相对信息编码 (Linear Biases)
借鉴 ALiBi 的思想，直接在 Attention Score 中加入无参数的线性惩罚：
$$score_{i,j} = \frac{q_i \cdot k_j^T}{\sqrt{d}} - m_p \cdot (p_i - p_j) - m_t \cdot \text{bucket}(t_i - t_j)$$
这种设计利用了距离越远、时间越久影响越小这一强先验，省去了昂贵的学习成本。



### 4. 架构设计原则：参数 vs 规则
GenRank 的成功验证了一个关键哲学：
* **参数建模：** 用于处理复杂的、非线性的模式（如物品与行为的语义融合）。
* **规则编码：** 用于处理普适的、近似线性的规律（如时间与距离的衰减）。

通过这种原理驱动的优化，GenRank 在保持 HSTU 核心优势的前提下，实现了近 100% 的训练加速。
