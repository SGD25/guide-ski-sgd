"""V07.68: targeted native changes and one consistent high-contrast reminder.

The V07.67 manifest is immutable input. Approved poster content outside requested
areas is retained. Safety pages retain their original pixels outside the reminder
text box, their badge and their external links.
"""
from pathlib import Path
import importlib.util,json,sys
from copy import deepcopy
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as base
from render import Page,WHITE,INK,BODY,TEAL,CORAL,DARK,LINE
spec=importlib.util.spec_from_file_location('final767',ROOT/'sources/finalisation/render.py')
final=importlib.util.module_from_spec(spec);spec.loader.exec_module(final)
base.OUT=ROOT/'assets/guide-v768';base.OUT.mkdir(exist_ok=True)
BASELINE=json.loads((HERE/'baseline-v767.json').read_text())['records']
MEMORY=json.loads((HERE/'remember.json').read_text())

def radius():
    p=final.radius()
    p.rect((838,2430,1562,2865),WHITE,LINE,22,3)
    p.text(868,2460,'Lire le rayon',43,'serif',INK,width=664)
    p.text(868,2535,'R = 17 m',53,'bold',TEAL,width=664)
    p.text(868,2614,'Aussi appelé « radius ».',32,'bold',TEAL,width=664)
    p.text(868,2670,'Chercher R ou « radius » près des lignes de cotes, au talon ou au patin. La valeur dépend de la longueur du ski.',34,width=664,leading=39,bottom=2855)
    return p

BUILDERS={3:final.anatomy,4:final.dimensions,5:radius,9:final.piste,
          11:base.allmountain,15:final.juniors.advice_page,
          17:final.rando.intro_page,19:final.boots.alpine}

def safety(record):
    n=record['page'];p=Page(n);p.im=Image.open(ROOT/record['path']).convert('RGB');original=p.im.copy();p.d=ImageDraw.Draw(p.im)
    boxes={25:(252,1320,1024,1385),26:(252,1340,1024,1404),27:(252,1350,1024,1411),28:(229,1380,1023,1435)}
    box=boxes[n];x,y,x2,y2=box
    p.d.rectangle(box,fill='#FAFCFD');p.rect(box,DARK,CORAL,13,2)
    if n==25:
        p.text(x+16,y+12,'Le calcul est une étape. La sécurité dépend de tout l’ensemble ski–fixation–chaussure.',19,'serif',WHITE,width=x2-x-32,leading=23,bottom=y2-3)
    else:
        heads={26:'Donnée manquante, incompatibilité, défaut ou contrôle non concluant :',27:'DVA + sonde + pelle + pratique régulière, pour chacun.',28:'S’entraîner à toute la chaîne : chercher → sonder → pelleter → secourir.'}
        bodies={26:'PAS DE DÉPART. Faire intervenir le responsable atelier.',27:'Le matériel ne remplace ni la préparation ni le renoncement.',28:'Lire ces pages ne suffit pas à maîtriser un sauvetage.'}
        p.text(x+15,y+7,heads[n],16 if n==26 else 18,'serif',WHITE,width=x2-x-30,leading=21,bottom=y+30)
        p.text(x+15,y+33 if n!=28 else y+30,bodies[n],17,'bold' if n==26 else 'sans',WHITE,width=x2-x-30,leading=20,bottom=y2-1)
    diff=ImageChops.difference(original,p.im);ImageDraw.Draw(diff).rectangle(box,fill=0)
    assert diff.getbbox() is None,('Safety pixels changed outside reminder',n)
    dest=base.OUT/f'page-{n:02}.png';p.im.save(dest,optimize=True)
    preview=p.im.copy();preview.thumbnail((1000,1415));preview.save(base.CHECK/f'page-{n:02}.jpg',quality=93)
    return dict(record,path=str(dest.relative_to(ROOT)))

def main():
    records=deepcopy(BASELINE)
    for n in range(3,25):
        approved=BASELINE[n-1]
        if n in BUILDERS:p=BUILDERS[n]()
        else:
            p=Page(n);p.im=Image.open(ROOT/approved['path']).convert('RGB');p.d=ImageDraw.Draw(p.im)
        assert p.im.size==(2400,3394)
        before=p.im.copy()
        p.d.rectangle((65,2940,2340,3220),fill=base.P['fond'])
        p.remember(*MEMORY[str(n)])
        if n not in BUILDERS:
            diff=ImageChops.difference(before,p.im);ImageDraw.Draw(diff).rectangle((65,2940,2340,3220),fill=0)
            assert diff.getbbox() is None,('Approved content modified',n)
        p.links=deepcopy(approved.get('links',[]))
        record=p.save();record.update({k:v for k,v in approved.items() if k not in ['path','page','links']})
        records[n-1]=record;print('Page',n,'OK',flush=True)
    for n in range(25,29):records[n-1]=safety(BASELINE[n-1]);print('Page',n,'OK',flush=True)
    assert records[:2]==BASELINE[:2]
    (ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    config=ROOT/'sources/guide/catalog.json';c=json.loads(config.read_text());c.update(version='V07.68',cache='20261024-68');config.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
