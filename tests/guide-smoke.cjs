const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const config=JSON.parse(read('sources/guide/catalog.json')),manifest=JSON.parse(read('sources/freeride-freestyle/manifest.json')),previous=JSON.parse(read('sources/bindings-v776-publish/baseline-v775.json'));
const tracked=new Set(cp.execFileSync('git',['ls-tree','-r','--name-only','HEAD'],{cwd:root,encoding:'utf8'}).trim().split('\n'));
const html=read('index.html'),ctx=vm.createContext({window:{}}),scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1].split('?')[0]);
assert.deepEqual(scripts.filter(s=>s.startsWith('./pages/')),['./pages/00-init.js',...Array.from({length:44},(_,i)=>`./pages/${String(i+1).padStart(2,'0')}.js`)]);
for(const s of scripts){assert(fs.existsSync(path.join(root,s)));if(s.startsWith('./pages/'))vm.runInContext(read(s),ctx)}
const pages=ctx.window.SGD_PAGES;assert.equal(pages.length,44);assert.equal(manifest.length,44);assert.equal(config.pages.length,44);
for(let i=0;i<44;i++){
 const p=pages[i],r=manifest[i];assert.equal(r.page,i+1);assert.equal(p.title,config.pages[i].title);assert.equal(p.chapter,config.pages[i].chapter);
 const imgs=[...p.html.matchAll(/<img src="([^"]+)"/g)];assert.equal(imgs.length,1);assert.equal(imgs[0][1].split('?')[0],'./'+r.path);
 if(fs.existsSync(path.join(root,r.path)))assert(fs.statSync(path.join(root,r.path)).size>1000);else assert(tracked.has(r.path),'Missing published asset '+r.path);
 for(const m of p.html.matchAll(/data-jump="(\d+)"/g))assert(+m[1]>=0&&+m[1]<44);
}
const toc=[...pages[1].html.matchAll(/data-jump="(\d+)"/g)].map(m=>+m[1]+1);assert.deepEqual([...new Set(toc)].sort((a,b)=>a-b),Array.from({length:42},(_,i)=>i+3));
const baseline=JSON.parse(read('sources/final-polish-v781/baseline-v780.json'));
for(let n=1;n<=44;n++){
 if(n!==2)assert.deepEqual(manifest[n-1].links,baseline.records[n-1].links);
 assert.deepEqual(manifest[n-1].overlays,baseline.records[n-1].overlays);
}
for(const n of [31,32]){
 assert.equal(config.pages[n-1].title,baseline.catalog.pages[n-1].title);
 assert.equal(config.pages[n-1].description,baseline.catalog.pages[n-1].description);
}
for(const [lo,hi,ch] of [[3,7,'01 · Comprendre'],[8,24,'02 · Reconnaître et conseiller le matériel'],[25,30,'03 · Reconnaître et conseiller textiles et accessoires'],[31,40,'04 · Sécuriser'],[41,44,'05 · Accueillir, louer et accompagner']]){
 for(let n=lo;n<=hi;n++)assert.equal(pages[n-1].chapter,ch);
}
assert.match(pages[34].title,/NX12/);assert.match(pages[36].title,/PLUM/);assert.match(pages[38].title,/Avalanche/);
assert.match(html,/V07.81/);assert.match(html,/01–02 \/ 44/);
console.log('OK: 44 pages, complete clickable contents, five chapters, original 31–32 text preserved, complete navigation.');
