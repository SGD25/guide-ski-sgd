// Integration check: load the actual scripts in their HTML order.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const context=vm.createContext({window:{}});
const local=src=>path.join(root,src.split('?')[0]);
const scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1]);
assert(scripts.length>1);
for(const src of scripts){
  assert(fs.existsSync(local(src)),`Missing script: ${src}`);
  if(src.startsWith('./pages/'))vm.runInContext(fs.readFileSync(local(src),'utf8'),context,{filename:src});
}
const pages=context.window.SGD_PAGES;
assert.equal(pages.length,20,'The guide must expose all 20 pages');
for(const [i,page] of pages.entries()){
  const images=[...page.html.matchAll(/<img src="([^"]+)"/g)];
  assert.equal(images.length,1,`Page ${i+1} must be one complete image`);
  assert(fs.existsSync(local(images[0][1])),`Missing image on page ${i+1}`);
  for(const m of page.html.matchAll(/data-jump="(\d+)"/g))assert(Number(m[1])<pages.length);
}
for(const m of html.matchAll(/<link rel="stylesheet" href="([^"]+)"/g))assert(fs.existsSync(local(m[1])));
console.log('OK: script order, 20 complete pages, images, styles and navigation targets.');
