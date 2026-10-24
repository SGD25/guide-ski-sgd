"""Apply selected client tabs and the soft orange reminder tint."""
from pathlib import Path
import sys,json
from copy import deepcopy
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'sources/guide'))
import render as base
from render import Page
BASELINE=json.loads((HERE/'baseline-v770.json').read_text())['records']
MEMORY=json.loads((ROOT/'sources/finalisation-v768/remember.json').read_text())
base.OUT=ROOT/'assets/guide-v771';base.OUT.mkdir(exist_ok=True)
BOXES={25:(32,1320,1024,1385),26:(32,1340,1024,1404),27:(32,1350,1024,1411),28:(32,1380,1023,1435)}
CLEAR={25:(27,1318,1028,1391),26:(27,1339,1028,1406),27:(27,1348,1028,1412),28:(27,1378,1028,1436)}
SECURITY={
25:('Le calcul est une étape. La sécurité dépend de tout l’ensemble ski–fixation–chaussure.',''),
26:('Donnée manquante, incompatibilité, défaut ou contrôle non concluant :','PAS DE DÉPART. Faire intervenir le responsable atelier.'),
27:('DVA + sonde + pelle + pratique régulière, pour chacun.','Le matériel ne remplace ni la préparation ni le renoncement.'),
28:('S’entraîner à toute la chaîne : chercher → sonder → pelleter → secourir.','Lire ces pages ne suffit pas à maîtriser un sauvetage.')}

CLIENTS=json.loads((HERE/'client-panels.json').read_text())

def main():
    records=deepcopy(BASELINE);log=[]
    for n in range(3,29):
        original=BASELINE[n-1];p=Page(n)
        p.im=Image.open(ROOT/original['path']).convert('RGB');p.d=ImageDraw.Draw(p.im);before=p.im.copy()
        clear=CLEAR[n] if n>=25 else (65,2940,2340,3220)
        p.d.rectangle(clear,fill=base.P['fond'])
        if n>=25:p.remember(*SECURITY[n],box=BOXES[n],compact=True)
        else:p.remember(*MEMORY[str(n)])
        areas=[clear]
        for c in [c for c in CLIENTS if c['page']==n]:
            a,b,a2,b2=c['box'];zone=(a-2,b-2,a2+2,b2+2);areas.append(zone)
            p.d.rectangle(zone,fill=base.P['fond'] if n==15 else base.WHITE)
            result=p.client(c['box'],c['speech'],c['size'],c.get('heading'));log.append(dict(page=n,**result))
        diff=ImageChops.difference(before,p.im)
        for area in areas:ImageDraw.Draw(diff).rectangle(area,fill=0)
        assert diff.getbbox() is None,('Content outside reminder changed',n)
        p.links=deepcopy(original.get('links',[]))
        if n<25:record=p.save()
        else:
            dest=base.OUT/f'page-{n:02}.png';p.im.save(dest,optimize=True)
            record=dict(page=n,path=str(dest.relative_to(ROOT)),links=p.links)
            preview=p.im.copy();preview.thumbnail((1000,1415));preview.save(base.CHECK/f'page-{n:02}.jpg',quality=93)
        record.update({k:v for k,v in original.items() if k not in ['page','path','links']})
        records[n-1]=record;print('Page',n,'OK',flush=True)
    (HERE/'layout-report.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
    assert len(log)==len(CLIENTS)
    assert records[:2]==BASELINE[:2]
    (ROOT/'sources/freeride-freestyle/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    path=ROOT/'sources/guide/catalog.json';c=json.loads(path.read_text());c.update(version='V07.71',cache='20261024-71');path.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
