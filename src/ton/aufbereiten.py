"""Macht aus den Kenney-Paketen und der Musik (alles CC0) die MP3 in src/ton/ und musik/. Nur noetig, wenn Toene neu gewaehlt werden.

  pip install soundfile lameenc numpy
  python src/ton/aufbereiten.py <Ordner mit den entpackten Kenney-Paketen> <Ordner mit der Musik>

Toene: mono, 44.1 kHz, Stille unter -50 dBFS vorne und hinten weg, Ende 10 ms ausblenden, Spitze auf -1 dBFS,
dann Lautstaerke pro Ton (TOENE), MP3 64 kb/s. Mehrere Dateien pro Ton werden zu name_1, name_2 ... (das Spiel waehlt zufaellig).
Musik: Stereo, 44.1 kHz, Stille am Ende weg, Spitze auf -1 dBFS, MP3 96 kb/s, nach musik/ (wird erst geladen, wenn Ton an ist).
musik/musik.json haelt pro Stueck die Laenge in Samples und das erste hoerbare Sample: Damit findet das Spiel die Schleife
genau, auch wenn der Browser den MP3-Vorlauf nicht abschneidet.
"""
import glob, json, pathlib, sys
import lameenc, numpy as np, soundfile as sf

HIER = pathlib.Path(__file__).resolve().parent
MUSIK = HIER.parent.parent / "musik"
# Name im Spiel: ([Dateien im Paket], Lautstaerke 0..1, hoechstens Sekunden)
TOENE = {
    "klick": (["click_002", "click_003"], 0.45, 0.2),
    "waehlen": (["card-place-1", "card-place-2", "card-place-3"], 0.8, 0.4),
    "zurueck": (["card-slide-1", "card-slide-2"], 0.7, 0.4),
    "herz": (["pluck_001", "pluck_002"], 0.6, 0.3),
    "herzweg": (["drop_001", "drop_002"], 0.5, 0.3),
    "nein": (["error_004"], 0.5, 0.3),
    "geld": (["handleCoins", "handleCoins2"], 0.6, 0.7),
    "glocke": (["impactBell_heavy_000", "impactBell_heavy_001"], 0.55, 1.6),
    "kanton": (["tick_002"], 0.25, 0.1),
    "ja": (["jingles_PIZZI02"], 0.85, 1.2),
    "nein_abst": (["jingles_PIZZI05"], 0.7, 0.8),
    "krise": (["bong_001", "impactMetal_heavy_002"], 0.8, 0.9),
    "chance": (["confirmation_002", "maximize_006"], 0.65, 0.6),
    "etappe": (["glass_001"], 0.55, 0.5),
    "schluss": (["jingles_PIZZI12"], 0.85, 1.2),
    "seite": (["bookFlip1", "bookFlip2", "bookFlip3"], 0.55, 0.5),
    "schritt": (["footstep_grass_000", "footstep_grass_001", "footstep_grass_002", "footstep_grass_003"], 0.45, 0.3),
    "figur": (["cloth1", "cloth2"], 0.6, 0.5),
    "bauen": (["impactPlank_medium_000", "impactPlank_medium_001", "impactPlank_medium_002"], 0.5, 0.4),
}
# Name im Spiel: Datei im Musik-Ordner
STUECKE = {
    "dorf": "Calm1 - A Place I Call Home",
    "runde1": "Calm3 - Peaceful Days",
    "runde2": "Calm5 - Summer Memories",
    "runde3": "Quaint Town - LOOPABLE",
    "abend": "Calm2 - Childhood Friends",
    "schluss": "Calm6 - Innocence",
}

def lies(quelle, name, mono=True):
    f = [p for p in glob.glob(f"{quelle}/**/*", recursive=True) if pathlib.Path(p).stem == name and p[-4:] in (".ogg", ".wav")]
    if not f:
        sys.exit(f"{name} fehlt in {quelle}")
    x, sr = sf.read(f[0], always_2d=True)
    if mono:
        x = x.mean(1, keepdims=True)
    if sr != 44100:
        t = np.arange(0, len(x) * 44100 // sr) * sr / 44100
        x = np.stack([np.interp(t, np.arange(len(x)), x[:, c]) for c in range(x.shape[1])], 1)
    return x

def mp3(x, kbs):
    e = lameenc.Encoder()
    e.set_bit_rate(kbs); e.set_in_sample_rate(44100); e.set_channels(x.shape[1]); e.set_quality(2)
    return e.encode((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()) + e.flush()

def ton(x, laut, maxs):
    s = np.flatnonzero(np.abs(x[:, 0]) > 10 ** (-50 / 20))
    x = x[s[0]:s[-1] + 1] if len(s) else x
    x = x[: int(maxs * 44100)].copy()
    f = min(len(x), 441)
    x[-f:] *= np.linspace(1, 0, f)[:, None]
    return mp3(x / (np.abs(x).max() or 1) * 10 ** (-1 / 20) * laut, 64)

def stueck(x):
    s = np.flatnonzero(np.abs(x).max(1) > 10 ** (-60 / 20))
    x = x[: s[-1] + 1]
    x = x / (np.abs(x).max() or 1) * 10 ** (-1 / 20)
    return x, int(np.flatnonzero(np.abs(x[:, 0]) > 0.003)[0])

if __name__ == "__main__":
    pakete, musik = sys.argv[1], sys.argv[2]
    for f in HIER.glob("*.mp3"):
        f.unlink()
    for k, (namen, laut, maxs) in TOENE.items():
        for i, name in enumerate(namen):
            ziel = k if len(namen) == 1 else f"{k}_{i + 1}"
            b = ton(lies(pakete, name), laut, maxs)
            (HIER / f"{ziel}.mp3").write_bytes(b)
            print(f"{ziel:12} {name:24} {len(b):6} Bytes")
    MUSIK.mkdir(exist_ok=True)
    info = {}
    for k, name in STUECKE.items():
        x, lead = stueck(lies(musik, name, mono=False))
        b = mp3(x, 96)
        (MUSIK / f"{k}.mp3").write_bytes(b)
        info[k] = {"n": len(x), "lead": lead}
        print(f"{k:12} {name:32} {len(x) / 44100:5.1f} s {len(b):8} Bytes")
    (MUSIK / "musik.json").write_text(json.dumps(info) + "\n")
