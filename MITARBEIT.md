# Regeln für die Arbeit an «13 Tonnen»

Gilt für alle, die an diesem Repo arbeiten (Spiel und Dorf).

- Vor jedem Push die Tests laufen lassen (`python -m pytest tests -q`, siehe README).
- Vor jedem Push `git fetch` und prüfen, ob ein anderer Chat inzwischen etwas gepusht hat. Nie fremde Änderungen überschreiben.
- Commit und Push nur nach ausdrücklichem OK von Thierry.
- Keine Einträge in die echte Bestenliste. Gruppentests nur im Testmodus (`tests/manuell/gruppe_testmodus.py`), Raum danach verlassen.
- Der Quellcode liegt hier im Repo, nicht mehr im Hub: `src/` (Code, Texte, Zahlen) und `grafik/` (privates Submodul thjoo/13-tonnen-grafik mit allen Kenmi-Grafiken und den Dorfdaten). Der alte Ordner `13_Tonnen_Prototyp/src` im Hub ist ein veraltetes Archiv.
- `index.html` nie von Hand ändern: im Quellcode ändern, `python src/build.py` ausführen und `index.html` mitcommitten. GitHub prüft bei jedem Push, ob `index.html` zum Quellcode passt.
- Änderungen an Grafiken oder Dorfdaten: im Ordner `grafik/` committen und ins private Repo pushen, danach im Hauptrepo den neuen Stand des Submoduls committen.
- Zahlen und Quellen: `13_Tonnen_Zahlentabelle.md` im Hub. Ändert sich ein Wert im Spiel, die Tabelle nachführen.
- Texte im Spiel: Deutsch (Schweiz, ss), keine Gedankenstriche im Fliesstext, gendern mit Doppelpunkt, Schweizer Anführungszeichen « ».
- Grafiken von Kenmi dürfen nicht als einzelne Dateien veröffentlicht werden (siehe README). Rohbilder und Dateien mit eingebetteten Bildern gehören nur ins private Repo `grafik/`, nie nach `src/`.
- Commits immer unter dem Namen «Thierry Joerin» mit der Adresse `thjoo@users.noreply.github.com` (Autor und Committer). In Commit-Nachrichten keine Zeilen zu Mitautor:innen und keine Links auf Chats oder Sessions.
- Die Versionsgeschichte wurde am 22.11.2026 neu aufgesetzt. Ältere Arbeitskopien nicht mehr pushen, sondern das Repo neu klonen.
