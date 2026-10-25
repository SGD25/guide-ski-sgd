const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE_PATH,args:['--no-sandbox','--disable-gpu'],headless:true});
 const page=await browser.newPage({viewport:{width:1366,height:768}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8765/#page=3');await page.evaluate(()=>document.fonts.ready);
 await page.locator('#reading-button').click();await page.waitForTimeout(250);
 const bottom=()=>page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));
 async function top(expected){await page.waitForTimeout(150);assert(page.url().endsWith('page='+expected));const y=await page.locator('.book-frame').evaluate(e=>e.getBoundingClientRect().top);assert(Math.abs(y-16)<2,'New page starts at top: '+y);}
 await bottom();await page.waitForTimeout(100);assert(await page.evaluate(()=>scrollY)>500);
 await page.locator('#next').click();await top(4);
 await bottom();await page.keyboard.press('ArrowRight');await top(5);
 await bottom();await page.locator('#previous').click();await top(4);
 await page.evaluate(()=>scrollTo(0,600));await page.setViewportSize({width:1364,height:768});await page.waitForTimeout(250);assert(await page.evaluate(()=>scrollY)>500,'Resize must preserve reading position');
 await page.evaluate(()=>{location.hash='page=27'});await top(27);
 const header=page.locator('#left-page .page-brand-header');
 await header.screenshot({path:'/tmp/sgd792-chapter-header.png'});
 assert.equal(await page.locator('#print-pages .chapter-separator').count(),46);
 await page.locator('#reading-button').click();await page.locator('.spread-size-button').click();await page.evaluate(()=>scrollTo(0,300));await page.waitForTimeout(100);await page.keyboard.press('ArrowRight');await page.waitForTimeout(750);assert(await page.evaluate(()=>scrollY)>250,'Double-page view keeps its scroll');
 await page.setViewportSize({width:390,height:500});await page.goto('about:blank');await page.goto('http://127.0.0.1:8765/#page=3');await page.waitForTimeout(200);await bottom();await page.locator('#next').click();await top(4);
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS: zoom next/previous/keyboard/hash start at top; resize and double view retain position; mobile navigation; 46 separators');
})().catch(e=>{console.error(e);process.exit(1)});
