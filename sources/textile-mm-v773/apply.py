"""Install the approved membrane explanation, without rebuilding any other image."""
from pathlib import Path
from copy import deepcopy
import json, shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
manifest=ROOT/'sources/freeride-freestyle/manifest.json'
records=json.loads(manifest.read_text())
before=deepcopy(records)
assert len(records)==30 and records[25]['page']==26
source=HERE/'page-26-approved.png'
with Image.open(source) as image:
    image.verify()
destination=ROOT/'assets/guide-v773/page-26.png'
destination.parent.mkdir(exist_ok=True)
temporary=destination.with_suffix('.pending.png')
shutil.copyfile(source,temporary)
with Image.open(temporary) as image:
    image.verify()
temporary.replace(destination)
records[25]['path']=str(destination.relative_to(ROOT))
assert records[:25]==before[:25] and records[26:]==before[26:]
for record in records:
    path=ROOT/record['path']
    assert path.stat().st_size>1000,path
    with Image.open(path) as image:
        image.verify()
manifest.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
catalog=ROOT/'sources/guide/catalog.json'
config=json.loads(catalog.read_text())
config.update(version='V07.73',cache='20261024-73')
config['pages'][25]['description']='Déperlance, imperméabilité et respirabilité ; GORE-TEX et Sympatex ; colonne d’eau et indice Schmerber, 10 000, 15 000 et 20 000 mm, repères de conseil indicatifs, indices MVTR et RET et phrase à dire au client.'
catalog.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print('Page 26 installed; 29 other page records unchanged; all 30 images verified.')
