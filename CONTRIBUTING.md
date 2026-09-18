# 贡献指南

## 添加论文

在仓库根目录执行，下例日期可替换为任意起止日：

```bash
python3 scripts/collect_papers.py fetch --from 2026-09-17 --to 2026-09-18 --output /tmp/papers-review.json
```

检索按 arXiv 首次提交日期（UTC），自动翻页，并与主题库、每日记录和已审核数据按 arXiv ID 去重。检索结果只保存为候选清单，不直接进入论文库；关键词结果不保证覆盖全部相关论文。已收录论文放在 `existing_papers` 中供版本核查。

阅读官方摘要与元数据后，在候选清单 `papers` 中填写：

- `status`：确认收录时设为 `approved`；其余保留 `pending` 或改为 `rejected`。
- `target`：已有主题文件，例如 `library/inference/kv-cache.md`。
- `section`：完整小节标题，例如 `#### 3.3 Offloading / Hierarchical Cache`；没有小节的主题留空。
- `summary_zh`：简短中文说明，避免未经核实的性能结论。

审核完成后导入，并刷新所有展示：

```bash
python3 scripts/collect_papers.py import /tmp/papers-review.json --collected 2026-09-18
python3 scripts/render_recent.py
python3 scripts/plot_statistics.py
python3 scripts/check_library.py
```

重复导入会跳过已有 ID。渲染脚本按 `collected` 自动创建每日页，保留生成区域以外的手写笔记；主题页按 `section` 分类，已核实提交日期的条目倒序展示。缺少精确日期的历史条目保留原顺序。

## 数据与统计

`data/recent-papers.json` 保存已审核论文；`scripts/paper_data.py` 为主题页、首页和统计图提供统一计数。`data/library-baseline.json` 与 `data/training-index.json` 保存历史条目的完整性索引。统计单位为收录条目，不宣称全库已去重。

不要直接编辑 `papers`、`count` 或 `daily-papers` 注释标记包围的生成区域；在数据文件中修改后重新渲染。历史正文修正需同步核查索引，避免静默丢失条目。

## 每日记录

`python3 scripts/daily_papers.py --new YYYY-MM-DD` 可以单独建立空白工作页。收录日期与首次提交日期分开记录；没有候选结果不代表当天没有相关论文。本仓库未启用无人审核的定时发布。

保留许可证与论文作者信息。摘要核查不等于全文精读或实验复现。
