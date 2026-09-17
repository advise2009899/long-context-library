"""Render curated additions from data/recent-papers.json (offline)."""
from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[1]
MARKER = '<!-- curated-additions -->'
records = json.loads((ROOT / 'data/recent-papers.json').read_text())
groups = defaultdict(list)
for row in records:
    groups[row['target']].append(row)
for target, rows in groups.items():
    path = ROOT / target
    text = path.read_text().split(MARKER)[0].rstrip()
    text += '\n\n' + MARKER + '\n\n## 近期补录\n\n'
    for row in sorted(rows, key=lambda r: r['published'], reverse=True):
        text += f"- [{row['title']}]({row['url']}) — {row['published'][:10]}\n"
        text += f"  - {row['summary_zh']}\n"
        text += '  - 核查：官方元数据与摘要；[每日收录](../../daily/2026/2026-09-17.md)。\n\n'
    path.write_text(text.rstrip() + '\n')
page = '''# 2026-09-17 · 每日论文

[← 每日索引](../README.md) · [知识库首页](../../README.md)

- 日期口径：收录日期（Asia/Shanghai）；每篇另列 arXiv 首次提交日期（UTC）。
- 状态：已记录；本次为历史区间补录，不代表论文均发表于今天。
- 范围：2026-08-14—2026-09-17；[检索说明与按发表日期索引](../backfill-2026-09-17.md)。
- 核查程度：官方元数据与摘要，未全文精读、未复现实验。

## 新收录论文

'''
for row in sorted(records, key=lambda r: r['published'], reverse=True):
    authors = ', '.join(row['authors'][:3]) + (' et al.' if len(row['authors']) > 3 else '')
    title = (ROOT / row['target']).read_text().splitlines()[0].lstrip('# ')
    page += f"- Paper: [{row['title']}]({row['url']})\n"
    page += f"  - 作者：{authors}；首次提交：{row['published'][:10]}；arXiv：{row['arxiv_id']}。\n"
    page += f"  - 主题：[{title}](../../{row['target']})。\n"
    page += f"  - 摘要说明：{row['summary_zh']}\n\n"
(ROOT / 'daily/2026/2026-09-17.md').write_text(page.rstrip() + '\n')
report = f'''# 2026-08-14—2026-09-17 论文补录

[← 每日索引](README.md) · [本次收录详情](2026/2026-09-17.md)

本次从 arXiv 官方 API 检索 273 条候选，筛选 65 篇直接相关论文，其中 3 篇已收录，新增 **{len(records)} 篇**。新增论文同时进入对应主题页。

## 检索口径

- 执行日期：2026-09-17；范围按 arXiv v1 首次提交日期（UTC）判断，包含起止日期。
- 检索词：`long context`、`long-context`、`KV cache`、`context compression`，以 OR 组合，限定 `submittedDate`。
- 官方入口：[arXiv API](https://export.arxiv.org/api/query)；[完整查询、候选标题与检索记录](../data/search-2026-09-17.json)。
- 收录标准：研究重点直接涉及长上下文训练、注意力、推理缓存、压缩、记忆、长程 Agent 或相应评测。
- 核查：标题、作者、首次提交日期与摘要；按去除版本号的 arXiv ID 检查主题库重复。
- 覆盖限制：关键词检索与人工筛选，**不保证穷尽该时段全部相关论文**。候选列表最新首次提交日为 2026-09-16；09-17 可能存在尚未公布或尚未索引的论文，不能解读为当天没有论文。
- 首次提交早于范围、仅在范围内更新的论文，不算本次新论文。收录日为 09-17，不把补录行为倒填为历史每日检索。

## 已收录，未重复添加

- [SimpleOPD](https://arxiv.org/abs/2608.14277)
- [KV Cache Compression Through the Lens of Transform Coding](https://arxiv.org/abs/2608.14191)
- [MemoryLake on MemoryArena](https://arxiv.org/abs/2608.13883)

## 新增论文 · 按首次提交日

| 首次提交日期（UTC） | 论文 | 主题 |
| --- | --- | --- |
'''
for row in sorted(records, key=lambda r: r['published'], reverse=True):
    title = (ROOT / row['target']).read_text().splitlines()[0].lstrip('# ')
    report += f"| {row['published'][:10]} | [{row['title']}]({row['url']}) | [{title}](../{row['target']}) |\n"
(ROOT / 'daily/backfill-2026-09-17.md').write_text(report)
print(f'Rendered {len(records)} additions across {len(groups)} topics')
