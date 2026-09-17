# 按问题查资料

[← 首页](../README.md)

以下是阅读导航，不代表方法已在相同条件下比较，也不构成性能排名。

| 我想解决的问题 | 先阅读 | 再对照 |
| --- | --- | --- |
| 想了解长上下文研究全貌 | [综述](../library/foundations/survey.md) | [教程](../library/foundations/blogs.md) |
| 想扩大模型上下文窗口 | [位置机制与外推](../library/architecture/position-encoding.md) | [训练与适配](../library/training/long-context-training.md) |
| 长上下文计算或显存成本太高 | [高效注意力](../library/architecture/efficient-attention.md) | [KV Cache](../library/inference/kv-cache.md) |
| 推理服务吞吐或延迟不理想 | [推理加速](../library/inference/inference-acceleration.md) | [模型压缩](../library/inference/model-compression.md) |
| 希望减少输入上下文 | [上下文压缩](../library/inference/context-compression.md) | [检索增强](../library/memory-retrieval/retrieval-augmented-generation.md) |
| 想比较长上下文与检索路线 | [RAG](../library/memory-retrieval/retrieval-augmented-generation.md) | [评测](../library/evaluation/benchmarks.md) |
| 想研究跨会话或持久记忆 | [长期记忆](../library/memory-retrieval/long-term-memory.md) | [长程 Agent](../library/applications/long-horizon-agents.md) |
| 想研究非标准 Transformer 路线 | [递归 Transformer](../library/architecture/recurrent-transformers.md) | [状态空间与混合架构](../library/architecture/state-space-models.md) |
| 想研究长推理或长文生成 | [长推理](../library/applications/long-reasoning.md) | [长文生成](../library/applications/long-form-text-generation.md) |
| 想研究长视频和多模态输入 | [视频与图像](../library/applications/long-video-image.md) | [多模态评测目录](../library/evaluation/README.md) |
| 想查看模型完整技术方案 | [模型技术报告](../library/training/technical-reports.md) | [训练方法](../library/training/long-context-training.md) |
| 想研究 many-shot 学习 | [上下文学习](../library/memory-retrieval/in-context-learning.md) | [基准与评测](../library/evaluation/benchmarks.md) |

阅读实验结果时同时记录：模型版本、训练与测试长度、tokenizer、任务、硬件、批量、推理配置和结果出处。不同条件的分数不直接混排。
