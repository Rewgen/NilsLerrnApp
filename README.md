# HBOD Lern-App

Lern-App für E-Commerce und HBOD, aufgebaut wie Anki: 6 Bereiche (A bis F) mit 30 Stapeln und gut 350 Fragen. Fällige und neue Fragen kommen in kurzen Runden, nach jeder richtigen Antwort bewertet man mit Schwer, Gut oder Leicht, und die App plant die nächste Wiederholung. Antworten lassen sich mit einem Tipp im eigenen Claude-Chat erklären. Fragen lassen sich anmerken (z. B. „Antwort stimmt nicht“), neue Fragen oder Themen per Plus-Knopf wünschen. Der Fortschritt wird auf jedem Gerät gespeichert und über einen persönlichen Lern-Code zwischen Handy und PC abgeglichen.

Der Katalog enthält nur Inhalte, die öffentlich sein dürfen (Unternehmenspräsentation, öffentliche Quellen, Preisliste und Rechenbeispiele, Abläufe ohne Namen). Keine Kundennamen, keine Umsätze, keine internen Interna. Die Regeln dazu stehen in `CLAUDE.md`.

## Einmal einrichten (Netlify)

1. Bei Netlify anmelden und **Add new site → Import an existing project → GitHub** wählen.
2. Das Repository `Rewgen/NilsLerrnApp` auswählen. Die Einstellungen kommen automatisch aus `netlify.toml` (Veröffentlichungsordner `public`, Funktionen in `netlify/functions`). Einfach auf **Deploy** klicken.
3. Die Seite öffnen, oben auf **Einstellungen** gehen und **Lern-Code erstellen** tippen.
4. **Geräte-Link kopieren** und den Link auf dem Handy öffnen. Danach im Browser „Zum Home-Bildschirm“ wählen, dann läuft die Lern-App wie eine normale App.

Wichtig: Die Seite über die GitHub-Verbindung veröffentlichen, nicht per Drag and Drop. Nur so werden die Sync-Funktionen mit veröffentlicht. Für die Speicherung (Netlify Blobs) muss nichts eingestellt werden. Jeder Push auf `main` veröffentlicht automatisch die neue Version.

## Wie gespeichert wird

- Jede Antwort wird sofort im Browser gespeichert, auch offline.
- Mit Lern-Code geht jede Änderung zusätzlich an `/api/fortschritt` (Netlify Function) und landet im Blob-Speicher `lernfortschritt`. Gespeichert wird unter einem Hash des Codes, der Code selbst liegt nicht auf dem Server.
- Beim Öffnen und beim Zurückkehren zur App wird der neueste Stand geholt. Auch eine angefangene Runde wird mitgenommen.
- Bei zwei Geräten gewinnt pro Frage die neueste Antwort. Runden und Notizen werden zusammengeführt.
- Der Lern-Code ist wie ein Schlüssel. Wer ihn kennt, kann den Fortschritt sehen und ändern.

## Mit Claude besprechen

- **In Claude erklären lassen:** Unter **Einstellungen → Claude-Chats** einen oder mehrere Chats mit Namen und claude.ai-Link speichern (am besten ein Chat im Projekt HBOD, auch ein Projekt-Link geht). Unter jeder Antwort kopiert die App Frage, eigene Antwort, Lösung, Erklärung, Hinweis und Quelle in die Zwischenablage und öffnet den Chat. Dort nur einfügen und senden.
- Unter **Einstellungen → Bericht-Link kopieren** gibt es einen Nur-Lese-Link (`/api/bericht?t=…`) mit Stand je Stapel, schweren Fragen und Notizen als Text. Alternativ „Als Text kopieren“.

## Aufbau

```
public/                 die Website (wird veröffentlicht)
  index.html            die App (HTML, CSS, JavaScript in einer Datei)
  fragen.json           der Fragenkatalog (wird aus inhalte/ gebaut, nicht von Hand ändern)
  sw.js                 Offline-Unterstützung
  manifest.webmanifest  App-Symbol und Name für den Home-Bildschirm
netlify/functions/      Sync-Funktionen (fortschritt, bericht)
netlify/lib/kern.mjs    gemeinsame Logik: Zusammenführen, Bericht
inhalte/                die Quellen des Fragenkatalogs
  dsl.py                Kurzschreibweise: modul, stapel und Fragen (S, M, W, Z, R, P, T)
  q_a.py … q_f.py       Bereiche A bis F mit ihren Stapeln
  pflege.py             verwandte Fragen, geprüfte Paare, gelöschte IDs
  rueckmeldungen.py     Claudes Antworten auf Nils' Anmerkungen (erscheinen in der App)
  aehnlich.py           Ähnlichkeitssuche für Build, suche.py und doppelte.py
  suche.py              prüft vor dem Einbau, ob es eine Frage oder einen Stapel schon gibt
  doppelte.py           zeigt sehr ähnliche Fragenpaare und ihren Stand
  build.py              baut public/fragen.json und enthält die Liste "Was ist neu"
werkzeuge/lokal.mjs     lokaler Testserver mit Speicher im Arbeitsspeicher
```

## Fragen ändern oder ergänzen

1. Die passende Datei in `inhalte/` bearbeiten (Bereich A bis F, dort der Stapel).
2. In `inhalte/build.py` unter `AENDERUNGEN` kurz eintragen, was sich geändert hat, und `VERSION` sowie `STAND` anpassen.
3. `python3 inhalte/build.py` ausführen. Das prüft den Katalog und schreibt `public/fragen.json`.
4. Committen und pushen. Netlify veröffentlicht automatisch.

Regeln für die Pflege:

- Jede Frage hat eine feste ID als ersten Parameter (z. B. `S("t14-03", ...)`). Neue Fragen bekommen die nächste freie Nummer im Stapel. Gelöschte IDs stehen in `pflege.GELOESCHT` und werden nie neu vergeben.
- Jede Frage hat einen Fingerabdruck aus Fragetext, Antworten und Lösung. Ändert er sich, zählt nur diese Frage neu. Änderungen an Erklärung, Quelle oder Hinweis setzen nichts zurück.
- Unsichere Aussagen bekommen einen Hinweis (`hinweis=`), z. B. „Aus einem Gespräch. Intern bestätigen.“
- Bei `S(...)` ist die erste Option immer die richtige, bei `M(...)` alle aus `richtig`. Die App mischt die Reihenfolge.

## Lokal testen

```
npm install
npm run lokal        # http://localhost:8888, Sync mit Speicher im Arbeitsspeicher
```

## Lernmethode in der App

- **Abrufen statt Wiederlesen:** Jede Frage wird erst beantwortet, dann kommt die Erklärung.
- **Runden wie in Anki:** standardmäßig 5 Fragen (einstellbar 5, 10, 15 oder 20), aus allen Bereichen, einem Bereich oder einem Stapel. Fälliges und Neues gemischt, höchstens 60 % Wiederholungen, solange es Neues gibt.
- **Bewerten:** Nach einer richtigen Antwort Schwer, Gut oder Leicht. Auf dem Knopf steht, wann die Frage wiederkommt. Gut: nach 2, 4, 8, 15 und 30 Tagen (5 Fächer). Leicht springt ein Fach weiter, Schwer bleibt im Fach und kommt nach dem halben Abstand. Falsch: am Ende der Runde noch einmal und am nächsten Tag wieder. Richtig vor dem Termin (Üben) lässt Fach und Termin unverändert. Gemeistert ab Fach 3.
- **Freitexte:** erst selbst überlegen, dann die Lösung zeigen und selbst bewerten (Nochmal, Schwer, Gut, Leicht). Höchstens ein Freitext je Runde.
- **Keine Wiederholung am selben Tag:** Dieselbe Frage und verwandte Fragen (gleiche Tatsache, siehe `pflege.py`) kommen nicht zweimal am selben Tag und nie in derselben Runde.
- **Schwere üben:** Fragen, die zuletzt falsch oder schwer waren, lassen sich gezielt wiederholen.
- **Stapel ansehen:** Jeder Stapel hat „Das Wichtigste zum Einlesen“ und eine Liste aller Fragen mit Lösung (auch zum Drucken).
- **Anmerken und Wünsche:** Unter jeder Antwort „Anmerken“ (Antwort stimmt nicht, unklar, doppelt, Ergänzung; auf Wunsch pausiert die Frage bis zur Prüfung). Der Plus-Knopf öffnet ein Fenster für neue Fragen, Themen oder Erkenntnisse und zeigt sofort ähnliche vorhandene Fragen. Claude arbeitet alles ein und antwortet über `inhalte/rueckmeldungen.py`. Die Antwort erscheint an der Notiz, die Notiz gilt dann als erledigt.
- **Am PC:** Tasten 1 bis 9 wählen eine Antwort, Enter prüft. Danach 1 = Schwer, 2 = Gut, 3 = Leicht (Enter = Gut).
