const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const config=JSON.parse(read('sources/guide/catalog.json')),manifest=JSON.parse(read('sources/freeride-freestyle/manifest.json')),previous=JSON.parse(read('sources/snow-publish-v783/baseline-v782.json'));
const tracked=new Set(cp.execFileSync('git',['ls-tree','-r','--name-only','HEAD'],{cwd:root,encoding:'utf8'}).trim().split('\n'));
const html=read('index.html'),ctx=vm.createContext({window:{}}),scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1].split('?')[0]);
assert.deepEqual(scripts.filter(s=>/^\.\/pages\/\d/.test(s)),['./pages/00-init.js',...Array.from({length:46},(_,i)=>`./pages/${String(i+1).padStart(2,'0')}.js`)]);
for(const s of scripts){assert(fs.existsSync(path.join(root,s)));if(/^\.\/pages\/\d/.test(s))vm.runInContext(read(s),ctx)}
const pages=ctx.window.SGD_PAGES;assert.equal(pages.length,46);assert.equal(manifest.length,46);assert.equal(config.pages.length,46);
for(let i=0;i<46;i++){
 const p=pages[i],r=manifest[i];assert.equal(r.page,i+1);assert.equal(p.title,config.pages[i].title);assert.equal(p.chapter,config.pages[i].chapter);
 const imgs=[...p.html.matchAll(/<img src="([^"]+)"/g)];assert.equal(imgs.length,1);assert.equal(imgs[0][1].split('?')[0],'./'+r.path);
 if(fs.existsSync(path.join(root,r.path)))assert(fs.statSync(path.join(root,r.path)).size>1000);else assert(tracked.has(r.path),'Missing published asset '+r.path);
 for(const m of p.html.matchAll(/data-jump="(\d+)"/g))assert(+m[1]>=0&&+m[1]<46);
}
const toc=[...pages[1].html.matchAll(/data-jump="(\d+)"/g)].map(m=>+m[1]+1);assert.deepEqual([...new Set(toc)].sort((a,b)=>a-b),Array.from({length:44},(_,i)=>i+3));
const baseline=previous;
for(let old=1;old<=44;old++){
 const n=old>=21?old+2:old;
 if(old!==2)assert.deepEqual(manifest[n-1].links.map(({box,...l})=>l),baseline.records[old-1].links.map(({box,...l})=>({...l,page:l.page>=21?l.page+2:l.page})));
 assert.deepEqual(manifest[n-1].overlays,baseline.records[old-1].overlays);
}
for(const old of [31,32]){
 assert.equal(config.pages[old+1].title,baseline.catalog.pages[old-1].title);
 assert.equal(config.pages[old+1].description,baseline.catalog.pages[old-1].description);
}
for(const [lo,hi,ch] of [[3,7,'01 · Comprendre'],[8,26,'02 · Reconnaître et conseiller le matériel'],[27,32,'03 · Reconnaître et conseiller textiles et accessoires'],[33,42,'04 · Sécuriser'],[43,46,'05 · Accueillir, louer et accompagner']]){
 for(let n=lo;n<=hi;n++)assert.equal(pages[n-1].chapter,ch);
}
assert.match(pages[36].title,/NX12/);assert.match(pages[38].title,/PLUM/);assert.match(pages[40].title,/Avalanche/);
assert.match(html,/V07.87/);assert.match(html,/01–02 \/ 46/);
console.log('OK: 46 pages, complete clickable contents, five chapters, original 31–32 text preserved, complete navigation.');
assert.match(html,/assets\/branding-v785\/logo-header.svg/);
for(const r of manifest)for(const l of r.links||[])assert(l.box[0]>=0&&l.box[1]>=0&&l.box[2]<=2400&&l.box[3]<=3394);

vm.runInContext(read("pages/branding.js"),ctx);
for(const p of pages){assert.match(p.html,/page-brand-header/);assert.match(p.html,/page-brand-footer/)}
console.log("OK: approved header/footer overlays on all 46 pages.");
