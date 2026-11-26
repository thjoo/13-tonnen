// Gruppenspiel mit drei Geraeten gegen einen nachgebauten Speicher (kein Firebase).
// Prueft: alle sehen die gleichen Vorlagen und Resultate, alle kommen ans Ende, die Punkte stimmen ueberein.
// Aufruf: node tests/gruppe.js [index.html]
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const js=fs.readFileSync(process.argv[2]||'index.html','utf8').split('<script>')[1].split('</script>')[0];
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
 onDisc:()=>{},now:{'.sv':'timestamp'},cleanup:async()=>{}};}
function client(){const app={innerHTML:''};
 const ctx={console,setImmediate,setTimeout,setInterval,clearInterval,Math,JSON,Date,Promise,performance:{now:()=>Date.now()},
  localStorage:{getItem:k=>k==='13t_aktiv'?String(Date.now()):'1',setItem(){},removeItem(){}},
  window:{__FAKENET:fake,scrollTo(){},scrollY:0},document:{getElementById:()=>app,querySelectorAll:()=>[]}};
 ctx.window.window=ctx.window;vm.createContext(ctx);vm.runInContext(js,ctx);
 return {run:c=>vm.runInContext(c,ctx),app};}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// Gieriger Spieler: waehlt Karten mit der besten Wirkung pro Herz, Rest der Herzen auf die erste Vorlage
const SPIELEN=`{let ok=true;while(ok){ok=false;let best=null,bv=0;
 for(const id of S.hand){if(S.chosen[id]!==undefined||blocked(id))continue;const e=effOwn(id),h=costH(id)+Math.max(0,costG(id))*0.4+0.1;if(e/h>bv){bv=e/h;best=id}}
 if(best&&(freeH()>1||costH(best)==0)){choose(best);ok=true}}
 while(freeH()>0)alloc(S.ballot[0],1);}`;
(async()=>{
 const A=client(),B=client(),C=client(),all=[A,B,C],each=c=>all.map(X=>X.run(c));
 A.run("S.mode='kurz';Group.create()");await sleep(30);
 const code=A.run('G.code');
 B.run(`Group.join('${code}')`);C.run(`Group.join('${code}')`);await sleep(30);
 A.run("Group.pickFig('Daniel')");B.run("Group.pickFig('Lia')");C.run("Group.pickFig('Elif')");await sleep(30);
 assert(A.app.innerHTML.includes('Spiel starten (3'),'Lobby zeigt nicht 3 Personen');
 A.run("Group.start()");await sleep(50);
 const last=A.run('LAST');
 for(let r=0;r<=last;r++){
  for(const X of all)X.run(SPIELEN);await sleep(20);
  assert.equal(new Set(each('S.ballot.join("+")')).size,1,`Runde ${r}: verschiedene Vorlagen`);
  A.run('vote()');B.run('vote()');await sleep(20);
  assert.deepEqual(A.run('G.missing()'),['Elif'],`Runde ${r}: falsch, wer noch fehlt`);
  C.run('vote()');await sleep(60);
  const res=each('JSON.stringify(S.results)');
  assert(res[0]!=='null',`Runde ${r}: keine Resultate`);
  assert.equal(new Set(res).size,1,`Runde ${r}: verschiedene Resultate`);
  for(const X of all)X.run('toEvent();nextRound()');await sleep(40);
 }
 assert.equal(new Set(each('JSON.stringify(S.adopted)')).size,1,'verschiedene angenommene Vorlagen');
 for(const X of all)X.run('toEnd()');await sleep(60);
 assert.deepEqual(each('S.screen'),['end','end','end']);
 assert(A.app.innerHTML.includes('Eure Gruppe'),'Gruppentabelle fehlt');
 const sc=each('JSON.stringify(scoreOf(scoreNow()))');
 assert.equal(new Set(sc).size,1,'verschiedene Punkte');
 console.log('ok',code,each('S.fig+" "+val(2050,ACT).toFixed(2)').join(', '),sc[0]);
 process.exit(0);
})().catch(e=>{console.error(e);process.exit(1)});
