# Hinweise für Claude: HBOD Lern-App

Nils (Key Account Manager bei HBOD seit 01.10.2026) lernt mit dieser App E-Commerce und HBOD. Er gibt Korrekturen, neue Erkenntnisse und Dokumente laufend nach. Diese Datei sagt, wie der Katalog gepflegt wird.

## Vertraulichkeit (wichtig)
Das Repository und die veröffentlichte App sind öffentlich erreichbar. Alles in `inhalte/`, `public/fragen.json` (auch „Was ist neu“) und in Commit-Nachrichten kann jeder lesen.
- Erlaubt: Inhalte der Unternehmenspräsentation, öffentlich einsehbare Informationen (Marktplätze, Gesetze, GS1 usw.), die HBOD-Preisliste und Zahlen, die man für Berechnungen braucht (mit neutralen Beispielen), Abläufe ohne Namen, Erfahrungswerte, Auftreten in Gesprächen.
- Nie aufnehmen: Namen, Kontakte oder Mails von Kunden und Interessenten, Umsätze oder Kennzahlen einzelner Kunden, Inhalte aus Verträgen mit Kunden, interne Strategie (Zielkunden-Listen, Wettbewerber-Einschätzungen, Vertriebsziele), Vorfälle, Pläne und Projekte, interne Systeme und Werkzeuge, Namen von Kolleginnen und Kollegen außerhalb der Unternehmenspräsentation.
- Im Zweifel weglassen oder neutral formulieren („eine Marke“, „ein Kunde“). Das gilt auch für Rückmeldungen in `rueckmeldungen.py`.

## Aufbau
- Bereiche A bis F (`modul(...)`) enthalten Stapel (`stapel(...)`, wie in Anki), Stapel enthalten Fragen. Alles steht in `inhalte/q_a.py` bis `inhalte/q_f.py`, Kurzschreibweise in `inhalte/dsl.py`.
- Jede Frage hat eine feste ID als ersten Parameter, z. B. `S("t01-05", ...)`. Die ID bleibt für immer, daran hängt Nils' Fortschritt. Neue Fragen bekommen die nächste freie Nummer im Stapel. IDs aus `pflege.GELOESCHT` nie neu vergeben.
- Das Wichtigste zum Einlesen steht direkt am Stapel (`punkte`, `merksatz`, `quelle`, `hinweis`).
- Ändert sich Fragetext, Antworten oder Lösung, ändert sich der Fingerabdruck und nur diese Frage zählt für Nils neu. Erklärung, Quelle und Hinweis kann man ändern, ohne Fortschritt zu verlieren.

