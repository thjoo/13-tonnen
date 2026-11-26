"""Macht aus den Kenney-Paketen (CC0) die kleinen MP3 in src/ton/. Nur noetig, wenn Toene neu gewaehlt werden.

  pip install soundfile lameenc numpy
  python src/ton/aufbereiten.py <Ordner mit den entpackten Paketen interface-sounds/ und music-jingles/>

Verarbeitung: mono, 44.1 kHz, Stille unter -50 dBFS vorne und hinten weg, Ende 10 ms ausblenden,
Spitze auf -3 dBFS, dann Lautstaerke pro Ton (TOENE), MP3 64 kb/s.
"""
import glob, pathlib, sys
import lameenc, numpy as np, soundfile as sf

HIER = pathlib.Path(__file__).resolve().parent
# Name im Spiel: (Datei im Paket, Lautstaerke 0..1, hoechstens Sekunden)
TOENE = {
    "klick": ("click_002", 0.35, 0.2), "waehlen": ("select_001", 0.55, 0.3), "zurueck": ("back_001", 0.45, 0.3),
    "herz": ("pluck_001", 0.45, 0.3), "herzweg": ("drop_001", 0.4, 0.3), "nein": ("error_004", 0.4, 0.3),
    "kanton": ("tick_002", 0.18, 0.1), "ja": ("jingles_PIZZI02", 0.6, 1.2), "nein_abst": ("jingles_PIZZI05", 0.5, 0.8),
    "krise": ("bong_001", 0.6, 0.5), "chance": ("confirmation_002", 0.45, 0.6), "etappe": ("glass_001", 0.45, 0.4),
    "schluss": ("jingles_PIZZI12", 0.6, 1.2),
}

def lies(quelle, name):
    f = glob.glob(f"{quelle}/**/{name}.ogg", recursive=True)
    if not f:
        sys.exit(f"{name}.ogg fehlt in {quelle}")
    x, sr = sf.read(f[0], always_2d=True)
    x = x.mean(1)
    if sr != 44100:
        t = np.arange(0, len(x) * 44100 // sr) * sr / 44100
        x = np.interp(t, np.arange(len(x)), x)
    return x

def mache(x, laut, maxs):
    s = np.flatnonzero(np.abs(x) > 10 ** (-50 / 20))
    x = x[s[0]:s[-1] + 1] if len(s) else x
    x = x[: int(maxs * 44100)]
    f = min(len(x), 441)
    x[-f:] *= np.linspace(1, 0, f)
    x = x / (np.abs(x).max() or 1) * 10 ** (-3 / 20) * laut
    e = lameenc.Encoder()
    e.set_bit_rate(64); e.set_in_sample_rate(44100); e.set_channels(1); e.set_quality(2)
    return e.encode((x * 32767).astype("<i2").tobytes()) + e.flush()

if __name__ == "__main__":
    quelle = sys.argv[1]
    for k, (name, laut, maxs) in TOENE.items():
        b = mache(lies(quelle, name), laut, maxs)
        (HIER / f"{k}.mp3").write_bytes(b)
        print(f"{k:10} {name:18} {len(b):6} Bytes")
