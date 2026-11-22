import json
GREY=['sonst','freizeit','kleider','beherb','wuebrig','bau','moebel','ernrest','milch','fleisch']
BASE={'auto':1.3,'flug':1.4,'oev':0.2,'heiz':0.9,'strom':0.2,'wuebrig':1.0,'bau':0.8,'moebel':0.4,
 'fleisch':0.43,'milch':0.26,'waste':0.19,'saison':0.1,'kette':0.2,'kantine':0.06,'ernrest':1.46,
 'sonst':0.05,'elek':0.05,'stream':0.03,'recyc':0.02,'lkw':0.4,'ind':0.2,'repar':0.05,'freizeit':0.5,'kleider':0.3,'beherb':0.2,
 'oeff':1.3,'oeffbesch':0.8}
assert abs(sum(BASE.values())-12.8)<0.01
CAT={'Mobilität':['auto','flug','oev'],'Wohnen':['heiz','strom','wuebrig','bau','moebel'],
 'Ernährung':['fleisch','milch','waste','saison','kette','kantine','ernrest'],
 'Konsum und Freizeit':['sonst','elek','stream','recyc','lkw','ind','repar','freizeit','kleider','beherb'],
 'Öffentliche Leistungen':['oeff','oeffbesch']}
KON=['sonst','elek','stream','recyc','lkw','ind','repar','freizeit']
CARDS={
 'I1a':dict(h=1,g=0,mult={'flug':0.5}),'I1b':dict(h=3,g=0,mult={'flug':0.0}),
 'I2':dict(h=2,g=-2,mult={'auto':0.0},add={'oev':0.1},excl=['I3','I4','I6']),
 'I3':dict(h=0,g=4,mult={'auto':1/3},excl=['I2']),'I7':dict(h=3,g=0,mult={'auto':1/3},excl=['I2','I3','I4','I6']),'I4':dict(h=1,g=0,mult={'auto':0.5},excl=['I2']),
 'W1':dict(h=1,g=0,mult={'heiz':0.88}),'W2':dict(h=0,g=4,mult={'heiz':0.1},excl=['W2b']),
 'W2b':dict(h=3,g=0,mult={'heiz':0.1},excl=['W2']),'W3':dict(h=1,g=4,mult={'heiz':0.7}),
 'W4':dict(h=2,g=-2,mult={'heiz':0.75,'bau':0.75,'moebel':0.75}),'W5':dict(h=0,g=1,mult={'strom':0.1}),
 'W6':dict(h=1,g=0,mult={'moebel':0.7}),
 'N1':dict(h=1,g=0,mult={'fleisch':0.3}),'N2':dict(h=2,g=0,mult={'fleisch':0.0}),
 'N3':dict(h=3,g=0,mult={'fleisch':0.0,'milch':0.0}),'N4':dict(h=1,g=0,mult={'waste':0.0}),'N5':dict(h=1,g=1,mult={'saison':0.0}),
 'I5':dict(h=0,g=2,mult={'flug':0.7}),'I6':dict(h=1,g=1,mult={'auto':0.85},excl=['I2']),
 'W7':dict(h=0,g=1,mult={'strom':0.8}),'N6':dict(h=0,g=2,mult={'ernrest':0.93}),
 'C1':dict(h=2,g=0,mult={'kleider':0.5}),'C2':dict(h=2,g=0,mult={'elek':0.67}),'C3':dict(h=1,g=0,mult={'stream':0.5}),
 'N7':dict(h=1,g=0,mult={'milch':0.5},excl=['N3']),'N8':dict(h=1,g=-1,mult={'ernrest':0.9}),
 'C4':dict(h=3,g=-2,mult={k:0.7 for k in KON}),'C5':dict(h=1,g=0,mult={k:0.9 for k in KON}),'C6':dict(h=1,g=0,mult={'recyc':0.0}),
}
VORL={'K1':(.14,{'auto':1/3}),'K6':(.18,{'flug':0.9}),'K9':(.18,{'auto':0.6}),'K3':(.22,{'heiz':0.1}),
 'K4':(.24,{'strom':0.5}),'K8':(.12,{'heiz':0.9,'bau':0.9,'moebel':0.9}),'K7':(.26,{'kette':0.0}),'K10':(.18,{'kantine':0.0}),
 'K2':(.20,{'lkw':0.0}),'K5':(.22,{'ind':0.0}),'K15':(.24,{'repar':0.0}),'K11':(.20,{'oeffbesch':0.0}),'K12':(.20,{}),  # Moorboeden: Wirkung im Code (MOOR, nach dem Trend), 21.11.2026
 'K17':(.18,{'oeff':0.85}),
 'K16':(.16,{k:0.75 for k in GREY})}
FIG={
 'Daniel':dict(mod={},ban=['W2b','I7'],life='43, so alt wie die Schweiz im Mittel. Wohnt mit Partnerin und zwei Kindern im eigenen Reihenhaus in der Agglomeration, hat ein Auto und arbeitet im Büro. Entscheidet bei allem mit, auch bei Heizung und Haus.'),
 'Lia':dict(mod={'I1a':1,'I2':-1,'I4':-1},ban=['W2','W3','I7'],life='25, wohnt in einer WG in Zürich, ÖV vor der Tür, fährt aber noch das alte Auto ihrer Eltern. Reist für ihr Leben gern. Mieterin: über die Heizung entscheidet die Vermieterin.'),
 'Noah':dict(mod={'I2':1,'I4':1,'I6':1,'N1':1,'N2':1},ban=['W2','W3','W4','N3','I7'],life='25, Lehrabschluss, wohnt bei den Eltern im Einfamilienhaus auf dem Land, der Bus fährt stündlich, isst gern Fleisch.'),
 'Ruth':dict(mod={'W4':1,'I1b':-1},ban=['W2b','I7'],life='70, pensioniert, wohnt allein im eigenen Haus. Hat Ersparnisse, zieht aber ungern um.'),
 'Elif':dict(mod={'C1':-1,'C2':-1,'C3':-1,'C4':-1,'C5':-1,'C6':-1},ban=['W2','W3','W4','I2','I3','I4','I6'],life='17, Gymnasiastin, wohnt mit Eltern und Bruder in einer Mietwohnung, wenig eigenes Geld. Über Auto und Heizung entscheiden die Eltern.'),
}
SYN={'K9':{'h':['I2','I4','I7']},'K10':{'h':['N2']},'K15':{'h':['C2']},'K6':{'h':['I1a','I1b']},'K3':{'g':['W2'],'h':['W2b']},'K1':{'g':['I3']}}
VCH={}  # Schweiz-Wirkung in Mio. t/Jahr, wenn die Vorlage nicht auf den persoenlichen Fussabdruck wirkt (ZHAW 2020)
START={'Daniel':2,'Lia':1,'Noah':2,'Ruth':3,'Elif':2}
INC={'Daniel':[1],'Lia':[1],'Noah':[2],'Ruth':[1],'Elif':[0,1]}  # Startgeld vom Ausgleich 20.11.2026 (Ruth 3 + 1 = 4 in Runde 1, reicht fuer W2): Noah verdient nach der Lehre, Ruth lebt von der Rente, Elif hat fuer Kanada gespart
json.dump(dict(START=START,INC=INC,BASE=BASE,CAT=CAT,CARDS=CARDS,VORL={k:dict(c=c,mult=m,**({'ch':VCH[k]} if k in VCH else {})) for k,(c,m) in VORL.items()},FIG=FIG,SYN=SYN),open('mech.json','w'),ensure_ascii=False)
print('ok')
