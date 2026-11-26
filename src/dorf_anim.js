// Dorfband: alles auf einer Canvas in Kenmi-Pixeln, als Ganzes skaliert
(function(){
const D=__DATA__;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const rnd=(a,b)=>a+Math.random()*(b-a);
const IMG={};function im(src){if(!IMG[src]){const i=new Image();i.src=src;IMG[src]=i;}return IMG[src];}
// Farbe: Bilder kommen farbig, die graue Fassung rechnet das Spiel selbst (gleiche Formel wie pixel/dorf5.py)
let MODE='g',off=null,offc=null;const GR={};
const NOG=new Set(D.walkers.filter(w=>['Lia','Noah','Ruth','Elif','Daniel'].includes(w.name)).map(w=>w.src));
for(const n in (D.figsets||{}))for(const k in D.figsets[n])NOG.add(D.figsets[n][k].src);
const FCOL={};for(const n in (D.figsets||{}))if(D.figsetsF&&D.figsetsF[n])for(const k in D.figsets[n])if(D.figsetsF[n][k])FCOL[D.figsets[n][k].src]=D.figsetsF[n][k].src;
function grayOf(src,lo){const k=src+(lo?'#lo':'');if(GR[k])return GR[k];const i=im(src);if(!i.complete||!i.naturalWidth)return null;
 const c=document.createElement('canvas');c.width=i.naturalWidth;c.height=i.naturalHeight;const x=c.getContext('2d');x.drawImage(i,0,0);
 const d=x.getImageData(0,0,c.width,c.height),a=d.data;
 for(let j=0;j<a.length;j+=4){if(!a[j+3])continue;const r=a[j],g=a[j+1],b=a[j+2],l=0.299*r+0.587*g+0.114*b;let v;
  if(lo){v=Math.trunc(Math.min(255,(l-128)*0.55+205));if(b>r+40)v=Math.trunc((l-128)*0.7+165);}else v=Math.trunc(Math.max(0,Math.min(255,(l-128)*1.1+140)));
  a[j]=Math.min(255,v+4);a[j+1]=v;a[j+2]=Math.max(0,v-3);}
 x.putImageData(d,0,0);GR[k]=c;return c;}
function pic(src,lo){if(MODE==='f'||NOG.has(src)){const i=im(MODE==='f'&&FCOL[src]?FCOL[src]:src);return i.complete&&i.naturalWidth?i:null;}return grayOf(src,lo);}
let K=1,OY=0,SNAP=false,camFr=0,camX=0,cv=null,ctx=null,S=.75,VW=0,vx0=0,ents=[],last=0,raf=0,wt=0,clouds=[];
// Wolkenschatten: schwarze Silhouetten vorbereiten
function shadowOf(src){const c=document.createElement('canvas'),i=im(src);const mkS=()=>{c.width=i.width;c.height=i.height;const x=c.getContext('2d');x.drawImage(i,0,0);x.globalCompositeOperation='source-in';x.fillStyle='#000';x.fillRect(0,0,c.width,c.height);};if(i.complete)mkS();else i.addEventListener('load',mkS);return c;}
function lane(){return rnd(D.band[0],D.band[1]);}
function wdx(a,b){return(((b-a)%D.W)+D.W*1.5)%D.W-D.W/2;}
function face(o,vx,vy){const s=o.set;if(!s.up||Math.abs(vx)>=Math.abs(vy)){o.st=s.side;o.flip=vx<0;}else{o.st=vy<0?s.up:s.down;o.flip=false;}}
function rest(o,back){const s=o.set;o.st=back&&s.idleB?s.idleB:(s.idleF||s.side);o.flip=false;}
function isFol(o){return window.DORF_FOLLOW&&o.set&&o.set.side&&o.set.side.name===window.DORF_FOLLOW;}
function folEnt(){return ents.find(o=>o.k==='p'&&isFol(o));}
function decide(o){const r=Math.random();
 if(isFol(o)){const W0=window.DORF_WALK;if(W0!=null){const d=wdx(o.x,W0);if(Math.abs(d)>1.5){if(o.wt!==W0){o.wt=W0;o.boost=1;}o.v=52*(o.boost||1);const yc=(D.band[0]+D.band[1])/2,n=Math.max(1,Math.round(Math.abs(d)/80));o.q=[];let y=o.y;
  for(let j=1;j<=n;j++){const x=o.x+d*j/n;o.q.push([x,y]);const ny=j===n?yc:lane();if(Math.abs(ny-y)>6){o.q.push([x,ny]);y=ny;}}
  if(Math.abs(y-yc)>1)o.q.push([o.x+d,yc]);}else{o.wait=0.3;rest(o,false);}return;}o.q=[[o.x+rnd(140,320),lane()]];return;}
 if(o.role==='road'){
  if(o.set.up&&r<0.3){let best=null,bd=1e9;for(const d of D.doors){const dd=Math.abs(wdx(o.x,d.p[0][0]));if(dd<bd&&dd<350){bd=dd;best=d;}}
   // Weg bis genau zur Haustuer, dort verschwinden, spaeter aus derselben Tuer zurueck
   if(best){const off=o.x+wdx(o.x,best.p[0][0])-best.p[0][0],pts=best.p.map(([x,y])=>[x+off,y]);
    o.q=[...pts.slice(0,-1),[...pts[pts.length-1],'door',best],...pts.slice(0,-1).reverse(),[pts[0][0]+rnd(-60,60),lane()]];return;}}
  if(r<0.85){o.q=[[o.x+(Math.random()<.5?-1:1)*rnd(60,380),lane()]];return;}
  o.wait=rnd(1,3);rest(o,false);return;}
 if(o.role==='shop'){const pl=D.plazas[0];
  if(r<0.6&&D.stalls.length){const s=D.stalls[Math.floor(Math.random()*D.stalls.length)];o.q=[[s[0]+rnd(-16,16),s[1]+rnd(9,18),'stall']];return;}
  o.q=[[rnd(pl[0],pl[2]),rnd(pl[1],pl[3]),'look']];}}
function stepP(o,dt){
 if(o.wait>0){const w0=o.wait;o.wait-=dt;o.f+=dt*3;
  if(o.door&&w0>0.35&&o.wait<=0.35)o.door.open=performance.now()+800;
  if(o.wait<=0){o.hid=false;if(o.door){rest(o,false);o.door=null;}}return;}
 if(!o.q.length){decide(o);if(o.wait>0)return;}
 const t=o.q[0],dx=t[0]-o.x,dy=t[1]-o.y,dd=Math.hypot(dx,dy);
 if(dd<0.8){o.q.shift();
  if(t[2]==='door'){o.wait=rnd(3,9);o.hid=true;o.door=t[3];t[3].open=performance.now()+450;}
  else if(t[2]==='stall'){o.wait=rnd(4,11);rest(o,true);}
  else if(t[2]==='look'){o.wait=rnd(1,4);rest(o,false);}
  return;}
 const sp=o.v*dt;o.x+=dx/dd*Math.min(sp,dd);o.y+=dy/dd*Math.min(sp,dd);face(o,dx,dy);o.f+=dt*8*(isFol(o)?Math.min(2.5,Math.max(1,o.v/52)):1);}
// Verdecker nach x in Faecher (64 px) einteilen
// z = Zeichenreihenfolge im Hintergrundbild: meist die Unterkante b; 10 Ausnahmen aus dem Bild bestimmt (21.11.2026)
const ZFIX={575:76.5,621:268.5,622:268.5,797:268.5,641:76.5,642:76.5,819:76.5,408:130.5,349:336.5,455:131.0};
const OC=D.occl.map(([k,x,y],i)=>{const a=D.atlas[k];return{k,x,y,w:a[2],h:a[3],b:y+a[3],z:ZFIX[i]!==undefined?ZFIX[i]:y+a[3]};});
const BK={};for(const o of OC){for(let c=Math.floor(o.x/64);c<=Math.floor((o.x+o.w)/64);c++){const cc=((c%50)+50)%50;(BK[cc]=BK[cc]||[]).push(o);}}
function occluders(o,out){const st=o.st,x0=o.x-st.w/2,x1=o.x+st.w/2,y0=o.y-st.h,y1=o.y;
 for(let c=Math.floor(x0/64);c<=Math.floor(x1/64);c++){const L=BK[((c%50)+50)%50];if(!L)continue;
  for(const q of L){if(q.b<=y1)continue;const dx=wdx(x0,q.x);if(dx>=st.w||dx+q.w<=0)continue;if(q.y>=y1||q.b<=y0)continue;out.add(q);}}}
// Wird ein Verdecker neu gezeichnet, muessen alle Verdecker, die im Bild darueber liegen, ebenfalls neu gezeichnet werden (sonst liegt z. B. ein Baum ueber einem Haus davor).
function occClose(oc){const st=[...oc];while(st.length){const q=st.pop();for(let c=Math.floor(q.x/64);c<=Math.floor((q.x+q.w)/64);c++){const L=BK[((c%50)+50)%50];if(!L)continue;
 for(const r of L){if(oc.has(r)||r.z<=q.z)continue;const dx=wdx(q.x,r.x);if(dx>=q.w||dx+r.w<=0)continue;if(r.y>=q.y+q.h||r.y+r.h<=q.y)continue;oc.add(r);st.push(r);}}}}
function drawOcc(q){const a=D.atlas[q.k],i=pic(D.atlasimg);if(!i)return;let x=Math.round(q.x-vx0);x=((x%D.W)+D.W)%D.W;
 for(const xx of [x,x-D.W])if(xx<VW&&xx+q.w>0)ctx.drawImage(i,a[0],a[1],a[2],a[3],xx,q.y,a[2],a[3]);}
function drawDoor(d){let x=Math.round(d.x-4-vx0);x=((x%D.W)+D.W)%D.W;const y=d.y-17;
 ctx.fillStyle=MODE==='f'?'#2a1d1a':'#3a3836';for(const xx of [x,x-D.W])if(xx<VW&&xx+8>0){ctx.fillRect(xx,y+1,8,13);ctx.fillRect(xx+1,y,6,1);}}
// Animierte Deko und Tiere aus dem Atlas dorf5_anim (Bild unten mittig auf x,y)
const AFPS={fountain:8,boat:2.5};
function drawA(key,fi,x,y,flip){const a=D.anim[key],i=pic(D.animimg);if(!a||!i)return;const w=a[2],h=a[3],sx=a[0]+(fi%a[4])*w;
 let X=Math.round(x-w/2-vx0);X=((X%D.W)+D.W)%D.W;const Y=Math.round(y-a[5]);
 for(const xx of [X,X-D.W]){if(xx>VW||xx+w<0)continue;
  if(flip){ctx.save();ctx.translate(xx+w,Y);ctx.scale(-1,1);ctx.drawImage(i,sx,a[1],w,h,0,0,w,h);ctx.restore();}else ctx.drawImage(i,sx,a[1],w,h,xx,Y,w,h);}}
function drawExt(e,a){const i=pic(D.extimg);if(!i)return;let x=Math.round(e[5]-vx0);x=((x%D.W)+D.W)%D.W;const y=e[6]-Math.round((1-a)*8);
 ctx.globalAlpha=a;for(const xx of [x,x-D.W])if(xx<VW&&xx+e[3]>0)ctx.drawImage(i,e[1],e[2],e[3],e[4],xx,y,e[3],e[4]);ctx.globalAlpha=1;}
function setup(){ents=[];
 for(const [sx,sy] of D.sail)ents.push({k:'sail',st:{src:D.sailimg,w:64,h:80,n:4},x:sx+32,y:sy+80,f:0,top:1});
 D.smoke.forEach(([cx,cy],i)=>ents.push({k:'smoke',si:(i*7+3)%D.smoke.length,st:D.smokeimg,x:cx+9.5,y:cy+13,f:Math.random()*5,v:rnd(5,7),top:1,a:.85}));
 const figs=D.walkers.filter(w=>['Lia','Noah','Ruth','Elif','Daniel'].includes(w.name)).map(w=>{const fs=D.figsets&&D.figsets[w.name];if(fs){const s={...fs};s.side={...fs.side,name:w.name};return s;}return {side:w};});
 const P=(set,role,x,y)=>ents.push({k:'p',set,role,x,y,q:[],v:rnd(8,13),f:Math.random()*6,wait:rnd(0,2),st:set.side});
 figs.forEach((s,i)=>P(s,'road',(i+Math.random())*D.W/5,lane()));
 for(let i=0;i<9;i++)P(D.npcs[i%D.npcs.length],'road',Math.random()*D.W,lane());
 for(const pl of D.plazas)for(let i=0;i<19;i++)P(D.npcs[(i*3+1)%D.npcs.length],'shop',rnd(pl[0],pl[2]),rnd(pl[1],pl[3]));
 for(const [x0,y0,x1,y1] of D.coops)for(let i=0;i<3;i++){const b=[(x0+1.2)*16,(y0+1.6)*16,(x1-0.2)*16,(y1+0.6)*16];ents.push({k:'chick',st:D.chicken.peck,x:rnd(b[0],b[2]),y:rnd(b[1],b[3]),f:Math.random()*8,b,t:rnd(1,4)});}
 for(const [hx,hy] of D.ducks){const near=D.water.filter(([x,y])=>Math.abs(x-hx)<=3&&Math.abs(y-hy)<=3);if(!near.length)continue;const [sx,sy]=near[Math.floor(Math.random()*near.length)];
  ents.push({k:'duck',st:D.duck.idle,near,x:(sx+.5)*16,y:sy*16+14,f:Math.random()*2,t:rnd(1,5)});}
 for(const [t,x,y,...b] of (D.herd||[]))ents.push({k:'herd',t,x,y,b,f:Math.random()*6,tm:rnd(0.5,5),s:Math.random()<.5?'graze':'idle',st:{w:32,h:28},coop:t==='Rooster',v:t==='Rooster'?11:t==='Goose_01'?8:t==='Horse_01'?9:5});
 for(const [hx,hy] of (D.swans||[])){const near=D.water.filter(([x,y])=>Math.abs(x-hx)<=3&&Math.abs(y-hy)<=2);if(!near.length)continue;const [sx,sy]=near[Math.floor(Math.random()*near.length)];
  ents.push({k:'swan',near,x:(sx+.5)*16,y:sy*16+14,f:Math.random()*2,t:rnd(1,5),s:'idle',st:{w:32,h:26}});}
 for(let i=0;i<5;i++){const y=rnd(40,D.H-40);ents.push({k:'fly',st:D.butterfly,x:rnd(0,D.W),y,by:y,ph:rnd(0,6),v:rnd(8,14)*(Math.random()<.5?-1:1),f:0,top:1});}
 clouds=[];for(let i=0;i<4;i++)clouds.push({c:shadowOf(D.clouds[i%2]),x:rnd(0,D.W),y:rnd(-60,D.H-140),v:rnd(4,7),sc:rnd(2.5,3.5)});
}
function update(dt){
 wt+=dt;
 for(const o of ents){
  if(o.k==='sail')o.f+=dt*3.3;
  else if(o.k==='smoke')o.f+=dt*o.v;
  else if(o.k==='p')stepP(o,dt);
  else if(o.k==='chick'){o.t-=dt;if(o.tx!==undefined){const dx=o.tx-o.x,dy=o.ty-o.y,dd=Math.hypot(dx,dy);if(dd<1){o.tx=undefined;o.st=D.chicken.peck;o.t=rnd(1.5,4);}else{o.x+=dx/dd*12*dt;o.y+=dy/dd*12*dt;o.flip=dx>0;}o.f+=dt*9;}
   else{o.f+=dt*7;if(o.t<0){o.tx=rnd(o.b[0],o.b[2]);o.ty=rnd(o.b[1],o.b[3]);o.st=D.chicken.walk;}}}
  else if(o.k==='duck'){o.t-=dt;if(o.tx!==undefined){const dx=o.tx-o.x,dy=o.ty-o.y,dd=Math.hypot(dx,dy);if(dd<.6){o.tx=undefined;o.st=D.duck.idle;o.t=rnd(2,6);}else{o.x+=dx/dd*5*dt;o.y+=dy/dd*5*dt;o.flip=dx>0;}o.f+=dt*5;}
   else{o.f+=dt*2;if(o.t<0){const [tx,ty]=o.near[Math.floor(Math.random()*o.near.length)];o.tx=(tx+.5)*16;o.ty=ty*16+14;o.st=D.duck.swim;}}}
  else if(o.k==='herd'){o.tm-=dt;
   if(o.s==='walk'){const dx=o.tx-o.x,dy=o.ty-o.y,dd=Math.hypot(dx,dy);if(dd<1){o.s=Math.random()<.55?'graze':'idle';o.tm=rnd(2,7);}else{o.x+=dx/dd*o.v*dt;o.y+=dy/dd*o.v*dt;if(Math.abs(dx)>0.5)o.flip=dx>0;}o.f+=dt*(o.t==='Horse_01'?7:8);}
   else{o.f+=dt*(o.s==='graze'?5:2);if(o.tm<0){if(Math.random()<.6){o.tx=rnd(o.b[0],o.b[2]);o.ty=rnd(o.b[1],o.b[3]);o.s='walk';}else{o.s=o.s==='graze'?'idle':'graze';o.tm=rnd(2,6);}}}}
  else if(o.k==='swan'){o.t-=dt;if(o.tx!==undefined){const dx=o.tx-o.x,dy=o.ty-o.y,dd=Math.hypot(dx,dy);if(dd<.6){o.tx=undefined;o.s='idle';o.t=rnd(2,6);}else{o.x+=dx/dd*4*dt;o.y+=dy/dd*4*dt;o.flip=dx>0;}o.f+=dt*4;}
   else{o.f+=dt*2;if(o.t<0){const [tx,ty]=o.near[Math.floor(Math.random()*o.near.length)];o.tx=(tx+.5)*16;o.ty=ty*16+14;o.s='swim';}}}
  else if(o.k==='fly'){o.ph+=dt*2;o.x+=o.v*dt+Math.sin(o.ph*1.3)*8*dt;o.y=o.by+Math.sin(o.ph)*10;o.f+=dt*12;o.flip=o.v<0;}
  if(o.x!==undefined)o.x=((o.x%D.W)+D.W)%D.W;}
 for(const c of clouds){c.x+=c.v*dt;if(c.x>D.W)c.x-=D.W;}}
function sprite(o){if(o.k==='herd'){drawA(o.t+':'+o.s,Math.floor(o.f),o.x,o.y,o.flip);return;}if(o.k==='swan'){drawA('Swan_01:'+o.s,Math.floor(o.f),o.x,o.y,o.flip);return;}
 const st=o.st,i=pic(st.src);if(!i)return;
 const fi=Math.floor(o.f)%st.n,w=st.w,h=st.h;
 const fol=isFol(o);let x=fol?Math.round((o.x-w/2-vx0)*K)/K:Math.round(o.x-w/2-vx0),y=Math.round(o.y-h);x=((x%D.W)+D.W)%D.W;
 if(fol&&window.DORF_JUMP){const tj=(performance.now()-window.DORF_JUMP)/1000;if(tj<1.6)y-=Math.round(Math.abs(Math.sin(tj*Math.PI*2.5))*(window.DORF_JAMP||5)*(1-tj/1.6));}
 for(const xx of [x,x-D.W]){if(xx>VW||xx+w<0)continue;
  if(o.a)ctx.globalAlpha=o.a;
  if(o.flip){ctx.save();ctx.translate(xx+w,y);ctx.scale(-1,1);ctx.drawImage(i,fi*w,0,w,h,0,0,w,h);ctx.restore();}
  else ctx.drawImage(i,fi*w,0,w,h,xx,y,w,h);
  ctx.globalAlpha=1;}}
function scene(){
 const base=im(MODE==='f'?D.baseF:D.base),wat=pic(D.wasser,true);if(!base.complete||!wat)return false;
 const k=RM?0:Math.floor(wt/1.3*8)%8;let ox=-(((vx0%D.W)+D.W)%D.W);
 for(let x=ox;x<VW;x+=D.W){ctx.drawImage(wat,0,k*D.H,D.W,D.H,x,0,D.W,D.H);ctx.drawImage(base,x,0);}
 const ON=window.DORF_ON||{},now=performance.now(),ex=[];
 // Huehner verschwinden, sobald das Moor (K12) im Gehege erscheint
 const mo=ON.K12!==undefined&&now-ON.K12>200&&!(window.DORF_OUT&&now-window.DORF_OUT>250)?(D.ext||[]).filter(e=>e[0]==='K12'):[];
 const underMoor=o=>{if((o.k!=='chick'&&!o.coop)||!mo.length)return false;const cx=(o.b[0]+o.b[2])/2,cy=(o.b[1]+o.b[3])/2;return mo.some(e=>cx>=e[5]-8&&cx<=e[5]+e[3]+8&&cy>=e[6]-8&&cy<=e[6]+e[4]+16);};
 const vis=ents.filter(o=>!o.hid&&!o.top&&!underMoor(o));const oc=new Set();for(const o of vis)occluders(o,oc);
 const OUTF=window.DORF_OUT?Math.max(0,1-(now-window.DORF_OUT)/500):1;
 for(const e of (D.ext||[])){const t=ON[e[0]];if(t===undefined)continue;const a=Math.max(0,Math.min(1,(now-t)/450))*OUTF;if(a<=0)continue;ex.push({y:e[7],x:e,a});occluders({st:{w:e[3],h:e[4]},x:e[5]+e[3]/2,y:e[7]},oc);}
 const an=[],cx0=vx0+VW/2;for(const it of (D.anims||[])){const a=D.anim[it[0]];if(!a||Math.abs(wdx(cx0,it[1]))>VW/2+40)continue;an.push({y:it[2],an:it});occluders({st:{w:a[2],h:a[5]},x:it[1],y:it[2]},oc);}
 const dr=(D.doors||[]).filter(d=>d.open&&d.open>now).map(d=>({y:d.y+0.01,d}));
 for(const e of dr){const x0=e.d.x-6,y0=e.d.y-18;for(const q of OC)if(q.b===e.d.y&&wdx(x0,q.x)<12&&wdx(x0,q.x)+q.w>0&&q.y<y0+18)oc.add(q);}
 occClose(oc);
 const L=vis.map(o=>({y:o.y,o})).concat(ex,dr,an,[...oc].map(q=>({y:q.z,q}))).sort((a,b)=>a.y-b.y);
 for(const e of L){if(e.o)sprite(e.o);else if(e.an){const it=e.an,a=D.anim[it[0]];drawA(it[0],RM?0:Math.floor(wt*(AFPS[it[0]]||5)+it[3]),it[1],it[2],false);}else if(e.d)drawDoor(e.d);else if(e.x)drawExt(e.x,e.a);else drawOcc(e.q);}
 // Rauch: window.DORF_SMOKEOFF Kamine rauchen nicht mehr (Heizungen ersetzt)
 const SO=+(window.DORF_SMOKEOFF||0)*D.smoke.length;for(const o of ents)if(o.top&&!(o.k==='smoke'&&o.si<SO))sprite(o);return true;}
function render(){if(!ctx)return;
 const P=Math.max(0,Math.min(1,+(window.DORF_P||0))),OFF=Math.round(camFr*K);
 ctx.setTransform(K,0,0,K,-OFF,0);
 if(P<0.99){MODE='g';if(!scene())return;}
 if(P>0.01){if(!off||off.width!==cv.width||off.height!==cv.height){off=document.createElement('canvas');off.width=cv.width;off.height=cv.height;offc=off.getContext('2d');}
  offc.setTransform(1,0,0,1,0,0);offc.clearRect(0,0,off.width,off.height);offc.imageSmoothingEnabled=false;offc.setTransform(K,0,0,K,-OFF,0);
  const m=ctx;ctx=offc;MODE='f';const okf=scene();ctx=m;MODE='g';
  if(okf){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=P;ctx.drawImage(off,0,0);ctx.globalAlpha=1;ctx.setTransform(K,0,0,K,-OFF,0);}}
 ctx.globalAlpha=.07;
 for(const c of clouds){if(!c.c.width)continue;const w=Math.round(c.c.width*c.sc),h=Math.round(c.c.height*c.sc);let x=Math.round(c.x-vx0);x=((x%D.W)+D.W)%D.W;
  for(const xx of [x,x-D.W])if(xx<VW&&xx+w>0)ctx.drawImage(c.c,xx,Math.round(c.y),w,h);}
 ctx.globalAlpha=1;}
function layout(){const d=document.getElementById('dorf');if(!d)return false;OY=0;
 if(!cv||!d.contains(cv)){d.innerHTML='';cv=document.createElement('canvas');d.appendChild(cv);ctx=cv.getContext('2d');}
 S=+getComputedStyle(d).getPropertyValue('--ds')||.75;SNAP=!!(d.closest&&d.closest('.szene')&&!d.closest('.nosnap'));
 const cw=d.clientWidth;
 if(SNAP){// Pixeldichte begrenzen: Bei 3x zeichnet ein Handy 9-mal so viele Pixel, die Ueberblendung grau zu farbig sogar doppelt.
  // Das Bild wird danach vom Browser pixelgenau hochskaliert (image-rendering: pixelated).
  const dpr=Math.min(matchMedia('(pointer: coarse)').matches?1.5:2,window.devicePixelRatio||1)*(window.UIZ||1);
  const set=(k,crop=0)=>{K=k;S=K/dpr;VW=Math.ceil(cw/S)+2;cv.width=Math.ceil(VW*K);cv.height=D.H*K;cv.style.width=(cv.width/dpr)+'px';cv.style.height=(D.H*S)+'px';
   OY=Math.round(crop/2);cv.style.marginTop=OY?(-OY)+'px':'';d.style.height=(D.H*S-crop)+'px';};
  set(Math.max(1,Math.round(S*dpr)));
  // Dorf nach der Abstimmung (window.DORF_FIT): Alles soll ohne Scrollen sichtbar sein (Spieltest 26.11.2026). Ganze Bildpunkte machen die Stufen grob
  // (Retina 1.5 statt 1.25, Windows 125 % 1.6 statt 1.25). Fehlt wenig, wird oben und unten je ein Rand abgeschnitten (hoechstens 20 % des Bildes),
  // fehlt mehr, kommt die naechstkleinere scharfe Stufe.
  if(window.DORF_FIT){const de=document.documentElement,over=()=>(de.scrollHeight-innerHeight)/(window.UZF||1);
   for(let i=0;i<4;i++){const o=over();if(o<=1)break;const h=D.H*S;if(o+4<=h*0.2){set(K,o+4);break;}if(K>1&&(K-1)/dpr>=0.75)set(K-1);else{set(K,h*0.2);break;}}}}
 else{K=1;VW=Math.ceil(cw/S)+1;cv.width=VW;cv.height=D.H;cv.style.width=(VW*S)+'px';cv.style.height=(D.H*S)+'px';d.style.height='';}
 ctx.imageSmoothingEnabled=false;if(!camX)camX=D.W/2;vx0=Math.round(camX-VW/2);return true;}
// Kamera: auf schmalen Bildschirmen zum Element fahren, das gerade neu erscheint (window.DORF_FOCUS)
const CX={};for(const e of (D.ext||[])){const c=e[5]+e[3]/2;if(CX[e[0]]===undefined||Math.abs(c-D.W/2)<Math.abs(CX[e[0]]-D.W/2))CX[e[0]]=c;}
function camTarget(){if(window.DORF_FOLLOW){const o=folEnt();if(o)return o.x;}const F=window.DORF_FOCUS;if(!F||!F.length||VW>=1000)return D.W/2;const now=performance.now();let k=null;for(const f of F)if(f.t<=now)k=f.k;
 if(k===null||CX[k]===undefined)return D.W/2;return Math.max(VW/2,Math.min(D.W-VW/2,CX[k]));}
window.dorfBox=k=>{if(!cv||CX[k]===undefined)return null;let best=null;for(const e of D.ext){if(e[0]!==k)continue;if(!best||Math.abs(e[5]+e[3]/2-CX[k])<Math.abs(best[5]+best[3]/2-CX[k]))best=e;}
 let x=((Math.round(best[5]-vx0)%D.W)+D.W)%D.W;if(x>VW)x-=D.W;return {x:(x-camFr)*S,y:best[6]*S-OY,w:best[3]*S,h:best[4]*S};};
window.dorfHit=(px,py)=>{if(!cv)return null;py+=OY;const ON=window.DORF_ON||{},now=performance.now();let hit=null;
 for(const e of D.ext){const t=ON[e[0]];if(t===undefined||t>now)continue;let x=((Math.round(e[5]-vx0)%D.W)+D.W)%D.W;if(x>VW)x-=D.W;
  const X=px/S+camFr,Y=py/S;if(X>=x-2&&X<=x+e[3]+2&&Y>=e[6]-2&&Y<=e[6]+e[4]+2)hit={k:e[0],x:(x-camFr)*S,y:e[6]*S,w:e[3]*S,h:e[4]*S};}return hit;};
function camStep(dt){const t=camTarget(),d=wdx(camX,t);if(window.DORF_FOLLOW&&folEnt()&&Math.abs(d)<40)camX=t;else camX+=d*Math.min(1,dt*3.5);camX=((camX%D.W)+D.W)%D.W;if(Math.abs(d)<0.05)camX=t;const fx=camX-VW/2;vx0=Math.floor(fx);camFr=SNAP?Math.round((fx-vx0)*K)/K:0;}
window.dorfSkipWalk=()=>{const o=folEnt();if(!o||window.DORF_WALK==null)return;if(RM){o.x=window.DORF_WALK;o.y=(D.band[0]+D.band[1])/2;o.q=[];o.wait=0;return;}if(o.wt!==window.DORF_WALK){o.wt=window.DORF_WALK;o.boost=1;}o.boost=Math.min(6,(o.boost||1)*2.5);o.v=52*o.boost;};
window.dorfArrived=()=>{const o=folEnt();return !!o&&window.DORF_WALK!=null&&Math.abs(wdx(o.x,window.DORF_WALK))<=1.5;};
window.dorfEnt=()=>{const o=folEnt();if(!o||!cv)return null;let x=((Math.round(o.x-vx0)%D.W)+D.W)%D.W;if(x>VW)x-=D.W;x+=Math.round((o.x-vx0)*K)/K-Math.round(o.x-vx0);return {x:(x-camFr)*S,y:(o.y-(o.set.side.h||o.st.h))*S-OY};};
function loop(ts){const dt=Math.min(.1,(ts-(last||ts))/1000);last=ts;
 if(document.getElementById('dorf')&&cv&&document.getElementById('dorf').contains(cv)){camStep(dt);update(dt);render();}
 raf=requestAnimationFrame(loop);}
setup();
new MutationObserver(()=>{const d=document.getElementById('dorf');if(d&&!d.dataset.ok){d.dataset.ok=1;cv=null;camX=D.W/2;if(window.DORF_FOLLOW){const o=folEnt();if(o){o.hid=false;o.wait=0;o.q=[];if(window.DORF_WALK0!=null){o.x=window.DORF_WALK0;o.y=(D.band[0]+D.band[1])/2;}camX=o.x;}}if(layout()){im(D.base).decode?.().then(render).catch(()=>{});render();}}}).observe(document.documentElement,{childList:true,subtree:true});
addEventListener('resize',()=>{if(layout())render();});
for(const src of [D.base,D.baseF,D.wasser,D.sailimg,D.atlasimg,D.animimg])im(src).addEventListener('load',()=>render());
window.dorfRender=()=>{if(cv&&document.getElementById('dorf')&&document.getElementById('dorf').contains(cv))render();};
if(!RM)raf=requestAnimationFrame(loop);
})();
