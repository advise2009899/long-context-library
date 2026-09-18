# 编码器、记忆与架构适配

[← 首页](../../README.md) · [训练与数据目录](README.md)

<!-- count -->
共 **6** 个条目。
<!-- /count -->

引入编码器、记忆或混合注意力来处理长上下文；不强行归为 SFT。

<!-- papers:topic -->
- [Learning Length-Extrapolatable Recurrent Models](https://arxiv.org/abs/2609.09157) — 2026-09-08
  - 稳定反向传播中的状态信用信号，研究循环模型的长度外推。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

- [Proteus: Incremental Memory Activation for Long-Context Sequence Modeling](https://arxiv.org/abs/2608.16844) — 2026-08-17
  - 随上下文增长逐步激活记忆容量，减少早期信息对后续信息的干扰。
  - 官方摘要已核查；[收录记录](../../daily/2026/2026-09-17.md)。

<!-- /papers -->

1. <!-- entry:A6 -->
   [**Long-Context Language Modeling with Parallel Context Encoding.**](https://arxiv.org/abs/2402.16617) _Howard Yen, Tianyu Gao, Danqi Chen._ ACL 2024. [![GitHub Repo stars](https://img.shields.io/github/stars/princeton-nlp/CEPE)](https://github.com/princeton-nlp/CEPE)
   <!-- /entry -->

   **摘要已核查**：摘要核查：小型编码器分块处理输入，通过交叉注意力供冻结解码器使用。

2. <!-- entry:A14 -->
   [**E2LLM: Encoder Elongated Large Language Models for Long-Context Understanding and Reasoning.**](https://arxiv.org/abs/2409.06679) _Zihan Liao, Jun Wang, Hang Yu, Lingxiao Wei, Jianguo Li, Jun Wang, Wei Zhang._ Arxiv 2024.
   <!-- /entry -->

   **摘要已核查**：摘要核查：编码器将分块压缩为软提示，再与解码器对齐；包含重建和指令微调目标。

3. <!-- entry:A15 -->
   [**A Little Goes a Long Way: Efficient Long Context Training and Inference with Partial Contexts.**](https://arxiv.org/abs/2410.01485) _Suyu Ge, Xihui Lin, Yunan Zhang, Jiawei Han, Hao Peng._ Arxiv 2024.
   <!-- /entry -->

   **摘要已核查**：摘要核查：LongGen 将混合注意力架构与长度扩展训练结合，归入架构适配。

4. <!-- entry:C9 -->
   [**UIO-LLMs: Unbiased Incremental Optimization for Long-Context LLMs.**](https://arxiv.org/abs/2406.18173) _Wenhao Li, Mingbao Lin, Yunshan Zhong, Shuicheng Yan, Rongrong Ji._ Arxiv 2024. [![GitHub Repo stars](https://img.shields.io/github/stars/wenhaoli-xmu/UIO-LLMs)](https://github.com/wenhaoli-xmu/UIO-LLMs)
   <!-- /entry -->

   **摘要已核查**：已撤回：arXiv 当前页面标明作者撤回。保留原条目供追溯，不作为有效性推荐。方法涉及记忆增强模型的增量优化。
