"""Erste Runde zum Mitmachen und Dorf ohne Scrollen (Review 26.11.2026)."""
from conftest import URL

def _seite(browser, **ctx):
    c = browser.new_context(**({"viewport": {"width": 1280, "height": 720}} | ctx))
    p = c.new_page()
    p.route("**/*firebase*/**", lambda r: r.abort())
    p.route("**/*googleapis*/**", lambda r: r.abort())
    p.add_init_script("localStorage.setItem('13t_aktiv',String(Date.now()));")
    p.goto(URL + "?spiel=4A")
    p.wait_for_timeout(400)
    p.evaluate("if(S.screen==='intro')introDone(false)")
    return c, p

def test_erste_runde_zum_mitmachen(browser):
    c, p = _seite(browser)
    p.evaluate("()=>startFig('Noah')")
    p.wait_for_timeout(300)
    p.click("#coachbox >> text=Weiter")
    p.wait_for_timeout(300)
    assert p.evaluate("S.coach") == 1
    assert p.query_selector("#coachbox >> text=Weiter") is None  # Schritt mit Aufgabe: kein Weiter
    try:  # ausserhalb der Karten ist gesperrt
        p.click("#finish", timeout=800)
        assert False, "Abstimmen war waehrend der Anleitung klickbar"
    except Exception as e:
        assert "Abstimmen war" not in str(e)
    p.click(".card >> text=Wählen >> nth=0")
    p.wait_for_timeout(300)
    assert p.evaluate("S.coach") == 2
    p.click("#panel >> button:has-text('+') >> nth=0")
    p.wait_for_timeout(300)
    assert p.evaluate("S.coach") == 3
    p.click("#finish")
    p.wait_for_timeout(300)
    assert p.evaluate("S.coach") is None and p.evaluate("localStorage.getItem('13t_tut')") == "1"
    c.close()

def test_dorf_ohne_scrollen_am_computer(browser):
    for w, h, dpr in [(1920, 1080, 1), (1440, 790, 2), (1366, 768, 1)]:
        c, p = _seite(browser, viewport={"width": w, "height": h}, device_scale_factor=dpr, reduced_motion="reduce")
        p.evaluate("()=>{localStorage.setItem('13t_tut','1');startFig('Noah');S.coach=null;S.crisisSeen=S.r;for(const id of S.hand)if(!blocked(id))choose(id);vote(true);document.querySelector('.vov').remove();toEvent();}")
        p.wait_for_timeout(300)
        if p.evaluate("S.screen") != "dorf":
            p.evaluate("()=>startDorf()")
        p.wait_for_timeout(800)
        assert p.evaluate("S.screen") == "dorf"
        ueber = p.evaluate("document.documentElement.scrollHeight-innerHeight")
        assert ueber <= 2, f"{w}x{h}@{dpr}: {ueber} px zum Scrollen"
        c.close()

def test_ton_zu_beginn_aus_und_schaltbar(browser):
    c, p = _seite(browser)
    p.evaluate("localStorage.setItem('13t_tut','1')")
    assert "Ton aus" in p.inner_text(".tonbtn") and p.evaluate("TONCTX") is None
    p.click(".tonbtn")
    p.wait_for_function("Object.keys(TONBUF).length===Object.keys(TON).length", timeout=5000)
    assert "Ton an" in p.inner_text(".tonbtn")
    p.reload()
    p.wait_for_timeout(400)
    assert p.evaluate("lsGet('13t_ton')") == "1"  # Schalter bleibt gespeichert
    c.close()
