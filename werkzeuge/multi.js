const fs=require('fs'),vm=require('vm');
const js=fs.readFileSync('index.html','utf8').split('<script>')[1].split('</script>')[0];
const store={};let uidc=0;const watchers=[];
const clone=x=>x===undefined?null:JSON.parse(JSON.stringify(x));
const parts=p=>p.split('/').filter(Boolean);
function getP(p){let o=store;for(const k of parts(p)){if(o==null||typeof o!=='object')return null;o=o[k];}return o===undefined?null:o;}
function setP(p,v){const ks=parts(p);let o=store;for(let i=0;i<ks.length-1;i++){if(typeof o[ks[i]]!=='object'||o[ks[i]]===null)o[ks[i]]={};o=o[ks[i]];}
 if(v===null||v===undefined)delete o[ks.at(-1)];else o[ks.at(-1)]=resolveTs(clone(v));}
function resolveTs(v){if(v&&typeof v==='object'){if(v['.sv'])return Date.now();for(const k in v)v[k]=resolveTs(v[k]);}return v;}
function notify(){setImmediate(()=>{for(const w of watchers)w.cb(clone(getP(w.p)));});}
function fake(){const uid='u'+(++uidc);return {uid,init:async()=>{},
 set:async(p,v)=>{setP(p,v);notify()},update:async(p,v)=>{for(const k in v)setP(p+'/'+k,v[k]);notify()},
 remove:async p=>{setP(p,null);notify()},get:async p=>clone(getP(p)),
 watch:(p,cb)=>{const w={p,cb};watchers.push(w);setImmediate(()=>cb(clone(getP(p))));return ()=>{watchers.splice(watchers.indexOf(w),1)}},
 txn:async(p,fn)=>{const r=fn(clone(getP(p)));if(r===undefined)return false;setP(p,r);notify();return true},
 push:async(p,v)=>{const k='k'+Date.now()+Math.random().toString(36).slice(2,6);setP(p+'/'+k,v);notify();return k},top:async(p,n)=>{const o=getP(p)||{};return Object.entries(o).map(([id,v])=>({id,...v})).sort((a,b)=>b.s-a.s).slice(0,n)},onDisc:()=>{},now:{'.sv':'timestamp'},cleanup:async()=>{}};}
function client(){const app={innerHTML:''};
 const ctx={console,setImmediate,setTimeout,setInterval,clearInterval,Math,JSON,Date,Promise,performance:{now:()=>Date.now()},localStorage:{getItem:()=>'1',setItem(){}},
  window:{__FAKENET:fake,scrollTo(){},scrollY:0},document:{getElementById:()=>app,querySelectorAll:()=>[]}};
 ctx.window.window=ctx.window;vm.createContext(ctx);
 vm.runInContext(js.replace(/typeof window!=="undefined"&&window.__FAKENET/,'window.__FAKENET'),ctx);
 return {ctx,run:c=>vm.runInContext(c,ctx),app};}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const A=client(),B=client(),C=client();
 A.run("S.mode='kurz';Group.create()");await sleep(30);
 const code=A.run('G.code');console.log('code',code);
 B.run(`Group.join('${code}')`);C.run(`Group.join('${code}')`);await sleep(30);
 A.run("Group.pickFig('Daniel')");B.run("Group.pickFig('Lia')");C.run("Group.pickFig('Elif')");await sleep(30);
 console.log('lobby has',A.app.innerHTML.includes('Spiel starten (3'));
 A.run("Group.start()");await sleep(50);
 const all=[A,B,C];
 for(let r=0;r<4;r++){
  for(const X of all){X.run(`{
   let ok=true;while(ok){ok=false;let best=null,bv=0;
    for(const id of S.hand){if(S.chosen[id]!==undefined||blocked(id))continue;const e=effOwn(id);const h=costH(id)+Math.max(0,costG(id))*0.4+0.1;if(e/h>bv){bv=e/h;best=id}}
    if(best&&(freeH()>1||costH(best)==0)){choose(best);ok=true}}
   while(freeH()>0)alloc(S.ballot[0],1);}`);}
  await sleep(20);
  console.log('r',r,'ballots',all.map(X=>X.run('S.ballot.join("+")')).join(' | '),'chance seen',all.map(X=>X.run('chance(S.ballot[0])')).join(','));
  A.run('vote()');B.run('vote()');await sleep(20);
  console.log(' waiting A missing:',A.run('G.missing().join(",")'));
  C.run('vote()');await sleep(60);
  console.log(' results',all.map(X=>X.run('S.results?S.results.map(x=>x.k+(x.ok?"✓":"✗")+x.c).join(" "):"none"')).join(' | '));
  for(const X of all)X.run('toEvent();nextRound()');await sleep(40);
 }
 console.log('screens',all.map(X=>X.run('S.screen')).join(','),'adopted',all.map(X=>X.run('Object.keys(S.adopted).join("")')).join(' | '));
 await sleep(40);
 console.log('end table ok',A.app.innerHTML.includes('Eure Gruppe'),(A.app.innerHTML.match(/class="n">\d+\.\d/g)||[]).length);
 console.log(all.map(X=>X.run('S.fig+" "+val(2050,ACT).toFixed(2)')).join(' ; '));
 console.log('score',all.map(X=>X.run('JSON.stringify(scoreOf(scoreNow()))')).join(' | '));
 A.run('submitScore()');await sleep(40);B.run('submitScore()');await sleep(40);
 console.log('board',JSON.stringify(getP('scores')),'B msg',B.run('S.scoreMsg'));
 console.log('A html has board',A.app.innerHTML.includes('class="board"'));
 process.exit(0);
})().catch(e=>{console.error(e);process.exit(1)});
