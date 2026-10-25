/* Build sparse, lossless colour overlays; retain the original HD page images. */
const fs=require('node:fs'),path=require('node:path'),sharp=require('sharp');
const root=path.resolve(__dirname,'../..'),out=path.join(root,'assets/palette-v795');
fs.mkdirSync(out,{recursive:true});
const W=2400,H=3394,N=W*H,target=[240,77,46];
// Illustrated spreads already use a vivid orange. Keep those illustrations intact.
const unchanged=new Set([27,28,29,30,31,32,41,42]);
// Protect product and scene photographs (coordinates on the 2400 × 3394 source).
// Only old palette lettering and graphic components outside these zones are eligible.
const photos={
1:[[0,1000,2400,2800]],3:[[1430,400,2400,1050],[1060,400,1390,2800]],
4:[[80,730,450,1210],[850,730,1220,1210],[1620,730,1980,1210],[85,1950,670,2695],[850,1950,1440,2695],[1620,1950,2210,2695]],
7:[[75,690,2330,1620]],8:[[0,120,2400,1390]],
9:[[80,500,490,1100],[1200,500,1630,1100],[80,1690,490,2270],[1200,1690,1630,2270]],
10:[[85,470,460,1500],[1210,470,1600,1500],[85,1730,460,2760],[1210,1730,1600,2760]],
11:[[80,700,2320,1180]],12:[[75,590,390,1530],[845,590,1160,1530],[1610,590,1930,1530],[80,1720,400,2730],[1205,1720,1530,2730]],
13:[[75,620,2320,1190]],14:[[85,470,470,1500],[1210,470,1600,1500],[85,1710,470,2730],[1210,1710,1600,2730]],
15:[[1930,600,2300,1050]],16:[[90,485,470,1470],[1210,485,1600,1470],[90,1720,470,2730],[1210,1720,1600,2730]],
17:[[70,410,1450,930],[145,960,910,1350]],18:[[85,960,425,1290],[85,1350,425,1780],[85,1830,425,2240],[85,2360,425,2790]],
19:[[100,460,830,980]],20:[[90,440,880,1060]],21:[[383,712,2016,1003],[155,1760,241,2061],[877,1760,963,2061],[1598,1760,1684,2061]],22:[[164,1890,782,2303]],
23:[[1280,400,2320,830],[95,2160,920,2870]],24:[[80,460,470,1470],[1205,460,1600,1470],[80,1730,470,2750],[1205,1730,1600,2750]],
25:[[80,600,2320,1260]],26:[[90,790,610,1250],[1205,790,1725,1250],[90,1650,610,2110],[1205,1650,1725,2110],[90,2470,610,2830],[1205,2470,1725,2830]],
35:[[150,580,1490,1370],[120,1940,750,2810]],36:[[100,590,1600,1340]],37:[[80,560,1700,1300],[80,1800,1800,2550]],
38:[[105,1020,800,1690],[1260,1020,1780,1690]],39:[[90,530,1770,1450],[95,1920,1700,2730]],
40:[[80,550,2300,1200],[90,1800,1050,2310],[1210,1800,2220,2310]],43:[[75,545,1430,985]],44:[[75,545,1430,985]],
46:[[75,990,2330,1680]]};
function blocked(n,x,y){if(n===3&&x>=1060&&x<=1390&&y>=2630&&y<=2700)return false;return (photos[n]||[]).some(b=>x>=b[0]&&x<=b[2]&&y>=b[1]&&y<=b[3]);}
(async()=>{
 const audit=[];
 for(let n=1;n<=46;n++){
  if(unchanged.has(n))continue;
  const src=path.join(root,`assets/guide-v785/page-${String(n).padStart(2,'0')}.webp`);
  const rgb=await sharp(src).removeAlpha().raw().toBuffer();
  const candidate=new Uint8Array(N),seed=new Uint8Array(N),alpha=new Float32Array(N);
  for(let y=120;y<3170;y++)for(let x=0;x<W;x++){
   if(blocked(n,x,y))continue;
   const k=y*W+x,p=k*3,r=rgb[p],g=rgb[p+1],b=rgb[p+2];
   if(r-g<10||g-b<2||r<135||g>245||b>240)continue;
   let error=1e9,coverage=0;
   for(const old of [[186,98,79],[199,99,77]]){
    const a=Math.min(1.12,(255-b)/(255-old[2]));
    const e=Math.abs(r-(255-(255-old[0])*a))+Math.abs(g-(255-(255-old[1])*a));
    if(e<error){error=e;coverage=a;}
   }
   if(error>10||coverage<.1)continue;
   candidate[k]=1;alpha[k]=Math.min(1,coverage);seed[k]=error<4&&coverage>.55?1:0;
  }
  const overlay=Buffer.alloc(N*4),queue=new Int32Array(N);let changed=0,groups=0;
  for(let k=120*W;k<3170*W;k++){
   if(candidate[k]!==1)continue;
   let tail=1,head=0,cores=0;queue[0]=k;candidate[k]=2;
   while(head<tail){const q=queue[head++];cores+=seed[q];const x=q%W;
    for(const a of [q-W-1,q-W,q-W+1,q-1,q+1,q+W-1,q+W,q+W+1]){
     if(a<0||a>=N||Math.abs(a%W-x)>1||candidate[a]!==1)continue;candidate[a]=2;queue[tail++]=a;
    }
   }
   if(cores<12||tail<20)continue;
   groups++;
   for(let j=0;j<tail;j++){
    const q=queue[j],s=q*3,o=q*4,a=alpha[q];
    for(let c=0;c<3;c++)overlay[o+c]=Math.round(255-(255-target[c])*a);
    overlay[o+3]=255;changed++;
   }
  }
  if(!changed)continue;
  const name=`page-${String(n).padStart(2,'0')}.webp`,dest=path.join(out,name);
  await sharp(overlay,{raw:{width:W,height:H,channels:4}}).webp({lossless:true,effort:6}).toFile(dest);
  const check=await sharp(dest).ensureAlpha().raw().toBuffer();
  for(let k=0;k<N;k++)if(check[k*4+3]&&blocked(n,k%W,Math.floor(k/W)))throw Error('Photo modified '+n);
  audit.push({page:n,path:`assets/palette-v795/${name}`,pixels:changed,components:groups,bytes:fs.statSync(dest).size,protected_photos:photos[n]||[]});
  console.log(n,changed,fs.statSync(dest).size);
 }
 fs.writeFileSync(path.join(__dirname,'audit.json'),JSON.stringify({source:'assets/guide-v785',accent:'#F04D2E',unchanged:[...unchanged],pages:audit},null,2)+'\n');
 console.log('TOTAL BYTES',audit.reduce((s,p)=>s+p.bytes,0));
})().catch(e=>{console.error(e);process.exit(1)});
