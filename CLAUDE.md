# Hinweise für Claude: HBOD Lern-App

Nils (Key Account Manager bei HBOD seit 01.10.2026) lernt mit dieser App E-Commerce und HBOD. Er gibt Korrekturen, neue Erkenntnisse und Dokumente laufend nach. Diese Datei sagt, wie der Katalog gepflegt wird.

## Ablauf bei Änderungen
1. Fragen in `inhalte/q_a.py` bis `inhalte/q_f.py` ändern (Kurzschreibweise in `inhalte/dsl.py`).
2. In `inhalte/build.py` `VERSION`, `STAND` und die Liste `AENDERUNGEN` ergänzen (einfaches Deutsch, ein Punkt je Änderung).
3. `python3 inhalte/build.py` ausführen. Es bricht bei doppelten IDs oder Optionen ab.
4. Optional lokal prüfen: `npm install && npm run lokal`.
5. Committen und auf `main` pushen. Netlify veröffentlicht automatisch.

## Regeln für den Inhalt
- Frage-IDs ergeben sich aus der Position. Neue Fragen ans Ende eines Tests, falsche Fragen ersetzen statt löschen.
- Bei `S(...)` ist die erste Option richtig. Antworten einfach und kurz formulieren, Distraktoren plausibel.
- Jede Frage braucht eine Quelle. Was nur aus einer Gesprächsaufnahme, aus Claude-Zusammenfassungen oder aus dem Einarbeitungs-Chat stammt, bekommt einen Hinweis („Intern bestätigen“).
- Quellen nach Verlässlichkeit: Vertrag, Preisliste/Excel (aktuell 10/2026), Company Profile, echte Mails (Laurin, Kunden), Nils' eigene Notizen und Regeln; danach die Gesprächs-Zusammenfassungen 02 bis 07; PDF 01 und Claudes Chat-Erklärungen nur mit Hinweis.
- Nicht verwenden: das entfernte Dokument „HBOD_KAM_Erkenntnisse“ und alles zum Markencheck. Die Aussage zur Galeria-Insolvenz ist laut Nils falsch.
- Nils' Mail-Regeln gelten auch für Musterlösungen: Erstantwort beginnt mit dem Pitch (ein Vertrag, über 40 Marktplätze, über 30 Länder, operatives Geschäft, Fulfillment), Provision als „10 bis 12 % je nach Umsatz“, Anhang „Unternehmenspräsentation“, am Ende weitere Infos oder ein persönliches Gespräch anbieten, nie „Logistik zu unseren Kosten“ schreiben.
- Steuer- und Rechtsfragen sind Grundprinzipien zum Verstehen und bekommen den Steuer-Hinweis.

## Nils' Fortschritt lesen
- Nils gibt einen Bericht-Link (`/api/bericht?t=…`) oder kopierten Text in den Chat. Darin stehen Stand, Fehler, unsichere Fragen und Notizen.
- Notizen mit Status „offen“ sind Korrekturwünsche oder neue Erkenntnisse. Nach dem Einarbeiten Nils sagen, welche er in der App auf „erledigt“ stellen kann.
