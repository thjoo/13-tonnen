"""Erste Runde zum Mitmachen und Dorf ohne Scrollen (Review 26.11.2026)."""
import functools, http.server, pathlib, threading
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

def test_ton_und_musik(browser):
    """Ton und Musik sind zu Beginn an, starten erst nach der ersten Beruehrung, laufen als Schleife und lassen sich in drei Stufen schalten."""
    root = pathlib.Path(__file__).resolve().parent.parent
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Still, directory=str(root)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    c = browser.new_context(viewport={"width": 1280, "height": 720})
    p = c.new_page()
    p.route("**/*firebase*/**", lambda r: r.abort())
    p.route("**/*googleapis*/**", lambda r: r.abort())
    p.add_init_script("localStorage.setItem('13t_aktiv',String(Date.now()));localStorage.setItem('13t_tut','1');")
    p.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html")
    p.wait_for_timeout(400)
    p.evaluate("if(S.screen==='intro')introDone(false)")
    assert "Musik und Ton" in p.inner_text(".tonbtn") and p.evaluate("TONCTX") is None  # vor der ersten Beruehrung still
    p.mouse.click(5, 5)
    p.wait_for_function("MUSJETZT==='dorf'", timeout=8000)
    p.wait_for_function("Object.keys(TONBUF).length===Object.keys(TON).length", timeout=5000)
    schleife = p.evaluate("[MUSQ.loop,MUSQ.loopEnd-MUSQ.loopStart,MUSIK.dorf.n/44100]")
    assert schleife[0] and abs(schleife[1] - schleife[2]) < 0.01
    assert p.evaluate("TONVAR.waehlen.length") == 3  # Varianten
    p.evaluate("()=>startFig('Noah')")
    p.wait_for_function("MUSJETZT==='runde1'", timeout=8000)
    p.click(".actbar .tonbtn")
    assert "Nur Ton" in p.inner_text(".actbar .tonbtn") and p.evaluate("MUSJETZT") is None
    p.click(".actbar .tonbtn")
    assert "Ton aus" in p.inner_text(".actbar .tonbtn")
    p.reload()
    p.wait_for_timeout(400)
    assert p.evaluate("[lsGet('13t_ton'),tonStufe()]") == ["0", 0]  # Schalter bleibt gespeichert
    p.click(".tonbtn")
    assert p.evaluate("tonStufe()") == 2
    c.close()
    srv.shutdown()

class _Still(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass
