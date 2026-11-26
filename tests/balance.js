// Balance mit Bots: spielt viele ganze Partien mit den echten Regeln aus index.html (ohne Browser).
// Drei Spielweisen: stark (waehlt, was am meisten bringt, und setzt sich fuer Vorlagen ein),
// mittel (waehlt zufaellig, was gerade geht) und schwach (hoechstens eine Karte pro Runde, kein Engagement).
// Aufruf: node tests/balance.js [index.html] [--zeigen]   (--zeigen druckt die Tabelle ohne zu pruefen)
const fs=require('fs'),vm=require('vm');
const datei=process.argv.find(a=>a.endsWith('.html'))||'index.html',zeigen=process.argv.includes('--zeigen');
const js=fs.readFileSync(datei,'utf8').split('<script>')[1].split('</script>')[0];
const app={innerHTML:''};
const ctx={console,Math,JSON,Date,setTimeout:()=>0,performance:{now:()=>0},
 localStorage:{getItem:k=>k==='13t_aktiv'?String(Date.now()):'1',setItem(){},removeItem(){}},
 window:{scrollTo(){}},document:{getElementById:()=>app}};
ctx.window.window=ctx.window;vm.createContext(ctx);vm.runInContext(js,ctx);
const N=30; // Partien pro Figur und Spielweise
const BOTS={
 stark:`{let ok=true;while(ok){ok=false;let best=null,bv=0;
  for(const id of S.hand){if(S.chosen[id]!==undefined||blocked(id))continue;const e=effOwn(id),h=costH(id)+Math.max(0,costG(id))*0.4+0.1;if(e/h>bv){bv=e/h;best=id}}
  if(best&&(freeH()>1||costH(best)==0)){choose(best);ok=true}}
  const ps=projState(S.r);if(ps&&!ps.done)while(freeH()>0&&ps.acc+projLive()<ps.need)palloc(1);
  for(const k of S.ballot)while(freeH()>0&&chance(k)<95)alloc(k,1);
  for(const k of S.ballot)if(moneyFree()>=SPENDE+1&&chance(k)<95)donate(k);}`,
 mittel:`{const R=BOT();for(const id of shuffle([...S.hand],R))if(!blocked(id)&&R()<0.6)choose(id);
  for(const k of S.ballot)if(freeH()>0&&R()<0.5)alloc(k,1);}`,
 schwach:`{const R=BOT();const ok=S.hand.filter(id=>!blocked(id)&&costH(id)<=1);if(ok.length&&R()<0.7)choose(ok[Math.floor(R()*ok.length)]);}`};
function spiele(mode,fig,bot,seed){
 return vm.runInContext(`(()=>{S.mode='${mode}';fresh();S.seed='${seed}';let b=0;BOT=()=>rngS(hashS(S.seed+'|bot|'+S.r+'|'+(b++)));startFig('${fig}');
  for(let r=0;r<=LAST;r++){S.crisisSeen=S.r;${BOTS[bot]};vote(true);nextRound();}
  const v=val(2050,ACT);if(!(v>0&&v<13.5)||S.money<0)throw new Error('ungueltig '+v+' '+S.money);return v})()`,ctx);}
vm.runInContext('var BOT;',ctx);
const tab={};
for(const mode of ['kurz','lang'])for(const bot of Object.keys(BOTS)){const v=[];
 for(const fig of vm.runInContext('Object.keys(M.FIG)',ctx))for(let i=0;i<N;i++)v.push(spiele(mode,fig,bot,`B${i}`));
 v.sort((a,b)=>a-b);tab[mode+' '+bot]={median:+v[v.length>>1].toFixed(2),unter6:Math.round(v.filter(x=>x<6).length/v.length*100)};}
if(zeigen){console.table(tab);process.exit(0);}
const fehler=[],pruefe=(ok,txt)=>{if(!ok)fehler.push(txt)};
// Grenzen mit Spielraum um die Messung vom 26.11.2026 (je 5 Figuren x 30 Partien, unter 6 t):
// kurz stark 78 %, mittel 34 %, schwach 0 %; lang stark 73 %, mittel 54 %, schwach 0 %.
// Wer die Zahlen im Spiel aendert und hier rot wird: mit --zeigen nachsehen, ob die neue Balance gewollt ist, dann die Grenzen anpassen.
// Ziel laut Spielentscheid 24.11.2026: Die erste Etappe (unter 6 t) ist schwierig, aber erreichbar; starke Spiele schaffen sie meistens.
for(const mode of ['kurz','lang']){const s=tab[mode+' stark'],m=tab[mode+' mittel'],w=tab[mode+' schwach'];
 pruefe(s.median<m.median&&m.median<w.median,`${mode}: stark < mittel < schwach (Median 2050)`);
 pruefe(s.unter6>=60,`${mode}: stark unter 6 t in ${s.unter6} % (erwartet mindestens 60 %)`);
 pruefe(m.unter6<=65,`${mode}: mittel unter 6 t in ${m.unter6} % (erwartet hoechstens 65 %)`);
 pruefe(w.unter6<=10,`${mode}: schwach unter 6 t in ${w.unter6} % (erwartet hoechstens 10 %)`);}
console.log(JSON.stringify(tab));
if(fehler.length){console.error(fehler.join('\n'));process.exit(1);}
