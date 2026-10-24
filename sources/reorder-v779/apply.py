from pathlib import Path
import json,sys,copy,io,os,html
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v779'
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE,ft
PURPLE='#75638F'
baseline=HERE/'baseline-v778.json'
if not baseline.exists():baseline.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(baseline.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog'])
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');data=b.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 Image.open(path).load()
for old,new in [(34,33),(35,34),(33,35)]:
 r=copy.deepcopy(base['records'][old-1]);m=copy.deepcopy(base['catalog']['pages'][old-1]);im=Image.open(ROOT/r['path']).convert('RGB');before=im.copy();d=ImageDraw.Draw(im)
 if old in [34,35]:
  boxes=[(2050,50,2310,115)];d.rectangle(boxes[0],fill=im.getpixel((2050,120)));d.text((round(513*2400/595.28),round(17*3394/841.89)),f'PAGE {new}',font=ft(32,'bold'),fill=INK,anchor='lt')
 else:
  boxes=[(2110,36,2324,102),(2270,3340,2375,3393)];p=Page(new);p.im=im;p.d=d;p.rect(boxes[0],'#F9FBFC','#8BA3AF',28,2);p.text(2217,53,f'PAGE {new:02}',31,'bold',INK,center=True);d.rectangle(boxes[1],fill=im.getpixel((2280,3335)));p.text(2325,3350,f'{new:02}',29,'bold',INK,center=True)
 diff=ImageChops.difference(before,im)
 for b in boxes:ImageDraw.Draw(diff).rectangle(b,fill=0)
 assert diff.getbbox() is None
 save(im,OUT/f'page-{new}.png');r.update(page=new,path=f'assets/guide-v779/page-{new}.png');m['page']=new;records[new-1]=r;cat['pages'][new-1]=m
cat.update(version='V07.79',cache='20261024-79');(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text();part=s[s.index('p=Page(2);'):s.index("assert [r['page']")].replace('assets/guide-v776/page-02.png','assets/guide-v779/page-02.png');exec(part)
(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
exec(s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261024-79').replace('V07.76','V07.79'))
for f in ['README.md','tests/guide-smoke.cjs']:
 p=ROOT/f;t=p.read_text().replace('V07.78','V07.79').replace('pages[32].title,/NX12/','pages[34].title,/NX12/');p.write_text(t)
for n in [31,32,36,37,38,39,40]:assert records[n-1]==base['records'][n-1]
print('Only page-number pixels changed on reordered posters; other content preserved.')
