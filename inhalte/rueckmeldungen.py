"""Antworten von Claude auf Nils' Anmerkungen und Wünsche aus der App.

Jede Rückmeldung erscheint in der App direkt an der Notiz. Die Notiz gilt dann als erledigt
(eine pausierte Frage wird wieder abgefragt). Nils kann sie wieder öffnen.

rueck(notiz_id, zeit, text)
- notiz_id: steht im Bericht in eckigen Klammern, z. B. "nmhk2x8ab12cd34"
- zeit: jetzt in UTC, z. B. mit: date -u +%Y-%m-%dT%H:%M:%SZ
- text: kurz und einfach, was gemacht wurde. Beispiele:
  "Korrigiert: Die Lösung von T14-03 lautet jetzt …"
  "Gibt es schon: T01-05 und das Thema GMV, Umsatz und Kennzahlen."
  "Geprüft, die Antwort stimmt laut Preisliste 10/2026, weil …"
  "Doppelt zu T03-09, deshalb ausgeblendet."
  "Neue Frage T12-13 ergänzt."
"""

RUECKMELDUNGEN = []


def rueck(notiz_id, zeit, text):
    RUECKMELDUNGEN.append({"id": notiz_id, "zeit": zeit, "text": text})


# Neue Rückmeldungen hier unten anhängen:
