# HBOD Lern-App

Lern- und Prüfungs-App für E-Commerce und HBOD: 32 Tests, gut 400 Fragen, 23 Themen zum Vertiefen, Tagesrunde mit 5 Fragen und Wiederholungsplan, schnelle Runden mit 5 oder 10 Fragen, Prüfungssimulation, Lernzettel und Notizen. Antworten lassen sich mit einem Tipp im eigenen Claude-Chat erklären. Fragen lassen sich als leicht, mittel oder schwer bewerten, anmerken (z. B. „Antwort stimmt nicht“) und neue Fragen oder Themen per Plus-Knopf wünschen. Der Fortschritt wird auf jedem Gerät gespeichert und über einen persönlichen Lern-Code zwischen Handy und PC abgeglichen.

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

- **In Claude erklären lassen:** Unter **Geräte → Deine Claude-Chats** einen oder mehrere Chats mit Namen und claude.ai-Link speichern (am besten ein Chat im Projekt HBOD, auch ein Projekt-Link geht). Unter jeder Erklärung wählt man dann den Chat. Die App kopiert Frage, eigene Antwort, Lösung, Erklärung, Hinweis und Quelle in die Zwischenablage und öffnet den Chat. Dort nur einfügen und senden. Ein Chat lässt sich per Link nicht zuverlässig vorausfüllen, deshalb der Weg über die Zwischenablage. Die Chats stehen in den Einstellungen und werden mit dem Lern-Code auf alle Geräte übertragen.
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
  themen.py             Themen zum Vertiefen: Kurzerklärung und zugeordnete Frage-IDs
  pflege.py             doppelte Fragen ausblenden, verwandte Fragen verknüpfen
  rueckmeldungen.py     Claudes Antworten auf Nils' Anmerkungen (erscheinen in der App)
  aehnlich.py           Ähnlichkeitssuche für Build, suche.py und doppelte.py
  suche.py              prüft vor dem Einbau, ob es eine Frage oder ein Thema schon gibt
  doppelte.py           zeigt sehr ähnliche Fragenpaare und ihren Stand
  build.py              baut public/fragen.json und enthält die Liste "Was ist neu"
werkzeuge/lokal.mjs     lokaler Testserver mit Speicher im Arbeitsspeicher
```

## Fragen ändern oder ergänzen

1. Die passende Datei in `inhalte/` bearbeiten (Modul A bis F).
2. Bei neuen oder ersetzten Fragen in `inhalte/themen.py` prüfen, zu welchen Themen sie gehören (Frage-ID in die Liste des Themas).
3. In `inhalte/build.py` unter `AENDERUNGEN` kurz eintragen, was sich geändert hat, und `VERSION` sowie `STAND` anpassen.
4. `python3 inhalte/build.py` ausführen. Das prüft Katalog und Themen und schreibt `public/fragen.json`.
5. Committen und pushen. Netlify veröffentlicht automatisch.

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
- **Verteiltes Wiederholen (Leitner, 5 Fächer):** richtig, dann nach 2, 4, 8, 15 und 30 Tagen wieder (bis Version 2.2: 1, 3, 7, 14, 30); falsch, dann am nächsten Tag. Richtig vor dem Termin (gleicher Tag, schnelle Runde, Test nochmal) lässt Fach und Termin unverändert. Gemeistert ab Fach 3, also dreimal zum Termin richtig.
- **Tagesrunde:** standardmäßig 5 Fragen (einstellbar 5, 10, 15 oder 20). Höchstens 60 % sind Wiederholungen (bei 5 Fragen 3), der Rest ist neu. Dieselbe Frage kommt nicht zweimal am selben Tag, verwandte Fragen (gleiche Tatsache, siehe `pflege.py`) nie in derselben Runde oder am selben Tag. Gilt auch für schnelle Runden, Themen und Prüfung.
- **Bewertung:** Nach jeder Antwort Leicht, Mittel oder Schwer. Schwer hält die Frage in Fach 1 oder 2 (direkt nach dem Bewerten morgen wieder), Leicht lässt sie zum Termin ein Fach mehr aufsteigen. „Nur schwere lernen“ unter Heute, Fehler und im Thema.
- **Anmerken und Wünsche:** Unter jeder Frage „Anmerken“ (Antwort stimmt nicht, unklar, doppelt, Ergänzung; auf Wunsch pausiert die Frage bis zur Prüfung). Der Plus-Knopf öffnet ein Fenster für neue Fragen, Themen oder Erkenntnisse und zeigt sofort ähnliche vorhandene Fragen. Claude arbeitet alles ein und antwortet über `inhalte/rueckmeldungen.py`. Die Antwort erscheint an der Notiz, die Notiz gilt dann als erledigt.
- **Themen vertiefen:** 23 Themen (z. B. GMV und Kennzahlen, Provision, Retouren, Zalando, EPR) mit Kurzerklärung und Merksatz. Gelernt wird in Runden zu 5 Fragen: zuerst Fälliges und Fehler aus dem Thema, dann neue Fragen in der Lernreihenfolge des Themas. Heute schon Beantwortetes kommt nach hinten, damit „Nächste 5 Fragen“ weiterführt. Unter jeder Erklärung führt „Thema vertiefen“ zum passenden Thema.
- **Schnelle Runde:** 5 oder 10 Fragen ohne Freitext, aus allen Themen, einem Modul oder einem Test. Reihenfolge der Auswahl: fällig, zuletzt falsch, neu (reihum aus verschiedenen Tests), am längsten her. Mit Serie für richtige Antworten in Folge.
- **Am PC:** Tasten 1 bis 9 wählen eine Antwort, Enter prüft und geht weiter.
- **Mischen:** Die Tagesrunde mischt Themen, damit ähnliche Begriffe sicher unterschieden werden.
- **Sicherheit angeben:** Wer rät, hakt „unsicher“ an. Die Frage steigt dann nicht auf. Sichere Irrtümer werden in der Rückmeldung besonders hervorgehoben.
- **Selbst erklären:** Lernzettel je Test, Freitexte mit Kernpunkten zum Abhaken.
