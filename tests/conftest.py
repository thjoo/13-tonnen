"""Gemeinsame Hilfen fuer die Tests von «13 Tonnen».

Getestet wird die gebaute Datei index.html im Hauptordner des Repos (oder die Adresse in GAME_URL).
Firebase wird in allen automatischen Tests blockiert: Es entstehen keine Raeume.
"""
import os, pathlib, pytest
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = os.environ.get("GAME_URL") or (ROOT / "index.html").as_uri()
GERAETE = {
    "laptop": dict(viewport={"width": 1440, "height": 900}),
    "ipad": dict(viewport={"width": 820, "height": 1180}, is_mobile=True, has_touch=True),
    "handy": dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True),
}

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("CHROME_PATH"):
            kw["executable_path"] = os.environ["CHROME_PATH"]
        b = p.chromium.launch(**kw)
        yield b
        b.close()

@pytest.fixture
def spiel(browser):
    """Oeffnet das Spiel auf einem Geraet. Gibt (page, fehler) zurueck; fehler sammelt JavaScript-Fehler."""
    offen = []
    def oeffnen(geraet="laptop", tutorial=False, bewegung=False):
        ctx = browser.new_context(**GERAETE[geraet], reduced_motion="no-preference" if bewegung else "reduce")
        page = ctx.new_page()
        fehler = []
        page.on("pageerror", lambda e: fehler.append(str(e)))
        page.route("**/*firebase*/**", lambda r: r.abort())
        page.route("**/*googleapis*/**", lambda r: r.abort())
        init = "localStorage.setItem('13t_aktiv',String(Date.now()));"
        if not tutorial:
            init += "localStorage.setItem('13t_tut','1');"
        page.add_init_script(init)
        page.goto(URL)
        page.wait_for_timeout(400)
        # Das Intro laeuft bei jedem Oeffnen; fuer die Tests direkt zur Startseite
        page.evaluate("if(S.screen==='intro')introDone(false)")
        offen.append(ctx)
        return page, fehler
    yield oeffnen
    for c in offen:
        c.close()
