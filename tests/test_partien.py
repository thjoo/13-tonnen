"""Ganze Partien: mit allen Figuren und zufaellig ueber die Knoepfe, auf Laptop, iPad und Handy."""
import json, random, pytest

PRUEFEN = """()=>{const e=[];const v=val(PER[S.r].a,ACT);if(!(v>=0&&v<=13.5))e.push('Fussabdruck '+v);
 if(S.money<0)e.push('Geld '+S.money);if(freeH()<0)e.push('Herzen '+freeH());
 const t=document.body.innerText;const m=t.match(/.{20}(NaN|undefined|\\[object).{20}/);if(m)e.push('Text: '+m[0]);
 if(document.documentElement.scrollWidth>innerWidth+2)e.push('seitlich scrollbar');return e}"""

@pytest.mark.parametrize("geraet", ["laptop", "handy"])
def test_alle_figuren_ganze_partie(spiel, geraet):
    page, fehler = spiel(geraet)
    r = page.evaluate("""async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms)),out=[];
     for(const f of ['Daniel','Lia','Noah','Ruth','Elif']){fresh();render();startFig(f);
      for(let r=0;r<=LAST;r++){S.crisisSeen=S.r;render();for(const id of S.hand)if(!blocked(id))choose(id);
       for(const k of S.ballot)if(freeH()>0)alloc(k,1);vote(true);await w(20);const g=document.querySelector('#vgo');if(g)g.click();await w(20);
       if(S.screen==='dorf')toSummary();if(S.screen!=='summary')out.push(f+' Runde '+r+': '+S.screen);nextRound();await w(5);}
      if(S.screen==='dorf')toEnd();if(typeof outroEnd==='function'&&S.outro)outroEnd();if(S.screen!=='end')out.push(f+' Ende: '+S.screen);}
     return out}""")
    assert r == []
    assert not fehler

def _spielen(page, rnd, figur, modus):
    page.evaluate(f"()=>{{S.startMode='solo';setMode('{modus}');S.mode='{modus}';render()}}")
    page.click(f".fig:has(h3:text-is('{figur}'))")
    probleme = []
    for _ in range(400):
        st = page.evaluate("()=>({scr:S.screen,r:S.r,coach:S.coach,krise:!!document.querySelector('#crisisBig'),vov:!!document.querySelector('.vov'),outro:!!document.querySelector('.ovl.outro'),frage:!!document.querySelector('#finish2'),res:!!S.results})")
        if st["outro"]:
            page.evaluate("()=>{if(window.dorfSkipWalk)window.dorfSkipWalk();outroNext()}"); page.wait_for_timeout(100); continue
        if st["scr"] == "end":
            return probleme, page.evaluate("()=>+val(2050,ACT).toFixed(2)")
        probleme += [f"Runde {st['r']} {st['scr']}: {x}" for x in page.evaluate(PRUEFEN)]
        if st["coach"] is not None: page.evaluate("()=>coachEnd()"); continue
        if st["krise"]: page.click("#crisisBig button.primary"); continue
        if st["vov"]:
            g, k = page.query_selector("#vgo"), page.query_selector("#vskip")
            if g and g.is_visible(): g.click()
            elif k and k.is_visible(): k.click()
            else: page.wait_for_timeout(300)
            continue
        if st["frage"]: page.click("#finish2"); continue
        if st["scr"] == "round" and not st["res"]:
            for _ in range(rnd.randint(0, 4)):
                bs = [b for b in page.query_selector_all(".card .ft button:not([disabled])") if b.inner_text().strip() == "Wählen"]
                if bs: rnd.choice(bs).click()
            for _ in range(rnd.randint(0, 3)):
                ps = [b for b in page.query_selector_all(".ctl button.small:not([disabled])") if b.inner_text().strip() == "+"]
                if ps: rnd.choice(ps).click()
            page.click("#finish"); continue
        b = page.query_selector(".actbar button.primary")
        if not b:
            probleme.append(f"kein Knopf auf {st['scr']}"); break
        b.click(); page.wait_for_timeout(150)
    return probleme + ["Partie haengt"], None

@pytest.mark.parametrize("seed", range(9))
def test_zufallspartie(spiel, seed):
    geraet = ["laptop", "ipad", "handy"][seed % 3]
    page, fehler = spiel(geraet, tutorial=(seed % 3 == 0))
    rnd = random.Random(seed)
    probleme, ende = _spielen(page, rnd, ["Daniel", "Lia", "Noah", "Ruth", "Elif"][seed % 5], "lang" if seed % 4 == 0 else "kurz")
    assert probleme == [], probleme[:5]
    assert ende is not None and 3 < ende < 13
    assert not fehler


def test_intro_mit_20_minuten_pause(browser):
    """Intro beim ersten Oeffnen; nach Neuladen innert 20 Minuten nicht; nach mehr als 20 Minuten Pause wieder."""
    from conftest import URL
    ctx = browser.new_context(reduced_motion="reduce")
    page = ctx.new_page()
    page.route("**/*firebase*/**", lambda r: r.abort())
    page.route("**/*googleapis*/**", lambda r: r.abort())
    page.goto(URL)
    page.wait_for_timeout(400)
    assert page.evaluate("S.screen") == "intro"
    page.click("text=Überspringen")
    page.wait_for_timeout(300)
    assert page.evaluate("S.screen") == "start"
    page.reload()
    page.wait_for_timeout(400)
    assert page.evaluate("S.screen") == "start"
    page.evaluate("localStorage.setItem('13t_aktiv', String(Date.now() - 21*60*1000))")
    page.reload()
    page.wait_for_timeout(400)
    assert page.evaluate("S.screen") == "intro"
    ctx.close()


def test_anleitung_nach_pause(browser):
    """Nach mehr als 20 Minuten Pause kommen Intro und Anleitung wieder, auch wenn die Anleitung schon einmal lief."""
    from conftest import URL, GERAETE
    ctx = browser.new_context(**GERAETE["handy"], reduced_motion="reduce")
    page = ctx.new_page()
    page.route("**/*firebase*/**", lambda r: r.abort())
    page.route("**/*googleapis*/**", lambda r: r.abort())
    page.goto(URL)
    page.evaluate("localStorage.setItem('13t_tut','1');localStorage.setItem('13t_aktiv',String(Date.now()-21*60*1000))")
    page.reload()
    page.wait_for_timeout(400)
    page.evaluate("introDone(false)")
    page.evaluate("()=>{S.startMode='solo';render()}")
    page.click(".fig:has(h3:text-is('Daniel'))")
    assert page.evaluate("S.coach") == 0
    ctx.close()
