"""Capture exact existing client sentences and their existing box coordinates.

Renderers are evaluated in memory; their page images are never saved or used as
replacement posters. The page-12 script is parsed only, because it writes files.
"""
from pathlib import Path
import sys,json,ast,importlib.util
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as base
from render import Page,DARK

def module(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

final=module('final71','sources/finalisation/render.py')
ff=module('ff71','sources/freeride-freestyle/render.py')
items=[]
old_init,old_rect,old_text=Page.__init__,Page.rect,Page.text

def init(self,n):old_init(self,n);self._rectangles=[];self._pending=None
def rect(self,box,fill=base.WHITE,*args,**kwargs):
    self._rectangles.append((tuple(box),fill));return old_rect(self,box,fill,*args,**kwargs)
def text(self,x,y,s,size=36,*args,**kwargs):
    normalized=' '.join(s.upper().split())
    if normalized.startswith('À DIRE AU CLIENT'):
        c=[(b,f) for b,f in self._rectangles if b[0]<=x<=b[2] and b[1]<=y<=b[3]]
        dark=[b for b,f in c if f==DARK];c=dark or [b for b,f in c]
        assert c,(self.n,s)
        box=min(c,key=lambda b:(b[2]-b[0])*(b[3]-b[1]))
        rec=dict(page=self.n,box=box,size=size,speech='')
        items.append(rec);self._pending=rec
        if ':' in s:rec['speech']=s.split(':',1)[1].strip();self._pending=None
    elif self._pending and s.startswith('«'):
        self._pending['speech']=s;self._pending['size']=size;self._pending=None
    return old_text(self,x,y,s,size,*args,**kwargs)

Page.__init__,Page.rect,Page.text=init,rect,text
builders=[base.radius,final.piste,base.products,base.allmountain,ff.family_page,ff.examples_page,final.juniors.examples_page,final.rando.choice_page,final.boots.touring,final.snow.examples_page,final.nordic.intro_page,final.nordic.examples_page]
for build in builders:
    p=build();del p
assert all(i['speech'] for i in items),items
for i in items:
    if i['page']==5:i['heading']='Quel type de virages ?'
tree=ast.parse((ROOT/'sources/page12/render.py').read_text())
node=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cards' for t in n.targets))
cards=[{kw.arg:ast.literal_eval(kw.value) for kw in c.keywords} for c in node.elts]
for x,c in zip([70,838,1606],cards):items.append(dict(page=12,box=(x+24,2630,x+700,2876),size=35,speech=c['speech']))
items.append(dict(page=15,box=(70,2340,2330,2392),size=34,speech='Aux parents : « On choisit pour sa taille d’aujourd’hui, sans prendre trop grand pour l’an prochain. »'))
items.sort(key=lambda x:(x['page'],x['box'][1],x['box'][0]))
(HERE/'client-panels.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
print(len(items),'encarts',dict(sorted(Counter(i['page'] for i in items).items())))
