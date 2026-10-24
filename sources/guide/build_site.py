"""Build every published image page from the shared catalog without dropping later chapters."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[2]
records=json.loads((ROOT/'sources/freeride-freestyle/manifest.json').read_text())
config=json.loads((ROOT/'sources/guide/catalog.json').read_text())
catalog=config['pages'];total=len(records);cache=config['cache']
assert total==len(catalog)
for n,(record,meta) in enumerate(zip(records,catalog),1):
    assert record['page']==meta['page']==n
    assert (ROOT/record['path']).is_file(),record['path']
    markup=f'<figure class="sgd-poster" data-page="{n}"><img src="./{record["path"]}?v={cache}" alt="{html.escape(meta["description"],quote=True)}" width="2400" height="3394" loading="eager" decoding="async">'
    for link in record.get('links',[]):
        target=link['page'];assert 1<=target<=total
        x,y,x2,y2=link['box'];assert 0<=x<x2<=2400 and 0<=y<y2<=3394
        style=f'left:{x/24:.5f}%;top:{y/33.94:.5f}%;width:{(x2-x)/24:.5f}%;height:{(y2-y)/33.94:.5f}%'
        markup+=f'<button type="button" class="poster-link page-jump" data-jump="{target-1}" style="{style}" aria-label="{html.escape(link["label"]+" — page "+str(target),quote=True)}"></button>'
    markup+=''.join(record.get('overlays',[]))+'</figure>'
    page={'title':meta['title'],'chapter':meta['chapter'],'html':markup}
    (ROOT/f'pages/{n:02}.js').write_text('window.SGD_PAGES.push('+json.dumps(page,ensure_ascii=False,separators=(',',':'))+');\n')
scripts=f'<script src="./pages/00-init.js?v={cache}"></script>\n'+'\n'.join(f'<script src="./pages/{n:02}.js?v={cache}"></script>' for n in range(1,total+1))
template=(ROOT/'sources/guide/reader-template.html').read_text()
for key,value in {'__CACHE__':cache,'__VERSION__':config['version'],'__TOTAL__':str(total),'__SCRIPTS__':scripts}.items():template=template.replace(key,value)
assert '__SCRIPTS__' not in template
(ROOT/'index.html').write_text(template)
print(f'Lecteur {config["version"]}, {total} pages, catalogue et liens reliés.')
