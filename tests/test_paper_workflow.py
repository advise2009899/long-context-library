"""Regression tests for date-aware importing and non-destructive rendering."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import paper_data
import collect_papers
import render_recent
import daily_papers

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        source=paper_data.ROOT
        for directory in ('data','library','daily'):
            shutil.copytree(source/directory,self.root/directory)
        shutil.copy(source/'README.md',self.root/'README.md')
        self.patches=[patch.object(module,'ROOT',self.root) for module in (paper_data,collect_papers,render_recent,daily_papers)]
        self.patches.append(patch.object(daily_papers,'DAILY',self.root/'daily'))
        for p in self.patches:p.start()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(lambda:[p.stop() for p in self.patches])

    def snapshot(self):
        return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*.md')}

    def test_render_is_idempotent_and_preserves_baseline(self):
        before={str(p):paper_data.strip_generated(p.read_text()) for p in (self.root/'library').glob('*/*.md')}
        render_recent.render(); first=self.snapshot()
        render_recent.render()
        self.assertEqual(first,self.snapshot())
        for path,body in before.items():
            self.assertEqual(body,paper_data.strip_generated(Path(path).read_text()))
        self.assertEqual(sum(paper_data.topic_counts().values()),2029)

    def queue(self):
        row=dict(paper_data.records()[0],arxiv_id='2609.99999',url='https://arxiv.org/abs/2609.99999',
                 title='Workflow test fixture',published='2026-09-18T00:00:00Z',updated='2026-09-18T00:00:00Z',status='pending')
        path=self.root/'review.json';path.write_text(json.dumps({'papers':[row]}))
        return path,row

    def test_review_gate_reimport_and_new_day_preserve_notes(self):
        path,row=self.queue()
        collect_papers.import_review(path,'2026-09-18')
        self.assertEqual(len(paper_data.records()),62)
        row['status']='approved';path.write_text(json.dumps({'papers':[row]}))
        collect_papers.import_review(path,'2026-09-18')
        collect_papers.import_review(path,'2026-09-18')
        self.assertEqual(len(paper_data.records()),63)
        daily=self.root/'daily/2026/2026-09-18.md'
        daily.write_text('# 2026-09-18\n\nMy manual note.\n')
        render_recent.render();render_recent.render()
        self.assertIn('My manual note.',daily.read_text())
        self.assertEqual(daily.read_text().count(row['url']),1)
        topic=(self.root/row['target']).read_text()
        self.assertEqual(topic.count(row['url']),1)
        self.assertIn('共 **268** 个条目',topic)
        self.assertIn('**1,987 个论文及报告条目**',(self.root/'README.md').read_text())
        self.assertLess(topic.index(row['url']),topic.index('https://arxiv.org/abs/2609.17983'))

    def test_invalid_topic_does_not_write(self):
        path,row=self.queue();row.update(status='approved',section='#### nonexistent')
        path.write_text(json.dumps({'papers':[row]}))
        before=(self.root/'data/recent-papers.json').read_bytes()
        with self.assertRaises(ValueError):collect_papers.import_review(path,'2026-09-18')
        self.assertEqual(before,(self.root/'data/recent-papers.json').read_bytes())

    def test_fetch_pagination_and_dedup(self):
        path,row=self.queue()
        old=dict(paper_data.records()[0])
        old['published']='2026-09-18T00:00:00Z'
        with patch.object(collect_papers,'request',return_value=b'fixture'), patch.object(collect_papers,'parse_feed',side_effect=[(2,[old]),(2,[row])]),patch.object(collect_papers.time,'sleep'):
            output=self.root/'fetched.json'
            collect_papers.fetch('2026-09-18','2026-09-18','all:test',output)
        result=json.loads(output.read_text())
        self.assertEqual(result['already_indexed'],1)
        self.assertEqual([r['arxiv_id'] for r in result['papers']],['2609.99999'])

if __name__=='__main__':unittest.main()
