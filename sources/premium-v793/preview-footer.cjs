// Proposal only: changes the browser DOM, never pages/branding.js.
const {chromium}=require('playwright');const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE_PATH,args:['--no-sandbox','--disable-gpu'],headless:true});
 const page=await browser.newPage({viewport:{width:1366,height:900},deviceScaleFactor:2});
 await page.goto('http://127.0.0.1:8765/#page=3');await page.locator('#reading-button').click();await page.evaluate(()=>document.fonts.ready);await page.locator('#left-page img').evaluate(i=>i.decode());await page.waitForTimeout(250);
 await page.evaluate(()=>scrollTo(0,0));
 const bounds=await page.locator('#left-page').boundingBox();
 await page.screenshot({path:'/tmp/sgd793-header-and-title.png',clip:{x:bounds.x,y:bounds.y,width:bounds.width,height:180}});
 await page.evaluate(()=>{
  const footer=document.querySelector('#left-page .page-brand-footer');
  footer.querySelector('path[d="M2190 60V160"]').setAttribute('d','M2015 60V160');
  footer.querySelector('text:last-child').remove();
  const ns='http://www.w3.org/2000/svg';
  for(const [label,y,size,color,spacing] of [['ÉDITION',88,25,'#6A6F73',2],['2026–2027',134,34,'#242426',.5]]){
   const t=document.createElementNS(ns,'text');t.textContent=label;
   for(const [name,value] of Object.entries({x:2180,y,'text-anchor':'middle','font-family':'Arial,sans-serif','font-size':size,fill:color,'letter-spacing':spacing}))t.setAttribute(name,String(value));
   footer.append(t);
  }
 });
 await page.locator('#left-page .page-brand-footer').screenshot({path:path.join(__dirname,'proposition-bas-de-page.png')});
 await browser.close();console.log('Saved footer proposal, guide footer unchanged.');
})().catch(e=>{console.error(e);process.exit(1)});
