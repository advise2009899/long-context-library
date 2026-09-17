"""Check bibliography integrity and relative Markdown links (offline, stdlib only)."""
from pathlib import Path
import hashlib
import json
import re
from collections import Counter
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'data/library-baseline.json').read_text())
errors = []
entries = 0
for item in manifest['chapters']:
    path = ROOT / item['path']
    if not path.exists():
        errors.append(f"Missing chapter: {item['path']}")
        continue
    current = path.read_text().split('<!-- curated-additions -->')[0].rstrip() + '\n'
    if item['id'] == 7:
        continue
    entries += len(re.findall(r'^\d+\.\s', current, re.M))
    body = '\n'.join(current.splitlines()[3:]).rstrip()
    if hashlib.sha256(body.encode()).hexdigest() != item['body_sha256']:
        errors.append(f"Chapter body changed: {item['path']}")
# The training chapter is split; compare entry text, independent of numbering.
registry = json.loads((ROOT / 'data/training-index.json').read_text())
records = registry['records']
expected_keys = [f'A{i}' for i in range(1, 29)] + [f'B{i}' for i in range(1, 22)] + [f'C{i}' for i in range(1, 15)]
if Counter(row['source_key'] for row in records) != Counter(expected_keys):
    errors.append('Training registry has missing or duplicate source keys')
found = {}
for path in ROOT.glob('library/*/*.md'):
    for key, body in re.findall(r'<!-- entry:(\w+) -->\n(.*?)\n\s*<!-- /entry -->', path.read_text(), re.S):
        if key in found:
            errors.append(f'Duplicate entry: {key}')
        found[key] = (path.relative_to(ROOT).as_posix(), re.sub(r'^\d+\. ', '', body).strip())
if Counter(found.keys()) != Counter(expected_keys):
    errors.append('Training pages have missing or unexpected entry markers')
for row in records:
    key = row['source_key']
    if key not in found:
        continue
    target, body = found[key]
    if target != row['target'] or hashlib.sha256(body.encode()).hexdigest() != row['entry_sha256']:
        errors.append(f'Entry target or content mismatch: {key}')
entries += len(found)
if entries != manifest['numbered_entries']:
    errors.append(f"Entry count changed: {entries} vs {manifest['numbered_entries']}")
# Verify curated additions independently of the historical bibliography.
from datetime import datetime
additions = json.loads((ROOT / 'data/recent-papers.json').read_text())
ids = [row['arxiv_id'] for row in additions]
if len(ids) != len(set(ids)):
    errors.append('Duplicate curated arXiv IDs')
baseline = '\n'.join(p.read_text().split('<!-- curated-additions -->')[0]
                     for p in ROOT.glob('library/*/*.md'))
for row in additions:
    day = datetime.fromisoformat(row['published'].replace('Z', '+00:00')).date().isoformat()
    if not '2026-08-14' <= day <= '2026-09-17':
        errors.append(f"Date outside backfill range: {row['arxiv_id']}")
    if row['arxiv_id'] in baseline:
        errors.append(f"Already in bibliography: {row['arxiv_id']}")
    target = ROOT / row['target']
    if not target.exists() or target.read_text().count(row['url']) != 1:
        errors.append(f"Missing or duplicate topic entry: {row['arxiv_id']}")
    daily = ROOT / 'daily/2026/2026-09-17.md'
    if daily.read_text().count(row['url']) != 1:
        errors.append(f"Missing or duplicate daily entry: {row['arxiv_id']}")
for path in ROOT.rglob('*.md'):
    if '.git' in path.parts:
        continue
    for link in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
        if link.startswith(('https:', 'http:', 'mailto:', 'data:', '#')):
            continue
        target = unquote(link.split('#', 1)[0])
        if target and not (path.parent / target).exists():
            errors.append(f"Broken relative link: {path.relative_to(ROOT)} -> {link}")
if (ROOT / 'README.md').stat().st_size > 512000:
    errors.append('README exceeds GitHub rendering limit')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(manifest["chapters"])} chapters; {entries} numbered entries; relative file links valid.')
print('PASS: chapter and training-entry content hashes verified without Git history.')

print(f'PASS: {len(additions)} curated additions, dates and unique topic/daily links checked.')
