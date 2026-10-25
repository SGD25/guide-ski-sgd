/* Reader for complete page images. Content is loaded from pages/NN.js. */
(() => {
  'use strict';
  const pages=window.SGD_PAGES||[],el=id=>document.getElementById(id);
  const book=el('book'),left=el('left-page'),right=el('right-page'),leaf=el('flip-sheet');
  const prev=el('previous'),next=el('next'),toc=el('toc-overlay'),grid=el('toc-grid'),bookSize=el('book-size-button');
  // Align chrome with the rendered book in double, wide and single-page modes.
  const frame=book.closest('.book-frame'),edgeControls=prev.parentElement;
  let chromeFrame=0,chromeSizeKey='',reservedBannerExtra=0;
  function alignReaderChrome(){
    chromeFrame=0;
    const r=frame.getBoundingClientRect(),mobile=matchMedia('(max-width:780px)').matches;
    const singleView=mobile||document.body.classList.contains('reading-mode');
    const sizeKey=[innerWidth,innerHeight,singleView,document.body.classList.contains('wide-spread')].join(':');
    if(sizeKey!==chromeSizeKey){chromeSizeKey=sizeKey;reservedBannerExtra=0;}
    document.body.style.setProperty('--reader-width',r.width+'px');
    const banner=document.querySelector('.appbar').getBoundingClientRect();
    const actions=document.querySelector('.appbar-actions').getBoundingClientRect();
    const brand=document.querySelector('.brand').getBoundingClientRect();
    // The banner follows book width and the book fits below the banner. Reserve the
    // largest measured banner height in this layout to prevent breakpoint oscillation.
    reservedBannerExtra=Math.max(reservedBannerExtra,banner.height-80,0);
    document.body.style.setProperty('--banner-extra',reservedBannerExtra+'px');
    const actionsX=actions.left-banner.left,brandEnd=brand.right-banner.left;
    const darkLeft=Math.min(actionsX-12,Math.max(brandEnd+8,Math.min(banner.width*(mobile?.44:.56),actionsX-36)));
    document.body.style.setProperty('--banner-dark-left',darkLeft+'px');
    document.body.style.setProperty('--banner-cut',Math.max(0,Math.min(mobile?32:64,actionsX-darkLeft-8))+'px');
    const cover=window.SGD_BOOK_EFFECTS?.layout(r.width,r.height,singleView,mobile)||(mobile?11:19),half=mobile?15:20;
    document.body.style.setProperty('--book-cover',cover+'px');
    const top=Math.max(0,r.top),bottom=Math.min(innerHeight,r.bottom);
    const controlsY=(top+bottom)/2;
    // Follow the tapered cover at the buttons' actual vertical position.
    const progress=Math.max(0,Math.min(1,(controlsY-r.top)/r.height));
    const taper=singleView?0:.04,localScale=1-taper+taper*progress;
    const edge=(r.width/2+cover)*localScale;
    document.body.style.setProperty('--book-previous-x',(r.left+r.width/2-edge-half)+'px');
    document.body.style.setProperty('--book-next-x',(r.left+r.width/2+edge-half)+'px');
    document.body.style.setProperty('--book-controls-y',controlsY+'px');
    edgeControls.dataset.offscreen=String(bottom<=top);
  }
  function queueReaderChrome(){if(!chromeFrame)chromeFrame=requestAnimationFrame(alignReaderChrome);}
  const chromeObserver=new ResizeObserver(queueReaderChrome);
  chromeObserver.observe(frame);chromeObserver.observe(document.querySelector('.appbar'));
  chromeObserver.observe(document.querySelector('.brand'));chromeObserver.observe(document.querySelector('.appbar-actions'));
  document.fonts.ready.then(queueReaderChrome);
  addEventListener('resize',queueReaderChrome);addEventListener('scroll',queueReaderChrome,{passive:true});
  queueReaderChrome();
  let current=0,busy=false,hasRendered=false;
  const single=()=>matchMedia('(max-width:780px)').matches||document.body.classList.contains('reading-mode');
  const step=()=>single()?1:2,snap=n=>single()?n:Math.floor(n/2)*2;
  const markup=p=>p?'<div class="sheet-pad">'+p.html+'</div>':'';
  function apply(node,p){node.innerHTML=markup(p);node.setAttribute('aria-label',p?p.title:'Page vierge');}
  function renderAt(n){
    const previousPage=current;
    current=Math.max(0,Math.min(pages.length-1,snap(n)));
    apply(left,pages[current]);apply(right,pages[current+1]);
    const last=Math.min(pages.length,current+step());
    el('page-count').textContent=(single()?String(current+1).padStart(2,'0'):String(current+1).padStart(2,'0')+'–'+String(last).padStart(2,'0'))+' / '+String(pages.length).padStart(2,'0');
    const visible=pages.slice(current,current+step());
    const chapters=[...new Set(visible.map(p=>p.chapter))];
    el('chapter-band').replaceChildren(...chapters.map(c=>{const s=document.createElement('span');s.className=c.startsWith('01')?'chapter-one':c.startsWith('02')?'chapter-two':c.startsWith('03')?'chapter-three':c.startsWith('04')?'chapter-four':c.startsWith('05')?'chapter-five':'chapter-opening';s.textContent=c==='Ouverture'?'LE GUIDE DU SKI · OUVERTURE':'CHAPITRE '+c.toUpperCase();return s;}));
    prev.disabled=current===0;next.disabled=current+step()>=pages.length;el('progress').style.width=last/pages.length*100+'%';
    document.title=pages[current].title+' — SPORT GOOD DEAL';history.replaceState(null,'','#page='+(current+1));
    // Every new page/spread starts at its heading, including the wide book. Resizing or
    // rerendering the same page must not interrupt the reader's scroll position.
    if(hasRendered&&current!==previousPage){
      requestAnimationFrame(()=>{
        scrollTo({top:Math.max(0,scrollY+frame.getBoundingClientRect().top-16),behavior:'instant'});
        queueReaderChrome();
      });
    }
    hasRendered=true;
  }
  function go(dir){
    const target=current+dir*step();if(busy||target<0||target>=pages.length)return;
    if(single()||matchMedia('(prefers-reduced-motion:reduce)').matches){renderAt(target);return;}
    busy=true;leaf.innerHTML='<div class="flip-side flip-front">'+markup(pages[dir>0?current+1:current])+'</div><div class="flip-side flip-back">'+markup(pages[dir>0?target:target+1])+'</div>';
    book.classList.add(dir>0?'is-forward':'is-backward');setTimeout(()=>renderAt(target),325);
    setTimeout(()=>{book.classList.remove('is-forward','is-backward');leaf.innerHTML='';busy=false;},660);
  }
  function setBookWide(on){
    document.body.classList.toggle('wide-spread',on);
    const label=on?'Rétrécir le livre':'Élargir le livre';
    const arrows=on?'M3 12h6m-3-3 3 3-3 3M21 12h-6m3-3-3 3 3 3':'M9 12H3m3-3-3 3 3 3M15 12h6m-3-3 3 3-3 3';
    bookSize.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4h6M9 20h6'+arrows+'"/></svg>'+label;
    bookSize.setAttribute('aria-pressed',String(on));
    bookSize.setAttribute('aria-label',label);
    queueReaderChrome();
  }
  bookSize.addEventListener('click',()=>{
    if(busy)return;
    const wide=!document.body.classList.contains('wide-spread');
    setReading(false);setBookWide(wide);renderAt(current);
  });
  function closeToc(){toc.classList.remove('open');el('toc-button').setAttribute('aria-expanded','false');el('toc-button').focus();}
  prev.addEventListener('click',()=>go(-1));next.addEventListener('click',()=>go(1));
  el('toc-button').addEventListener('click',()=>{toc.classList.add('open');el('toc-button').setAttribute('aria-expanded','true');el('toc-close').focus();});
  el('toc-close').addEventListener('click',closeToc);toc.addEventListener('click',e=>{if(e.target===toc)closeToc();});
  document.addEventListener('click',e=>{const b=e.target.closest('.page-jump');if(!b)return;const n=Number(b.dataset.jump);if(!Number.isInteger(n)||n<0||n>=pages.length)return;if(toc.classList.contains('open'))closeToc();renderAt(n);});
  // A page click is the single-page zoom. Leaving it always restores the compact book.
  function setReading(on){
    setBookWide(false);
    document.body.classList.toggle('reading-mode',on);
    try{localStorage.setItem('sgd-reading-mode',on?'1':'0');}catch{}
  }
  document.addEventListener('click',e=>{if(busy||!e.target.matches('.sheet-left .sgd-poster>img,.sheet-right .sgd-poster>img')||matchMedia('(max-width:780px)').matches)return;const n=Number(e.target.parentElement.dataset.page)-1;if(!Number.isInteger(n)||n<0||n>=pages.length)return;setReading(!document.body.classList.contains('reading-mode'));renderAt(n);});
  el('print-button').addEventListener('click',()=>window.print());
  addEventListener('keydown',e=>{if(e.key==='Escape'&&toc.classList.contains('open')){closeToc();return;}if(toc.classList.contains('open'))return;if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();go(1);}if(e.key==='ArrowLeft'){e.preventDefault();go(-1);}});
  addEventListener('resize',()=>renderAt(current));addEventListener('hashchange',()=>{const m=location.hash.match(/^#page=(\d+)$/);if(m)renderAt(Number(m[1])-1);});
  if(!pages.length){left.textContent='Le guide n’est pas disponible.';return;}
  pages.forEach((p,i)=>{const b=document.createElement('button');b.type='button';b.className='toc-choice page-jump';b.dataset.jump=i;const n=document.createElement('span');n.className='toc-n';n.textContent=String(i+1).padStart(2,'0');const info=document.createElement('span'),title=document.createElement('b'),chapter=document.createElement('small');title.textContent=p.title;chapter.textContent=p.chapter;info.append(title,chapter);b.append(n,info);grid.append(b);});
  el('print-pages').innerHTML=pages.map(p=>'<div class="print-page"><div class="sheet">'+markup(p)+'</div></div>').join('');
  try{setReading(localStorage.getItem('sgd-reading-mode')==='1');}catch{setReading(false);}
  const h=location.hash.match(/^#page=(\d+)$/);renderAt(h?Number(h[1])-1:0);
})();
