# Kamera im Dorf: faehrt auf schmalen Bildschirmen zum Element, das gerade erscheint.
# Anwenden auf src/dorf_anim.js + src/template.html (oder direkt auf index.html): python3 kamera.py DATEI...
import sys
R_DORF=[
("let cv=null,ctx=null,S=.75,VW=0,vx0=0,","let camX=0,cv=null,ctx=null,S=.75,VW=0,vx0=0,"),
("ctx.imageSmoothingEnabled=false;vx0=Math.round(D.W/2-VW/2);return true;}",
 """ctx.imageSmoothingEnabled=false;if(!camX)camX=D.W/2;vx0=Math.round(camX-VW/2);return true;}
// Kamera: auf schmalen Bildschirmen zum Element fahren, das gerade neu erscheint (window.DORF_FOCUS)
const CX={};for(const e of (D.ext||[])){const c=e[5]+e[3]/2;if(CX[e[0]]===undefined||Math.abs(c-D.W/2)<Math.abs(CX[e[0]]-D.W/2))CX[e[0]]=c;}
function camTarget(){const F=window.DORF_FOCUS;if(!F||!F.length||VW>=1000)return D.W/2;const now=performance.now();let k=null;for(const f of F)if(f.t<=now)k=f.k;
 if(k===null||CX[k]===undefined)return D.W/2;return Math.max(VW/2,Math.min(D.W-VW/2,CX[k]));}
function camStep(dt){const t=camTarget();camX+=(t-camX)*Math.min(1,dt*2.2);if(Math.abs(t-camX)<0.5)camX=t;vx0=Math.round(camX-VW/2);}"""),
("if(document.getElementById('dorf')&&cv&&document.getElementById('dorf').contains(cv)){update(dt);render();}",
 "if(document.getElementById('dorf')&&cv&&document.getElementById('dorf').contains(cv)){camStep(dt);update(dt);render();}"),
("if(d&&!d.dataset.ok){d.dataset.ok=1;cv=null;","if(d&&!d.dataset.ok){d.dataset.ok=1;cv=null;camX=D.W/2;"),
]
R_GAME=[
(" for(const k in S.adopted)if(DORFK.includes(k)&&on[k]===undefined)on[k]=0;",
 " window.DORF_FOCUS=Object.keys(on).filter(k=>on[k]>0).sort((a,b)=>on[a]-on[b]).map(k=>({k,t:on[k]-500}));\n for(const k in S.adopted)if(DORFK.includes(k)&&on[k]===undefined)on[k]=0;"),
("function viewStart(){window.DORF_P=0;window.DORF_ON={};","function viewStart(){window.DORF_P=0;window.DORF_ON={};window.DORF_FOCUS=[];"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read();n=0
    for a,b in R_DORF+R_GAME:
        c=s.count(a)
        if c==1: s=s.replace(a,b);n+=1
        elif c>1: raise SystemExit(f'{f}: mehrfach: {a[:50]}')
    open(f,'w',encoding='utf-8').write(s);print(f,n,'Ersetzungen')
