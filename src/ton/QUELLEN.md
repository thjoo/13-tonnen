# Töne und Musik

Alles steht unter **Creative Commons Zero (CC0)**: frei verwendbar, auch öffentlich, Nennung nicht nötig. Heruntergeladen am 26.11.2026.

Töne von Kenney (www.kenney.nl):

- Interface Sounds: https://kenney.nl/assets/interface-sounds
- Music Jingles: https://kenney.nl/assets/music-jingles
- Casino Audio (Karten): https://kenney.nl/assets/casino-audio
- RPG Audio (Münzen, Buchseiten, Stoff): https://kenney.nl/assets/rpg-audio
- Impact Sounds (Glocke, Schritte, Holz, Metall): https://kenney.nl/assets/impact-sounds

Musik:

- Juhani Junkala, «JRPG Music Pack #4 [Calm]»: https://opengameart.org/content/jrpg-pack-4-calm
- neonarkade, «Quaint Town»: https://opengameart.org/content/quaint-town

Aufbereitet mit `aufbereiten.py` (Einstellungen dort). Töne: mono, Stille weg, Spitze auf −1 dBFS mal Lautstärke, MP3 64 kb/s, eingebettet in `index.html`. Hat ein Ton mehrere Dateien, wählt das Spiel zufällig und verstimmt leicht. Musik: Stereo, MP3 96 kb/s, liegt in `musik/` neben `index.html` und wird erst geladen, wenn sie spielt.

| Ton | Wann | Quelle im Paket | Lautstärke | Bytes |
|---|---|---|---|---|
| klick | Knopf ohne eigenen Ton | click_002.ogg, click_003.ogg | 0.45 | 834 |
| waehlen | Karte wählen | card-place-1.ogg, card-place-2.ogg, card-place-3.ogg | 0.8 | 9611 |
| zurueck | Karte oder Spende zurücknehmen | card-slide-1.ogg, card-slide-2.ogg | 0.7 | 5850 |
| herz | Herz setzen | pluck_001.ogg, pluck_002.ogg | 0.6 | 2297 |
| herzweg | Herz wegnehmen | drop_001.ogg, drop_002.ogg | 0.5 | 3133 |
| nein | Geht nicht (Herz, Spende) | error_004.ogg | 0.5 | 1044 |
| geld | Spenden | handleCoins.ogg, handleCoins2.ogg | 0.6 | 8358 |
| glocke | Abstimmungssonntag beginnt | impactBell_heavy_000.ogg, impactBell_heavy_001.ogg | 0.55 | 22569 |
| kanton | Kanton ausgezählt | tick_002.ogg | 0.25 | 417 |
| ja | Vorlage angenommen | jingles_PIZZI02.ogg | 0.85 | 7941 |
| nein_abst | Vorlagen abgelehnt | jingles_PIZZI05.ogg | 0.7 | 4597 |
| krise | Krise oder Klima-Ereignis | bong_001.ogg, impactMetal_heavy_002.ogg | 0.8 | 2506 |
| chance | Gelegenheit | confirmation_002.ogg, maximize_006.ogg | 0.65 | 7940 |
| etappe | Etappe abgehakt (jede etwas höher) | glass_001.ogg | 0.55 | 2298 |
| schluss | Schluss-Auswertung | jingles_PIZZI12.ogg | 0.85 | 8150 |
| seite | Weiterblättern im Intro und Outro, «Mehr dazu» | bookFlip1.ogg, bookFlip2.ogg, bookFlip3.ogg | 0.55 | 9611 |
| schritt | Figur geht durchs Dorf | footstep_grass_000.ogg, footstep_grass_001.ogg, footstep_grass_002.ogg, footstep_grass_003.ogg | 0.45 | 6057 |
| figur | Figur wählen | cloth1.ogg, cloth2.ogg | 0.6 | 7104 |
| bauen | Haus erscheint im Dorf | impactPlank_medium_000.ogg, impactPlank_medium_001.ogg, impactPlank_medium_002.ogg | 0.5 | 10656 |

| Musik | Wann | Stück | Länge | Bytes |
|---|---|---|---|---|
| musik/dorf.mp3 | Intro und Startseite | Juhani Junkala: «A Place I Call Home» | 46 s | 558144 |
| musik/runde1.mp3 | Runden 1, 4, 7 | Juhani Junkala: «Peaceful Days» | 64 s | 768528 |
| musik/runde2.mp3 | Runden 2, 5, 8 | Juhani Junkala: «Summer Memories» | 65 s | 786240 |
| musik/runde3.mp3 | Runden 3, 6 | neonarkade: «Quaint Town» (Loopable) | 102 s | 1229904 |
| musik/abend.mp3 | Abstimmungsabend und Dorf nach der Runde | Juhani Junkala: «Childhood Friends» | 103 s | 1235088 |
| musik/schluss.mp3 | Outro und Auswertung | Juhani Junkala: «Innocence» | 71 s | 854064 |
