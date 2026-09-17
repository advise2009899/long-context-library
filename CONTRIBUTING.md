# 贡献指南

## 内容位置

- `library/`：按主题维护论文、模型报告与技术资料。
- `daily/`：按收录日记录新论文；每篇另记首次提交日期。
- `data/recent-papers.json`：近期新增论文的结构化记录。
- `guides/`：跨主题阅读路线。
- `updates/`：历史更新，日期尚未逐篇复核。

## 添加论文

1. 阅读原始论文或官方摘要，核对标题、作者、首次提交日期。
2. 以不含版本号的 arXiv ID 或 DOI 检查重复，指定一个主要主题。
3. 在结构化记录中保存官方链接、主题与简短说明；不要把摘要核查标为全文精读或实验复现。
4. 运行 `python3 scripts/render_recent.py` 更新本批次主题条目与每日页面。此脚本专用于 2026-09-17 补录，后续批次需扩展日期与范围。
5. 运行 `python3 scripts/daily_papers.py` 刷新索引，运行 `python3 scripts/plot_statistics.py` 刷新统计图。
6. 运行 `python3 scripts/check_library.py` 与 Markdown lint 检查内容和链接。

## 每日记录

使用 `python3 scripts/daily_papers.py --new YYYY-MM-DD` 创建空白页面；模板见[每日收录规则](daily/TEMPLATE.md)。自动建页不等于完成论文检索，也不会启用定时任务。

## 内容维护

保留必要的许可证与版权声明。既有正文受完整性检查保护；修正条目时同步调整核查记录，避免静默丢失论文。检索结果应注明日期口径、检索词和覆盖限制。
