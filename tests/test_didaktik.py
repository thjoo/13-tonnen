"""Didaktische Pruefung 26.11.2026: Vorhersage vor der Bilanz, Hinweise, Punkte fuer die Wirkung auf die Schweiz."""
from conftest import URL

def _seite(browser):
    c = browser.new_context(viewport={"width": 1280, "height": 800}, reduced_motion="reduce")
    p = c.new_page()
    fehler = []
    p.on("pageerror", lambda e: fehler.append(str(e)))
    p.route("**/*firebase*/**", lambda r: r.abort())
    p.route("**/*googleapis*/**", lambda r: r.abort())
    p.add_init_script("localStorage.setItem('13t_aktiv',String(Date.now()));localStorage.setItem('13t_tut','1');localStorage.setItem('13t_ton','0');")
    p.goto(URL + "?spiel=4A")
    p.wait_for_timeout(400)
    p.evaluate("if(S.screen==='intro')introDone(false)")
    return c, p, fehler

# Eine Runde nur mit Karten spielen, ohne Herz fuer Vorlagen, bis zur Bilanz
RUNDE = """()=>{S.crisisSeen=S.r;for(const id of S.hand)if(!blocked(id))choose(id);vote(true);document.querySelector(".vov").remove();toEvent();
  S.screen="summary";render();}"""

def test_vorhersage_vor_der_bilanz(browser):
    c, p, fehler = _seite(browser)
    p.evaluate("()=>startFig('Ruth')")
    p.evaluate(RUNDE)
    assert p.is_visible("text=Was schätzt du") and p.query_selector(".evbox ~ .ibox svg.chart") is None
    titel = p.inner_text(".btitle")
    assert "Am meisten" not in titel  # die Antwort steht erst nach der Schaetzung da
    p.click(".guess button >> nth=2")
    assert p.query_selector("text=Was schätzt du") is None
    assert p.is_visible(".chart") and "Am meisten" in p.inner_text(".btitle")
    assert p.evaluate("S.guess[0]") == "Du"
    assert not fehler
    c.close()

def test_hinweis_ohne_vorlagen_und_punkte_fuer_die_schweiz(browser):
    c, p, fehler = _seite(browser)
    p.evaluate("()=>startFig('Lia')")
    for _ in range(2):
        p.evaluate(RUNDE)
        p.evaluate("nextRound()")
    assert p.evaluate("S.r") == 2
    assert any("noch kein Herz für eine Vorlage" in x for x in p.evaluate("S.roundNote"))
    # Punkte: die Wirkung der Vorlagen auf die Schweiz zaehlt mit 20 Punkten pro Mio. t
    s = p.evaluate("()=>{S.adopted={K2:2030,K7:2035};const o=scoreNow();return [o.s,scoreOf(o).S]}")
    assert s[0] > 0 and s[1] == round(s[0] * 20)
    assert not fehler
    c.close()
