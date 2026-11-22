const fs=require('fs');const html=fs.readFileSync('index.html','utf8');
const js=html.split('<script>')[1].split('</script>')[0];
let out='';global.document={getElementById:()=>({set innerHTML(v){out=v}})};global.window={scrollTo(){}};
eval(js.replace(/^const |^let /gm,'var ').replace(/\nfunction /g,'\nglobal.__f=1;function '));
for(const f of Object.keys(M.FIG)){ for(let run=0;run<3;run++){
 fresh();startFig(f);
 for(let r=0;r<4;r++){
  // greedy: pick card with best effect per heart
  let ok=true;while(ok){ok=false;let best=null,bv=0;
   for(const id in M.CARDS){if(S.chosen[id]!==undefined||blocked(id))continue;const e=effOwn(id);const h=costH(id)+costG(id)*0.3+0.2;if(e/h>bv){bv=e/h;best=id}}
   if(best&&S.hearts>1){choose(best);ok=true}}
  while(S.hearts-Object.values(S.alloc).reduce((a,b)=>a+b,0)>0){alloc(S.ballot[0],1)}
  vote();toEvent();nextRound();
 }
 console.log(f,run,'2050',val(2050,ACT).toFixed(2),'VO',val(2050,VO).toFixed(2),'sum',sum(2026,2050,ACT).toFixed(0),Object.keys(S.chosen).join(','),'|',Object.keys(S.adopted).join(','),'| money',S.money, out.length>1000?'ok':'EMPTY');
}}
