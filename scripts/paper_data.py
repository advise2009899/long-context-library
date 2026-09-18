"""Shared bibliography data, validation and counts."""
from pathlib import Path
from collections import Counter
from datetime import date, datetime
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def read_json(name):
    return json.loads((ROOT / name).read_text())

def strip_generated(text):
    text = text.split('<!-- curated-additions -->')[0].rstrip() + '\n'
    return re.sub(r'<!-- (?:papers:[^\n]+|count) -->\n.*?<!-- /(?:papers|count) -->\n\n', '', text, flags=re.S)

def records(rows=None):
    rows = rows if rows is not None else read_json('data/recent-papers.json')
    ids = set()
    for row in rows:
        aid = row['arxiv_id']
        if not re.fullmatch(r'\d{4}\.\d{4,5}', aid) or aid in ids:
            raise ValueError(f'Invalid or duplicate arXiv ID: {aid}')
        ids.add(aid)
        date.fromisoformat(row['collected'])
        published = datetime.fromisoformat(row['published'].replace('Z', '+00:00')).date()
        if published > date.fromisoformat(row['collected']):
            raise ValueError(f'Publication follows collection: {aid}')
        target = ROOT / row['target']
        if target.resolve().parent.parent != (ROOT / 'library').resolve() or not target.is_file():
            raise ValueError(f'Invalid topic: {row["target"]}')
        section = row.get('section', '')
        if section and section not in strip_generated(target.read_text()).splitlines():
            raise ValueError(f'Missing section: {aid}: {section}')
        if row['url'] != 'https://arxiv.org/abs/' + aid:
            raise ValueError(f'ID/link mismatch: {aid}')
    return rows

def topic_counts():
    training = read_json('data/training-index.json')['records']
    base = Counter(row['target'] for row in training)
    for chapter in read_json('data/library-baseline.json')['chapters']:
        if chapter['id'] != 7:
            base[chapter['path']] = len(re.findall(r'^\d+\.\s', strip_generated((ROOT / chapter['path']).read_text()), re.M))
    counts = base.copy()
    counts.update(row['target'] for row in records())
    return counts

def known_ids():
    text = '\n'.join(p.read_text() for folder in ('library', 'daily') for p in (ROOT / folder).rglob('*.md'))
    return set(re.findall(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})', text)) | {r['arxiv_id'] for r in records()}
