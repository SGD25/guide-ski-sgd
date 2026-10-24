from pathlib import Path
import json,sys,copy,io,os,html,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v780'
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE
PURPLE='#75638F';OUT.mkdir(exist_ok=True)
baseline=HERE/'baseline-v779.json'
if not baseline.exists():baseline.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(baseline.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog'])
for n,t,d in [(41,'Location : accueillir et équiper','Comprendre le programme, recueillir les données, faire essayer les chaussures et choisir un ensemble cohérent.'),(42,'Location : départ et retour','Préparer le départ, montrer les manipulations, recueillir le retour client et orienter le matériel.'),(43,'Au comptoir : les bonnes questions','Quatre situations clients, les questions utiles, les bons réflexes et les erreurs à éviter.'),(44,'Un doute : vérifier et transmettre','Reconnaître un problème, mettre le matériel de côté et transmettre les faits au référent ou à l’atelier.')]:
 dest=OUT/f'page-{n}.png'
 if not dest.exists():shutil.copyfile(ROOT.parent/f'output/closing-pages/page-{n}.png',dest)
 records.append({'page':n,'path':str(dest.relative_to(ROOT)),'links':[]});cat['pages'].append({'page':n,'title':t,'chapter':'03 · Sécuriser','description':d})
cat.update(version='V07.80',cache='20261024-80');cat['pages'][1]['description']='Sommaire cliquable des 44 pages : matériel, réglages, sécurité, parcours de location et situations clients.'
(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');data=b.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 Image.open(path).load()
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text();part=s[s.index('p=Page(2);'):s.index("assert [r['page']")].replace('40 pages pour','44 pages pour').replace('assets/guide-v776/page-02.png','assets/guide-v780/page-02.png').replace("1220,1810,2325,2840,'03 / Sécuriser',range(31,41),PURPLE,88","1220,1810,2325,3175,'03 / Sécuriser',range(31,45),PURPLE,86")
a=part.index('p.rect((75,2890');b=part.index('p.footer();',a)
part=part[:a]+"p.rect((75,2890,1180,3175),INK,None,24);p.text(115,2930,'Le parcours au comptoir.',47,'serif',WHITE,width=1020);p.text(115,3020,'Questionner → conseiller → contrôler.',36,'sans',WHITE,width=1020);p.text(115,3100,'Chaque ligne est cliquable.',31,'bold',WHITE)\n"+part[b:]
exec(part)
(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
builder=s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261024-80').replace('V07.76','V07.80').replace('range(1,41)','range(1,45)').replace("'__TOTAL__':'40'","'__TOTAL__':'44'")
exec(builder)
for f in ['README.md','tests/guide-smoke.cjs']:
 p=ROOT/f;t=p.read_text().replace('V07.79','V07.80')
 if f.endswith('.cjs'):
  t=t.replace('length:40','length:44').replace('pages.length,40','pages.length,44').replace('manifest.length,40','manifest.length,44').replace('config.pages.length,40','config.pages.length,44').replace('i<40','i<44').replace('+m[1]<40','+m[1]<44').replace('length:38','length:42').replace('01–02 \\/ 40','01–02 \\/ 44').replace('OK: 40 pages','OK: 44 pages')
 else:t=t.replace('40 pages','44 pages')
 p.write_text(t)
for n in range(1,41):
 if n!=2:assert records[n-1]==base['records'][n-1];assert cat['pages'][n-1]==base['catalog']['pages'][n-1]
for n in range(41,45):assert (OUT/f'page-{n}.png').read_bytes()==(ROOT.parent/f'output/closing-pages/page-{n}.png').read_bytes()
print('44 pages; all original content and four approved image files preserved exactly.')
