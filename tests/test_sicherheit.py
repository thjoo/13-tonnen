"""Daten aus der Datenbank duerfen keinen Code ins Spiel einschleusen."""

BOESE = '<img src=x onerror="window.__xss=1">'


def test_bereinigen(spiel):
    page, _ = spiel("laptop")
    sauber = page.evaluate("v=>CL(v)", {"s": BOESE, "<b>": 1, "liste": [BOESE], "n": 5})
    assert sauber == {"s": "img src=x onerror=window.__xss=1", "liste": ["img src=x onerror=window.__xss=1"], "n": 5}


def test_bestenliste_ohne_code(spiel):
    page, fehler = spiel("laptop")
    page.evaluate("""b=>{loadBoard=()=>{};S.boardN=1;S.boardMode='kurz';S.screen='board';
      BOARD={key:boardKey(1,'kurz'),rows:[CL({id:'x',kz:b,figs:b,kl:b,b:b,e:1,g:1,s:b,at:Date.now()})],err:null};render()}""", BOESE)
    page.wait_for_timeout(300)
    assert not page.evaluate("!!window.__xss")
    assert not page.query_selector("table.board img")
    assert not fehler


def test_lehrpersonen_ohne_code(spiel):
    page, fehler = spiel("laptop")
    page.evaluate("""b=>{S.screen='teacher';TROOMS=CL({ABCDE:{createdAt:Date.now(),klasse:b,mode:'kurz',status:'play',
      players:{u1:{fig:b,end:{v:1,sum:2}}},stage:{0:{res:[{k:b,ok:true}]}}}});render()}""", BOESE)
    page.wait_for_timeout(300)
    assert not page.evaluate("!!window.__xss")
    assert not fehler
