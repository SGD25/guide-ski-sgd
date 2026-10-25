/* Decorative paper and cover. All coordinates use CSS pixels; page images stay intact. */
(() => {
  'use strict';
  const frame=document.querySelector('.book-frame');
  if(!frame)return;
  const ns='http://www.w3.org/2000/svg';
  const book=frame.querySelector('.book');
  const object=document.createElement('div');
  object.className='book-object';
  book.before(object);object.append(book);
  const shell=document.createElementNS(ns,'svg');
  shell.classList.add('book-shell');
  shell.setAttribute('aria-hidden','true');
  shell.setAttribute('focusable','false');
  object.prepend(shell);
  let previous='';
  window.SGD_BOOK_EFFECTS={layout(w,h,single,mobile){
    const cover=mobile?11:Math.min(42,Math.max(25,w*.034));
    const signature=[w,h,single,mobile].join(':');
    if(signature===previous)return cover;
    previous=signature;
    const f=n=>Number(n.toFixed(2));
    // One projective transform for pages, paper and cover. Top is 4% narrower;
    // bottom width and height stay fixed. Source images keep their A4 geometry.
    const taper=single?0:.04,scale=1-taper;
    object.style.transform=single?'none':`matrix3d(${scale},0,0,0,0,${scale},0,${-taper/h},0,0,1,0,0,0,0,1)`;
    object.dataset.perspective=single?'flat':'tapered';
    const c=f(cover),fan=c-5,lift=single?0:Math.min(7,w*.006),bottom=h+7;
    shell.style.left=-c+'px';shell.style.top='-12px';
    shell.style.width=(w+2*c)+'px';shell.style.height=(h+32)+'px';
    shell.setAttribute('viewBox',`${-c} -12 ${w+2*c} ${h+32}`);
    const defs=`<defs>
      <linearGradient id="sgd-cover" x1="0" x2="1"><stop stop-color="#48565e"/><stop offset=".018" stop-color="#78858b"/><stop offset=".04" stop-color="#59666d"/><stop offset=".48" stop-color="#57646b"/><stop offset=".5" stop-color="#34434b"/><stop offset=".53" stop-color="#606e75"/><stop offset=".97" stop-color="#5a6870"/><stop offset=".99" stop-color="#7e8a90"/><stop offset="1" stop-color="#43515a"/></linearGradient>
      <linearGradient id="sgd-paper-left"><stop stop-color="#bfc3c1"/><stop offset=".25" stop-color="#f2f1eb"/><stop offset=".76" stop-color="#fafaf7"/><stop offset="1" stop-color="#c3c8c6"/></linearGradient>
      <linearGradient id="sgd-paper-right"><stop stop-color="#c3c8c6"/><stop offset=".24" stop-color="#fafaf7"/><stop offset=".75" stop-color="#f2f1eb"/><stop offset="1" stop-color="#bfc3c1"/></linearGradient>
      <linearGradient id="sgd-paper-bottom" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fafaf7"/><stop offset="1" stop-color="#aeb6b5"/></linearGradient>
    </defs>`;
    const coverPath=`M ${-c+4} 5 Q ${-c} 5 ${-c} 10 L ${-c} ${bottom-3} Q ${-c} ${bottom+1} ${-c+5} ${bottom+1} L ${w+c-5} ${bottom+1} Q ${w+c} ${bottom+1} ${w+c} ${bottom-3} L ${w+c} 10 Q ${w+c} 5 ${w+c-4} 5 L ${w+fan} 7 L ${-fan} 7 Z`;
    let html=defs+`<path class="book-cover" d="${coverPath}" fill="url(#sgd-cover)" stroke="#354149" stroke-width="1.2"/><path d="M ${-c+2} 11 L ${-c+2} ${bottom-3} Q ${-c+2} ${bottom-1} ${-c+5} ${bottom-1} H ${w+c-5} Q ${w+c-2} ${bottom-1} ${w+c-2} ${bottom-3} V 11" fill="none" stroke="#9ba7ac" stroke-opacity=".3" stroke-width=".65"/>`;
    // Broad, gently fanned sides rather than a striped rectangular frame.
    html+=`<path d="M ${-fan+4} 4 Q ${-fan*.45} ${-lift-3} 0 ${-lift} L 0 ${h-lift} Q ${-fan*.45} ${h+1} ${-fan} ${h+2} Z" fill="url(#sgd-paper-left)"/>
      <path d="M ${w+fan-4} 4 Q ${w+fan*.45} ${-lift-3} ${w} ${-lift} L ${w} ${h-lift} Q ${w+fan*.45} ${h+1} ${w+fan} ${h+2} Z" fill="url(#sgd-paper-right)"/>
      <path d="M ${-fan} ${h+2} Q ${w*.24} ${h+.5} ${w*.5} ${h+2} Q ${w*.76} ${h+.5} ${w+fan} ${h+2} V ${h+3} Q ${w*.75} ${h+1.5} ${w*.5} ${h+3} Q ${w*.25} ${h+1.5} ${-fan} ${h+3} Z" fill="url(#sgd-paper-bottom)"/>`;
    const count=mobile?7:Math.max(14,Math.round(fan/.95));
    for(let i=0;i<count;i++){
      const t=i/(count-1),x=-fan*(1-t),y=4-(lift+4)*t,b=h+2-(lift+2)*t;
      const bend=Math.sin(t*Math.PI)*2.4;
      const opacity=[.26,.14,.31,.18,.21][i%5];
      const line=`M ${f(x+4*(1-t))} ${f(y)} C ${f(x-bend)} ${f(h*.22)} ${f(x-bend*.5)} ${f(h*.75)} ${f(x)} ${f(b)}`;
      html+=`<path d="${line}" fill="none" stroke="#767f7e" stroke-opacity="${opacity}" stroke-width=".7"/><path d="${line}" transform="translate(${w} 0) scale(-1 1)" fill="none" stroke="#767f7e" stroke-opacity="${opacity}" stroke-width=".7"/>`;
    }
    if(!single){
      // White silhouettes extend the top edge into two shallow, curved leaves.
      html+=`<path d="M 0 ${-lift} C ${w*.19} ${-lift-3} ${w*.42} ${-lift-1} ${w*.5} 0 C ${w*.58} ${-lift-1} ${w*.81} ${-lift-3} ${w} ${-lift} V 14 H 0 Z" fill="#fff"/>
        <path d="M 0 ${-lift} C ${w*.19} ${-lift-3} ${w*.42} ${-lift-1} ${w*.5} 0 C ${w*.58} ${-lift-1} ${w*.81} ${-lift-3} ${w} ${-lift}" fill="none" stroke="#c9cece" stroke-width=".55"/>
        <path d="M 0 ${h-lift} Q ${w*.3} ${h-lift-2} ${w*.5} ${h} Q ${w*.7} ${h-lift-2} ${w} ${h-lift} L ${w} ${h+1.5} Q ${w*.7} ${h} ${w*.5} ${h+1.5} Q ${w*.3} ${h} 0 ${h+1.5} Z" fill="#ebede8"/>`;
    }
    shell.innerHTML=html;
    return cover;
  }};
})();
