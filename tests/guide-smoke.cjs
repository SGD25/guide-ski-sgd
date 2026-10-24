const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const config=JSON.parse(read('sources/guide/catalog.json')),manifest=JSON.parse(read('sources/freeride-freestyle/manifest.json')),previous=JSON.parse(read('sources/bindings-v776-publish/baseline-v775.json'));
const tracked=new Set(cp.execFileSync('git',['ls-tree','-r','--name-only','HEAD'],{cwd:root,encoding:'utf8'}).trim().split('\n'));
const html=read('index.html'),ctx=vm.createContext({window:{}}),scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1].split('?')[0]);
assert.deepEqual(scripts.filter(s=>s.startsWith('./pages/')),['./pages/00-init.js',...Array.from({length:40},(_,i)=>`./pages/${String(i+1).padStart(2,'0')}.js`)]);
for(const s of scripts){assert(fs.existsSync(path.join(root,s)));if(s.startsWith('./pages/'))vm.runInContext(read(s),ctx)}
const pages=ctx.window.SGD_PAGES;assert.equal(pages.length,40);assert.equal(manifest.length,40);assert.equal(config.pages.length,40);
for(let i=0;i<40;i++){
 const p=pages[i],r=manifest[i];assert.equal(r.page,i+1);assert.equal(p.title,config.pages[i].title);assert.equal(p.chapter,config.pages[i].chapter);
 const imgs=[...p.html.matchAll(/<img src="([^"]+)"/g)];assert.equal(imgs.length,1);assert.equal(imgs[0][1].split('?')[0],'./'+r.path);
 if(fs.existsSync(path.join(root,r.path)))assert(fs.statSync(path.join(root,r.path)).size>1000);else assert(tracked.has(r.path),'Missing published asset '+r.path);
 for(const m of p.html.matchAll(/data-jump="(\d+)"/g))assert(+m[1]>=0&&+m[1]<40);
}
const toc=[...pages[1].html.matchAll(/data-jump="(\d+)"/g)].map(m=>+m[1]+1);assert.deepEqual([...new Set(toc)].sort((a,b)=>a-b),Array.from({length:38},(_,i)=>i+3));
for(let old=1;old<=34;old++){
 const n=old>=33?old+6:old,before=previous.records[old-1],after=manifest[n-1];
 if(old!==2)assert.deepEqual(after.links,before.links.map(l=>({...l,page:l.page>=33?l.page+6:l.page})));
 assert.deepEqual(after.overlays,before.overlays);
 if(![2,17,21,33,34].includes(old))assert.equal(after.path,before.path,'Unchanged poster must retain original asset');
}
for(const n of [31,32]){assert.deepEqual(manifest[n-1],previous.records[n-1]);assert.deepEqual(config.pages[n-1],previous.catalog.pages[n-1]);}
for(let n=33;n<=40;n++)assert.equal(pages[n-1].chapter,'03 · Sécuriser');
assert.match(pages[32].title,/NX12/);assert.match(pages[36].title,/PLUM/);assert.match(pages[38].title,/Avalanche/);
assert.match(html,/V07.77/);assert.match(html,/01–02 \/ 40/);
console.log('OK: 40 pages, complete clickable contents, original 31–32 preserved, six additions, avalanche links and external links preserved.');
