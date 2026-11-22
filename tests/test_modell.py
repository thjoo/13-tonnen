"""Rechenmodell und Spielregeln, direkt im Spiel ausgefuehrt (ohne Klicks)."""

def test_start_und_trend(spiel):
    page, fehler = spiel()
    r = page.evaluate("""()=>{fresh();S.fig='Elif';return {start:+val(2026,NO).toFixed(2),trend2050:+val(2050,NO).toFixed(2),summe:Math.round(sum(2026,2050,NO))}}""")
    assert r["start"] == 12.8
    assert 10.5 <= r["trend2050"] <= 11.2      # Zahlentabelle 3b: rund 10.9 t
    assert 285 <= r["summe"] <= 300             # Zahlentabelle 3b: rund 294 t
    assert not fehler

def test_heizung_mit_k3_wird_waermepumpe(spiel):
    page, fehler = spiel()
    r = page.evaluate("""()=>{const o={};
      fresh();startFig('Lia');S.adopted.K3=2030;S.r=1;S.nextEvent='E2m';S.ballot=[];S.results=[];S.log=[{}];toEvent();o.lia=[S.e2mRes,hasWP()];
      fresh();startFig('Daniel');S.adopted.K3=2030;S.r=1;S.nextEvent='E2';S.ballot=[];S.results=[];S.log=[{}];toEvent();o.daniel=[S.e2Res,hasWP(),!!S.flags.w2locked,oilHeat()];
      fresh();startFig('Ruth');S.r=1;S.nextEvent='E2';S.ballot=[];S.results=[];S.log=[{}];toEvent();S.r=2;nextRound();o.ruth=[!!S.flags.w2locked,oilHeat()];
      return o}""")
    assert r["lia"] == ["wp", True]
    assert r["daniel"] == ["wp", True, False, False]   # keine Sperre, kein Oel mehr
    assert r["ruth"] == [True, True]                   # ohne K3: Karte gesperrt, Oel bleibt
    assert not fehler

def test_heizung_geht_sicher_einmal_kaputt(spiel):
    page, _ = spiel()
    n = page.evaluate("""()=>{let n=0;for(let i=0;i<100;i++){startFig('Noah');S.r=LAST-1;announceEvent();if(S.nextEvent==='E2m')n++;}return n}""")
    assert n == 100

def test_abstimmung_volks_und_staendemehr(spiel):
    page, _ = spiel()
    r = page.evaluate("""()=>{startFig('Daniel');S.r=1;const o={initMin:99,split:0,abgelehnt:0,falsch:0,staende:23};
      for(let i=0;i<3000;i++){const k=['K9','K12','K3','K16'][i%4],c=10+(i*37)%85,roll=(i*53)%100,ok=roll<c,u=urne({k,c,roll,ok});
        if(TYP[k]&&ok)o.initMin=Math.min(o.initMin,u.st);
        if(TYP[k]&&!ok){o.abgelehnt++;if(u.split)o.split++;if(u.st>=12&&u.ja>50)o.falsch++;}
        if(ok&&!TYP[k]&&u.ja<=50)o.falsch++;}
      o.staende=KT.reduce((s,[c])=>s+(HALB.has(c)?0.5:1),0);return o}""")
    assert r["staende"] == 23
    assert r["initMin"] >= 12          # angenommene Initiative hat immer das Staendemehr
    assert r["falsch"] == 0
    assert r["split"] / r["abgelehnt"] < 0.15   # «Volk Ja, Staende Nein» bleibt selten

def test_schrittweise_einfuehrung(spiel):
    page, _ = spiel()
    r = page.evaluate("""()=>{startFig('Elif');const d=k=>{S.adopted={[k]:2030};return val(2030,NO)-val(2030,ACT)};const e=k=>{S.adopted={[k]:2030};return val(2050,NO)-val(2050,ACT)};
      return {k16_2030:d('K16'),k16_2050:e('K16'),k11_2030:d('K11'),k11_2050:e('K11'),k12_2050:e('K12')}}""")
    # im ersten Jahr wirkt nur ein Zehntel (K16) bzw. ein Fuenfzehntel (K11)
    assert r["k16_2030"] < 0.2 * r["k16_2050"] and r["k16_2050"] > 0.8
    assert r["k11_2030"] < 0.1 * r["k11_2050"]
    assert 0.02 <= r["k12_2050"] <= 0.04       # Moorboeden rund 0.03 t

def test_stufe1_braucht_eigenen_beitrag(spiel):
    page, _ = spiel()
    r = page.evaluate("""()=>{startFig('Elif');S.adopted={K7:2030};return stufenTop()}""")
    assert r == 0

def test_outro_texte(spiel):
    page, _ = spiel()
    t = page.evaluate("""()=>{startFig('Ruth');S.chosen={W2:2026};S.adopted={K3:2030};return outroTexts()}""")
    assert len(t) == 3
    for s in t:
        assert "NaN" not in s and "undefined" not in s and len(s) < 260
