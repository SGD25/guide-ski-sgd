from pathlib import Path
import sys,json,copy,io,os,html
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,ft,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE,P
BG=P['fond'];PURPLE='#75638F';OUT=ROOT/'assets/guide-v776';OUT.mkdir(exist_ok=True)
basefile=HERE/'baseline-v775.json'
if not basefile.exists():basefile.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(basefile.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog']);audit=[]
def save(im,path):
 stream=io.BytesIO();im.save(stream,format='PNG');data=stream.getvalue();tmp=Path(str(path)+'.tmp')
 with open(tmp,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 os.replace(tmp,path);Image.open(path).load()
def numbered(source,n,old):
 p=Page(n);p.im=Image.open(source).convert('RGB');p.d=ImageDraw.Draw(p.im);before=p.im.copy()
 boxes=[(2110,36,2324,102),(2270,3340,2375,3393)]
 p.rect(boxes[0],BG,P['reperes'],28,2);p.text(2217,53,f'PAGE {n:02}',31,'bold',INK,center=True)
 p.d.rectangle(boxes[1],fill=BG);p.text(2325,3350,f'{n:02}',29,'bold',INK,center=True)
 diff=ImageChops.difference(before,p.im)
 for b in boxes:ImageDraw.Draw(diff).rectangle(b,fill=0)
 assert diff.getbbox() is None
 dest=OUT/f'page-{n:02}.png';save(p.im,dest);audit.append({'source':str(source.relative_to(ROOT)),'page':n,'only_changed_regions':boxes});return str(dest.relative_to(ROOT))
for r in records:
 old=r['page']
 if old>=33:r['page']+=6;r['path']=numbered(ROOT/r['path'],r['page'],old)
 for link in r.get('links',[]):
  if link['page']>=33:link['page']+=6
for m in cat['pages']:
 if m['page']>=33:m['page']+=6
 m['description']=m['description'].replace('avalanche 33–34','avalanche 39–40')
titles=['LOOK NX12 : anatomie et graduations','Fixations alpines : les déclenchements','Konect : rails, BSL et poussée','NX12 : régler et contrôler','PLUM Guide 12 : les pièces','PLUM Guide 12 : montée et descente']
for i,n in enumerate(range(33,39)):
 path=numbered(ROOT/f'sources/bindings-v776-revision/pages/page-{n-2}.png',n,n-2)
 records.append({'page':n,'path':path,'links':[]});cat['pages'].append({'page':n,'title':titles[i],'chapter':'03 · Sécuriser','description':titles[i]+'. Page illustrée de formation vendeurs et loueurs.'})
records.sort(key=lambda r:r['page']);cat['pages'].sort(key=lambda m:m['page']);cat.update(version='V07.76',cache='20261024-76')
cat['pages'][1]['description']='Sommaire des 40 pages. Pages 31–32 conservées, compléments fixations LOOK NX12 et PLUM en 33–38, avalanche en 39–40.'
# Existing avalanche references, preserving all other pixels.
notes={17:'En terrain avalancheux : DVA, pelle, sonde et formation. Voir pages 39–40. Photos : Elan, POMOCA (peau illustrative 65/35), Dynafit, SCARPA. Le mix 70/30 reste le repère SGD. Budgets : hors accessoires et matériel de secours.',21:'Repères adultes indicatifs, hors planches de carving alpin et splitboards. Hors-piste : équipement et formation adaptés ; voir sécurité avalanche pages 39–40. Sources : Nitro, RIDE, Burton, Nidecker. Photos fabricants.'}
for n,note in notes.items():
 r=records[n-1];p=Page(n);p.im=Image.open(ROOT/r['path']).convert('RGB');p.d=ImageDraw.Draw(p.im);before=p.im.copy();b=(70,3230,2000,3318);p.d.rectangle(b,fill=BG);p.text(76,3237,note,26,width=1890,bottom=3313)
 diff=ImageChops.difference(before,p.im);ImageDraw.Draw(diff).rectangle(b,fill=0);assert diff.getbbox() is None
 dest=OUT/f'page-{n:02}.png';save(p.im,dest);r['path']=str(dest.relative_to(ROOT));audit.append({'page':n,'only_changed_regions':[b]})
# Legible complete contents in four blocks.
p=Page(2);p.header('','40 pages pour comprendre, reconnaître, conseiller et sécuriser.')
labels={m['page']:m['title'] for m in cat['pages']}
labels.update({3:'Anatomie & lignes de cotes',4:'Largeur & longueur',5:'Rayon de courbure',6:'Cambres & rockers',7:'Construction & noyaux',8:'Les familles de skis',9:'Skis de piste',10:'Exemples piste',11:'Skis all-mountain',12:'Exemples all-mountain',13:'Freeride & freestyle',14:'Exemples freeride & freestyle',15:'Skis juniors',16:'Exemples juniors',17:'Skis de randonnée',18:'Exemples de skis de randonnée',19:'Chaussures alpines',20:'Chaussures de ski de randonnée',21:'Choisir son snowboard',22:'Quatre exemples Nitro',23:'Ski de fond : les pratiques',24:'Exemples classique & skating',25:'Textile : les trois couches',26:'Textile : membranes & indices',27:'Chaussures de randonnée pédestre',28:'Randonnée : choisir et essayer',29:'Masques & lunettes : météo',30:'Masques & lunettes : technologies',31:'Fixations : comprendre le réglage',32:'Fixations : contrôler avant de louer',39:'Avalanche : s’équiper et contrôler',40:'Avalanche : rechercher et secourir'})
for x,y,x2,y2,title,nums,color,row in [(75,440,1180,1250,'01 / Comprendre',range(3,8),BLUE,128),(75,1290,1180,2840,'02 / Reconnaître & conseiller',range(8,19),CORAL,126),(1220,440,2325,1770,'02 / Les équipements',range(19,31),CORAL,94),(1220,1810,2325,2840,'03 / Sécuriser',range(31,41),PURPLE,88)]:
 p.rect((x,y,x2,y2),WHITE,color,25,3);p.text(x+30,y+30,title,48,'serif',color,width=x2-x-60)
 for i,n in enumerate(nums):
  yy=y+135+i*row
  if i:p.line((x+25,yy-15,x2-25,yy-15),LINE,2)
  p.text(x+30,yy,labels[n],34,'bold',INK,width=865,leading=40,bottom=yy+80)
  p.text(x2-70,yy+4,f'{n:02}',34,'bold',color,center=True);p.link((x+15,yy-12,x2-15,yy+row-13),n,labels[n])
p.rect((75,2890,2325,3175),INK,None,24);p.text(115,2930,'Le bon parcours au comptoir.',58,'serif',WHITE,width=2150);p.text(115,3030,'Terrain → niveau → gabarit → matériel compatible → contrôles.',44,'sans',WHITE,width=2150);p.text(115,3120,'Chaque ligne du sommaire est cliquable.',31,'bold',WHITE)
p.footer();save(p.im,OUT/'page-02.png');records[1].update(path='assets/guide-v776/page-02.png',links=p.links)
assert [r['page'] for r in records]==list(range(1,41))
for n in [31,32]:assert records[n-1]==base['records'][n-1],f'Original page {n} changed'
(HERE/'content-preservation.json').write_text(json.dumps(audit,indent=2));(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
# Build page records without re-encoding any other poster.
for r,m in zip(records,cat['pages']):
 n=r['page'];markup=f'<figure class="sgd-poster" data-page="{n}"><img src="./{r["path"]}?v=20261024-76" alt="{html.escape(m["description"],quote=True)}" width="2400" height="3394" loading="eager" decoding="async">'
 for l in r.get('links',[]):
  x,y,x2,y2=l['box'];markup+=f'<button type="button" class="poster-link page-jump" data-jump="{l["page"]-1}" style="left:{x/24:.5f}%;top:{y/33.94:.5f}%;width:{(x2-x)/24:.5f}%;height:{(y2-y)/33.94:.5f}%" aria-label="{html.escape(l["label"],quote=True)} — page {l["page"]}"></button>'
 markup+=''.join(r.get('overlays',[]))+'</figure>';obj={'title':m['title'],'chapter':m['chapter'],'html':markup};(ROOT/f'pages/{n:02}.js').write_text('window.SGD_PAGES.push('+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+');\n')
template=(ROOT/'sources/guide/reader-template.html').read_text();scripts='<script src="./pages/00-init.js?v=20261024-76"></script>\n'+'\n'.join(f'<script src="./pages/{n:02}.js?v=20261024-76"></script>' for n in range(1,41))
for k,v in {'__CACHE__':'20261024-76','__VERSION__':'V07.76','__TOTAL__':'40','__SCRIPTS__':scripts}.items():template=template.replace(k,v)
(ROOT/'index.html').write_text(template)
print('40 pages prepared. Original 31–32 unchanged; only page numbers changed on new pages and avalanche.')
