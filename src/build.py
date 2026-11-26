"""Baut index.html aus src/ (Code, Texte, Zahlen) und grafik/ (privates Submodul mit den Grafiken).

  python src/build.py          index.html neu schreiben
  python src/build.py --check  nur pruefen, ob index.html zum Quellcode passt (Exit 1, wenn nicht)

Der Ordner mit den Grafiken kann mit der Umgebungsvariable GRAFIK_DIR ueberschrieben werden.
"""
import base64, io, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
GRAFIK = pathlib.Path(os.environ.get("GRAFIK_DIR") or ROOT / "grafik")

def lies(p):
    return pathlib.Path(p).read_text(encoding="utf-8")

def dorf_snippet():
    """Stil und Skript fuer das Dorfband (frueher dorf_snippet.py im Hub)."""
    d = GRAFIK / "dorf"
    b64 = lambda f: "data:image/png;base64," + base64.b64encode((d / f).read_bytes()).decode()
    J = json.loads(lies(d / "dorf5.json")); A = json.loads(lies(d / "dorf4_anim_farbe.json")); EXT = json.loads(lies(d / "dorf_extras.json"))
    W, H = J["W"], J["H"]
    DATA = {"W": W, "H": H, "sail": J["sail"], "coops": J["coops"], "walkers": A["walkers"], "chicken": A["chicken"], "butterfly": A["butterfly"], "duck": A["duck"],
            "water": J["water"], "ducks": J["ducks"], "clouds": A["clouds"], "npcs": A["npcs"], "band": J["band"], "doors": J["doors"], "plazas": J["plazas"], "stalls": J["stalls"],
            "smoke": J["smoke"], "smokeimg": A["smoke"], "sailimg": b64("dorf4_sail_farbe.png"), "base": b64("dorf5_basis_grau.png"), "baseF": b64("dorf5_basis_farbe.png"),
            "atlasimg": b64("dorf5_atlas_farbe.png"), "atlas": J["atlas"], "occl": J["occl"], "wasser": b64("dorf5_wasser_farbe.png"), "ext": EXT,
            "figsets": A.get("figsets", {}), "figsetsF": A.get("figsetsF", {}), "extimg": b64("dorf_extras_farbe.png"), "anim": J["anim"], "anims": J["anims"],
            "herd": J["herd"], "swans": J["swans"], "animimg": b64("dorf5_anim_farbe.png")}
    css = lies(SRC / "dorf_style.css").replace("__H__", str(H))
    js = lies(SRC / "dorf_anim.js").replace("__DATA__", json.dumps(DATA))
    return "<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>\n"

def webp(html):
    """Eingebettete PNG als verlustfreies WebP: gleiche Pixel, rund ein Drittel der Bytes (26.11.2026: 1.11 MB -> 0.36 MB).
    Nur wenn kleiner. Pillow ist in tests/requirements.txt fest auf eine Version gesetzt, damit --check ueberall gleich baut."""
    from PIL import Image
    def neu(m):
        raw = base64.b64decode(m.group(1))
        o = io.BytesIO(); Image.open(io.BytesIO(raw)).save(o, "WEBP", lossless=True, exact=True, method=6)
        w = o.getvalue()
        return "data:image/webp;base64," + base64.b64encode(w).decode() if len(w) < len(raw) else m.group(0)
    return re.sub(r"data:image/png;base64,([A-Za-z0-9+/=]+)", neu, html)

def toene():
    """Kurze Toene (src/ton/*.mp3, CC0) als data-URL fuer das Objekt TON."""
    return json.dumps({f.stem: "data:audio/mpeg;base64," + base64.b64encode(f.read_bytes()).decode() for f in sorted((SRC / "ton").glob("*.mp3"))})

def baue():
    if not (GRAFIK / "sprites.json").exists():
        sys.exit("Grafiken fehlen: git submodule update --init (Zugriff auf das private Repo thjoo/13-tonnen-grafik noetig)")
    subprocess.run([sys.executable, str(SRC / "mech.py")], check=True, cwd=SRC, stdout=subprocess.DEVNULL)
    t = lies(SRC / "template.html")
    for k, v in [("__FONTS__", lies(SRC / "fonts.css")), ("__TEXTS__", lies(SRC / "texts.json")), ("__MECH__", lies(SRC / "mech.json")),
                 ("__SPR__", lies(GRAFIK / "sprites.json")), ("__DORF__", dorf_snippet()), ("__TON__", toene()), ("__MUSIK__", lies(ROOT / "musik" / "musik.json"))]:
        t = t.replace(k, v)
    return webp(t)

if __name__ == "__main__":
    html = baue()
    ziel = ROOT / "index.html"
    if "--check" in sys.argv:
        if not ziel.exists() or ziel.read_text(encoding="utf-8") != html:
            sys.exit("index.html passt nicht zum Quellcode: python src/build.py ausfuehren und index.html mitcommitten")
        print("index.html passt zum Quellcode")
    else:
        ziel.write_text(html, encoding="utf-8")
        print("index.html gebaut,", len(html.encode()), "Bytes")
