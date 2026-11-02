// ===== Shorts motion engine: deterministik, frame-frame render (window.seek(t)) =====
const $=id=>document.getElementById(id);
const EW=window.EW||1080, EH=window.EH||1920;
const C=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const P=(t,a,b)=>C((t-a)/(b-a));
const L=(a,b,p)=>a+(b-a)*p;
const E={
  lin:x=>x, oC:x=>1-Math.pow(1-x,3), iC:x=>x*x*x,
  ioC:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,
  oE:x=>x>=1?1:1-Math.pow(2,-10*x), iE:x=>x<=0?0:Math.pow(2,10*x-10),
  ioE:x=>x<=0?0:x>=1?1:x<.5?Math.pow(2,20*x-10)/2:(2-Math.pow(2,-20*x+10))/2,
  oB:x=>{const c1=1.7,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)},
  ioQ:x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2,
  oEl:x=>x===0?0:x===1?1:Math.pow(2,-10*x)*Math.sin((x*10-.75)*(2*Math.PI)/3)+1,
};
const k=(t,a,b,e=E.oE)=>e(P(t,a,b));
const pulse=(t,t0,rate=6)=>t>=t0?Math.exp(-(t-t0)*rate):0;
function rnd(seed){let s=seed>>>0;return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}}
const fmt=n=>Math.round(n).toLocaleString('de-DE');
function set(el,{o=1,x=0,y=0,s=1,sx=null,sy=null,rx=0,ry=0,r=0,b=0}={}){
  if(typeof el==='string')el=$(el);
  el.style.opacity=o;
  const sc=sx!==null||sy!==null?`scale(${sx??s},${sy??s})`:`scale(${s})`;
  el.style.transform=`translate(${x}px,${y}px) ${sc} rotateX(${rx}deg) rotateY(${ry}deg) rotate(${r}deg)`;
  el.style.filter=b>0.05?`blur(${b}px)`:'';
}
const NB=String.fromCharCode(160);
function split(id){const el=$(id);const g=[...el.classList].find(c=>['gold','cyan','ember','violet'].includes(c));
  const t=el.textContent;el.textContent='';el.style.perspective='900px';if(g)el.classList.remove(g);
  const arr=[...t].map(c=>{const s=document.createElement('span');s.className='ch'+(g?' '+g:'');s.textContent=c===' '?NB:c;el.appendChild(s);return s});
  arr.g=g;arr.el=el;return arr}
function sweep(chs,pct){if(!chs.g)return;const W=chs.W||(chs.W=chs.reduce((a,c)=>a+c.offsetWidth,0)),x0=chs[0].offsetLeft;
  chs.forEach(c=>{c.style.backgroundSize=`${W*2.5}px 100%`;c.style.backgroundPosition=`${-(c.offsetLeft-x0)+(pct/100)*(-W*1.5)}px 0`})}
// harf girişleri
function charsIn(chs,t,start,{st=.035,dur=.7,dy=110,rx=-75,bl=22,s0=1.15,from='left',out=null,outDur=.35}={}){
  const n=chs.length;
  chs.forEach((c,i)=>{const j=from==='center'?Math.abs(i-(n-1)/2):from==='right'?n-1-i:i;
    const p=k(t,start+j*st,start+j*st+dur,E.oE), po=out?k(t,out+j*.015,out+j*.015+outDur,E.iC):0;
    set(c,{o:C(p*1.4)*(1-po),y:(1-p)*dy-po*70,rx:(1-p)*rx,b:(1-p)*bl+po*16,s:L(s0,1,p)})});
}
function slam(chs,t,start,{st=.05,dur=.5,s0=2.3,bl=36,from='center',out=null,outDur=.35}={}){
  const n=chs.length;
  chs.forEach((c,i)=>{const j=from==='center'?Math.abs(i-(n-1)/2):i;
    const p=k(t,start+j*st,start+j*st+dur,E.oE), po=out?k(t,out,out+outDur,E.iC):0;
    set(c,{o:C(p*2)*(1-po),s:L(s0,1,p)*(1+po*.15),b:(1-p)*bl+po*20,y:-po*60})});
}
function maskLine(id,t,inT,outT,{dur=.65,outDur=.45}={}){
  const el=$(id),sp=el.firstElementChild;
  const pi=k(t,inT,inT+dur,E.oE), po=outT?k(t,outT,outT+outDur,E.iE):0;
  el.style.opacity=(t<inT||(outT&&t>outT+outDur))?0:1;
  sp.style.transform=`translateY(${(1-pi)*110-po*110}%)`;
  sp.style.filter=`blur(${(1-pi)*6+po*10}px)`;
}
function fadeBlock(id,t,inT,outT,{dur=.6,dy=60,outDur=.4,s0=1,x0=0}={}){
  const pi=k(t,inT,inT+dur), po=outT?k(t,outT,outT+outDur,E.iC):0;
  set(id,{o:pi*(1-po),x:(1-pi)*x0,y:(1-pi)*dy-po*dy,b:(1-pi)*14+po*14,s:L(s0,1,pi)});
}
function rr(g,x,y,w,h,r){r=Math.min(r,w/2,h/2);g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath()}

