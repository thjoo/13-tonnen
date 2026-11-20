# Kamera Teil 2: auf schmalen Bildschirmen mehr Zeit pro Element (1.6 s), Jahreszahl oben links statt ueber der Strasse.
import sys
R=[
('return L.map((x,i)=>x.replace("<li ",`<li style="animation-delay:${600+i*700}ms" `)).join("");',
 'return L.map((x,i)=>x.replace("<li ",`<li style="animation-delay:${600+i*dorfGap()}ms" `)).join("");'),
("function dorfOn(){","function dorfGap(){return typeof innerWidth!=='undefined'&&innerWidth<1000?1600:700}\nfunction dorfOn(){"),
("on[x.k]=rm?0:now+600+i*700+300","on[x.k]=rm?0:now+600+i*dorfGap()+300"),
("on[ps.pid]=rm?0:now+600+i*700+300","on[ps.pid]=rm?0:now+600+i*dorfGap()+300"),
(".szene .dtitel{transform:none;top:auto;bottom:18px;animation:none}",
 ".szene .dtitel{transform:none;top:10px;bottom:auto;left:16px;right:auto;justify-content:start;font-size:calc(320px*var(--ds)*.2);animation:none}"),
("camX+=(t-camX)*Math.min(1,dt*2.2)","camX+=(t-camX)*Math.min(1,dt*3.5)"),
]
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read();n=0
    for a,b in R:
        c=s.count(a)
        if c==1:s=s.replace(a,b);n+=1
        elif c>1: raise SystemExit('mehrfach '+a[:40])
    open(f,'w',encoding='utf-8').write(s);print(f,n)
