/* Approved orange accents; sparse lossless overlays preserve the source page images. */
(()=>{
 const active=new Set([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 45, 46]);
 window.SGD_PAGES.forEach((p,i)=>{
  const n=i+1;if(!active.has(n))return;
  const file=String(n).padStart(2,'0');
  const overlay=`<svg class="page-palette" viewBox="0 0 2400 3394" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1"><image href="./assets/palette-v795/page-${file}.webp" width="2400" height="3394"/></svg>`;
  p.html=p.html.replace('</figure>',overlay+'</figure>');
 });
})();