// ===== sahne altyapısı =====
const SPARKCOL={gold:i=>`255,${200+((i*37)%55)},${120+((i*13)%90)}`,cyan:i=>`${120+((i*37)%80)},${220+((i*13)%35)},255`,
  red:i=>`255,${70+((i*37)%80)},${80+((i*13)%60)}`,ember:i=>`255,${130+((i*37)%90)},${60+((i*13)%60)}`,violet:i=>`${160+((i*37)%70)},${140+((i*13)%60)},255`,white:i=>`255,255,255`};
const ENG={};
function boot(CONFIG){
  window.CONFIG=CONFIG;
  const st=document.createElement('div');st.id='stage';if(CONFIG.bg)st.style.setProperty('--bg',CONFIG.bg);
  const mk=(tag,id,cls)=>{const e=document.createElement(tag);e.id=id;if(cls)e.className=cls;return e};
  const bok=mk('canvas','bokeh');bok.width=EW;bok.height=EH;
  const l1=mk('div','leak1','leak'),l2=mk('div','leak2','leak');
  const cam=$('cam')||mk('div','cam'), scr=$('screen')||mk('div','screen');
  const mid=mk('canvas','mid');mid.width=EW;mid.height=EH;mid.style.position='absolute';mid.style.left='0';mid.style.top='0';
  cam.insertBefore(mid,cam.firstChild);
  const fx=mk('canvas','fx');fx.width=EW;fx.height=EH;
  [bok,l1,l2,cam,scr,fx,mk('div','tint'),mk('div','flash'),mk('div','vig'),mk('div','grain')].forEach(e=>st.appendChild(e));
  document.body.appendChild(st);
  const lc=CONFIG.leaks||['255,150,60','70,100,255'];
  l1.style.background=`radial-gradient(circle,rgba(${lc[0]},.42) 0%,rgba(${lc[0]},.12) 35%,transparent 65%)`;
  l2.style.background=`radial-gradient(circle,rgba(${lc[1]},.38) 0%,rgba(${lc[1]},.10) 35%,transparent 65%)`;
  // grain
  const gc=document.createElement('canvas');gc.width=gc.height=256;const gg=gc.getContext('2d');const d=gg.createImageData(256,256),R=rnd(9);
  for(let i=0;i<d.data.length;i+=4){const v=R()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}
  gg.putImageData(d,0,0);$('grain').style.backgroundImage=`url(${gc.toDataURL()})`;
  ENG.bctx=bok.getContext('2d');ENG.mid=mid.getContext('2d');ENG.fx=fx.getContext('2d');
  ENG.BK=[];{const R=rnd(3);for(let i=0;i<46;i++)ENG.BK.push({x:R()*EW,y:R()*EH,d:R(),sp:8+R()*26,ph:R()*6.28,r:R()})}
  ENG.SP=[];{const R=rnd(11);for(let i=0;i<190;i++){const a=R()*Math.PI*2,v=600+R()*1700;ENG.SP.push({a,v,l:.6+R()*1.1,w:1+R()*3})}}
  if(CONFIG.init)CONFIG.init();
  window.seek=t=>{frame(t);return true};
  document.fonts.ready.then(()=>{frame(0);window.ready=true});
}
function drawBokeh(t){
  const g=ENG.bctx,col=CONFIG.bokeh?CONFIG.bokeh(t):'255,190,110';g.clearRect(0,0,EW,EH);
  ENG.BK.forEach(p=>{const y=((p.y-p.sp*t*(.4+p.d))%EH+EH)%EH,x=p.x+Math.sin(t*.3+p.ph)*30*p.d;
    const r=6+p.d*p.d*60,a=(.05+.12*(1-p.d))*(.6+.4*Math.sin(t*.8+p.ph));
    const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(${col},${a})`);gr.addColorStop(.6,`rgba(${col},${a*.5})`);gr.addColorStop(1,`rgba(${col},0)`);
    g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,7);g.fill()});
}
function drawSparks(t){
  const g=ENG.fx;g.clearRect(0,0,EW,EH);
  (CONFIG.sparks||[]).forEach(([t0,cx,cy,amt,ck])=>{const dt=t-t0;if(dt<0||dt>1.8)return;const cf=SPARKCOL[ck||'gold'];
    ENG.SP.forEach((p,i)=>{if(i/ENG.SP.length>amt||dt>p.l)return;
      const dr=p.v*(1-Math.exp(-dt*3.2))/3.2,dr0=p.v*(1-Math.exp(-Math.max(0,dt-.035)*3.2))/3.2;
      const x=cx+Math.cos(p.a)*dr,y=cy+Math.sin(p.a)*dr+120*dt*dt,x0=cx+Math.cos(p.a)*dr0,y0=cy+Math.sin(p.a)*dr0+120*dt*dt;
      g.strokeStyle=`rgba(${cf(i)},${1-dt/p.l})`;g.lineWidth=p.w;g.beginPath();g.moveTo(x0,y0);g.lineTo(x,y);g.stroke()})});
}
function frame(t){
  const CF=CONFIG;
  drawBokeh(t);
  const la=CF.leakAmt?CF.leakAmt(t):1;
  set('leak1',{o:(.55+.35*Math.sin(t*.6))*la,x:L(-700,300,(t%12)/12)});$('leak1').style.top=L(-500,500,(Math.sin(t*.25)+1)/2)+'px';
  set('leak2',{o:(.45+.3*Math.sin(t*.45+2))*la,x:L(500,-400,(t%15)/15)});$('leak2').style.top=L(900,1300,(Math.cos(t*.2)+1)/2)+'px';
  // kamera
  const cm=Object.assign({s:1+0.03*Math.sin(t*.5),fx:EW/2,fy:EH/2,blur:0,o:1},CF.cam?CF.cam(t):{});
  let sh=0;(CF.shakes||[]).forEach(([tt,a])=>{if(t>=tt)sh+=a*Math.exp(-(t-tt)*7)});
  const sx=sh*(Math.sin(t*93.1)+Math.sin(t*51.7))*.5,sy=sh*(Math.sin(t*77.3)+Math.cos(t*61.9))*.5;
  const c=$('cam');c.style.transform=`translate(${EW/2-cm.fx*cm.s+sx}px,${EH/2-cm.fy*cm.s+sy}px) scale(${cm.s})`;
  c.style.filter=cm.blur>.1?`blur(${cm.blur}px)`:'';c.style.opacity=cm.o;
  $('screen').style.transform=`translate(${sx*.6}px,${sy*.6}px)`;
  // flaşlar
  let fl=0;(CF.flashes||[]).forEach(([tt,a,r])=>{fl=Math.max(fl,pulse(t,tt,r||10)*a)});$('flash').style.opacity=fl;
  if(CF.tint){const [col,a]=CF.tint(t);$('tint').style.background=col;$('tint').style.opacity=a}
  drawSparks(t);
  if(CF.scene)CF.scene(t);
  $('stage').style.opacity=k(t,0,.25,E.lin)*(1-k(t,CF.dur-.55,CF.dur,E.lin));
  const R=rnd(Math.floor(t*30)*7+1);$('grain').style.transform=`translate(${(R()*64|0)}px,${(R()*64|0)}px)`;
}
