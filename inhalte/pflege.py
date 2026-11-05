"""Pflege des Katalogs: verwandte und gelöschte Fragen.

VERWANDT: Gruppen von Fragen, die dieselbe Tatsache aus verschiedenen Blickwinkeln abfragen.
    Sie bleiben, kommen aber nie in derselben Runde und nicht am selben Tag dran. Jede Frage höchstens in einer Gruppe.
GEPRUEFT: Paare, die sich ähneln, aber bewusst beide bleiben. build.py meldet sie dann nicht mehr als mögliche Doppel.
GELOESCHT: IDs gelöschter Fragen. Sie dürfen nie neu vergeben werden (alter Fortschritt hängt daran).

Doppelte Fragen löscht man einfach aus ihrer Datei und trägt die ID hier unter GELOESCHT ein.
Prüfen: python3 inhalte/doppelte.py zeigt alle ähnlichen Paare und ihren Stand.
"""

VERWANDT = [
    ("t09-08 t10-10 t07-08", "Peak Season: Wareneingang dauert länger, früh planen"),
    ("t26-09 t28-04", "Nur aus dem eigenen Lager"),
    ("t29-05 t02-04", "Verkauf im eigenen Namen und auf eigene Rechnung"),
    ("t10-13 t30-09", "Exklusive Artikel laufen oft besser als Basics"),
    ("t11-06 t25-04", "Schweiz und Zalando"),
    ("t13-05 t25-03", "Versand nach Österreich"),
    ("t06-07 t13-12 t18-10", "HBOD-Provisionsstaffel"),
    ("t28-12 t29-14 t06-08", "Logistikkosten richtig formulieren"),
    ("t04-02 t12-12", "Amazon: Kunde erzeugt das Retourenlabel selbst"),
    ("t13-03 t15-08", "Kosten je Bestellung"),
    ("t22-01 t22-02", "Gutschriftsverfahren"),
    ("t19-08 t30-07", "Schwache Ergebnisse proaktiv melden"),
    ("t01-11 t14-12", "Warenkorb und Artikel pro Bestellung"),
    ("t16-01 t16-02", "Retoure: Provisionen zurück, Prozesskosten bleiben"),
    ("t17-12 t19-01", "Auszahlungsquote im Monatsreport"),
    ("t15-05 t28-01", "Logistik 2,07 € je Warenkorb"),
    ("t13-07 t25-12", "Teure Versandländer"),
    ("t17-04 t32-03", "Auszahlung pro Artikel: durch 0,96 teilen"),
    ("t17-11 t32-05", "Amazon zahlt oft mehr aus als Zalando"),
    ("t22-11 t28-05", "Keine eigenen Registrierungen im Ausland nötig"),
    ("t06-06 t06-10", "Erfolgsbasierte Vergütung"),
    ("t01-05 t01-14", "GMV-Definition"),
    ("t02-06 t02-20", "Fulfillment, Logistik und Full-Service"),
]

GEPRUEFT = [
    "t12-01 t18-05",  # Amazon-Provision pauschal vs. warum Kategorie wählen
    "t20-01 t20-02",  # Was ist die UVP vs. darf man über UVP verkaufen
    "t06-12 t20-12",  # asset-light vs. Kapitalbindung allgemein
    "t04-04 t04-05",  # Was ist die BuyBox vs. wovon hängt sie ab
]

GELOESCHT = """
t02-10 t04-14 t05-01 t05-06 t05-07 t05-11 t07-06 t09-09 t09-10 t11-10
t12-07 t12-08 t12-10 t13-11 t21-01 t21-02 t21-03 t21-04 t21-05 t21-06
t21-07 t21-08 t21-09 t21-10 t21-11 t21-12 t21-13 t21-14 t21-15 t21-16
t21-17 t21-18 t22-07 t24-10 t25-01 t25-05 t25-07 t25-09 t26-01 t26-02
t26-03 t26-04 t26-07 t26-10 t26-11 t26-12 t27-01 t27-02 t27-03 t27-05
t27-06 t27-07 t27-08 t27-10 t28-07 t28-08 t29-06 t29-09 t31-10 t32-02
""".split()
