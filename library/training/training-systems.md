# 训练系统与效率

[← 首页](../../README.md) · [训练与数据目录](README.md)

<!-- count -->
共 **10** 个条目。
<!-- /count -->

并行、分片、激活显存与高效训练实现。

<!-- papers:topic -->
- [Flattening Every Memory Peak in Long-Context Mixture-of-Experts Training](https://arxiv.org/abs/2609.14306) — 2026-09-13
  - 联合约束专家分发、词表投影、检查点和优化器的内存峰值。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

- [Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training](https://arxiv.org/abs/2609.07108) — 2026-09-07
  - 结合上下文并行与流水线特征传输，在线共同训练 RL 推测解码草稿。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

- [BASP: Communication-Efficient Batch-Aware Sequence Parallelism for LLM Training](https://arxiv.org/abs/2609.03151) — 2026-09-02
  - 利用微批结构划分序列并行组，减少长序列训练通信。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

<!-- /papers -->

1. <!-- entry:A18 -->
   [**Adjoint sharding for very long context training of state space models.**](https://arxiv.org/abs/2501.00692) _Xingzi Xu, Amir Tavanaei, Kavosh Asadi, Karim Bouyarmane._ Arxiv 2025.
   <!-- /entry -->

   **初步归档**。

2. <!-- entry:A19 -->
   [**Sliding Window Attention Training for Efficient Large Language Models.**](https://arxiv.org/abs/2502.18845) _Zichuan Fu, Wentao Song, Yejing Wang, Xian Wu, Yefeng Zheng, Yingying Zhang, Derong Xu, Xuetao Wei, Tong Xu, Xiangyu Zhao._ Arxiv 2025. [![GitHub Repo stars](https://img.shields.io/github/stars/Lyun0912-wu/LongAttn](https://anonymous.4open.science/r/SWAT-attention/README.md)
   <!-- /entry -->

   **初步归档**。

3. <!-- entry:A20 -->
   [**ByteScale: Efficient Scaling of LLM Training with a 2048K Context Length on More Than 12,000 GPUs.**](https://arxiv.org/abs/2502.21231) _Hao Ge, Junda Feng, Qi Huang, Fangcheng Fu, Xiaonan Nie, Lei Zuo, Haibin Lin, Bin Cui, Xin Liu._ Arxiv 2025.
   <!-- /entry -->

   **初步归档**。

4. <!-- entry:A23 -->
   [**Arctic Long Sequence Training: Scalable And Efficient Training For Multi-Million Token Sequences.**](https://arxiv.org/abs/2506.13996) _Stas Bekman, Samyam Rajbhandari, Michael Wyatt, Jeff Rasley, Tunji Ruwase, Zhewei Yao, Aurick Qiao, Yuxiong He._ Arxiv 2025. [![GitHub Repo stars](https://img.shields.io/github/stars/snowflakedb/ArcticTraining)](https://github.com/snowflakedb/ArcticTraining/blob/main/projects/sequence-parallelism/README.md)
   <!-- /entry -->

   **初步归档**。

5. <!-- entry:A24 -->
   [**Heterogeneous Parallelism for Multimodal Large Language Model Training.**](https://arxiv.org/abs/2605.27678) _Yashaswi Karnati, Kamran Jafari, Akash Mehra, Li Ding, Pranav Prashant Thombre, Ali Roshan Ghias, Shifang Xu, Parth Mannan, Yu Yao, Hao Wu, Eric Harper, Ashwath Aithal, Nima Tajbakhsh._ Arxiv 2026.
   <!-- /entry -->

   **初步归档**。

6. <!-- entry:A25 -->
   [**Long-Context Fine-Tuning with Limited VRAM.**](https://arxiv.org/abs/2607.15105) _Vladimir Fedosov, Aleksandr Sazhin, Artemiy Grinenko, Frank Woernle._ Arxiv 2026.
   <!-- /entry -->

   **初步归档**。

7. <!-- entry:B9 -->
   [**LeMo: Enabling LEss Token Involvement for MOre Context Fine-tuning.**](https://arxiv.org/abs/2501.09767) _Tuowei Wang, Xingyu Chen, Kun Li, Ting Cao, Ju Ren, Yaoxue Zhang._ Arxiv 2025.
   <!-- /entry -->

   **摘要已核查**：摘要核查：LeMo 优化 token 参与、激活显存与内核，是微调系统。
