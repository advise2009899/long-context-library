"""Render reviewed records into topic sections, daily pages and counts."""
from collections import defaultdict
import re
from paper_data import ROOT, records, strip_generated, topic_counts
from daily_papers import rebuild


def render():
    rows = records()  # Validate everything before writing.
    counts = topic_counts()
    groups = defaultdict(list)
    days = defaultdict(list)
    for row in rows:
        groups[(row['target'], row.get('section', ''))].append(row)
        days[row['collected']].append(row)
    outputs = {}
    for target, count in counts.items():
        path = ROOT / target
        text = strip_generated(path.read_text())
        # Remove obsolete hand-maintained totals in the training pages.
        text = re.sub(r'^共 \d+ 个条目。[^\n]*\n\n', '', text, flags=re.M)
        for (name, heading), entries in groups.items():
            if name != target:
                continue
            block = f'<!-- papers:{heading or "topic"} -->\n'
            for row in sorted(entries, key=lambda r: (r['published'], r['arxiv_id']), reverse=True):
                day = row['collected']
                block += f"- [{row['title']}]({row['url']}) — {row['published'][:10]}\n"
                block += f"  - {row['summary_zh']}\n"
                block += f'  - 官方摘要已核查；[收录记录](../../daily/{day[:4]}/{day}.md)。\n\n'
            block += '<!-- /papers -->\n\n'
            if heading:
                text = text.replace(heading + '\n\n', heading + '\n\n' + block, 1)
            else:
                match = re.search(r'^\d+\. ', text, re.M)
                if match:
                    text = text[:match.start()] + block + text[match.start():]
                else:
                    text += '\n' + block
        # Common count placement immediately after the backlink.
        lines = text.splitlines(keepends=True)
        lines.insert(4, f'<!-- count -->\n共 **{count}** 个条目。\n<!-- /count -->\n\n')
        outputs[path] = ''.join(lines)
    for day, entries in days.items():
        path = ROOT / 'daily' / day[:4] / f'{day}.md'
        block = '<!-- daily-papers -->\n'
        for row in sorted(entries, key=lambda r: (r['published'], r['arxiv_id']), reverse=True):
            title = (ROOT / row['target']).read_text().splitlines()[0].lstrip('# ')
            authors = ', '.join(row['authors'][:3]) + (' et al.' if len(row['authors']) > 3 else '')
            block += f"- Paper: [{row['title']}]({row['url']})\n"
            block += f"  - 作者：{authors}；首次提交：{row['published'][:10]}；arXiv：{row['arxiv_id']}。\n"
            block += f"  - 主题：[{title}](../../{row['target']})。\n"
            block += f"  - 摘要说明：{row['summary_zh']}\n\n"
        block += '<!-- /daily-papers -->'
        text = path.read_text() if path.exists() else f'''# {day} · 每日论文

[← 每日索引](../README.md) · [知识库首页](../../README.md)

- 日期口径：收录日期（Asia/Shanghai）；首次提交日期按 UTC。
- 状态：已记录；已核查官方元数据与摘要，未复现实验。

## 新论文

'''
        if '<!-- daily-papers -->' in text:
            text = re.sub(r'<!-- daily-papers -->.*?<!-- /daily-papers -->', lambda m: block, text, flags=re.S)
        else:
            # Never overwrite manual entries; stop for a human merge if IDs overlap.
            if any(row['url'] in text for row in entries):
                raise ValueError(f'Manual records overlap generated records: {path}')
            text = text.rstrip() + '\n\n' + block + '\n'
        outputs[path] = text
    p = ROOT / 'library/training/README.md'
    text = p.read_text()
    for target,count in counts.items():
        if target.startswith('library/training/'):
            text = re.sub(r'(\]\('+re.escape(target.split('/')[-1])+r'\) \| )\d+',lambda m:m[1]+str(count),text)
    outputs[p] = text
    p = ROOT / 'README.md'
    text = p.read_text()
    blogs = counts['library/foundations/blogs.md']; total = sum(counts.values())-blogs
    text = re.sub(r'共 \*\*[\d,]+ 个论文及报告条目\*\*',f'共 **{total:,} 个论文及报告条目**',text)
    text = re.sub(r'另收录 \*\*\d+ 个博客与教程条目\*\*',f'另收录 **{blogs} 个博客与教程条目**',text)
    if days:
        latest = max(days)
        text = re.sub(r'\[\d{4}-\d{2}-\d{2} 收录页\]\(daily/[^)]+\)',f'[{latest} 收录页](daily/{latest[:4]}/{latest}.md)',text)
    outputs[p] = text
    for path,text in outputs.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text)
    rebuild()
    print(f'Rendered {len(rows)} reviewed papers across {len(days)} collection dates; counts updated.')

if __name__ == '__main__':
    render()
