# HBOD Lern-App

Lern- und Prüfungs-App für E-Commerce und HBOD: 32 Tests, gut 400 Fragen, Tagesrunde mit Wiederholungsplan, Prüfungssimulation, Lernzettel und Notizen. Der Fortschritt wird auf jedem Gerät gespeichert und über einen persönlichen Lern-Code zwischen Handy und PC abgeglichen.

## Einmal einrichten (Netlify)

1. Bei Netlify anmelden und **Add new site → Import an existing project → GitHub** wählen.
2. Das Repository `Rewgen/NilsLerrnApp` auswählen. Die Einstellungen kommen automatisch aus `netlify.toml` (Veröffentlichungsordner `public`, Funktionen in `netlify/functions`). Einfach auf **Deploy** klicken.
3. Die Seite öffnen, oben auf **Geräte** gehen und **Lern-Code erstellen** tippen.
4. **Geräte-Link kopieren** und den Link auf dem Handy öffnen. Danach im Browser „Zum Home-Bildschirm“ wählen, dann läuft die Lern-App wie eine normale App.

Wichtig: Die Seite über die GitHub-Verbindung veröffentlichen, nicht per Drag and Drop. Nur so werden die Sync-Funktionen mit veröffentlicht. Für die Speicherung (Netlify Blobs) muss nichts eingestellt werden. Jeder Push auf `main` veröffentlicht automatisch die neue Version.

## Wie gespeichert wird

- Jede Antwort wird sofort im Browser gespeichert, auch offline.
- Mit Lern-Code geht jede Änderung zusätzlich an `/api/fortschritt` (Netlify Function) und landet im Blob-Speicher `lernfortschritt`. Gespeichert wird unter einem Hash des Codes, der Code selbst liegt nicht auf dem Server.
- Beim Öffnen und beim Zurückkehren zur App wird der neueste Stand geholt. Auch ein angefangener Test wird mitgenommen.
- Bei zwei Geräten gewinnt pro Frage die neueste Antwort. Durchgänge und Notizen werden zusammengeführt.
- Der Lern-Code ist wie ein Schlüssel. Wer ihn kennt, kann den Fortschritt sehen und ändern.

## Mit Claude besprechen

- Unter **Geräte → Bericht-Link kopieren** gibt es einen Nur-Lese-Link (`/api/bericht?t=…`) mit Stand, Fehlern und Notizen als Text.
- Alternativ „Bericht als Text kopieren“ oder bei einem Test „Antworten für Claude kopieren“ und in den Chat einfügen.

## Aufbau

```
public/                 die Website (wird veröffentlicht)
  index.html            die App (HTML, CSS, JavaScript in einer Datei)
  fragen.json           der Fragenkatalog (wird aus inhalte/ gebaut, nicht von Hand ändern)
  sw.js                 Offline-Unterstützung
  manifest.webmanifest  App-Symbol und Name für den Home-Bildschirm
netlify/functions/      Sync-Funktionen (fortschritt, bericht)
netlify/lib/kern.mjs    gemeinsame Logik: Zusammenführen, Bericht, Test-Speicher
inhalte/                die Quellen des Fragenkatalogs
  dsl.py                Kurzschreibweise für Fragen (S, M, W, Z, R, P, T)
  q_a.py … q_f.py       Module A bis F
  build.py              baut public/fragen.json und enthält die Liste "Was ist neu"
werkzeuge/lokal.mjs     lokaler Testserver mit Speicher im Arbeitsspeicher
```

## Fragen ändern oder ergänzen

1. Die passende Datei in `inhalte/` bearbeiten (Modul A bis F).
2. In `inhalte/build.py` unter `AENDERUNGEN` kurz eintragen, was sich geändert hat, und `VERSION` sowie `STAND` anpassen.
3. `python3 inhalte/build.py` ausführen. Das prüft den Katalog und schreibt `public/fragen.json`.
4. Committen und pushen. Netlify veröffentlicht automatisch.

Regeln für die Pflege:

- Die Frage-ID (z. B. `t14-03`) ergibt sich aus der Position im Test. Neue Fragen deshalb ans Ende eines Tests setzen.
- Eine falsche Frage lieber ersetzen als löschen. Beim Löschen rutschen die folgenden IDs nach.
- Jede Frage hat einen Fingerabdruck aus Fragetext, Antworten und Lösung. Ändert er sich, zählt nur diese Frage neu und wird als „überarbeitet“ markiert. Änderungen an Erklärung, Quelle oder Hinweis setzen nichts zurück.
- Unsichere Aussagen bekommen einen Hinweis (letzter Parameter), z. B. „Aus einer Gesprächsaufnahme. Intern bestätigen.“
- Bei `S(...)` ist die erste Option immer die richtige. Die App mischt die Reihenfolge.

## Lokal testen

```
npm install
npm run lokal        # http://localhost:8888, Sync mit Speicher im Arbeitsspeicher
```

## Lernmethode in der App

- **Abrufen statt Wiederlesen:** Jede Frage wird erst beantwortet, dann kommt die Erklärung.
- **Verteiltes Wiederholen (Leitner, 5 Fächer):** richtig, dann nach 1, 3, 7, 14 und 30 Tagen wieder; falsch, dann am nächsten Tag. Mehrmals am selben Tag zählt nur einmal. Gemeistert ab Fach 3, also an drei verschiedenen Tagen richtig.
- **Mischen:** Die Tagesrunde mischt Themen, damit ähnliche Begriffe sicher unterschieden werden.
- **Sicherheit angeben:** Wer rät, hakt „unsicher“ an. Die Frage steigt dann nicht auf. Sichere Irrtümer werden in der Rückmeldung besonders hervorgehoben.
- **Selbst erklären:** Lernzettel je Test, Freitexte mit Kernpunkten zum Abhaken.
