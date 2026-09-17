"""Create daily pages and rebuild the date index; no network requests."""
from pathlib import Path
from datetime import date
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / 'daily'

def new_page(day):
    parsed = date.fromisoformat(day)
    path = DAILY / str(parsed.year) / f'{day}.md'
    if path.exists():
        print(f'Already exists; kept unchanged: {path.relative_to(ROOT)}')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'''# {day} · 每日论文

[← 每日索引](../README.md) · [知识库首页](../../README.md)

- 日期口径：收录日期（Asia/Shanghai）
- 状态：待收录，尚未执行当天检索；不代表当天没有新论文。

## 新论文

<!-- 每篇使用模板中的 Paper 主链接；阅读笔记和归档链接写在其下。 -->

## 已收录论文的新版本

<!-- 使用 Revision 主链接，并注明原论文及本次变化。 -->

## 博客与项目动态

<!-- 使用 Blog 主链接，与论文分别统计。 -->
''')
    print(f'Created: {path.relative_to(ROOT)}')

def rebuild():
    pages = sorted(DAILY.glob('[0-9][0-9][0-9][0-9]/????-??-??.md'), reverse=True)
    lines = []
    for page in pages:
        date.fromisoformat(page.stem)
        text = page.read_text()
        n = len(re.findall(r'^- Paper: \[', text, re.M))
        b = len(re.findall(r'^- Blog: \[', text, re.M))
        v = len(re.findall(r'^- Revision: \[', text, re.M))
        status = '历史记录 · 日期未复核' if '日期口径：历史记录日期' in text else ('待收录' if '状态：待收录' in text else '已记录')
        lines.append(f'| [{page.stem}]({page.relative_to(DAILY).as_posix()}) | {n} | {v} | {b} | {status} |')
    (DAILY / 'README.md').write_text('''# 每日论文

[← 知识库首页](../README.md) · [收录模板与规则](TEMPLATE.md) · [历史更新](../updates/README.md)

这里按日期保存当天发现的论文、版本更新和项目动态；主题归类仍在知识库目录维护。

**新记录按收录日期（Asia/Shanghai）建档**，每篇另外注明论文首次发表日期，避免把“今天发现”当成“今天发表”。历史页面沿用历史记录日期，尚未逐条核查发布日期。

历史记录与新收录条目共同保存在此处。待收录页面是空白工作页；本目录尚未启用自动检索或定时更新。

## 日期索引

| 日期 | 论文条目 | 版本更新 | 博客 | 状态 |
| --- | ---: | ---: | ---: | --- |
''' + '\n'.join(lines) + '''

## 日常使用

在仓库根目录执行：

```bash
python3 scripts/daily_papers.py --new YYYY-MM-DD
```

从模板复制条目到当天页面，填好来源与发表日期；完成检索后，将页面状态改为“已记录”。再次执行下列命令刷新统计：

```bash
python3 scripts/daily_papers.py
```

相同日期重复创建不会覆盖已有记录。按 arXiv ID（去除版本号）或 DOI 识别同一论文：首次出现放“新论文”，后续修订放“新版本”并链接首次记录。历史条目保留原文，索引统计为条目数而非跨日去重论文数。
''')
    print(f'Indexed {len(pages)} daily pages')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--new', metavar='YYYY-MM-DD')
    args = parser.parse_args()
    DAILY.mkdir(exist_ok=True)
    if args.new:
        new_page(args.new)
    rebuild()
