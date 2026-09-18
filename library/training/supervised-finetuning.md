# 指令微调与对齐

[← 首页](../../README.md) · [训练与数据目录](README.md)

<!-- count -->
共 **10** 个条目。
<!-- /count -->

长文指令学习、参数高效微调与自改进；自改进可同时关联偏好优化。

<!-- papers:topic -->
- [Fine-Tuning a KV Cache Concatenation-Aware Model or Recomputing KV Caches? Why Not Both?](https://arxiv.org/abs/2609.09768) — 2026-09-09
  - 将感知 KV 拼接的微调与选择性缓存重算结合，用于长上下文 RAG。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

- [Learning how to Forget: Fine-tuning for Long-Context Sparse Attention](https://arxiv.org/abs/2608.19920) — 2026-08-20
  - 在稀疏注意力下微调模型，让模型与 KV 选择策略共同适配。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

- [Beyond Teacher Likelihood: Group-Calibrated On-Policy Distillation for Long-Context Reasoning](https://arxiv.org/abs/2608.19181) — 2026-08-19
  - 校准教师 token 指导与任务验证奖励，改进长上下文在线蒸馏。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

<!-- /papers -->

1. <!-- entry:B1 -->
   [**LongLoRA: Efficient Fine-tuning of Long-Context Large Language Models.**](https://arxiv.org/abs/2309.12307) _Yukang Chen, Shengju Qian, Haotian Tang, Xin Lai, Zhijian Liu, Song Han, Jiaya Jia._ ICLR 2024 Oral. [![GitHub Repo stars](https://img.shields.io/github/stars/dvlab-research/LongLoRA)](https://github.com/dvlab-research/LongLoRA)
   <!-- /entry -->

   **初步归档**。

2. <!-- entry:B3 -->
   [**Long Context Alignment with Short Instructions and Synthesized Positions.**](https://arxiv.org/abs/2405.03939) _Wenhao Wu, Yizhong Wang, Yao Fu, Xiang Yue, Dawei Zhu, Sujian Li._ Arxiv 2024. [![GitHub Repo stars](https://img.shields.io/github/stars/nightdessert/SkipAlign)](https://github.com/nightdessert/SkipAlign)
   <!-- /entry -->

   **初步归档**。

3. <!-- entry:B5 -->
   [**ChatQA 2: Bridging the Gap to Proprietary LLMs in Long Context and RAG Capabilities.**](https://arxiv.org/abs/2407.14482) _Peng Xu, Wei Ping, Xianchao Wu, Zihan Liu, Mohammad Shoeybi, Bryan Catanzaro._ Arxiv 2024.
   <!-- /entry -->

   **初步归档**。

4. <!-- entry:B8 -->
   [**Large Language Models Can Self-Improve in Long-context Reasoning.**](https://arxiv.org/abs/2411.08147) _Siheng Li, Cheng Yang, Zesen Cheng, Lemao Liu, Mo Yu, Yujiu Yang, Wai Lam._ Arxiv 2024. [![GitHub Repo stars](https://img.shields.io/github/stars/SihengLi99/SEALONG)](https://github.com/SihengLi99/SEALONG)
   <!-- /entry -->

   **摘要已核查**：摘要核查：对多个输出评分，用于 SFT 或偏好优化；本页是主归档，两种阶段均适用。

5. <!-- entry:B16 -->
   [**Pause-Tuning for Long-Context Comprehension: A Lightweight Approach to LLM Attention Recalibration.**](https://arxiv.org/abs/2502.20405) _James Begin, Namit Agrawal, Eshan Singh, Yicheng Fu, Sean O'Brien, Vasu Sharma, Kevin Zhu._ Arxiv 2025. [![GitHub Repo stars](https://img.shields.io/github/stars/microsoft/LongRoPE](https://anonymous.4open.science/r/LITM-PauseTokens-7357)
   <!-- /entry -->

   **初步归档**。

6. <!-- entry:B19 -->
   [**Long-Short Alignment for Effective Long-Context Modeling in LLMs.**](https://arxiv.org/abs/2506.11769) _Tianqi Du, Haotian Huang, Yifei Wang, Yisen Wang._ Arxiv 2025. [![GitHub Repo stars](https://img.shields.io/github/stars/PKU-ML/LongShortAlignment)](https://github.com/PKU-ML/LongShortAlignment)
   <!-- /entry -->

   **初步归档**。

7. <!-- entry:B20 -->
   [**Make Your LLM Fully Utilize the Context.**](https://arxiv.org/abs/2404.16811) _Shengnan An, Zexiong Ma, Zeqi Lin, Nanning Zheng, Jian-Guang Lou._ Arxiv 2024. [![GitHub Repo stars](https://img.shields.io/github/stars/microsoft/FILM)](https://github.com/microsoft/FILM)
   <!-- /entry -->

   **初步归档**。
