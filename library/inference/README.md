# 推理效率与压缩

[← 首页](../../README.md) · [完整目录](../README.md)

KV Cache、上下文压缩、模型压缩和推理系统。

## [3. KV-Cache Optimization](kv-cache.md)

- [3.1 Eviction / Selection](kv-cache.md#31-eviction--selection)
  - [3.1.1 Attention-Score & Heavy-Hitter Eviction](kv-cache.md#311-attention-score--heavy-hitter-eviction)
  - [3.1.2 Streaming & Sliding-Window Retention](kv-cache.md#312-streaming--sliding-window-retention)
  - [3.1.3 Query-Aware & Learnable Retention](kv-cache.md#313-query-aware--learnable-retention)
  - [3.1.4 Layer-Budget / Merge / Hybrid Eviction](kv-cache.md#314-layer-budget--merge--hybrid-eviction)
- [3.2 Quantization / Compression](kv-cache.md#32-quantization--compression)
- [3.3 Offloading / Hierarchical Cache](kv-cache.md#33-offloading--hierarchical-cache)
- [3.4 Architectural KV Reduction & Cache Sharing](kv-cache.md#34-architectural-kv-reduction--cache-sharing)

## [11. Context Compression](context-compression.md)

- [11.1 Token / Prompt Compression](context-compression.md#111-token--prompt-compression)
  - [11.1.1 Hard Prompt & Token Pruning](context-compression.md#1111-hard-prompt--token-pruning)
  - [11.1.2 Soft Prompt / Gist / Latent Compression](context-compression.md#1112-soft-prompt--gist--latent-compression)
  - [11.1.3 Visual & Multimodal Token Compression](context-compression.md#1113-visual--multimodal-token-compression)
  - [11.1.4 RAG / KV-Aware Compression](context-compression.md#1114-rag--kv-aware-compression)

## [12. Model Compression for Long Context](model-compression.md)

- [12.1 Quantization](model-compression.md#121-quantization)
- [12.2 Distillation / Pruning](model-compression.md#122-distillation--pruning)

## [17. Inference Acceleration & Serving](inference-acceleration.md)

- [17.1 Speculative & Parallel Decoding](inference-acceleration.md#171-speculative--parallel-decoding)
- [17.2 Quantization-Aware Long-Context Inference](inference-acceleration.md#172-quantization-aware-long-context-inference)
- [17.3 Prefill & Sparse Attention Acceleration](inference-acceleration.md#173-prefill--sparse-attention-acceleration)
- [17.4 System & Serving Optimization](inference-acceleration.md#174-system--serving-optimization)
