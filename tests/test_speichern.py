"""Spielstand, Fehlerkarte und Spielnummer: Neuladen verliert nichts, Fehler frieren nicht ein, gleiche Nummer gleiche Lose."""
from conftest import URL

def _oeffnen(browser, url=URL):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, reduced_motion="reduce")
    page = ctx.new_page()
    page.route("**/*firebase*/**", lambda r: r.abort())
    page.route("**/*googleapis*/**", lambda r: r.abort())
    page.add_init_script("localStorage.setItem('13t_aktiv',String(Date.now()));localStorage.setItem('13t_tut','1');")
    page.goto(url)
    page.wait_for_timeout(400)
    page.evaluate("if(S.screen==='intro')introDone(false)")
    return ctx, page

# Abstimmen ohne auf die Auszaehlung zu warten: Animation schliessen und wie «Weiter» das Ereignis ausloesen
ZWEI_RUNDEN = """()=>{startFig('Ruth');for(let r=0;r<2;r++){S.crisisSeen=S.r;for(const id of S.hand)if(!blocked(id))choose(id);vote(true);document.querySelector(".vov").remove();toEvent();nextRound();}
  S.crisisSeen=S.r;render();return {r:S.r,fig:S.fig,chosen:JSON.stringify(S.chosen),seed:S.seed}}"""

def test_allein_weiterspielen_nach_neuladen(browser):
    ctx, page = _oeffnen(browser)
    vorher = page.evaluate(ZWEI_RUNDEN)
    assert vorher["r"] == 2
    page.reload()
    page.wait_for_timeout(400)
    assert page.evaluate("S.screen") == "start" and page.evaluate("S.fig") is None
    page.click("text=Weiterspielen")
    page.wait_for_timeout(200)
    nachher = page.evaluate("()=>({r:S.r,fig:S.fig,chosen:JSON.stringify(S.chosen),seed:S.seed,screen:S.screen})")
    assert nachher.pop("screen") == "round"
    assert nachher == vorher
    # Neues Spiel loescht den Stand
    page.evaluate("()=>{S.r=LAST;S.outroSeen=true;S.screen='end';render()}")
    page.click("text=Neues Spiel")
    page.reload()
    page.wait_for_timeout(400)
    assert page.query_selector("text=Weiterspielen") is None
    ctx.close()

def test_fehlerkarte_statt_stillstand(browser):
    ctx, page = _oeffnen(browser)
    page.evaluate(ZWEI_RUNDEN)
    page.evaluate("()=>setTimeout(()=>{throw new Error('Test-Fehler')},0)")
    page.wait_for_timeout(200)
    assert page.is_visible("#crash")
    assert "Test-Fehler" in page.text_content("#crash pre")
    with page.expect_navigation(wait_until="load"):
        page.get_by_role("button", name="Neu laden", exact=True).click()
    zustand = "()=>({screen:S.screen,save:!!localStorage.getItem('13t_solo'),knoepfe:[...document.querySelectorAll('button')].map(b=>b.textContent.trim()).slice(0,8)})"
    try:
        page.wait_for_function("typeof S!=='undefined'&&S.screen==='start'", timeout=10000)
        page.get_by_role("button", name="Weiterspielen", exact=True).click(timeout=10000)
    except Exception as e:
        raise AssertionError(f"nach dem Neuladen: {page.evaluate(zustand)}") from e
    assert page.evaluate("S.r") == 2
    ctx.close()

def test_gleiche_spielnummer_gleiche_lose(browser):
    ergebnisse = []
    for _ in range(2):
        ctx, page = _oeffnen(browser, URL + "?spiel=4a")
        ergebnisse.append(page.evaluate("""()=>{startFig('Lia');const o=[];for(let r=0;r<=LAST;r++){S.crisisSeen=S.r;o.push(S.hand.join(),S.ballot.join(),S.nextEvent);
          vote(true);o.push(S.results.map(x=>x.roll).join());document.querySelector(".vov").remove();toEvent();o.push(S.event);nextRound();}return {seed:S.seed,o}}"""))
        ctx.close()
    assert ergebnisse[0]["seed"] == "4A"
    assert ergebnisse[0] == ergebnisse[1]
    ctx, page = _oeffnen(browser)
    andere = page.evaluate("()=>{startFig('Lia');return S.seed}")
    ctx.close()
    assert andere != "4A"
