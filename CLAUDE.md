# Hinweise für Claude: HBOD Lern-App

Nils (Key Account Manager bei HBOD seit 01.10.2026) lernt mit dieser App E-Commerce und HBOD. Er gibt Korrekturen, neue Erkenntnisse und Dokumente laufend nach. Diese Datei sagt, wie der Katalog gepflegt wird.

## Ablauf bei Änderungen
1. Fragen in `inhalte/q_a.py` bis `inhalte/q_f.py` ändern (Kurzschreibweise in `inhalte/dsl.py`).
2. Themen in `inhalte/themen.py` mitpflegen: neue Fragen den passenden Themen zuordnen (ID in die Liste, Reihenfolge = Lernreihenfolge), bei ersetzten Fragen prüfen, ob sie noch zum Thema passen. Ändert sich ein Fakt, auch die Kurzerklärung (`punkte`, `merksatz`) des Themas anpassen.
3. In `inhalte/build.py` `VERSION`, `STAND` und die Liste `AENDERUNGEN` ergänzen (einfaches Deutsch, ein Punkt je Änderung).
4. `python3 inhalte/build.py` ausführen. Es bricht bei doppelten IDs oder Optionen, unbekannten oder ausgeblendeten Frage-IDs in Themen, Themen mit weniger als 6 Fragen und fehlerhaften Einträgen in `pflege.py` oder `rueckmeldungen.py` ab. Es meldet, wie viele Fragen in keinem Thema stehen und ob es mögliche neue Doppel gibt.
5. Optional lokal prüfen: `npm install && npm run lokal`.
6. Committen und auf `main` pushen. Netlify veröffentlicht automatisch.

## Regeln für den Inhalt
- Frage-IDs ergeben sich aus der Position. Neue Fragen ans Ende eines Tests, falsche Fragen ersetzen statt löschen.
- Vor jeder neuen Frage prüfen, ob es sie schon gibt: `python3 inhalte/suche.py "Stichworte oder Frage"`. Ab etwa 0,35 ist es meist dieselbe Tatsache.
- Doppelte Fragen nicht löschen, sondern in `inhalte/pflege.py` ausblenden (`AUSBLENDEN`, mit Grund). Fragen, die dieselbe Tatsache aus anderem Blickwinkel abfragen, als `VERWANDT` verknüpfen: Sie kommen dann nie in derselben Runde oder am selben Tag. Bewusst ähnliche Paare als `GEPRUEFT` eintragen. Überblick: `python3 inhalte/doppelte.py`.
- Bei `S(...)` ist die erste Option richtig. Antworten einfach und kurz formulieren, Distraktoren plausibel.
- Jede Frage braucht eine Quelle. Was nur aus einer Gesprächsaufnahme, aus Claude-Zusammenfassungen oder aus dem Einarbeitungs-Chat stammt, bekommt einen Hinweis („Intern bestätigen“).
- Quellen nach Verlässlichkeit: Vertrag, Preisliste/Excel (aktuell 10/2026), Company Profile, echte Mails (Laurin, Kunden), Nils' eigene Notizen und Regeln; danach die Gesprächs-Zusammenfassungen 02 bis 07; PDF 01 und Claudes Chat-Erklärungen nur mit Hinweis.
- Nicht verwenden: das entfernte Dokument „HBOD_KAM_Erkenntnisse“ und alles zum Markencheck. Die Aussage zur Galeria-Insolvenz ist laut Nils falsch.
- Nils' Mail-Regeln gelten auch für Musterlösungen: Erstantwort beginnt mit dem Pitch (ein Vertrag, über 40 Marktplätze, über 30 Länder, operatives Geschäft, Fulfillment), Provision als „10 bis 12 % je nach Umsatz“, Anhang „Unternehmenspräsentation“, am Ende weitere Infos oder ein persönliches Gespräch anbieten, nie „Logistik zu unseren Kosten“ schreiben.
- Steuer- und Rechtsfragen sind Grundprinzipien zum Verstehen und bekommen den Steuer-Hinweis.
- Für die Kurzerklärungen der Themen gelten dieselben Regeln: nur Aussagen, die auch in Fragen mit Quelle stehen, Quellen angeben, Unsicheres mit Hinweis.

## Nils' Fortschritt lesen
- Nils gibt einen Bericht-Link (`/api/bericht?t=…`) oder kopierten Text in den Chat. Darin stehen Stand, Fehler, unsichere und als schwer bewertete Fragen sowie alle offenen Anmerkungen und Wünsche mit ihrer Notiz-ID in eckigen Klammern.

## Anmerkungen und Wünsche einarbeiten
Arten im Bericht: „Antwort prüfen“ (oft mit betroffener Antwortmöglichkeit), „Unklar“, „Doppelt“ (mit der anderen Frage), „Ergänzung“, „Wunsch: neue Frage“, „Wunsch: neues Thema“, „Erkenntnis“. „Bis zur Prüfung pausiert“ heißt: Die Frage wird nicht abgefragt, bis die Notiz erledigt ist.
1. Jeden Punkt einzeln prüfen. Bei Wünschen und Erkenntnissen immer zuerst `python3 inhalte/suche.py "…"` ausführen und die Themen ansehen. Gibt es das schon, nichts doppelt anlegen, sondern Nils die Fundstelle nennen (z. B. „Gibt es schon: T01-05 und Thema GMV“). Die App hat beim Eintragen selbst schon Ähnliches gesucht („Die App fand ähnlich“), das ist ein Hinweis, ersetzt aber nicht die eigene Prüfung.
2. „Antwort prüfen“ und „Unklar“: gegen die Quellen prüfen (Reihenfolge der Verlässlichkeit siehe oben). Stimmt die Frage nicht, korrigieren oder ersetzen. Stimmt sie, kurz begründen. Ist es unsicher, einen Hinweis „Intern bestätigen“ ergänzen.
3. „Doppelt“: beide Fragen vergleichen, dann ausblenden, verknüpfen oder als geprüft markieren (`pflege.py`).
4. Neue Fragen ans Ende des passenden Tests, mit Quelle, und in die passenden Themen (`themen.py`).
5. Zu jeder bearbeiteten Notiz eine Rückmeldung in `inhalte/rueckmeldungen.py` eintragen: `rueck("<Notiz-ID>", "<jetzt in UTC>", "<was gemacht wurde>")`, Zeit mit `date -u +%Y-%m-%dT%H:%M:%SZ`. Die Rückmeldung erscheint in der App an der Notiz, die Notiz gilt dann als erledigt, eine Pause endet.
6. `VERSION`, `STAND`, `AENDERUNGEN` ergänzen, bauen, veröffentlichen. Nils kurz sagen, was eingearbeitet wurde und was es schon gab.
- Der Bericht zeigt auch den Stand je Thema und die als schwer bewerteten Fragen. Schwache Themen und schwere Fragen eignen sich gut zum gemeinsamen Durchgehen.

## Erklär-Chats
- Nils schickt aus der App Fragen per „In Claude erklären lassen“ in einen Chat seiner Wahl. Der Text enthält Frage, seine Antwort, Lösung, Erklärung der App, Hinweis und Quelle.
- In solchen Chats einfach und kurz erklären, mit Beispiel aus dem HBOD-Alltag. Ist die Erklärung der App falsch oder ungenau, das klar sagen und Nils vorschlagen, unter der Frage eine Notiz anzulegen, damit es im Katalog korrigiert wird.
