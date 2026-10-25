from pathlib import Path
import sys,json,io,os
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'sources/guide'))
from render import Page,ft,INK,P
BG=P['fond'];base=json.loads((ROOT/'sources/snow-publish-v783/baseline-v782.json').read_text())
for old in [21,23,39]:
 n=old+2;im=Image.open(ROOT/base['records'][old-1]['path']).convert('RGB');d=ImageDraw.Draw(im)
 hb=(2107,33,2328,105);fb=(2265,3340,2380,3393)
 for b in [hb,fb]:d.rectangle(b,fill=BG)
 d.rounded_rectangle(hb,radius=24,fill=BG,outline='#8BA3AF',width=2);d.text(((hb[0]+hb[2])/2,(hb[1]+hb[3])/2),f'PAGE {n:02}',font=ft(31,'bold'),fill=INK,anchor='mm');d.text(((fb[0]+fb[2])/2,3350),f'{n:02}',font=ft(29,'bold'),fill=INK,anchor='mt')
 if n==23:
  p=Page(n);p.im=im;p.d=d;p.d.rectangle((70,3230,2000,3318),fill=BG);p.text(76,3237,'Repères adultes indicatifs, hors planches de carving alpin et splitboards. Hors-piste : équipement et formation adaptés ; voir sécurité avalanche pages 41–42. Sources : Nitro, RIDE, Burton, Nidecker. Photos fabricants.',26,width=1890,bottom=3313)
 out=io.BytesIO();im.save(out,format='PNG');data=out.getvalue();path=ROOT/f'assets/guide-v783/page-{n:02}.png'
 with open(path,'wb',buffering=0) as f:
  view=memoryview(data)
  while view:view=view[f.write(view):]
  os.fsync(f.fileno())
 assert path.read_bytes()==data
 print(n,len(data))
for f in [ROOT/'index.html',ROOT/'sources/guide/catalog.json',ROOT/'README.md',ROOT/'tests/guide-smoke.cjs',*list((ROOT/'pages').glob('*.js'))]:
 f.write_text(f.read_text().replace('20261025-83','20261025-84').replace('V07.83','V07.84'))
