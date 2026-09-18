"""Generate README statistics from the current local library."""
from pathlib import Path
from collections import Counter
import json, re, os
os.environ.setdefault('MPLCONFIGDIR','/tmp/long-context-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
ROOT=Path(__file__).resolve().parents[1]
labels={1:'综述',2:'高效注意力',3:'KV Cache 优化',4:'递归 Transformer',5:'状态空间与混合架构',6:'位置编码与长度外推',7:'长上下文训练',8:'长期记忆',9:'检索增强生成',10:'上下文学习',11:'上下文压缩',12:'模型压缩',13:'长推理',14:'长视频与图像',15:'长程 Agent',16:'长文生成',17:'推理加速与服务',18:'评测与基准',19:'模型技术报告',20:'博客与教程'}
from paper_data import read_json, topic_counts, records
manifest=read_json('data/library-baseline.json')
training_paths={r['target'] for r in read_json('data/training-index.json')['records']}
counts_by_topic=topic_counts()
category=[{'id':c['id'],'label':labels[c['id']],
           'count':sum(counts_by_topic[p] for p in training_paths) if c['id']==7 else counts_by_topic[c['path']]}
          for c in manifest['chapters']]
papers=sorted([x for x in category if x['id']!=20],key=lambda x:-x['count'])
sub=sorted([{'label':(ROOT/p).read_text().splitlines()[0].lstrip('# '),'count':counts_by_topic[p]} for p in training_paths],key=lambda x:(-x['count'],x['label']))
updated=max((r['collected'] for r in records()),default=manifest['date'])
fonts=font_manager.findSystemFonts()
font=next((f for f in fonts if 'Arial Unicode' in f),None) or next((f for f in fonts if 'Heiti' in f),None)
if not font: raise RuntimeError('A CJK font is required')
font_manager.fontManager.addfont(font)
plt.rcParams.update({'font.family':font_manager.FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'svg.fonttype':'path','font.size':11})
# Seven research areas form an exclusive partition of the bibliography.
from matplotlib.patches import FancyBboxPatch
areas = [
 ('推理与压缩', [3,11,12,17], 'KV Cache · 上下文压缩 · 模型压缩 · 推理服务'),
 ('推理与应用', [13,14,15,16], '长推理 · 视觉理解 · 长程 Agent · 长文生成'),
 ('模型架构', [2,4,5,6], '高效注意力 · 递归模型 · 状态空间 · 位置编码'),
 ('评测与基准', [18], '长上下文能力、效率与可靠性评测'),
 ('检索与记忆', [8,9,10], '检索增强 · 长期记忆 · 上下文学习'),
 ('数据与训练', [7,19], '训练方法与数据 · 模型技术报告'),
 ('综述', [1], '研究综述与领域全景'),
]
counts = {x['id']:x['count'] for x in category}
total = sum(x['count'] for x in papers)
blogs = counts[20]
groups = [{'label':label,'count':sum(counts[i] for i in ids),'detail':detail}
          for label,ids,detail in areas]
assert sum(x['count'] for x in groups) == total
BG, INK, MUTED, TEAL = '#F6F8FA', '#162C3D', '#72818D', '#167F86'
fig = plt.figure(figsize=(14,11.5), facecolor=BG)
ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
def text(x,y,s,size=12,color=INK,weight='normal',**kw):
 ax.text(x,y,s,fontsize=size,color=color,weight=weight,va='center',**kw)
def box(x,y,w,h,color,r=.012):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',
                           facecolor=color,edgecolor='none'))
text(.055,.954,'LONG CONTEXT LIBRARY',12,TEAL,weight='bold')
text(.945,.954,'收录概览  /  '+updated.replace('-', '.'),11,MUTED,ha='right')
box(.05,.737,.90,.172,INK,.02)
text(.078,.867,'长上下文研究知识库',20,'#FFFFFF')
text(.076,.786,f'{total:,}',51,'#FFFFFF',weight='bold')
text(.269,.786,'论文与报告条目',14,'#B7C8D1')
for x,value,label in [(.67,len(groups),'研究方向'),(.825,len(papers),'细分主题')]:
 text(x,.821,str(value),30,'#FFFFFF',weight='bold')
 text(x,.771,label,12,'#B7C8D1')
text(.061,.693,'研究方向分布',17,weight='bold')
text(.935,.693,'条目数 / 占比',11,MUTED,ha='right')
max_count=max(g['count'] for g in groups)
for i,g in enumerate(groups):
 y=.637-i*.074
 # Subtle full-width separators and quiet tracks keep the chart readable at README size.
 if i%2==0: box(.05,y-.038,.90,.068,'#FFFFFF',.009)
 text(.068,y+.007,f'{i+1:02d}',10,'#A5B0B8')
 text(.109,y+.010,g['label'],15,weight='bold')
 text(.109,y-.016,g['detail'],9.5,MUTED)
 box(.51,y-.005,.315,.013,'#E4EBEF',.0065)
 box(.51,y-.005,.315*g['count']/max_count,.013,TEAL,.0065)
 text(.873,y+.002,str(g['count']),17,weight='bold',ha='right')
 text(.934,y+.002,f"{g['count']/total:.1%}",10,MUTED,ha='right')
ax.plot([.06,.94],[.133,.133],color='#DCE4E9',lw=.8)
text(.061,.101,f'另收录 {blogs} 个博客与教程条目',12,INK)
text(.939,.101,'按主题归档 · 持续整理',11,MUTED,ha='right')
text(.061,.067,'统计口径：主题库条目数；不计每日页重复展示，非全库去重论文数。',10,MUTED)
out=ROOT/'assets'; out.mkdir(exist_ok=True)
fig.savefig(out/'paper-statistics.png',dpi=180,facecolor=BG)
fig.savefig(out/'paper-statistics.svg',facecolor=BG)
(out/'paper-statistics.json').write_text(json.dumps({
 'updated':updated,'counting_unit':'bibliography entries, not deduplicated papers',
 'paper_and_report_entries':total,'blog_entries':blogs,'research_areas':groups,
 'original_categories':[{k:v for k,v in x.items() if k not in ('baseline','added')} for x in category],
 'training_breakdown':[{k:v for k,v in x.items() if k not in ('baseline','added')} for x in sub]
},ensure_ascii=False,indent=2)+'\n')
print(f'Generated PNG, SVG, JSON: {total} paper/report entries in {len(groups)} research areas; {blogs} blogs.')
