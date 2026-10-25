from pathlib import Path
import sys,json,copy,io,os,html,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v782';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,ft,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE,P
PURPLE='#75638F';GREEN='#297A78'
basefile=HERE/'baseline-v781.json'
if not basefile.exists():basefile.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(basefile.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog'])
for n,v in [(41,784),(42,783)]:
 src=ROOT/f'sources/location-v{v}/pages/page-{n}.png';dest=OUT/f'page-{n}.png';shutil.copyfile(src,dest);assert src.read_bytes()==dest.read_bytes();Image.open(dest).load()
 records[n-1]['path']=str(dest.relative_to(ROOT))
cat.update(version='V07.82',cache='20261025-82')
cat['pages'][40].update(title='Location : accueillir et équiper',description='Accueillir, cerner le profil et le programme, faire essayer les chaussures, choisir le matériel, régler avec ISOSKI puis enregistrer les mesures et réglages dans Gingkoia.')
cat['pages'][41].update(title='Location : bien réceptionner au retour',description='Écouter le client, proposer l’achat avec déduction de la location ; contrôler et sécher les skis, transmettre à l’atelier, vérifier les chaussures et les bâtons puis les orienter.')
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');data=b.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 Image.open(path).load()
# Keep the five-section contents layout; only the return-page label changes.
code=(ROOT/'sources/final-polish-v781/apply.py').read_text()
part=code[code.index('p=Page(2);'):code.index('im=p.im.copy();')]
part=part.replace('assets/guide-v781/page-02.png','assets/guide-v782/page-02.png')
exec(part)
for n in range(1,45):
 if n not in [2,41,42]:assert records[n-1]==base['records'][n-1];assert cat['pages'][n-1]==base['catalog']['pages'][n-1]
(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text()
builder=s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261025-82').replace('V07.76','V07.82').replace('range(1,41)','range(1,45)').replace("'__TOTAL__':'40'","'__TOTAL__':'44'")
exec(builder)
for name in ['README.md','tests/guide-smoke.cjs']:
 f=ROOT/name;f.write_text(f.read_text().replace('V07.81','V07.82'))
print('Two approved images copied byte-for-byte. All other content preserved; contents label updated.')
