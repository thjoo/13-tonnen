const fs=require('fs');const js=fs.readFileSync('index.html','utf8').split('<script>')[1].split('</script>')[0];
let out='';global.document={getElementById:()=>({set innerHTML(v){out=v}})};global.window={scrollTo(){}};
eval(js.replace(/^const |^let /gm,'var '));
const mode=process.argv[2]||'kurz', N=+process.argv[3]||200;
const res={};
for(const f of Object.keys(M.FIG)){let a=[],mo=[],idle=[],don=0,errs=0;
 for(let run=0;run<N;run++){
  S.mode=mode;fresh();startFig(f);
  for(let r=0;r<=LAST;r++){
   let ok=true;while(ok){ok=false;let best=null,bv=0;
    for(const id of S.hand){if(S.chosen[id]!==undefined||blocked(id))continue;const e=effOwn(id);const h=costH(id)+Math.max(0,costG(id))*0.4+0.1;if(e/h>bv){bv=e/h;best=id}}
    if(best&&(freeH()>1||costH(best)==0)){choose(best);ok=true}}
   for(const k of S.ballot){while(freeH()>0&&chance(k)<95)alloc(k,1)}
   for(const k of S.ballot){if(S.money>=SPENDE+1&&chance(k)<95){donate(k);don++}}
   vote();toEvent();nextRound();
  }
  if(out.length<1000)errs++;
  a.push(val(2050,ACT));mo.push(S.money);
 }
 a.sort((x,y)=>x-y);mo.sort((x,y)=>x-y);
 console.log(mode,f.padEnd(7),'2050 median',a[N>>1].toFixed(2),'p10',a[N*0.1|0].toFixed(2),'p90',a[N*0.9|0].toFixed(2),'| Geld Ende median',mo[N>>1],'max',mo[N-1],'| Spenden/Spiel',(don/N).toFixed(1),errs?'ERR'+errs:'');
}
