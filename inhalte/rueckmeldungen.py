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
rueck("nmvyyngs35f115m6t", "2026-11-05T08:20:12Z", "Neue Ankreuz-Frage T01-13: „Ein Artikel hat viele Klicks, aber kaum Käufe. Woran kann das liegen?“")
rueck("nmvyyszvg2e73f374", "2026-11-05T08:20:12Z", "Geprüft, du hast teilweise recht: GMV ist nicht einheitlich definiert. Allgemein ist meist der Wert vor Retouren gemeint, Zalando berichtet GMV aber nach Stornos und Retouren (inkl. MwSt.). T01-05 und T01-06 erklären das jetzt, neu ist T01-14 zur Zalando-Definition.")
rueck("nmw0bex7f1v3n131h", "2026-11-05T08:20:12Z", "Neue Ankreuz-Frage T01-15 zu Onlineshop und Marktplatz. Weitere neue Fragen zum Ankreuzen: T01-13 und T02-17.")
rueck("nmw0c921t36j73371", "2026-11-05T08:20:12Z", "Neue Frage T02-16: Wer ist der Kommittent?")
rueck("nmw0cadpt524xv39n", "2026-11-05T08:20:12Z", "Neue Ankreuz-Frage T02-17 mit den Bedingungen nach § 383 HGB: im eigenen Namen, auf fremde Rechnung, Waren für einen anderen, gewerbsmäßig.")
rueck("nmw0chq3wp1q351r2", "2026-11-05T08:20:12Z", "Neue Frage T02-18 zum Gelegenheitskommissionär (§ 406 HGB). Die Frage T02-10, an der deine Notiz hing, war doppelt und ist gelöscht.")
rueck("nmw0dm8bk5t284q1i", "2026-11-05T08:20:12Z", "Neue Frage T02-19 zum Blitz-Eigentum. Das ist kein Gesetzesbegriff. Wie es im HBOD-Modell genau geregelt ist, bitte intern bestätigen.")
rueck("nmw0dq3yll1m2k5r1", "2026-11-05T08:20:12Z", "Das normale Konsignationslager steht in T02-09. Für „umgekehrtes Konsignationslager“ gibt es keine einheitliche Definition, deshalb steht dazu erst einmal ein Hinweis an T02-09. Frag bitte intern, wie es bei HBOD gemeint ist, dann ergänze ich eine eigene Frage.")
rueck("nmw1tdhat6a213l4a", "2026-11-05T08:20:12Z", "Neue Zuordnungsfrage T03-15 mit GTIN-8, -12, -13 und -14. Deine Antwort stimmt mit GS1 überein.")
rueck("nmw1tqj185m3n5x3m", "2026-11-05T08:20:12Z", "Gibt es schon: T02-09 (Konsignationslager). Die Erklärung sagt jetzt ausdrücklich, was Konsignation heißt. Deine Antwort passt: Die Ware liegt beim Händler, gehört aber bis zum Verkauf dem Lieferanten. Kommission ist eng verwandt, dort geht es zusätzlich darum, im eigenen Namen auf fremde Rechnung zu verkaufen.")
rueck("nmw1uc7uz341b3d4j", "2026-11-05T08:20:12Z", "Neue Frage T02-20 mit deiner Erklärung zu Logistik und Fulfillment. Sie ist mit T02-06 verknüpft, damit beide nie am selben Tag kommen.")
