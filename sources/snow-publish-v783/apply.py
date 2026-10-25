from pathlib import Path
import sys,json,copy,io,os,html,shutil,hashlib
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v783';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,ft,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE,P
BG=P['fond'];PURPLE='#75638F';GREEN='#297A78'
f=HERE/'baseline-v782.json'
if not f.exists():f.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(f.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog']);audit=[]
def save(im,path):
 stream=io.BytesIO();im.save(stream,format='PNG');data=stream.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 Image.open(path).load()
def shift(n):return n+2 if n>=21 else n
for r in records:
 old=r['page'];n=shift(old);r['page']=n
 for l in r.get('links',[]):l['page']=shift(l['page'])
 if old<21:continue
 im=Image.open(ROOT/r['path']).convert('RGB');before=im.copy();d=ImageDraw.Draw(im);sx=im.width/2400;sy=im.height/3394
 def box(b):return tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(b))
 boxes=[box((2107,33,2328,105)),box((2265,3340,2380,3393))]
 if old==29:boxes=[(908,15,1030,51),(995,1460,1040,1490)]
 if old==30:boxes=[(929,7,1034,36),(986,1461,1033,1490)]
 for b in boxes:d.rectangle(b,fill=BG)
 hb=boxes[0];d.rounded_rectangle(hb,radius=round(24*sx),fill=BG,outline='#8BA3AF',width=max(1,round(2*sx)))
 d.text(((hb[0]+hb[2])/2,(hb[1]+hb[3])/2),f'PAGE {n:02}',font=ft(round(31*sx),'bold'),fill=INK,anchor='mm')
 fb=boxes[1];d.text(((fb[0]+fb[2])/2,3350*sy if old not in [29,30] else fb[1]+4),f'{n:02}',font=ft(round(29*sx),'bold'),fill=INK,anchor='mt')
 diff=ImageChops.difference(before,im)
 for b in boxes:ImageDraw.Draw(diff).rectangle(b,fill=0)
 assert diff.getbbox() is None
 dest=OUT/f'page-{n:02}.png';save(im,dest);r['path']=str(dest.relative_to(ROOT));audit.append({'old':old,'new':n,'boxes':boxes})
for m in cat['pages']:
 m['page']=shift(m['page']);m['description']=m['description'].replace('avalanche 39–40','avalanche 41–42')
for n,version,title,desc in [(21,2,'Snowboard : les mots de la planche','Lexique snowboard : anatomie, Wide, shapes twin et directionnels, flex, torsion, pop, semelles extrudées et frittées. Exemples Nitro 2025–2026.'),(22,3,'Snowboard : placer le rider','Regular et goofy, stance, setback, angles illustrés et pièces de fixation : spoiler, straps, boucle, embase et arceau.')]:
 src=ROOT/f'sources/snow-lexicon-v{version}/pages/page-{n}.png';dest=OUT/f'page-{n}.png';shutil.copyfile(src,dest);assert src.read_bytes()==dest.read_bytes()
 records.append({'page':n,'path':str(dest.relative_to(ROOT)),'links':[]});cat['pages'].append({'page':n,'title':title,'chapter':'02 · Reconnaître et conseiller le matériel','description':desc})
records.sort(key=lambda r:r['page']);cat['pages'].sort(key=lambda m:m['page']);cat.update(version='V07.83',cache='20261025-83')
# Update the two existing references to the avalanche spread.
notes={17:'En terrain avalancheux : DVA, pelle, sonde et formation. Voir pages 41–42. Photos : Elan, POMOCA (peau illustrative 65/35), Dynafit, SCARPA. Le mix 70/30 reste le repère SGD. Budgets : hors accessoires et matériel de secours.',23:'Repères adultes indicatifs, hors planches de carving alpin et splitboards. Hors-piste : équipement et formation adaptés ; voir sécurité avalanche pages 41–42. Sources : Nitro, RIDE, Burton, Nidecker. Photos fabricants.'}
for n,note in notes.items():
 r=records[n-1];p=Page(n);p.im=Image.open(ROOT/r['path']).convert('RGB');p.d=ImageDraw.Draw(p.im);p.d.rectangle((70,3230,2000,3318),fill=BG);p.text(76,3237,note,26,width=1890,bottom=3313);dest=OUT/f'page-{n:02}.png';save(p.im,dest);r['path']=str(dest.relative_to(ROOT))
# Shift the cover's printed safety-page reference as well as its link.
p=Page(1);p.im=Image.open(ROOT/base['records'][0]['path']).convert('RGB');p.d=ImageDraw.Draw(p.im);p.d.rectangle((1815,2808,2020,2850),fill=WHITE);p.text(1821,2815,'PAGE 33  →',29,'bold',PURPLE);save(p.im,OUT/'page-01.png');records[0]['path']='assets/guide-v783/page-01.png'
# Preserve the familiar five-block contents layout.
p=Page(2);p.header('','46 pages pour comprendre, conseiller, sécuriser et accompagner.')
labels={shift(l['page']):l['label'] for l in base['records'][1]['links']};labels.update({21:'Snowboard : les mots de la planche',22:'Snowboard : placer le rider'})
blocks=[(75,440,1180,1110,'01 / Comprendre','Les bases du ski',range(3,8),BLUE,94),(75,1150,1180,3210,'02 / Le matériel','Reconnaître et conseiller',range(8,27),CORAL,97),(1220,440,2325,1220,'03 / Textiles et accessoires','Reconnaître et conseiller',range(27,33),GREEN,94),(1220,1260,2325,2450,'04 / Sécuriser','Réglages, contrôles et secours',range(33,43),PURPLE,96),(1220,2490,2325,3210,'05 / Accueillir, louer','Et accompagner le client',range(43,47),GREEN,128)]
for x,y,x2,y2,title,sub,nums,col,row in blocks:
 p.rect((x,y,x2,y2),WHITE,col,25,3);p.text(x+30,y+28,title,48,'serif',col,width=x2-x-60);p.text(x+30,y+96,sub,33,'bold',BODY,width=x2-x-60)
 for i,n in enumerate(nums):
  yy=y+175+i*row
  if i:p.line((x+25,yy-15,x2-25,yy-15),LINE,2)
  p.text(x+30,yy,labels[n],34,'bold',INK,width=865,leading=40,bottom=yy+82);p.text(x2-70,yy+4,f'{n:02}',34,'bold',col,center=True);p.link((x+15,yy-12,x2-15,yy+row-13),n,labels[n])
p.footer();save(p.im,OUT/'page-02.png');records[1].update(path='assets/guide-v783/page-02.png',links=p.links)
im=p.im.copy();im.thumbnail((1000,1415));im.save(HERE/'toc-preview.jpg')
(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text();builder=s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261025-83').replace('V07.76','V07.83').replace('range(1,41)','range(1,47)').replace("'__TOTAL__':'40'","'__TOTAL__':'46'");exec(builder)
(HERE/'content-preservation.json').write_text(json.dumps(audit,indent=2))
f=ROOT/'README.md';f.write_text(f.read_text().replace('V07.82','V07.83'))
print('46 pages built, approved snowboard images copied byte-for-byte.')
