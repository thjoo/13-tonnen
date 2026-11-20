Änderungen vom 20.11.2026, die nur in index.html stecken, weil der Hub-Ordner nicht erreichbar war.
Für die Quellen im Hub (src/dorf_anim.js und src/template.html) nacheinander anwenden:

    python3 kamera.py src/dorf_anim.js src/template.html
    python3 kamera2.py src/dorf_anim.js src/template.html

Danach build.py. Die Skripte ersetzen nur Stellen, die genau einmal vorkommen, und melden die Anzahl.
