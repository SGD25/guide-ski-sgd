from pathlib import Path
import json,sys,html,io,os
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v778'
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE
PURPLE='#75638F'
records=json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text());cat=json.loads((ROOT/'sources/guide/catalog.json').read_text())
for n,t,d in [(34,'Fixations : le déclenchement latéral','Déclenchement latéral : torsion et libération de l’avant de la chaussure par la butée.'),(35,'Fixations : le déclenchement frontal','Déclenchement frontal : basculement vers l’avant et libération du talon vers le haut par la talonnière.')]:
 records[n-1]['path']=f'assets/guide-v778/page-{n}.png';cat['pages'][n-1].update(title=t,description=d)
cat.update(version='V07.78',cache='20261024-78')
(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');data=b.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 Image.open(path).load()
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text();part=s[s.index("p=Page(2);"):s.index("assert [r['page']")].replace("assets/guide-v776/page-02.png","assets/guide-v778/page-02.png")
exec(part)
(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
# Retain the existing builder, only substituting the new cache version.
part=s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261024-78').replace('V07.76','V07.78')
exec(part)
for f in ['README.md','tests/guide-smoke.cjs']:
 p=ROOT/f;p.write_text(p.read_text().replace('V07.77','V07.78'))
