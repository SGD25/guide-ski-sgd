// Integration checks use the published HTML, real page scripts and source catalog.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('index.html'),config=JSON.parse(read('sources/guide/catalog.json'));
const manifest=JSON.parse(read('sources/freeride-freestyle/manifest.json'));
const baseline=JSON.parse(read('sources/finalisation/baseline-v766.json'));
const previous=JSON.parse(read('sources/textile-v772/baseline-v771.json'));
const context=vm.createContext({window:{}}),local=src=>path.join(root,src.split('?')[0]);
const scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1]);
const actual=scripts.filter(s=>s.startsWith('./pages/')).map(s=>s.split('?')[0]);
assert.deepEqual(actual,['./pages/00-init.js',...Array.from({length:30},(_,i)=>`./pages/${String(i+1).padStart(2,'0')}.js`)]);
for(const src of scripts){assert(fs.existsSync(local(src)),`Missing script: ${src}`);if(src.startsWith('./pages/'))vm.runInContext(fs.readFileSync(local(src),'utf8'),context,{filename:src});}
const pages=context.window.SGD_PAGES;assert.equal(pages.length,30,'All published chapters, including security, must survive a rebuild');
assert.equal(manifest.length,30);assert.equal(config.pages.length,30);
for(const [i,page] of pages.entries()){
 assert.equal(page.title,config.pages[i].title);assert.equal(page.chapter,config.pages[i].chapter);
 const imgs=[...page.html.matchAll(/<img src="([^"]+)"/g)];assert.equal(imgs.length,1,`Page ${i+1}: one complete image`);
 assert(fs.existsSync(local(imgs[0][1])),`Missing image on page ${i+1}`);
 assert(fs.statSync(local(imgs[0][1])).size>1000,`Empty or truncated image on page ${i+1}`);
 assert(page.html.includes(`data-page="${i+1}"`));
 assert.equal(manifest[i].page,i+1);
 for(const m of page.html.matchAll(/data-jump="(\d+)"/g)){const n=Number(m[1]);assert(n>=0&&n<pages.length);}
}
const contents=[...pages[1].html.matchAll(/data-jump="(\d+)"/g)].map(m=>Number(m[1])+1);
assert.deepEqual([...new Set(contents)].sort((a,b)=>a-b),Array.from({length:28},(_,i)=>i+3),'The printed contents must link to every content page');
assert.match(pages[18].title,/chaussures alpines/i);assert.match(pages[19].title,/chaussures.*randonn/i);
assert.match(pages[20].title,/snowboard/i);assert.match(pages[21].title,/Nitro/);
assert.match(pages[22].title,/fond/i);assert.match(pages[23].title,/classique.*skating/i);
assert.match(pages[24].title,/textile.*3 couches/i);
assert.match(pages[25].title,/textile.*membranes/i);
assert.equal(pages[24].chapter,'02 · Reconnaître & conseiller');
assert.equal(pages[25].chapter,'02 · Reconnaître & conseiller');
for(let old=1;old<=28;old++){
 if(old===2)continue; // contents has the two new entries and updated destinations
 const n=old>=25?old+2:old;
 const expected=previous.records[old-1].links.map(l=>({...l,page:l.page>=25?l.page+2:l.page}));
 assert.deepEqual(manifest[n-1].links,expected,`Internal links must follow insertion on page ${n}`);
 assert.deepEqual(manifest[n-1].overlays,previous.records[old-1].overlays,`External links preserved on page ${n}`);
}
for(const n of [27,28,29,30]){
 assert.equal(pages[n-1].chapter,'03 · Sécuriser');
 for(const overlay of previous.records[n-3].overlays||[])assert(pages[n-1].html.includes(overlay),`Security link lost on page ${n}`);
}
const products=JSON.parse(read('sources/guide/piste-products.json'));
assert.match(products[1].name,/Forza 40/);assert.equal(products[1].h,'Piste polyvalent');
assert.match(products[2].name,/Forza 70/);assert.equal(products[2].h,'Piste performance');
assert.equal(products[2].rows.find(r=>r[0]==='Niveau')[1],'Avancé à expert');
for(const m of html.matchAll(/<link rel="stylesheet" href="([^"]+)"/g))assert(fs.existsSync(local(m[1])));
console.log('OK: 30 pages, textile before safety, full contents, shifted internal links, preserved external safety links and Forza positioning.');
