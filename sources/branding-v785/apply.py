from pathlib import Path
import json,copy,sys,io,os,html
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;OUT=ROOT/'assets/guide-v785'
sys.path.insert(0,str(ROOT/'sources/guide'));from render import ft
basefile=HERE/'baseline-v784.json'
if not basefile.exists():basefile.write_text(json.dumps({'records':json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text()),'catalog':json.loads((ROOT/'sources/guide/catalog.json').read_text())},ensure_ascii=False,indent=2))
base=json.loads(basefile.read_text());records=copy.deepcopy(base['records']);cat=copy.deepcopy(base['catalog'])
BG='#F9FBFC';INK='#242426';W=2400;H=3394
hl=Image.open(ROOT/'assets/branding-v785/logo-header.png').convert('RGB');fl=Image.open(ROOT/'assets/branding-v785/logo-footer.png').convert('RGB')
def txt(d,xy,t,size=34,color=INK,anchor='lt'):d.text(xy,t,font=ft(size,'bold'),fill=color,anchor=anchor)
def logo(im,source,box):
 x,y,w=box;h=round(w*source.height/source.width);im.paste(source.resize((w,h),Image.Resampling.LANCZOS),(x,y))
def save(im,path):
 s=io.BytesIO();im.save(s,format='WEBP',lossless=True,method=4);data=s.getvalue()
 with open(path,'wb',buffering=0) as f:
  v=memoryview(data)
  while v:v=v[f.write(v):]
  os.fsync(f.fileno())
 with Image.open(path) as check:check.load();assert check.size==(2400,3394)
audit=[]
for r,m in zip(records,cat['pages']):
 n=r['page'];src=Image.open(ROOT/r['path']).convert('RGB');src=src.resize((W,H),Image.Resampling.LANCZOS) if src.size!=(W,H) else src
 top=106
 end={1:3220,28:3298,29:3298,30:3285,31:3260,32:3290}.get(n,3318)
 d=ImageDraw.Draw(src)
 if n==1:d.rectangle((0,106,W,340),fill=BG)
 if n not in [1,28,29,30,31,32]:
  logo_y=3268 if n in [3,21,22,35,36,37,38,39,40,42,43,44,45,46] else 3220
  d.rectangle((2020,logo_y,2315,3318),fill=BG)
 elif n in [28,29,30]:d.rectangle((2020,3288 if n!=30 else 3268,2315,end),fill=BG)
 body=src.crop((0,top,W,end));scale=(3170-120)/(end-top);bw=round(W*scale);bh=3050;left=(W-bw)//2
 im=Image.new('RGB',(W,H),'white');im.paste(body.resize((bw,bh),Image.Resampling.LANCZOS),(left,120));d=ImageDraw.Draw(im)
 chapter=m['chapter'];color='#337BA2' if 3<=n<=7 else '#BA624F' if 8<=n<=26 else '#297A78' if 27<=n<=32 or n>=43 else '#75638F'
 label='FORMATION VENDEURS & LOUEURS' if n==1 else 'OUVERTURE / LE SOMMAIRE' if n==2 else 'CHAPITRE '+chapter.replace(' · ',' / ').upper()
 d.rectangle((0,0,2399,7),fill=color);logo(im,hl,(75,11,180));size=31
 while d.textlength(label,font=ft(size,'bold'))>1750:size-=1
 txt(d,(310,48),label,size,color)
 d.rounded_rectangle((2110,30,2325,100),radius=24,fill='white',outline='#92999D',width=2);txt(d,(2217,65),f'PAGE {n:02}',30,anchor='mm')
 # Approved footer 01: logo left, guide title centred, separate page number.
 d.line((75,3210,2325,3210),fill='#85898D',width=2);logo(im,fl,(75,3246,720))
 d.text((1470,3310),'LE GUIDE DU SKI',font=ft(34,'sans'),fill='#55595D',anchor='mm')
 d.line((2190,3245,2190,3372),fill='#B2B5B8',width=2);d.text((2285,3310),f'{n:02}',font=ft(60,'sans'),fill=INK,anchor='mm')
 for l in r.get('links',[]):
  x,y,x2,y2=l['box'];l['box']=[left+x*scale,120+(y-top)*scale,left+x2*scale,120+(y2-top)*scale]
 dest=OUT/f'page-{n:02}.webp';save(im,dest);r['path']=str(dest.relative_to(ROOT));audit.append({'page':n,'source':base['records'][n-1]['path'],'body_crop':[0,top,W,end],'scale':scale,'offset':[left,120]})
 if n in [1,2,3,21,22,28,31,32,41,42]:
  preview=im.copy();preview.thumbnail((800,1132));preview.save(HERE/f'preview-{n:02}.jpg',quality=94)
 print(n,dest.stat().st_size,flush=True)
cat.update(version='V07.85',cache='20261025-85')
(ROOT/'sources/guide/catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');(ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');(HERE/'audit.json').write_text(json.dumps(audit,indent=2))
s=(ROOT/'sources/bindings-v776-publish/apply.py').read_text();builder=s[s.index('for r,m in zip(records,'):].replace('20261024-76','20261025-85').replace('V07.76','V07.85').replace('range(1,41)','range(1,47)').replace("'__TOTAL__':'40'","'__TOTAL__':'46'");exec(builder)
