"""Barrierefreiheit: automatische Pruefung (axe-core, WCAG 2.1 AA) und Tastatur."""
import pathlib, pytest

AXE = pathlib.Path(__file__).resolve().parent / "node_modules" / "axe-core" / "axe.min.js"
BILDSCHIRME = {
    "start": "S.screen='start';S.startMode=null;render()",
    "figurwahl": "S.screen='start';S.startMode='solo';render()",
    "runde": "startFig('Lia');S.crisisSeen=0;render()",
    "bilanz": "startFig('Ruth');S.chosen.W2=2026;S.r=1;S.snap[1]={y:2030,act:val(2030,ACT),c:bycat(subs(2030,ACT))};S.event='ruhig';S.screen='summary';render()",
    "ende": "startFig('Elif');S.adopted={K7:2030};S.r=3;S.outroSeen=true;S.screen='end';render()",
}

@pytest.mark.skipif(not AXE.exists(), reason="axe-core fehlt: npm install axe-core@4 --prefix tests")
@pytest.mark.parametrize("geraet", ["laptop", "handy"])
@pytest.mark.parametrize("name", list(BILDSCHIRME))
def test_axe(spiel, geraet, name):
    page, _ = spiel(geraet)
    page.evaluate("()=>{" + BILDSCHIRME[name] + "}")
    page.wait_for_timeout(500)
    page.add_script_tag(content=AXE.read_text())
    v = page.evaluate("async()=>(await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(x=>x.id+': '+x.nodes.length)")
    assert v == []

def test_tastatur_fokus_bleibt(spiel):
    page, _ = spiel()
    page.evaluate("()=>{S.startMode='solo';render()}")
    for _ in range(60):
        page.keyboard.press("Tab")
        if page.evaluate("()=>document.activeElement.classList.contains('fig')&&document.activeElement.innerText.includes('Lia')"):
            break
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    assert page.evaluate("()=>S.screen") == "round"
    page.evaluate("()=>{S.crisisSeen=S.r;render()}")
    for _ in range(80):
        page.keyboard.press("Tab")
        if page.evaluate("()=>(document.activeElement.innerText||'').trim()==='Wählen'"):
            break
    page.keyboard.press("Enter")
    page.wait_for_timeout(200)
    assert page.evaluate("()=>S.thisRound.length") == 1
    assert page.evaluate("()=>document.activeElement!==document.body")
