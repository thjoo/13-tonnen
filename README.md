# 13 Tonnen

Ein Lernspiel zum CO₂-Fussabdruck in der Schweiz für den Geografieunterricht (Kantonsschule Küsnacht, Einheit Klimawandel).

Du spielst eine Figur, die 2026 mit dem Schweizer Durchschnitt von 12.8 t Treibhausgasen pro Jahr startet, und versuchst, ihren Fussabdruck bis 2050 zu senken: mit eigenen Entscheiden und mit Engagement für politische Vorlagen. Man spielt allein oder in der Gruppe, jede Person auf ihrem eigenen Gerät.

- Alle Zahlen und Quellen stehen im Spiel unter «Mehr dazu» auf jeder Karte.
- Gruppenspiel: Firebase Realtime Database (Standort Belgien), anonyme Anmeldung, keine Namen. Räume lassen sich nach 24 Stunden nicht mehr verändern und werden beim Eröffnen neuer Räume gelöscht.
- Die Startseite zeigt ein belebtes Dorf in Pixelart. Es wird auf einer Canvas gezeichnet; bei «Bewegung reduzieren» im Betriebssystem steht es still.
- Spielnummer: Mit `?spiel=4A` am Ende der Adresse bekommen alle, die allein spielen, dieselben Abstimmungen, Würfe und Ereignisse. Die Karten sind nur bei gleicher Figur und gleichen Entscheiden gleich. So lassen sich Entscheide in der Nachbesprechung vergleichen. Ohne Zusatz gibt es pro Partie eine neue Nummer; sie steht am Schluss in der Auswertung.
- Ton und Musik: Zu Beginn an, sie starten mit der ersten Berührung. Der Schalter unten in der Leiste und auf der Startseite wechselt zwischen «Musik und Ton», «Nur Ton» und «Ton aus» und bleibt im Browser gespeichert. Die Musik liegt in `musik/` und wird nur geladen, wenn sie spielt; wer `index.html` allein öffnet, hat Töne ohne Musik. Alles CC0, siehe `src/ton/QUELLEN.md`.
- Eine angefangene Partie bleibt im Browser gespeichert und lässt sich nach dem Neuladen auf der Startseite fortsetzen.
- Das Spiel ist eine einzige Datei (`index.html`) ohne Abhängigkeiten ausser Firebase für das Gruppenspiel und der Musik in `musik/`.

## Grafiken und Schriften

- Figuren, Dorf, Häuser, Tiere, Bäume und einige Symbole: «Cute Fantasy RPG» von Kenmi (https://kenmi-art.itch.io/cute-fantasy-rpg), verändert und in Graustufen, nur als eingebettete Bilder im Spiel. Die Grafiken dürfen nicht separat weiterverwendet werden.
- Bereichs-Icons: «1-bit Pixel Icons» von Nikoichu (CC0).
- Autos: «TopDown Vehicles» von MinZiin (https://minzinn.itch.io/), Lizenz CC BY 4.0, in Graustufen.
- Schriften: Jersey 10, Silkscreen und Open Sans (SIL Open Font License), eingebettet.

## Aufbau

- `src/`: Code (`template.html`, `dorf_anim.js`), Texte der Karten (`texts.json`), Zahlen (`mech.py` erzeugt `mech.json`), Schriften und Stil. `src/build.py` baut daraus die eine Datei `index.html`, die GitHub Pages ausliefert.
- `grafik/`: privates Submodul (thjoo/13-tonnen-grafik) mit den Grafiken von Kenmi und den Dorfdaten. Die Lizenz erlaubt keine Weiterverbreitung der Grafiken als einzelne Dateien, darum sind sie nur eingebettet im fertigen Spiel öffentlich.
- `tests/`: automatische Tests, siehe unten.

Bauen (mit Zugriff auf das private Repo):

```
git clone --recurse-submodules https://github.com/thjoo/13-tonnen
python src/build.py
```

## Tests

Bei jedem Push prüft GitHub das Spiel automatisch (Reiter «Actions»). Getestet wird die fertige `index.html`:

- `tests/test_modell.py`: Rechenmodell und Regeln (Start 12.8 t, Trend bis 2050, Heizung mit und ohne K3, Volks- und Ständemehr, schrittweise Einführung, Stufen, Outro).
- `tests/test_partien.py`: ganze Partien mit allen Figuren sowie 9 Zufallspartien über die Knöpfe auf Laptop, iPad und Handy. Geprüft werden unter anderem Fussabdruck, Geld, Herzen, «NaN» im Text und seitliches Scrollen.
- `tests/test_gruppe.py`: Gruppenspiel mit drei Geräten gegen einen nachgebauten Speicher (`tests/gruppe.js`, braucht Node): gleiche Vorlagen, Resultate und Punkte für alle, alle kommen ans Ende.
- `tests/test_balance.py`: Balance mit Bots (`tests/balance.js`, braucht Node): starke, mittlere und schwache Spielweise in je 150 Partien pro Version. `node tests/balance.js --zeigen` druckt die Tabelle.
- `tests/test_speichern.py`: Weiterspielen nach Neuladen, Fehlerkarte und gleiche Lose bei gleicher Spielnummer.
- `tests/test_einfuehrung.py`: erste Runde zum Mitmachen, Dorf ohne Scrollen am Computer, Ton und Musik zu Beginn an, als Schleife, in drei Stufen schaltbar.
- `tests/test_didaktik.py`: Vorhersage vor der Bilanz, Hinweis ohne Engagement für Vorlagen, Punkte für die Wirkung auf die Schweiz.
- `tests/test_zugang.py`: Barrierefreiheit nach WCAG 2.1 AA (axe-core) und Bedienung mit der Tastatur.
- `tests/manuell/gruppe_testmodus.py`: Gruppenspiel mit Testfiguren gegen die echte Datenbank, nur von Hand starten.

In den automatischen Tests ist Firebase blockiert: Es entstehen keine Räume.

Lokal ausführen:

```
pip install -r tests/requirements.txt && python -m playwright install chromium
npm install axe-core@4 --prefix tests --no-save
python -m pytest tests -q
```

Stand: Prototyp, November 2026.
