"""Fetch a dated arXiv review queue; import only explicitly approved papers."""
import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from paper_data import ROOT, known_ids, records

NS = {'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
DEFAULT_QUERY = '(all:"long context" OR all:"long-context" OR all:"KV cache" OR all:"context compression")'

def parse_feed(body):
    root = ET.fromstring(body)
    total = int(root.findtext('o:totalResults', namespaces=NS))
    result = []
    for entry in root.findall('a:entry',NS):
        get = lambda k: ' '.join(entry.findtext('a:'+k, default='', namespaces=NS).split())
        match = re.search(r'/(\d{4}\.\d{4,5})(?:v\d+)?$', get('id'))
        if not match:
            raise ValueError('Unexpected arXiv entry: '+get('id'))
        aid=match[1]
        result.append({'arxiv_id':aid,'title':get('title'),
                       'authors':[a.findtext('a:name',namespaces=NS) for a in entry.findall('a:author',NS)],
                       'published':get('published'),'updated':get('updated'),
                       'url':'https://arxiv.org/abs/'+aid,'abstract':get('summary'),
                       'status':'pending','target':'','section':'','summary_zh':''})
    return total,result

def request(url):
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'LongContextLibrary/1.0 (paper index)'})
            with urllib.request.urlopen(req,timeout=45) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(3*(attempt+1))

def fetch(start,end,query,output):
    first,last=date.fromisoformat(start),date.fromisoformat(end)
    if first>last:
        raise ValueError('--from must not follow --to')
    search=f'({query}) AND submittedDate:[{first:%Y%m%d}0000 TO {last:%Y%m%d}2359]'
    offset=0; rows={}; total=None
    while total is None or offset<total:
        url='https://export.arxiv.org/api/query?'+urllib.parse.urlencode({
            'search_query':search,'start':offset,'max_results':100,
            'sortBy':'submittedDate','sortOrder':'ascending'})
        total,page=parse_feed(request(url))
        if not page and offset<total:
            raise RuntimeError('Incomplete arXiv pagination; no output written')
        for row in page:
            if start <= row['published'][:10] <= end:
                rows[row['arxiv_id']]=row
        offset+=len(page)
        if offset<total:
            time.sleep(3)
    known=known_ids()
    existing=[row for aid,row in rows.items() if aid in known]
    pending=[row for aid,row in rows.items() if aid not in known]
    report={'fetched_at':datetime.now(timezone.utc).isoformat(),
            'range':[start,end],'date_basis':'arXiv first submission, UTC','query':search,
            'api_total':total,'unique_in_range':len(rows),'already_indexed':len(existing),
            'coverage':'Keyword search only; candidates require manual relevance and metadata review.',
            'papers':pending,'existing_papers':existing}
    output=Path(output)
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite a review queue: {output}')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(rows)} candidates in range; {len(existing)} already indexed; {len(pending)} pending: {output}')

def import_review(path,collected):
    date.fromisoformat(collected)
    queue=json.loads(Path(path).read_text())
    current=records(); known=known_ids(); added=[]
    for row in queue['papers']:
        if row.get('status')!='approved' or row['arxiv_id'] in known:
            continue
        if not row.get('summary_zh','').strip() or not row.get('target'):
            raise ValueError(f'Approved paper needs a summary and topic: {row["arxiv_id"]}')
        fields=('arxiv_id','title','authors','published','updated','url','target','section','summary_zh')
        item={key:row.get(key,'') for key in fields}
        item.update(collected=collected,verification='Official metadata and abstract reviewed')
        added.append(item);known.add(item['arxiv_id'])
    combined=current+added
    records(combined)  # Validate before replacing the data file.
    if added:
        dest=ROOT/'data/recent-papers.json'
        temp=dest.with_suffix('.tmp')
        temp.write_text(json.dumps(combined,ensure_ascii=False,indent=2)+'\n');temp.replace(dest)
    print(f'Imported {len(added)} approved new papers; run scripts/render_recent.py next.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    search=commands.add_parser('fetch')
    search.add_argument('--from',dest='start',required=True)
    search.add_argument('--to',dest='end',required=True)
    search.add_argument('--query',default=DEFAULT_QUERY)
    search.add_argument('--output',required=True)
    review=commands.add_parser('import')
    review.add_argument('path')
    review.add_argument('--collected',required=True)
    args=parser.parse_args()
    if args.command=='fetch':
        fetch(args.start,args.end,args.query,args.output)
    else:
        import_review(args.path,args.collected)
