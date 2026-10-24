"""Insert the two approved hiking posters; preserve other content pixels."""
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
OUT=ROOT/'assets/guide-v774';OUT.mkdir(exist_ok=True)
BEFORE=json.loads((HERE/'baseline-v773.json').read_text())

# Reuse the established native contents layout; add two rows to chapter 2.
source=inspect.getsource(old.contents).replace('30 pages pour','32 pages pour')
source=source.replace("    labels={", "    desc={n+2 if n>=27 else n:v for n,v in desc.items()}\n    desc.update({27:'Construction, cuirs, semelles et membranes.',28:'Tige, rigidité, choix et essayage.'})\n    labels={")
source=source.replace('    groups=[', "    labels={n+2 if n>=27 else n:v for n,v in labels.items()}\n    labels.update({20:'Chaussures de ski de rando',27:'Chaussures de randonnée pédestre',28:'Randonnée : choisir et essayer'})\n    groups=[")
source=source.replace('range(17,27),119','range(17,29),100').replace('range(27,31),180','range(29,33),180')
source=source.replace('Rando, chaussures, snow, fond & textile','Rando ski et pédestre, textile & équipements')
exec(source,globals())
source=inspect.getsource(old.references)
source=re.sub('27–28|29–30',lambda m:{'27–28':'29–30','29–30':'31–32'}[m.group()],source)
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
        previous=record['page'];n=previous+2 if previous>=27 else previous
        new=deepcopy(record);new['page']=n
        for link in new.get('links',[]):
            if link['page']>=27:link['page']+=2
        if previous==2:
            p=contents();new['links']=p.links;areas=[]
        elif previous in [1,15,17,19,20,21] or previous>=27:
            p=Page(n);p.im=Image.open(ROOT/record['path']).convert('RGB');p.d=ImageDraw.Draw(p.im)
            assert p.im.size==(W,H)
            before=p.im.copy();areas=[]
            if previous==1:
                box=(1818,2805,2310,2862);areas.append(box);p.d.rectangle(box,fill=WHITE)
                p.text(1821,2815,'PAGE 29  →',29,'bold','#75638F')
            elif previous>=27:
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
    for n in [27,28]:
        source=HERE/f'page-{n}-approved.png';destination=OUT/f'page-{n:02}.png'
        pending=destination.with_suffix('.pending.png');shutil.copyfile(source,pending)
        with Image.open(pending) as check:check.verify()
        pending.replace(destination)
        assert source.read_bytes()==destination.read_bytes()
        records.append({'page':n,'path':str(destination.relative_to(ROOT)),'links':[]})
    records.sort(key=lambda r:r['page'])
    assert [r['page'] for r in records]==list(range(1,33))
    for r in records:
        path=ROOT/r['path'];assert path.stat().st_size>1000,path
        with Image.open(path) as check:check.verify()
    (ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    catalog=deepcopy(BEFORE['catalog']);catalog.update(version='V07.74',cache='20261024-74')
    for meta in catalog['pages']:
        if meta['page']>=27:meta['page']+=2
        meta['description']=re.sub('27–28|29–30',lambda m:{'27–28':'29–30','29–30':'31–32'}[m.group()],meta['description'])
    catalog['pages'][1]['description']='Sommaire cliquable des 32 pages : matériel 3–7, familles 8–18, chaussures de ski 19–20, snowboard 21–22, fond 23–24, textile 25–26, randonnée pédestre 27–28, fixations 29–30 et avalanche 31–32.'
    catalog['pages'][19]['title']='Les chaussures de ski de randonnée'
    catalog['pages'] += [
        {'page':27,'title':'Chaussures de randonnée pédestre','chapter':'02 · Reconnaître & conseiller','description':'Construction d’une chaussure de randonnée : tige, collier, pare-pierre, contrefort, semelles, cuir pleine fleur, nubuck, croûte, mesh, EVA et PU, cambrion, Vibram, crampons et membrane GORE-TEX.'},
        {'page':28,'title':'Randonnée pédestre : choisir et faire essayer','chapter':'02 · Reconnaître & conseiller','description':'Questions client, tiges basses, mid et hautes, flexion et torsion, rigidité, terrain, charge et durée. Essayage des deux pieds, chaussettes, laçage, maintien du talon, test en descente et entretien.'}]
    catalog['pages'].sort(key=lambda r:r['page'])
    (ROOT/'sources/guide/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    (HERE/'content-preservation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print('32 images verified; approved pages 27–28 copied byte-for-byte.')

if __name__=='__main__':main()
