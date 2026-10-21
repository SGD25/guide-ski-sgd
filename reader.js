/* Reader for complete page images. Content is loaded from pages/NN.js. */
(() => {
  'use strict';
  const pages=window.SGD_PAGES||[],el=id=>document.getElementById(id);
  const book=el('book'),left=el('left-page'),right=el('right-page'),leaf=el('flip-sheet');
  const prev=el('previous'),next=el('next'),toc=el('toc-overlay'),grid=el('toc-grid'),reading=el('reading-button');
  let current=0,busy=false;
  const single=()=>matchMedia('(max-width:780px)').matches||document.body.classList.contains('reading-mode');
  const step=()=>single()?1:2,snap=n=>single()?n:Math.floor(n/2)*2;
  const markup=p=>p?'<div class="sheet-pad">'+p.html+'</div>':'';
  function apply(node,p){node.innerHTML=markup(p);node.setAttribute('aria-label',p?p.title:'Page vierge');}
  function renderAt(n){
    current=Math.max(0,Math.min(pages.length-1,snap(n)));
    apply(left,pages[current]);apply(right,pages[current+1]);
    const last=Math.min(pages.length,current+step());
    el('page-count').textContent=(single()?String(current+1).padStart(2,'0'):String(current+1).padStart(2,'0')+'–'+String(last).padStart(2,'0'))+' / '+String(pages.length).padStart(2,'0');
    prev.disabled=current===0;next.disabled=current+step()>=pages.length;el('progress').style.width=last/pages.length*100+'%';
    document.title=pages[current].title+' — SPORT GOOD DEAL';history.replaceState(null,'','#page='+(current+1));
  }
  function go(dir){
    const target=current+dir*step();if(busy||target<0||target>=pages.length)return;
    if(single()||matchMedia('(prefers-reduced-motion:reduce)').matches){renderAt(target);return;}
    busy=true;leaf.innerHTML='<div class="flip-side flip-front">'+markup(pages[dir>0?current+1:current])+'</div><div class="flip-side flip-back">'+markup(pages[dir>0?target:target+1])+'</div>';
    book.classList.add(dir>0?'is-forward':'is-backward');setTimeout(()=>renderAt(target),325);
    setTimeout(()=>{book.classList.remove('is-forward','is-backward');leaf.innerHTML='';busy=false;},660);
  }
  function closeToc(){toc.classList.remove('open');el('toc-button').setAttribute('aria-expanded','false');el('toc-button').focus();}
  prev.addEventListener('click',()=>go(-1));next.addEventListener('click',()=>go(1));
  el('toc-button').addEventListener('click',()=>{toc.classList.add('open');el('toc-button').setAttribute('aria-expanded','true');el('toc-close').focus();});
  el('toc-close').addEventListener('click',closeToc);toc.addEventListener('click',e=>{if(e.target===toc)closeToc();});
  document.addEventListener('click',e=>{const b=e.target.closest('.page-jump');if(!b)return;const n=Number(b.dataset.jump);if(!Number.isInteger(n)||n<0||n>=pages.length)return;if(toc.classList.contains('open'))closeToc();renderAt(n);});
  function setReading(on){document.body.classList.toggle('reading-mode',on);reading.setAttribute('aria-pressed',String(on));reading.textContent=on?'Vue double':'Agrandir';try{localStorage.setItem('sgd-reading-mode',on?'1':'0');}catch{}}
  reading.addEventListener('click',()=>{setReading(!document.body.classList.contains('reading-mode'));renderAt(current);});
  document.addEventListener('click',e=>{if(!e.target.matches('.sheet-left .sgd-poster>img,.sheet-right .sgd-poster>img')||single())return;const n=Number(e.target.parentElement.dataset.page)-1;if(!Number.isInteger(n)||n<0||n>=pages.length)return;setReading(true);renderAt(n);});
  el('print-button').addEventListener('click',()=>window.print());
  addEventListener('keydown',e=>{if(e.key==='Escape'&&toc.classList.contains('open')){closeToc();return;}if(toc.classList.contains('open'))return;if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();go(1);}if(e.key==='ArrowLeft'){e.preventDefault();go(-1);}});
  addEventListener('resize',()=>renderAt(current));addEventListener('hashchange',()=>{const m=location.hash.match(/^#page=(\d+)$/);if(m)renderAt(Number(m[1])-1);});
  if(!pages.length){left.textContent='Le guide n’est pas disponible.';return;}
  pages.forEach((p,i)=>{const b=document.createElement('button');b.type='button';b.className='toc-choice page-jump';b.dataset.jump=i;const n=document.createElement('span');n.className='toc-n';n.textContent=String(i+1).padStart(2,'0');const info=document.createElement('span'),title=document.createElement('b'),chapter=document.createElement('small');title.textContent=p.title;chapter.textContent=p.chapter;info.append(title,chapter);b.append(n,info);grid.append(b);});
  el('print-pages').innerHTML=pages.map(p=>'<div class="print-page"><div class="sheet">'+markup(p)+'</div></div>').join('');
  try{if(localStorage.getItem('sgd-reading-mode')==='1')setReading(true);}catch{}
  const h=location.hash.match(/^#page=(\d+)$/);renderAt(h?Number(h[1])-1:0);
})();
