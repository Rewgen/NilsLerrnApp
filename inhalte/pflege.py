"""Pflege des Katalogs: doppelte und verwandte Fragen.

AUSBLENDEN: Frage-ID -> Grund. Die Frage bleibt in ihrer Datei (so bleiben alle Frage-IDs stabil),
    taucht in der App aber nirgends mehr auf: nicht im Test, nicht in Runden, Themen, Prüfung oder Statistik.
    Ausgeblendete Fragen dürfen in keinem Thema stehen.
VERWANDT: Gruppen von Fragen, die dieselbe Tatsache aus verschiedenen Blickwinkeln abfragen.
    Sie bleiben, kommen aber nie in derselben Runde und nicht am selben Tag dran. Jede Frage höchstens in einer Gruppe.
GEPRUEFT: Paare, die sich ähneln, aber bewusst beide bleiben. build.py meldet sie dann nicht mehr als mögliche Doppel.

Prüfen: python3 inhalte/doppelte.py zeigt alle ähnlichen Paare und ihren Stand.
"""

AUSBLENDEN = {
    "t12-08": "Doppelt zu T03-09 (Amazon: Für Bundles braucht HBOD freie EANs der Marke).",
    "t13-11": "Doppelt zu T09-11 (Preiserhöhungen der Paketdienste gibt HBOD schriftlich weiter).",
    "t28-07": "Doppelt zu T16-03 (Retourenkosten: Die Rechnung zeigt den Durchschnitt über viele Verkäufe).",
    "t31-10": "Doppelt zu T30-11 (Frage, die du nicht beantworten kannst: ehrlich sagen und Antwort nachliefern).",
    "t02-10": "Doppelt zu T28-04 (Nur aus dem eigenen Lager, weil HBOD als Verkäufer für die SLAs haftet).",
}

VERWANDT = [
    ("t09-08 t10-10 t07-08", "Peak Season: Wareneingang dauert länger, früh planen"),
    ("t26-09 t28-04", "Nur aus dem eigenen Lager"),
    ("t21-02 t29-05 t02-04", "Verkauf im eigenen Namen und auf eigene Rechnung"),
    ("t10-13 t30-09", "Exklusive Artikel laufen oft besser als Basics"),
    ("t11-06 t25-04", "Schweiz und Zalando"),
    ("t13-05 t25-03", "Versand nach Österreich"),
    ("t06-07 t13-12 t18-10", "HBOD-Provisionsstaffel"),
    ("t28-12 t29-14 t06-08", "Logistikkosten richtig formulieren"),
    ("t04-02 t12-12", "Amazon: Kunde erzeugt das Retourenlabel selbst"),
    ("t04-12 t11-10", "Zalando BrandHome"),
    ("t21-01 t28-08", "Zusammenarbeit nicht exklusiv"),
    ("t13-03 t15-08", "Kosten je Bestellung"),
    ("t22-01 t22-02", "Gutschriftsverfahren"),
    ("t19-08 t30-07", "Schwache Ergebnisse proaktiv melden"),
    ("t01-11 t14-12", "Warenkorb und Artikel pro Bestellung"),
    ("t16-01 t16-02", "Retoure: Provisionen zurück, Prozesskosten bleiben"),
    ("t17-12 t19-01", "Auszahlungsquote im Monatsreport"),
    ("t15-05 t28-01", "Logistik 2,07 € bei CiTO"),
    ("t13-07 t25-12", "Teure Versandländer"),
    ("t17-04 t32-03", "Auszahlung pro Artikel: durch 0,96 teilen"),
    ("t17-11 t32-05", "Amazon zahlt oft mehr aus als Zalando"),
    ("t22-11 t28-05", "Keine eigenen Registrierungen im Ausland nötig"),
    ("t06-06 t06-10", "Erfolgsbasierte Vergütung"),
]

GEPRUEFT = [
    "t12-01 t18-05",  # Amazon-Provision pauschal vs. warum Kategorie wählen
    "t20-01 t20-02",  # Was ist die UVP vs. darf man über UVP verkaufen
    "t06-12 t20-12",  # asset-light vs. Kapitalbindung allgemein
    "t04-04 t04-05",  # Was ist die BuyBox vs. wovon hängt sie ab
]
