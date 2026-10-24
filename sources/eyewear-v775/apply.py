"""Insert the two approved eyewear posters; preserve other content pixels."""
from pathlib import Path
from copy import deepcopy
import importlib.util, inspect, json, re, shutil, sys
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as base
from render import Page, INK, BODY, TEAL, BLUE, CORAL, WHITE, LINE, DARK, ft
BG=base.P['fond'];W,H=2400,3394
spec=importlib.util.spec_from_file_location('textile772',ROOT/'sources/textile-v772/render.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
furniture=old.furniture
OUT=ROOT/'assets/guide-v775';OUT.mkdir(exist_ok=True)
BEFORE=json.loads((HERE/'baseline-v774.json').read_text())

# Reuse the established native contents layout; add two rows to chapter 2.
source=inspect.getsource(old.contents).replace('30 pages pour','34 pages pour')
source=source.replace("    labels={", "    desc={n+4 if n>=27 else n:v for n,v in desc.items()}\n    desc.update({27:'Construction, cuirs, semelles et membranes.',28:'Tige, rigidité, choix et essayage.',29:'Catégories, VLT, UV et météo.',30:'Technologies, buée et essayage.'})\n    labels={")
source=source.replace('    groups=[', "    labels={n+4 if n>=27 else n:v for n,v in labels.items()}\n    labels.update({20:'Chaussures de ski de rando',27:'Chaussures de randonnée pédestre',28:'Randonnée : choisir et essayer',29:'Masques & lunettes : choisir',30:'Masques & lunettes : technologies'})\n    groups=[")
source=source.replace('range(17,27),119','range(17,31),100').replace('range(27,31),180','range(31,35),130')
source=source.replace('Rando, chaussures, snow, fond & textile','Rando ski et pédestre, textile & équipements')
source=source.replace('1230,440,2330,1875','1230,440,2330,2075').replace('1230,1905,2330,2845','1230,2105,2330,2845')
exec(source,globals())
source=inspect.getsource(old.references)
source=re.sub('27–28|29–30',lambda m:{'27–28':'31–32','29–30':'33–34'}[m.group()],source)
exec(source,globals())

def save_atomic(image,destination):
    pending=destination.with_suffix('.pending.png')
    image.save(pending,format='PNG',compress_level=6)
    with Image.open(pending) as check:check.verify()
    assert pending.stat().st_size>1000
    pending.replace(destination)

def main():
    records=[];audit=[]
    for record in BEFORE['records']:
        previous=record['page'];n=previous+2 if previous>=29 else previous
        new=deepcopy(record);new['page']=n
        for link in new.get('links',[]):
            if link['page']>=29:link['page']+=2
        if previous==2:
            p=contents();new['links']=p.links;areas=[]
        elif previous in [1,15,17,19,20,21] or previous>=29:
            p=Page(n);p.im=Image.open(ROOT/record['path']).convert('RGB');p.d=ImageDraw.Draw(p.im)
            assert p.im.size==(W,H)
            before=p.im.copy();areas=[]
            if previous==1:
                box=(1818,2805,2310,2862);areas.append(box);p.d.rectangle(box,fill=WHITE)
                p.text(1821,2815,'PAGE 31  →',29,'bold','#75638F')
            elif previous>=29:
                box=(2110,36,2324,102);areas.append(box)
                p.rect(box,BG,base.P['reperes'],28,2)
                p.text(2217,53,f'PAGE {n:02}',31,'bold',INK,center=True)
                box=(2270,3340,2375,3393);areas.append(box);p.d.rectangle(box,fill=BG)
                p.text(2325,3350,f'{n:02}',29,'bold',INK,center=True)
            else:areas=references(p,previous)
            difference=ImageChops.difference(before,p.im)
            for box in areas:ImageDraw.Draw(difference).rectangle(box,fill=0)
            assert difference.getbbox() is None,('Content changed outside pagination',previous)
            audit.append({'previous_page':previous,'page':n,'allowed_regions':areas})
        else:
            records.append(new);continue
        destination=OUT/f'page-{n:02}.png';save_atomic(p.im,destination)
        new['path']=str(destination.relative_to(ROOT));records.append(new)
        print('Page',n,'ready',flush=True)
    for n in [29,30]:
        source=HERE/f'page-{n}-approved.png';destination=OUT/f'page-{n:02}.png'
        pending=destination.with_suffix('.pending.png');shutil.copyfile(source,pending)
        with Image.open(pending) as check:check.verify()
        pending.replace(destination)
        assert source.read_bytes()==destination.read_bytes()
        records.append({'page':n,'path':str(destination.relative_to(ROOT)),'links':[]})
    records.sort(key=lambda r:r['page'])
    assert [r['page'] for r in records]==list(range(1,35))
    for r in records:
        path=ROOT/r['path'];assert path.stat().st_size>1000,path
        with Image.open(path) as check:check.verify()
    (ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    catalog=deepcopy(BEFORE['catalog']);catalog.update(version='V07.75',cache='20261024-75')
    for meta in catalog['pages']:
        if meta['page']>=29:meta['page']+=2
        meta['description']=re.sub('29–30|31–32',lambda m:{'29–30':'31–32','31–32':'33–34'}[m.group()],meta['description'])
    catalog['pages'][1]['description']='Sommaire cliquable des 34 pages : matériel 3–7, familles 8–18, chaussures de ski 19–20, snowboard 21–22, fond 23–24, textile 25–26, randonnée pédestre 27–28, masques et lunettes 29–30, fixations 31–32 et avalanche 33–34.'
    catalog['pages'][19]['title']='Les chaussures de ski de randonnée'
    catalog['pages'] += [
        {'page':29,'title':'Masques et lunettes : choisir selon la météo','chapter':'02 · Reconnaître & conseiller','description':'Catégories 0 à 4, VLT, protection UV, mauvais temps, temps changeant et soleil. Questions client et choix du masque ou des lunettes.'},
        {'page':30,'title':'Masques et lunettes : technologies et essayage','chapter':'02 · Reconnaître & conseiller','description':'Photochromique, polarisé, contrastes, exemples AZR Kromic, Smith ChromaPop et Cairn Evolight. Double écran, ventilation, antibuée, traitements, OTG, essayage et entretien.'}]
    catalog['pages'].sort(key=lambda r:r['page'])
    (ROOT/'sources/guide/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    (HERE/'content-preservation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print('34 images verified; approved pages 29–30 copied byte-for-byte.')

if __name__=='__main__':main()
