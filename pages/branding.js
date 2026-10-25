/* Approved page furniture. SVG overlays preserve the original HD page bodies. */
(() => {
 const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
 window.SGD_PAGES.forEach((p,i)=>{
 const n=i+1,color=n>=3&&n<=7?'#337BA2':n>=8&&n<=26?'#F04D2E':n>=27&&n<=32||n>=43?'#297A78':'#75638F';
 const label=n===1?'FORMATION VENDEURS & LOUEURS':n===2?'OUVERTURE / LE SOMMAIRE':'CHAPITRE '+p.chapter.replace(' · ',' / ').toUpperCase();
 const header=`<svg class="page-brand-header" viewBox="0 0 2400 120" style="overflow:visible" aria-hidden="true"><rect width="2400" height="120" fill="white"/><image href="./assets/branding-v786/s-symbol.svg" x="75" y="14" width="100" height="100"/><path class="header-separator" d="M75 130H2325" stroke="${color}" stroke-width="8"/><text x="215" y="73" font-family="Arial,sans-serif" font-weight="700" font-size="31" fill="${color}">${escape(label)}</text><rect x="2110" y="30" width="215" height="70" rx="24" fill="white" stroke="#92999D" stroke-width="2"/><text x="2217" y="76" text-anchor="middle" font-family="Arial,sans-serif" font-size="30" font-weight="700" fill="#242426">PAGE ${String(n).padStart(2,'0')}</text></svg>`;
 const footer=`<svg class="page-brand-footer" viewBox="0 0 2400 194" aria-hidden="true"><rect width="2400" height="194" fill="white"/><path d="M75 10H2325" stroke="#85898D" stroke-width="2"/><image href="./assets/branding-v785/logo-footer.svg" x="75" y="57" width="575" height="107"/><text x="1470" y="122" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="#55595D">LE GUIDE DU SKI</text><path d="M2015 60V160" stroke="#B2B5B8" stroke-width="2"/><text x="2180" y="88" text-anchor="middle" font-family="Arial,sans-serif" font-size="25" fill="#6A6F73" letter-spacing="2">ÉDITION</text><text x="2180" y="134" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="#242426" letter-spacing=".5">2026–2027</text></svg>`;
 p.html=p.html.replace('</figure>',header+footer+'</figure>');
 });
})();
