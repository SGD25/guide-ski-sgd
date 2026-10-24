from pathlib import Path
import sys,json,copy,io,os,html,shutil
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v781';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,ft,INK,BODY,CORAL,BLUE,TEAL,WHITE,LINE,P
BG=P['fond'];PURPLE='#75638F';GREEN='#297A78'
f=HERE/'baseline-v780.json'
if not f.exists():f.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(f.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog'])
chapters=[(3,7,'01 · Comprendre',BLUE),(8,24,'02 · Reconnaître et conseiller le matériel',CORAL),(25,30,'03 · Reconnaître et conseiller textiles et accessoires',GREEN),(31,40,'04 · Sécuriser',PURPLE),(41,44,'05 · Accueillir, louer et accompagner',GREEN)]
def save(im,path):
 b=io.BytesIO();im.save(b,format='PNG');data=b.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 Image.open(path).load()
redesigned=[3,*range(33,39),*range(41,45)];audit=[]
for lo,hi,ch,color in chapters:
 for n in range(lo,hi+1):
  cat['pages'][n-1]['chapter']=ch
  if n in redesigned:
   shutil.copyfile(HERE/f'pages/page-{n:02}.png',OUT/f'page-{n:02}.png')
  elif n>=8:
   p=Page(n);p.im=Image.open(ROOT/base['records'][n-1]['path']).convert('RGB');p.d=ImageDraw.Draw(p.im);before=p.im.copy();scale=p.im.width/2400
   boxes=[tuple(round(v*scale) for v in b) for b in [(0,0,2399,13),(60,30,2075,105)]]
   p.d.rectangle(boxes[0],fill=color);p.d.rectangle(boxes[1],fill=BG)
   title='CHAPITRE '+ch.replace(' · ',' / ').upper();size=round(35*scale)
   while p.d.textlength(title,font=ft(size,'bold'))>1985*scale:size-=1
   p.d.text((round(76*scale),round(48*scale)),title,font=ft(size,'bold'),fill=color,anchor='lt')
   diff=ImageChops.difference(before,p.im)
   for box in boxes:ImageDraw.Draw(diff).rectangle(box,fill=0)
   assert diff.getbbox() is None
   save(p.im,OUT/f'page-{n:02}.png');audit.append({'page':n,'source':base['records'][n-1]['path'],'only_changed_regions':boxes})
  else:continue
  records[n-1]['path']=f'assets/guide-v781/page-{n:02}.png'
cat.update(version='V07.81',cache='20261024-81')
cat['pages'][1]['description']='Sommaire cliquable : comprendre ; reconnaître et conseiller le matériel ; textiles et accessoires ; sécuriser ; accueillir, louer et accompagner.'
cat['pages'][2]['description']='Spatule, patin, talon : trois zones et les lignes de cotes 118–88–108 mm. Les repères de largeur se lisent dans l’encart Patin.'
p=Page(2);p.header('','44 pages pour comprendre, conseiller, sécuriser et accompagner.')
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text()
exec(s[s.index('labels={'):s.index('for x,y,x2,y2,title,nums,color,row')])
blocks=[(75,440,1180,1110,'01 / Comprendre','Les bases du ski',range(3,8),BLUE,94),(75,1150,1180,3210,'02 / Le matériel','Reconnaître et conseiller',range(8,25),CORAL,108),(1220,440,2325,1220,'03 / Textiles et accessoires','Reconnaître et conseiller',range(25,31),GREEN,94),(1220,1260,2325,2450,'04 / Sécuriser','Réglages, contrôles et secours',range(31,41),PURPLE,96),(1220,2490,2325,3210,'05 / Accueillir, louer','Et accompagner le client',range(41,45),GREEN,128)]
for x,y,x2,y2,title,sub,nums,col,row in blocks:
 p.rect((x,y,x2,y2),WHITE,col,25,3);p.text(x+30,y+28,title,48,'serif',col,width=x2-x-60);p.text(x+30,y+96,sub,33,'bold',BODY,width=x2-x-60)
 for i,n in enumerate(nums):
  yy=y+175+i*row
  if i:p.line((x+25,yy-15,x2-25,yy-15),LINE,2)
  p.text(x+30,yy,labels[n],34,'bold',INK,width=865,leading=40,bottom=yy+82)
  p.text(x2-70,yy+4,f'{n:02}',34,'bold',col,center=True);p.link((x+15,yy-12,x2-15,yy+row-13),n,labels[n])
p.footer();save(p.im,OUT/'page-02.png');records[1].update(path='assets/guide-v781/page-02.png',links=p.links)
im=p.im.copy();im.thumbnail((1000,1415));im.save(HERE/'pages/apercu-02.jpg',quality=95)
(HERE/'content-preservation.json').write_text(json.dumps(audit,indent=2))
(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
builder=s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261024-81').replace('V07.76','V07.81').replace('range(1,41)','range(1,45)').replace("'__TOTAL__':'40'","'__TOTAL__':'44'")
exec(builder)
f=ROOT/'README.md';f.write_text(f.read_text().replace('V07.80','V07.81'))
print('Five chapters, 44 pages. Preserved original body pixels including pages 31–32.')
