const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
  const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE_PATH,args:['--no-sandbox','--disable-gpu'],headless:true});
  const page=await browser.newPage({viewport:{width:1920,height:1080}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/#page=3');
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('#left-page img').evaluate(i=>i.decode());
  await page.waitForTimeout(250);
  async function geometry(){return page.evaluate(()=>{
    const object=document.querySelector('.book-object'),w=object.clientWidth,h=object.clientHeight;
    const point=(x,y)=>{const p=document.createElement('span');p.setAttribute('aria-hidden','true');p.style.cssText=`position:absolute;left:${x}px;top:${y}px;width:0;height:0;pointer-events:none`;object.append(p);const r=p.getBoundingClientRect();p.remove();return {x:r.x,y:r.y};};
    return {tl:point(0,0),tr:point(w,0),bl:point(0,h),br:point(w,h)};
  });}
  let g=await geometry();
  const top=g.tr.x-g.tl.x,bottom=g.br.x-g.bl.x;
  assert(top<bottom*.98&&top>bottom*.94,'Visible sides must taper toward the top');
  assert(Math.abs((g.tl.x+g.tr.x-g.bl.x-g.br.x)/2)<1,'Spine remains centered');
  const type=await page.evaluate(()=>{
    const brand=document.querySelector('.brand-name'),small=brand.querySelector('small');
    const titleRange=document.createRange();titleRange.selectNodeContents(brand.firstChild);
    const subRange=document.createRange();subRange.selectNodeContents(small);
    return {font:[...document.fonts].some(f=>f.family==='SGD Inter'&&f.status==='loaded'),title:titleRange.getBoundingClientRect().width,subtitle:subRange.getBoundingClientRect().width};
  });
  assert(type.font,'Bundled font loaded');assert(type.subtitle>type.title,'Subtitle is visibly wider than title');
  await page.locator('#right-page .sgd-poster>img').click();
  await page.waitForTimeout(250);g=await geometry();
  assert(Math.abs((g.tr.x-g.tl.x)-(g.br.x-g.bl.x))<1,'Single page has no perspective');
  assert(page.url().endsWith('page=4'),'Image zoom selects clicked right page');
  await page.locator('#reading-button').click();
  await page.locator('#previous').click();await page.waitForTimeout(750);
  assert(page.url().endsWith('page=1'));
  const target=page.locator('#right-page .poster-link[data-jump="20"]').first();
  await target.click();assert(page.url().endsWith('page=21'),'Transformed page contents remain clickable');
  await page.keyboard.press('ArrowRight');await page.waitForTimeout(750);
  assert(page.url().endsWith('page=23'),'Keyboard page turn works');
  await page.emulateMedia({media:'print'});
  const printing=await page.locator('.print-page').evaluateAll(pages=>({count:pages.length,plain:pages.every(p=>getComputedStyle(p.querySelector('.sheet')).transform==='none'),images:pages.every(p=>{const i=p.querySelector('img');return i.naturalWidth===2400&&i.naturalHeight===3394})}));
  assert.equal(printing.count,46);assert(printing.plain);assert(printing.images);
  assert.deepEqual(errors,[]);await browser.close();
  console.log('PASS: genuine taper, embedded font, subtitle proportions, flat zoom/print, transformed page links and keyboard navigation');
})().catch(e=>{console.error(e);process.exit(1)});
