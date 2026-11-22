const fs=require('fs');const js=fs.readFileSync('index.html','utf8').split('<script>')[1].split('</script>')[0];
let out='';global.document={getElementById:()=>({set innerHTML(v){out=v}})};global.window={scrollTo(){}};
eval(js.replace(/^const |^let /gm,'var '));
const mode=process.argv[2]||'kurz',N=300;
for(const f of ['Daniel','Ruth','Lia','Elif']){const c={};
 for(let run=0;run<N;run++){S.mode=mode;fresh();startFig(f);
  for(let r=0;r<=LAST;r++){let ok=true;while(ok){ok=false;let best=null,bv=0;
    for(const id of S.hand){if(S.chosen[id]!==undefined||blocked(id))continue;const e=effOwn(id);const h=costH(id)+Math.max(0,costG(id))*0.4+0.1;if(e/h>bv){bv=e/h;best=id}}
    if(best&&(freeH()>1||costH(best)==0)){choose(best);ok=true}}
   for(const k of S.ballot){while(freeH()>0&&chance(k)<95)alloc(k,1)}
   vote();toEvent();nextRound();}
  for(const k in S.chosen)c[k]=(c[k]||0)+1;}
 console.log(mode,f,Object.entries(c).sort((a,b)=>b[1]-a[1]).map(([k,v])=>k+':'+Math.round(v/N*100)).join(' '));}