## Ablauf bei Änderungen
1. Fragen im passenden Stapel ändern oder ergänzen.
2. Ändert sich ein Fakt, auch `punkte` und `merksatz` des Stapels anpassen.
3. In `inhalte/build.py` `VERSION`, `STAND` und die Liste `AENDERUNGEN` ergänzen (einfaches Deutsch, ein Punkt je Änderung, ohne vertrauliche Inhalte).
4. `python3 inhalte/build.py` ausführen. Es bricht ab bei doppelten oder ungültigen IDs, wiederverwendeten gelöschten IDs, fehlender Quelle, doppelten Optionen und fehlerhaften Einträgen in `pflege.py` oder `rueckmeldungen.py`. Es meldet mögliche neue Doppel.
5. Optional lokal prüfen: `npm install && npm run lokal` (http://localhost:8888).
6. Committen und auf `main` pushen. Netlify veröffentlicht automatisch.

## Regeln für den Inhalt
- Vor jeder neuen Frage prüfen, ob es sie schon gibt: `python3 inhalte/suche.py "Stichworte oder Frage"`. Ab etwa 0,35 ist es meist dieselbe Tatsache.
- Doppelte Fragen löschen (aus der Datei entfernen, ID in `pflege.GELOESCHT`). Fragen, die dieselbe Tatsache aus anderem Blickwinkel abfragen, als `VERWANDT` verknüpfen: Sie kommen dann nie in derselben Runde oder am selben Tag. Bewusst ähnliche Paare als `GEPRUEFT` eintragen. Überblick: `python3 inhalte/doppelte.py`.
- Bei `S(...)` ist die erste Option richtig, bei `M(...)` sind es alle aus der Liste `richtig`. Antworten einfach und kurz formulieren, Distraktoren plausibel.
- Nils mag Ankreuzfragen mit mehreren richtigen Antworten (`M`), wo es passt.
- Jede Frage braucht eine Quelle. Was nur aus einer Gesprächsaufnahme, aus Claude-Zusammenfassungen oder aus dem Einarbeitungs-Chat stammt, bekommt einen Hinweis („Intern bestätigen“).
- Quellen nach Verlässlichkeit: Preisliste (aktuell 10/2026), Unternehmenspräsentation, öffentliche Quellen (Gesetze, Marktplätze, GS1), echte Mails von Kollegen und Kunden (nur die Sache, nie Namen oder Zahlen des Kunden), Nils' eigene Notizen und Regeln; danach die Gesprächs-Zusammenfassungen 02 bis 07; PDF 01 und Claudes Chat-Erklärungen nur mit Hinweis.
- Nicht verwenden: das entfernte Dokument „HBOD_KAM_Erkenntnisse“ und alles zum Markencheck. Die Aussage zur Galeria-Insolvenz ist laut Nils falsch.
- Nils' Mail-Regeln gelten auch für Musterlösungen: Erstantwort beginnt mit dem Pitch (ein Vertrag, über 40 Marktplätze, über 30 Länder, operatives Geschäft, Fulfillment), Provision als „10 bis 12 % je nach Umsatz“, Anhang „Unternehmenspräsentation“, am Ende weitere Infos oder ein persönliches Gespräch anbieten, nie „Logistik zu unseren Kosten“ schreiben.
- Steuer- und Rechtsfragen sind Grundprinzipien zum Verstehen und bekommen den Steuer-Hinweis.
- Für die Kurzerklärungen der Stapel gelten dieselben Regeln: nur Aussagen, die auch in Fragen mit Quelle stehen, Quellen angeben, Unsicheres mit Hinweis.

## Nils' Fortschritt lesen
- Nils gibt einen Bericht-Link (`/api/bericht?t=…`) oder kopierten Text in den Chat. Darin stehen der Stand je Stapel, die schweren Fragen (zuletzt falsch oder als schwer bewertet) sowie alle offenen Anmerkungen und Wünsche mit ihrer Notiz-ID in eckigen Klammern.
- Gelernt wird wie in Anki: Nach einer richtigen Antwort bewertet Nils mit Schwer, Gut oder Leicht. Gemeistert ist eine Frage ab Fach 3.

## Anmerkungen und Wünsche einarbeiten
Arten im Bericht: „Antwort prüfen“ (oft mit betroffener Antwortmöglichkeit), „Unklar“, „Doppelt“ (mit der anderen Frage), „Ergänzung“, „Wunsch: neue Frage“, „Wunsch: neues Thema“, „Erkenntnis“. „Pausiert“ heißt: Die Frage wird nicht abgefragt, bis die Notiz erledigt ist.
1. Jeden Punkt einzeln prüfen. Bei Wünschen und Erkenntnissen immer zuerst `python3 inhalte/suche.py "…"` ausführen und die Stapel ansehen. Gibt es das schon, nichts doppelt anlegen, sondern Nils die Fundstelle nennen (z. B. „Gibt es schon: T01-05 im Stapel GMV“). Die App hat beim Eintragen selbst schon Ähnliches gesucht („aehnlich“), das ist ein Hinweis, ersetzt aber nicht die eigene Prüfung.
2. „Antwort prüfen“ und „Unklar“: gegen die Quellen prüfen (Reihenfolge der Verlässlichkeit siehe oben). Stimmt die Frage nicht, korrigieren. Stimmt sie, kurz begründen. Ist es unsicher, einen Hinweis „Intern bestätigen“ ergänzen.
3. „Doppelt“: beide Fragen vergleichen, dann löschen, verknüpfen oder als geprüft markieren (`pflege.py`).
4. Neue Fragen mit der nächsten freien ID in den passenden Stapel, mit Quelle. Vertrauliches (siehe oben) auch dann nicht aufnehmen, wenn Nils es notiert, sondern neutral formulieren und ihm das in der Rückmeldung sagen.
5. Zu jeder bearbeiteten Notiz eine Rückmeldung in `inhalte/rueckmeldungen.py` eintragen: `rueck("<Notiz-ID>", "<jetzt in UTC>", "<was gemacht wurde>")`, Zeit mit `date -u +%Y-%m-%dT%H:%M:%SZ`. Die Rückmeldung erscheint in der App an der Notiz, die Notiz gilt dann als erledigt, eine Pause endet.
6. `VERSION`, `STAND`, `AENDERUNGEN` ergänzen, bauen, veröffentlichen. Nils kurz sagen, was eingearbeitet wurde und was es schon gab.
- Schwache Stapel und schwere Fragen aus dem Bericht eignen sich gut zum gemeinsamen Durchgehen.

## Erklär-Chats
- Nils schickt aus der App Fragen per „In Claude erklären lassen“ in einen Chat seiner Wahl. Der Text enthält Frage, seine Antwort, Lösung, Erklärung der App, Hinweis und Quelle.
- In solchen Chats einfach und kurz erklären, mit Beispiel aus dem HBOD-Alltag. Ist die Erklärung der App falsch oder ungenau, das klar sagen und Nils vorschlagen, unter der Frage eine Notiz anzulegen, damit es im Katalog korrigiert wird.
