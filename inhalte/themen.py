"""Themen zum Vertiefen (z. B. GMV). Ein Thema sammelt passende Fragen aus allen Tests.

Pflege:
- Fragen werden über ihre ID zugeordnet (z. B. "t01-05"). Eine Frage darf in mehreren Themen stehen.
- Die Reihenfolge der IDs ist die Lernreihenfolge im Thema: erst die Grundlagen, dann Rechnen und Anwenden.
- Wird eine Frage ersetzt, prüfen, ob sie noch zu ihren Themen passt.
- "punkte" sind das Wichtigste zum Einlesen. Nur Aussagen, die auch in den Fragen mit Quelle stehen.
  Was aus Gesprächsaufnahmen oder dem Einarbeitungs-Chat stammt, bekommt einen Hinweis.
- build.py prüft die IDs und meldet, wie viele Fragen in keinem Thema stehen.
"""

GRUPPEN = ["Zahlen und Kalkulation", "HBOD und Abläufe", "Marktplätze", "Recht, Steuern und Ausland"]
THEMEN = []

STEUER_HINWEIS = "Grundprinzip zum Verstehen. Für konkrete Kundenfälle immer mit der Buchhaltung bestätigen."


def thema(tid, gruppe, titel, kurz, punkte, merksatz, quelle, fragen, hinweis=None):
    d = {"id": tid, "gruppe": gruppe, "titel": titel, "kurz": kurz, "punkte": list(punkte),
         "merksatz": merksatz, "quelle": quelle, "fragen": fragen.split()}
    if hinweis:
        d["hinweis"] = hinweis
    THEMEN.append(d)


# ================= Zahlen und Kalkulation =================

thema("gmv-kennzahlen", "Zahlen und Kalkulation", "GMV, Umsatz und Kennzahlen",
      "Welche Zahl misst was: GMV, Umsatz nach Retouren, Warenkorb, Conversion, ROAS und Auszahlungsquote.",
      ["GMV (Gross Merchandise Value) ist der gesamte Warenwert aller Verkäufe, bevor Retouren und Kosten abgezogen werden. Er zeigt, wie groß das Geschäft ist, aber nicht, was übrig bleibt.",
       "Umsatz nach Retouren zählt nur, was die Endkunden behalten. Beispiel: 100 Bestellungen zu je 50 € sind 5.000 € GMV. Kommen 20 zurück, bleiben 4.000 € Umsatz nach Retouren. Damit rechnet HBOD in der Abrechnung.",
       "Ein Warenkorb ist eine Bestellung. Ø 1,2 Artikel pro Bestellung heißt: 10 Bestellungen enthalten zusammen 12 Artikel.",
       "Conversion-Rate = Käufe ÷ Besucher. CTR = Klicks ÷ Anzeigen. ROAS = Umsatz ÷ Werbeausgaben. Ein hoher ROAS sagt noch nichts über Gewinn, weil Retouren und Kosten nicht abgezogen sind.",
       "Auszahlungsquote im Monatsreport = Auszahlung ÷ Umsatz nach Retouren. Der Auszahlungsbetrag ist für die Marke die wichtigste Zahl. Er steht nicht in Insights, sondern in der Monatsabrechnung.",
       "Die Gesamtretourenquote hängt vom Marktplatz-Mix ab: Wächst ein Marktplatz mit hoher Quote, steigt sie, obwohl jeder Marktplatz für sich gleich bleibt."],
      "GMV zeigt, wie viel verkauft wurde. Die Auszahlung zeigt, was bei der Marke ankommt.",
      "Deine Zusammenfassung (Glossar), Produktkalkulation, Monatsreport-Gespräch, Allgemeinwissen",
      "t01-05 t01-06 t01-07 t01-11 t14-12 t01-12 t01-10 t10-04 t10-05 t10-06 t10-07 "
      "t19-01 t17-12 t05-11 t05-07 t19-03 t19-04 t19-05 t19-06 t19-09 t19-12")

thema("warenkorb", "Zahlen und Kalkulation", "Je Artikel oder je Bestellung",
      "Der Schlüssel jeder Kalkulation: Welche Kosten fallen je Artikel an, welche je Bestellung, und wie rechnet man um?",
      ["Je Artikel: Wareneingang 0,15 €, Picking 0,55 €, Retourenbearbeitung 0,99 €, Aufbereitung 1,69 €. Je Bestellung: Verpackung und Versandprozess 1,09 € und der DHL-Versand (Deutschland unter 1 kg 3,69 €).",
       "Von Artikel auf Warenkorb: mal Ø Artikel pro Bestellung. Picking bei 1,2 Artikeln: 0,55 € × 1,2 = 0,66 €.",
       "Von Warenkorb auf Artikel: geteilt durch die Artikel pro Bestellung. Versand 3,69 € bei 1,5 Artikeln: 3,69 € ÷ 1,5 = 2,46 € je Artikel.",
       "Kosten je Bestellung verteilen sich, wenn mehr Artikel im Paket sind. Deshalb sind Bundles und Multipacks der größte Hebel gegen hohe Logistikkosten pro Artikel.",
       "Für die Auszahlung pro Artikel teilt man durch die behaltenen Artikel: 1,2 × (1 − 20 % Retouren) = 0,96.",
       "Ø Artikel pro Bestellung bei Neukunden: Referenz von Bestandskunden derselben Kategorie, sonst 1,2, 1,5 oder 1."],
      "Je Artikel: mal Artikel pro Bestellung. Je Bestellung: geteilt durch Artikel pro Bestellung.",
      "Preisliste 10/2026, Kalkulation CiTO, Einweisung Produktkalkulation",
      "t01-11 t14-12 t14-05 t14-06 t14-11 t13-03 t15-01 t15-02 t15-03 t15-04 t15-05 t15-06 "
      "t15-07 t15-08 t15-09 t15-10 t15-11 t15-12 t17-02 t17-04 t18-03")

thema("brutto-netto", "Zahlen und Kalkulation", "Brutto, netto und Mehrwertsteuer im Preis",
      "Warum die Kalkulation netto rechnet und wie man richtig von brutto auf netto kommt.",
      ["Der Endkunde zahlt brutto. Die Mehrwertsteuer ist durchlaufendes Geld fürs Finanzamt und gehört nicht der Marke. Deshalb rechnet die Kalkulation mit Nettopreisen.",
       "Netto = Brutto ÷ 1,19. Beispiel: 24,99 € ÷ 1,19 = 21,00 €.",
       "Typischer Fehler: 19 % abziehen. 24,99 € × 0,81 = 20,24 € ist falsch, weil sich die 19 % auf den Nettopreis beziehen.",
       "In der HBOD-Excel werden die Provisionen auf den Brutto-Warenkorb gerechnet, abgezogen werden sie aber vom Netto-Warenkorb.",
       "HBODs eigene Leistungen (Provision, Logistik) verstehen sich netto zuzüglich Umsatzsteuer.",
       "Andere Länder, andere Sätze: Schweiz 8,1 %, Großbritannien 20 %."],
      "Brutto durch 1,19 teilen, nie 19 % abziehen.",
      "Gesprächszusammenfassung BAOBABY, Kalkulation CiTO, Vertrag § 3, Allgemeinwissen",
      "t14-01 t14-03 t14-02 t14-04 t14-10 t14-06 t14-09 t17-13 t22-03 t22-04 t22-14 t22-15",
      STEUER_HINWEIS)

thema("provision", "Zahlen und Kalkulation", "Provisionen: HBOD und Marktplätze",
      "Wie HBOD verdient, wie die Marktplatzprovisionen gestaffelt sind und wie du das Kunden erklärst.",
      ["HBOD arbeitet rein erfolgsbasiert: keine Onboarding-, Integrations- oder Monatsgebühr. HBOD verdient eine Provision auf den Umsatz nach Retouren, die Logistik wird nach Preisliste berechnet.",
       "HBOD-Staffel: 12 % bis 100.000 € Monatsumsatz, 10 % ab 100.000 € (nur für diesen Monat). Laut Kollege fix und nicht verhandelbar. In Mails schreibst du: 10 bis 12 % je nach Umsatz.",
       "Die Marktplatzprovisionen gibt HBOD 1:1 an die Marke weiter. Basis laut Excel: bol 5,7 %, Kaufland 14 %, Amazon pauschal 15 %, OTTO 16,5 %.",
       "Zalando und ABOUT YOU staffeln nach Geschlecht, Kategorie und Preis (Zalando-Basis 7,18 %). Herrenartikel kosten oft mehr Provision, weil sie seltener retourniert werden.",
       "Bei einer Retoure gehen die Provisionen zurück, die Prozesskosten bleiben.",
       "Einwand „Eure Provision kommt noch dazu“: erklären, was sie abdeckt (Aufschaltung, Content, Preise, Service, Steuer, Kampagnen), dass es keine Fixkosten gibt und HBOD nur bei Erfolg verdient."],
      "Keine Fixkosten: HBOD verdient nur, wenn Endkunden kaufen und die Ware behalten.",
      "Company Profile 2026, Einweisung Produktkalkulation (Commission Fees), Deine Mail-Regeln, Gespräch Retoure",
      "t06-06 t06-05 t06-10 t06-07 t13-12 t18-10 t29-07 t28-02 t12-04 t12-01 t11-11 t11-12 "
      "t12-02 t12-03 t18-05 t14-07 t14-08 t14-09 t16-02 t16-10")

thema("retouren", "Zahlen und Kalkulation", "Retouren",
      "Warum Retouren der größte Kostentreiber sind, wie sie in die Kalkulation eingehen und was dagegen hilft.",
      ["Richtwerte aus den Gesprächen: Amazon etwa 2 bis 10 % Retouren, Zalando etwa 20 bis 30 %, BHs und Badehosen teils über 40 %. Amazon ist niedriger, auch weil der Kunde das Retourenlabel selbst erzeugen muss.",
       "Bei einer Retoure wird der Preis erstattet und die Provisionen gehen zurück. Pick, Verpackung, Hin- und Rückversand, Bearbeitung und Aufbereitung bleiben als Kosten.",
       "Die Kalkulation zeigt einen Durchschnitt: Bei 20 % Retouren werden die Kosten der Retouren anteilig auf jeden Artikel verteilt.",
       "Annahmen der Excel: 70 % der Retouren werden aufbereitet (1,69 €), etwa 5 % sind defekt (0,29 € für Spende, Entsorgung oder Rücksendung). Rückversand aus Deutschland 4,27 €.",
       "Retouren kommen mit 1 bis 2 Monaten Verzögerung. Nach starken Monaten wie Black Friday und Weihnachten kann der Folgemonat deshalb schwach oder sogar negativ sein.",
       "Hebel: Multipacks, wenig rabattieren, Artikel oder Marktplätze mit extrem hohen Retouren kappen. Retouren ablehnen geht nicht (Widerrufsrecht)."],
      "Eine Retoure bringt keinen Umsatz, aber die Kosten bleiben.",
      "Bestandskunden-Call (Sprache_001), Gespräch Retoure, Einweisung Produktkalkulation, Monatsreport-Gespräch, Preisliste 10/2026",
      "t04-02 t04-03 t12-12 t16-01 t16-02 t16-03 t16-04 t16-05 t16-06 t16-07 t16-08 t16-09 "
      "t16-10 t16-11 t16-12 t16-13 t16-14 t07-05 t21-04 t19-05 t19-06 t19-10 t19-11 t22-06 "
      "t18-04 t25-08 t28-07 t30-08",
      "Die Retourenquoten sind Richtwerte aus Gesprächsaufnahmen. Das Verhältnis von 70 % zu 5 % intern bestätigen.")

thema("auszahlung", "Zahlen und Kalkulation", "Auszahlung und Auszahlungsquote",
      "Was bei der Marke ankommt, wie man es pro Artikel rechnet und ab wann ein Wert gut ist.",
      ["Auszahlung je Warenkorb = Netto-Warenkorb minus Verkaufskosten minus Retourenkosten. CiTO-Beispiel: 25,20 € − 12,36 € − 5,10 € = 7,74 €.",
       "Auszahlung pro Artikel = Auszahlung je Warenkorb ÷ behaltene Artikel. Bei 1,2 Artikeln und 20 % Retouren: 7,74 € ÷ 0,96 = 8,06 €. Man teilt durch 0,96, weil nur für behaltene Artikel Geld fließt.",
       "Auszahlungsquote = Auszahlung ÷ Nettopreis (in der Kalkulation) bzw. Auszahlung ÷ Umsatz nach Retouren (im Monatsreport).",
       "Faustregeln des Kollegen: unter 30 % kritisch, über 30 % okay, über 35 % gut, über 40 % sehr gut. Im Neukundengespräch nannte HBOD 30 bis 45 % als üblichen Zielbereich.",
       "Rückwärtsrechnung: Die Marke nennt ihre Mindestauszahlung, das MPE rechnet den nötigen Verkaufspreis je Marktplatz aus.",
       "Bei einem „roten“ Artikel: Preis anheben, als Bundle oder Multipack anbieten oder auf diesem Marktplatz nicht listen. Ob die Auszahlung reicht, weiß nur die Marke, weil HBOD ihre Herstellkosten nicht kennt."],
      "Sie sagen uns Ihre Mindestauszahlung, wir rechnen den Preis zurück.",
      "Kalkulation CiTO, Gesprächszusammenfassung BAOBABY, Monatsreport-Gespräch, Bestandskunden-Call (Sprache_001), Gespräch Retoure",
      "t17-01 t17-02 t17-03 t17-04 t17-05 t17-06 t17-14 t32-03 t32-04 t19-01 t17-12 t17-07 "
      "t17-08 t17-09 t17-10 t17-11 t17-13 t20-08 t19-02 t18-07 t18-08 t18-09 t28-11",
      "Die Faustregeln sind Erfahrungswerte aus Gesprächen, keine feste HBOD-Regel.")

thema("preisliste", "Zahlen und Kalkulation", "Die Preisliste: Was kostet was?",
      "Alle Logistikpositionen der HBOD-Preisliste (Stand 10/2026), was inklusive ist und wie du über Kosten sprichst.",
      ["Wareneingang 0,15 € je Artikel (je Scan, auch bei sortenreinen Kartons), Picking 0,55 € je Artikel, Verpackung und Versandprozess 1,09 € je Bestellung.",
       "Lager: 29,95 € je m³ und Monat nach den gemeldeten Maßen. Nach 9 Monaten ohne Nachbestellung gilt das Langzeitlager mit 59,95 € je m³.",
       "DHL unter 1 kg: Deutschland 3,69 €, Österreich 5,52 €, Schweiz 8,19 €, Großbritannien 11,19 €, Bulgarien, Kroatien oder Zypern 15,70 €. Rückversand aus Deutschland 4,27 €.",
       "Retourenbearbeitung 0,99 €, Aufbereitung 1,69 €, Spende, Entsorgung oder Rücksendung 0,29 € je Artikel.",
       "Extras nur bei Bedarf: Polybag 0,54 € und EAN-Sticker 1,05 € (wenn die Ware nicht wie vereinbart kommt), Hollow-Man-Packshot 19,95 €, Grafikarbeit 89,95 € je Stunde.",
       "Inklusive: Account Manager, Endkundensupport, Produktseiten, Übersetzungen, Optimierung, Werbekampagnen erstellen, jährliche Inventur. Preiserhöhungen und Peak-Zuschläge der Paketdienste gibt HBOD schriftlich weiter."],
      "In Mails: sehr gute DHL-Konditionen durch unser Volumen, nie „Logistik zu unseren Kosten“.",
      "Preisliste 10/2026, Einweisung Produktkalkulation, Deine Mail-Regeln",
      "t13-01 t13-02 t09-01 t09-02 t13-03 t09-03 t09-04 t09-05 t09-06 t09-07 t13-04 t13-05 "
      "t13-06 t13-07 t13-08 t13-09 t13-10 t09-11 t13-11 t08-08 t03-11 t06-08 t28-01 t28-12 t29-14")

thema("preise-marge", "Zahlen und Kalkulation", "Preise, UVP und Marge",
      "Wer den Preis bestimmt, was UVP und MPE unterscheidet und wie Marge, Aufschlag und Faktor zusammenhängen.",
      ["Die UVP ist die unverbindliche Preisempfehlung der Marke. Sie darf über- und unterschritten werden und ist keine Gewinngarantie. Die Marke kann zusätzlich Preisgrenzen vorgeben.",
       "Das MPE (Marketplace Profit Engine) ist HBODs Rechentool: Preis je Marktplatz und Land, Rückwärtsrechnung von der Zielauszahlung, Rot-Grün-Signal, Preisgrenzen. MPE und UVP sind nicht dasselbe.",
       "Wer bestimmt die Preise? Die Marke gibt die Strategie vor, HBOD schlägt darin Preise je Marktplatz vor, Aktionen nur in Abstimmung. Das ist der Unterschied zu Händlern, die Preise eigenmächtig senken.",
       "Im Ausland sind die Preise meist höher, weil der teurere Versand eingerechnet wird. Zalandos Fair Pricing verhindert, dass der Zalando-Preis deutlich über dem eigenen Preis der Marke liegt.",
       "Faktor 2,5 vom EK zum VK: EK 10 € ergibt VK 25 €. Die Marge (vom VK) ist 60 %, der Aufschlag (auf den EK) 150 %. Gleicher Euro-Betrag, andere Basis.",
       "Deckungsbeitrag = Erlös minus variable Kosten. Erst wenn danach etwas übrig bleibt, lohnt sich ein Artikel."],
      "Die Marge bezieht sich auf den Verkaufspreis, der Aufschlag auf den Einkaufspreis.",
      "Deine Zusammenfassung, Monatsreport-Gespräch, Bestandskunden-Call (Sprache_001), Deine Notizen, Allgemeinwissen",
      "t20-01 t20-02 t05-09 t05-08 t05-10 t17-10 t28-06 t02-03 t11-01 t25-02 t13-07 t25-12 "
      "t20-03 t20-04 t20-05 t20-06 t20-07 t18-02 t20-09",
      "Die genaue Fair-Pricing-Regel von Zalando intern bestätigen.")

# ================= HBOD und Abläufe =================

thema("hbod-modell", "HBOD und Abläufe", "Das HBOD-Modell",
      "Wer verkauft an den Endkunden, wem gehört die Ware, und was unterscheidet HBOD von Wholesale, FBA und reinem Fulfillment?",
      ["HBOD verkauft im eigenen Namen und auf eigene Rechnung (Merchant of Record). Nach außen ist HBOD der Händler, für die Marke ein Dienstleister.",
       "Die Ware liegt in Mülheim, gehört aber bis zum Verkauf der Marke (Konsignationslager). Unmittelbar vor dem Verkauf kauft HBOD sie ab. HBOD bindet kein eigenes Kapital in Ware (asset-light).",
       "Wholesale bzw. Vendor: Die Plattform oder ein Händler kauft fest ein. Vorteil für die Marke: Cashflow und weniger Risiko. Nachteil: kaum Kontrolle über Preis und Darstellung.",
       "Fulfillment ist nur die Logistik vom Wareneingang bis zur Retoure. Full-Service umfasst zusätzlich Verkauf, Daten, Marketing, Service und Abrechnung. HBOD macht beides.",
       "Bei Amazon FBA bleibt die Marke Verkäufer und macht Produktseiten, Preise, Werbung und Steuern selbst. Amazon übernimmt nur die Logistik, und nur für Amazon.",
       "Oft ideal ist ein Mix: drei bis vier Onlinehändler, die wirklich einkaufen, plus HBOD für den übrigen Markt. HBOD ergänzt, statt zu ersetzen."],
      "Zwei Leitfragen: Wer verkauft an den Endkunden? Wer bestimmt den Preis?",
      "Company Profile 2026, Vertrag (Vorlage 2025) § 1 und § 2, Einarbeitung Marktplatz-Integration, Deine Zusammenfassung",
      "t02-04 t21-02 t29-05 t02-09 t21-03 t06-12 t02-01 t02-02 t02-11 t02-12 t20-13 t02-06 "
      "t02-07 t02-05 t02-08 t02-13 t06-09 t01-04 t20-12 t20-10 t20-11 t28-03 t28-09 t32-01 t32-08")

thema("onboarding", "HBOD und Abläufe", "Onboarding: vom Vertrag zum Livegang",
      "Welche Schritte und Unterlagen nötig sind, bis die Artikel einer neuen Marke verkauft werden.",
      ["Ablauf: Vertrag, Stammdaten und Bilder, Artikel im System anlegen, HBOD bestellt die Ware (Bestellvorschlag), Wareneingang, Artikel gehen live, Verkauf, Monatsabrechnung und Auszahlung.",
       "HBOD bestellt erst, wenn die Artikel angelegt sind. Sonst kann das Lager die Ware nicht annehmen, scannen und einsortieren.",
       "Unterlagen für Neukunden: Anlieferbedingungen, Stammdatenblatt, Vorgaben für Produktfotos, Preisliste, GPSR-Formular und Brand Info. Eine Onboarding-Gebühr gibt es nicht.",
       "Initialorder mindestens 3 Stück je SKU, geplant für etwa 8 Wochen Absatz, danach rollierend 4 bis 6 Wochen Reichweite.",
       "Live meist 1 bis 4 Wochen nach vollständigen Stammdaten. Häufigste Verzögerung: fehlende oder späte Daten und Bilder. Saisonware früh planen.",
       "Anlieferung im Karton oder Polybag mit EAN-Barcode, sonst kosten Polybag (0,54 €) und EAN-Sticker (1,05 €) extra. Modelfotos liefert die Marke."],
      "Erst die Daten, dann die Ware.",
      "Deine Zusammenfassung, Company Profile 2026, Bestandskunden-Call (Sprache_001), Preisliste 10/2026",
      "t07-01 t08-07 t08-01 t08-02 t08-03 t08-04 t08-05 t08-06 t08-10 t08-08 t08-09 t08-11 "
      "t08-12 t05-12 t24-04 t03-13")

thema("artikeldaten", "HBOD und Abläufe", "EAN, SKU und Stammdaten",
      "Artikelnummern, Artikelebenen, Bundles und was in gute Stammdaten gehört.",
      ["EAN: weltweit eindeutige Nummer, meist 13-stellig und als Barcode auf dem Artikel, je Farbe und Größe eine eigene. GTIN ist der Oberbegriff. SKU: interne Nummer. ASIN: Amazons eigene Nummer für eine Produktseite.",
       "Artikelebenen: Vaterartikel (das Modell), Farbartikel, Kindartikel (eine Farbe in einer Größe). Der Kindartikel ist die verkaufbare Einheit mit SKU und EAN.",
       "Multipack = mehrere gleiche Artikel, Bundle = verschiedene Artikel. Beide brauchen eine neue EAN. HBOD baut sie virtuell über Stücklisten.",
       "Bei Amazon muss der EAN-Nummernkreis zur Marke gehören. Für Bundles stellt die Marke deshalb freie EANs bereit.",
       "Stammdaten: EAN je Variante, Artikelname, Farbe und Größe, Material, UVP, Maße und Gewicht. Eine reine Nummernliste reicht nicht.",
       "Die Maße bestimmen die Lagerkosten. Bei Textilien muss die Faserzusammensetzung am Produkt und im Angebot stehen."],
      "Eine Farbe in einer Größe = ein Kindartikel = eine EAN.",
      "Deine Zusammenfassung (Glossar), Allgemeinwissen, Bestandskunden-Call (Sprache_001), Brand Info",
      "t03-01 t03-02 t03-03 t03-04 t03-05 t03-06 t03-07 t03-08 t03-09 t12-08 t03-10 t03-12 "
      "t03-13 t03-14 t18-06 t24-07 t03-11 t10-02")

thema("bestand-saison", "HBOD und Abläufe", "Bestand, Saison und Peak Season",
      "Wie HBOD Bestände plant, warum ausverkaufte Ware Geld kostet und was rund um Black Friday wichtig ist.",
      ["Lost Sales: Ist ein Artikel ausverkauft, kauft der Kunde woanders. Deshalb plant HBOD zum Start etwa 8 Wochen Absatz, danach rollierend 4 bis 6 Wochen Reichweite.",
       "HBOD schickt regelmäßig Bestellvorschläge. Die Marke darf mehr oder weniger liefern, bestätigte Mengen muss sie einhalten.",
       "NOS-Artikel (never out of stock) sind Dauerläufer. Saisonware hat nur ein kurzes Verkaufsfenster, also Stammdaten und Liefertermin früh hinterlegen.",
       "Zalando: Season Cleaning blockiert Artikel mit schwacher Performance der letzten 12 Monate. Unter etwa 80 % Size Availability droht die Einstufung als Saisonware. Alle gängigen Größen müssen verfügbar sein.",
       "Peak Season von Black Friday bis Weihnachten: Der November allein ist etwa so stark wie ein Quartal, der Wareneingang kann von etwa 7 auf 14 Tage steigen. Früh entscheiden und früh liefern.",
       "Ladenhüter kosten doppelt: Nach 9 Monaten ohne Nachbestellung gilt das Langzeitlager mit 59,95 € je m³."],
      "Nicht leerlaufen, aber auch kein großes Lager aufbauen.",
      "Company Profile 2026, Bestandskunden-Call (Sprache_001), Preisliste 10/2026, Deine Zusammenfassung (Glossar)",
      "t01-10 t08-03 t08-04 t03-12 t08-10 t11-02 t11-03 t11-04 t11-05 t07-08 t09-08 t10-08 "
      "t10-10 t09-05 t19-07 t30-06 t30-09",
      "Season Cleaning, Size Availability und Bestellrhythmus stammen aus einer Gesprächsaufnahme. Intern bestätigen.")

thema("account-health", "HBOD und Abläufe", "SLAs, Account Health und eigenes Lager",
      "Warum HBOD nur aus dem eigenen Lager verkauft und warum Probleme einer Marke alle Marken treffen können.",
      ["SLAs sind Vorgaben der Marktplätze zu Versand, Lieferzeit und Stornos. Wer sie verletzt, verliert z. B. Prime oder wird gesperrt.",
       "Alle Marken laufen über HBODs Verkäuferkonten. Probleme einer einzelnen Marke, etwa viele Stornos, können deshalb alle anderen treffen.",
       "Beispiele: HBOD hat Prime verloren, weil Pakete zu spät ankamen. Decathlon sperrte wegen zu hoher Stornoquote.",
       "Deshalb nutzt HBOD für die Marktplätze ausschließlich das eigene Lager, kein Dropshipping aus dem Lager der Marke. Jede neue Marke muss bereit sein, vollständig bei HBOD einzulagern.",
       "Amazon-Zielwerte: Auftragsmängelquote unter 1 %, Stornoquote vor Versand unter 2,5 %, verspätete Lieferungen unter 4 %, gültige Sendungsnummern über 95 %.",
       "Die BuyBox hängt an Preis, Lieferzeit, Verfügbarkeit, Verkäuferqualität und Prime. Die Abteilung Account Health überwacht die SLAs und löst Sperren."],
      "„Da wir selbst als Verkäufer auftreten und an die SLAs gebunden sind, benötigen wir die Kontrolle über das Fulfillment.“",
      "Einarbeitung Marktplatz-Integration, Laurins Mail an Maag, Bestandskunden-Call (Sprache_001), Allgemeinwissen Amazon Seller Central",
      "t04-06 t07-09 t07-10 t12-05 t12-07 t12-06 t02-10 t26-09 t28-04 t04-04 t04-05 t07-02 t09-12",
      "Amazon kann die Zielwerte ändern.")

thema("werbung-aktionen", "HBOD und Abläufe", "Werbung, Aktionen und Black Friday",
      "Sale-Events, Preisreduktionen, Sponsored Ads und die Kennzahlen dazu.",
      ["Marketing heißt bei HBOD: Aktionen, Preise und Werbung auf den Marktplätzen, keine Plakate oder TV-Spots.",
       "Sale-Event: Der Marktplatz startet eine Aktion, HBOD reicht EANs mit Rabatt ein. Preisreduktion: HBOD senkt den Preis selbst, in Absprache mit der Marke.",
       "Sponsored Product Ads bewerben immer den Vaterartikel, bezahlt wird pro Klick. Sponsored Display Ads sind Banner, vor allem für Aufmerksamkeit.",
       "Über Aktionen wie Black Friday entscheidet die Marke. HBOD gibt Impulse und nennt Fristen und Mindestrabatte.",
       "ROAS = Umsatz ÷ Werbeausgaben. Break-even-ROAS = 1 ÷ Marge vor Werbung. Ein hoher ROAS sagt nichts über Gewinn, besonders bei vielen Retouren.",
       "Richtwert aus Gesprächen: Viele Kunden nehmen etwa 5 % vom Umsatz als Werbebudget. Das Budget bringt der Kunde, HBOD schaltet, beobachtet, optimiert und berichtet."],
      "Die Marke entscheidet, HBOD macht Vorschläge und setzt um.",
      "Deine Zusammenfassung, Amazon Ads, CiTO-Mail, Chatverlauf Einarbeitung, Bestandskunden-Call (Sprache_001), Deine Notizen",
      "t07-03 t10-01 t10-02 t10-03 t10-11 t10-13 t10-04 t10-05 t10-06 t10-07 t10-12 t10-08 "
      "t10-09 t10-10",
      "Mindestrabatte und der Richtwert fürs Werbebudget stammen aus Gesprächen. Vor Nennung bei Marketing bestätigen.")

thema("abrechnung", "HBOD und Abläufe", "Monatsabrechnung und Gutschrift",
      "Wie die Monatsabrechnung funktioniert, warum sie schwanken oder negativ werden kann und wie du das erklärst.",
      ["HBOD rechnet monatlich im Gutschriftsverfahren ab, laut Vertrag spätestens bis zum 15. des Folgemonats. Die Marke schreibt keine Rechnung. HBOD erstellt die Gutschrift und darf sie als Einziger berichtigen.",
       "Ausgangspunkt ist der Umsatz nach Retouren. Davon gehen Marktplatzprovisionen, HBOD-Provision und Logistik ab. Was übrig bleibt, ist die Auszahlung.",
       "Sind die Kosten eines Monats höher als die Erlöse, schuldet die Marke HBOD den Betrag.",
       "Typische Gründe für schwache oder negative Monate: Retouren aus Vormonaten bei wenig neuem Umsatz, ausverkaufte Ware, hohe Lagerkosten bei Ladenhütern.",
       "Liefert ein Marktplatz seine Abrechnung zu spät (z. B. ABOUT YOU), informierst du den Kunden proaktiv.",
       "Bei Wholesale fließt Geld nach Zahlungsziel, bei HBOD erst nach dem Verkauf mit der Monatsabrechnung."],
      "Schwache Abrechnung? Vorher anrufen, nicht abwarten.",
      "Vertrag (Vorlage 2025) § 4, Monatsreport-Gespräch, Bestandskunden-Call (Sprache_001), Einweisung Produktkalkulation",
      "t21-11 t22-01 t22-02 t22-07 t22-05 t22-06 t16-13 t19-10 t12-09 t20-13 t05-11 t19-08 "
      "t30-07 t29-12 t32-07",
      STEUER_HINWEIS + " Auch den genauen Auszahlungstermin intern bestätigen.")

# ================= Marktplätze =================

thema("zalando", "Marktplätze", "Zalando",
      "Katalog zum Stöbern, viele Retouren, Fair Pricing, Season Cleaning und gestaffelte Provisionen.",
      ["Zalando funktioniert wie ein Katalog zum Stöbern. Kunden bestellen oft zur Auswahl, die Retoure ist kostenlos. Retourenquote laut Gesprächen etwa 20 bis 30 %.",
       "Zalando ist stark kuratiert. Eine technische Anbindung ist keine Markenfreigabe. Für die Freigabe zählen SKU-Anzahl, Durchschnittspreise, Kategorie und Social-Media-Präsenz.",
       "Fair Pricing: Der Zalando-Preis darf nicht deutlich über dem eigenen Preis der Marke liegen (laut Gesprächen etwa 15 %), sonst sperrt Zalando den Artikel.",
       "Season Cleaning blockiert schwache Artikel. Möglich sind dann etwa 10 % Rabatt, ein Doppellisting unter neuer EAN oder Retagging. Size Availability unter etwa 80 % ist kritisch.",
       "Provision gestaffelt nach Geschlecht, Kategorie und Preis, Basis 7,18 %. Herren-Textil 30 bis 49,99 €: 16,18 %.",
       "Zalando ist direkt per API angebunden. Kennzahlen wie die Retourenquote siehst du in zDirect. Neue BrandHomes gehen derzeit nicht."],
      "Viel Reichweite für Mode, aber durch Retouren oft weniger Auszahlung als bei Amazon.",
      "Bestandskunden-Call (Sprache_001), Chef-Feedback Silbermoos, Einweisung Produktkalkulation, Einarbeitung Marktplatz-Integration, Deine Notizen",
      "t04-01 t04-02 t04-07 t11-07 t11-08 t11-01 t11-02 t11-03 t11-04 t11-05 t11-06 t11-09 "
      "t11-10 t04-12 t04-11 t11-11 t11-12 t10-09 t17-11 t32-05",
      "Fair Pricing, Season Cleaning und Size Availability stammen aus einer Gesprächsaufnahme. Intern bestätigen.")

thema("amazon", "Marktplätze", "Amazon",
      "Suchmaschine statt Katalog, wenig Retouren, BuyBox, Prime, ASIN und pauschale Provision.",
      ["Amazon funktioniert wie eine Suchmaschine: Der Kunde weiß meist, was er will. Die Retourenquote ist niedrig (laut Gesprächen etwa 2 bis 10 %), auch weil der Kunde das Retourenlabel selbst erzeugen muss.",
       "Provision in der HBOD-Excel: pauschal 15 % vom Bruttopreis, ohne Kategorie.",
       "Die BuyBox (das Feld „In den Warenkorb“) bekommt nur ein Händler. Es zählen Preis, Lieferzeit, Verfügbarkeit, Verkäuferqualität und Prime.",
       "Prime verlangt pünktliche Lieferung. HBOD hat Prime schon einmal verloren, weil Pakete zu spät ankamen. Zielwerte: Auftragsmängelquote unter 1 %, Stornoquote unter 2,5 %.",
       "Die ASIN ist Amazons Nummer für eine Produktseite. Der EAN-Nummernkreis muss zur Marke gehören, deshalb braucht HBOD für Bundles freie EANs der Marke.",
       "Bei FBA bleibt die Marke selbst Verkäufer. HBOD verkauft dagegen im eigenen Namen auf über 40 Marktplätzen. Werbeformate: Sponsored Products, Sponsored Brands, Sponsored Display."],
      "Bei gleichem Preis zahlt Amazon oft deutlich mehr aus als Zalando, weil weniger zurückkommt.",
      "Bestandskunden-Call (Sprache_001), Einweisung Produktkalkulation, Einarbeitung Marktplatz-Integration, Allgemeinwissen Amazon Seller Central, Company Profile 2026",
      "t04-01 t04-02 t12-12 t12-01 t04-04 t04-05 t12-05 t12-06 t03-04 t03-09 t12-08 t02-01 "
      "t10-01 t10-02 t05-01 t17-11 t32-01 t32-05",
      "Amazon kann Zielwerte ändern. Die Retourenquoten sind Richtwerte aus Gesprächen.")

thema("weitere-marktplaetze", "Marktplätze", "OTTO, ABOUT YOU und weitere Marktplätze",
      "Welche Rolle bol, Galaxus, Allegro, Kaufland, OTTO, ABOUT YOU und Co. spielen und wie HBOD angebunden ist.",
      ["Rollen: bol für die Niederlande und Belgien, Galaxus für die Schweiz, Allegro für Polen, Galeries Lafayette französisch und stark kuratiert, Limango und Veepee als Shopping-Clubs für Aktionen und Abverkauf.",
       "GALERIA (deutsches Kaufhaus) und Galeries Lafayette (Frankreich) sind verschiedene Marktplätze.",
       "ABOUT YOU: HBOD ist in sieben Ländern aktiv. Geplant ist die Migration vom Partner- ins Marktplatzmodell mit Direktanbindung.",
       "Anbindung: Zalando und OTTO direkt per API, Amazon und eBay über JTL, ABOUT YOU, Decathlon, Galaxus und andere über die Middleware Tradebyte, Kaufland und Galeries Lafayette über Mirakl. Middleware kostet Transaktionsgebühren, eine Direktanbindung viel IT-Aufwand.",
       "Basisprovisionen laut Excel: bol 5,7 %, Kaufland 14 %, OTTO 16,5 %. ABOUT YOU staffelt nach Geschlecht und Preis.",
       "Allegro ist interessant, die Integration bei HBOD ist aber noch nicht abgeschlossen. Vertbaudet soll bald dazukommen."],
      "Eine Anbindung ist keine Markenfreigabe.",
      "Chef-Mail Villa Sorgenfrei, Chef-Feedback Silbermoos, Einarbeitung Marktplatz-Integration, Einweisung Produktkalkulation, Deine Notizen",
      "t01-03 t04-08 t04-09 t04-10 t04-13 t25-09 t04-14 t05-01 t05-02 t05-03 t05-04 t05-06 t12-10 t12-11 t25-07 "
      "t12-02 t12-04 t12-07 t12-09 t02-14 t25-05 t29-04",
      "Stand Okt. 2026. Wie HBOD Kaufland genau anbindet und wann Vertbaudet startet, intern bestätigen.")

# ================= Recht, Steuern und Ausland =================

thema("vertrag", "Recht, Steuern und Ausland", "Der Vertrag",
      "Laufzeit, Kündigung, Eigentum, Haftung und Pflichten: was im HBOD-Vertrag steht und wie du es Kunden sagst.",
      ["Nicht exklusiv: Die Marke wählt Marktplätze und Länder selbst und darf daneben andere Händler beliefern.",
       "Mindestlaufzeit 6 Monate, danach automatische Verlängerung um je 6 Monate. Kündigung 3 Monate vor Laufzeitende, schriftlich.",
       "Restware nach Kündigung: Die Marke holt sie auf eigene Kosten ab oder erstattet die Rücksendung. Kündigt HBOD, trägt HBOD die Kosten. „Alle Kosten fallen auf 0“ ist falsch.",
       "Keine Mindestumsätze, aber Pflichten: bestätigte Liefermengen, Compliance (§ 10, z. B. Lieferkettengesetz) und die Laufzeitregel. Einen Anspruch auf Verkauf hat die Marke nicht.",
       "Die Marke haftet für Produktmängel, Produktsicherheit und Rückrufe. Die Ware im Lager ist versichert, Inventurdifferenzen über 2,5 % gleicht HBOD aus.",
       "Preisänderungen kündigt HBOD mindestens 1 Monat vorher an. Zahlt ein Marktplatz nicht, haftet HBOD nicht, treibt das Geld aber weiter ein."],
      "Keine Mindestumsätze, aber auch nicht „zu nichts verpflichtet“.",
      "Vertrag (Vorlage 2025) § 1 bis § 10, Laurins Feedback, Laurins Mail an Maag",
      "t21-01 t28-08 t21-02 t21-03 t21-04 t21-05 t21-06 t21-07 t27-12 t29-06 t21-08 t21-09 "
      "t32-02 t21-10 t21-11 t21-12 t21-13 t21-14 t21-15 t21-16 t21-17 t21-18 t09-09 t09-10 "
      "t24-09 t24-10",
      "Rechtsfragen sind Grundprinzipien zum Verstehen. Für verbindliche Aussagen den Vertrag des Kunden prüfen.")

thema("umsatzsteuer", "Recht, Steuern und Ausland", "Umsatzsteuer und Steuern im Ausland",
      "Grundprinzipien: Vorsteuer, OSS, Bestimmungslandprinzip, Konsignationslager und warum das HBOD-Modell Marken Registrierungen erspart.",
      ["Die Umsatzsteuer läuft durch: Die Marke verkauft an HBOD und führt die Steuer ab, HBOD zieht sie als Vorsteuer. Für beide ist sie keine Kostenposition.",
       "Ab 10.000 € Fernverkäufen an Privatkunden im EU-Ausland pro Jahr gilt die Steuer des Ziellands (Bestimmungslandprinzip). Gemeldet wird zentral über das OSS-Verfahren.",
       "HBOD verkauft im eigenen Namen an die Endkunden. Die Marke verkauft nur an HBOD in Deutschland und muss sich dafür nicht in anderen EU-Ländern registrieren.",
       "Eine Marke aus einem anderen EU-Land (z. B. Dänemark) kann die Konsignationslagerregelung (§ 6b UStG) nutzen, wenn die Ware innerhalb von 12 Monaten an HBOD verkauft wird.",
       "Marken aus Drittländern wie der Schweiz oder der Türkei müssen ihre Ware in die EU einführen: Zollanmeldung und Einfuhrumsatzsteuer.",
       "Schweiz: 8,1 % Mehrwertsteuer, Steuerpflicht ab 100.000 Franken Umsatz mit Kleinsendungen, seit 2025 Plattformbesteuerung. Großbritannien: 20 % VAT, bis 135 £ führt der Marktplatz die VAT ab."],
      "Die Marke verkauft an HBOD in Deutschland, HBOD verkauft an die Endkunden in Europa.",
      "Vertrag § 2 und § 4, Recherche (DATEV, § 6b UStG, ESTV), gov.uk, Silbermoos-Mail",
      "t14-01 t22-03 t22-04 t22-08 t22-09 t22-10 t22-11 t28-05 t22-12 t22-13 t22-14 t22-15 "
      "t22-16 t25-06 t25-10 t07-07",
      STEUER_HINWEIS)

thema("international", "Recht, Steuern und Ausland", "International verkaufen",
      "Welche Länder Priorität haben, was die Schweiz und Großbritannien besonders macht und warum Marken den Auslandsverkauf scheuen.",
      ["Priorität: zuerst DACH (Deutschland, Österreich, Schweiz), dann Benelux, dann z. B. Frankreich, Spanien, Polen, Dänemark.",
       "Im Ausland sind die Preise meist höher, weil der Versand teurer ist: unter 1 kg Österreich 5,52 €, Schweiz 8,19 €, Großbritannien 11,19 €, Bulgarien oder Zypern 15,70 €. Manche Länder lohnen sich nur mit höherem Preis.",
       "Schweiz: nicht in der EU, also Zollanmeldung und Einfuhrsteuer (seit 2024 kein Zoll auf Kleidung), dafür höheres Preisniveau. Laut Gesprächen ist die Schweiz der zweitgrößte Zalando-Markt.",
       "Großbritannien ist seit dem Brexit Drittland: Zollanmeldung und 20 % VAT.",
       "Viele Marken scheuen das Ausland wegen Steuerregistrierungen, Verpackungs-EPR in jedem Land, Sprache und Service sowie höherer Versand- und Retourenkosten. Genau das übernimmt HBOD.",
       "Retourenquoten unterscheiden sich je Land. Deshalb rechnet das MPE je Land mit eigenen Werten."],
      "Ehrlich trennen: Was wissen wir sicher, was müssen wir prüfen?",
      "ICP-Profil, Preisliste 10/2026, SECO, gov.uk, Company Profile 2026, Silbermoos-Mail",
      "t25-01 t25-02 t25-03 t13-05 t13-06 t25-12 t25-04 t11-06 t25-05 t25-06 t25-07 t25-08 "
      "t25-09 t25-10 t25-11 t22-13 t22-16 t23-06 t23-10 t32-06",
      "Die Aussage zu Zalando Schweiz stammt aus einer Gesprächsaufnahme. Intern bestätigen. Steuer- und Zollfragen: " + STEUER_HINWEIS)

thema("verpackung-epr", "Recht, Steuern und Ausland", "Verpackung, EPR und PPWR",
      "Erweiterte Herstellerverantwortung, LUCID, die neue EU-Verpackungsverordnung und Textil-EPR.",
      ["EPR heißt: Wer Verpackungen oder Produkte in Verkehr bringt, zahlt für Sammlung und Recycling. In Deutschland regelt das für Verpackungen das Verpackungsgesetz.",
       "Pflichten in Deutschland: Registrierung im LUCID, Systembeteiligung bei einem dualen System und Mengen melden. Marktplätze und Fulfillment-Dienstleister prüfen das seit Juli 2022.",
       "Für den Versandkarton ist der Verkäufer verantwortlich, bei HBOD-Verkäufen also HBOD. Für die Produktverpackung der Marke ist die Marke verantwortlich.",
       "Die PPWR (EU 2025/40) gilt seit 12.08.2026. Wer direkt an Endkunden in anderen EU-Ländern verkauft, kann dort als Hersteller gelten und braucht Registrierung und EPR, als EU-Firma zusätzlich einen Bevollmächtigten je Land.",
       "Eine Erleichterung beim Bevollmächtigten wird gerade verhandelt (Stand 30.10.2026). Bis zu einer Einigung gilt die Pflicht. Ab 2030 dürfen Versandpakete höchstens 50 % Leerraum haben.",
       "Textil-EPR: Alle EU-Staaten müssen bis etwa April 2028 Systeme für Kleidung und Schuhe einführen."],
      "PPWR regelt Verpackungen, GPSR die Produktsicherheit.",
      "Recherche (ZSVR, Händlerbund, Onlinemarktplatz, IT-Recht Kanzlei 10/2026, CMS Law), PPWR (EU 2025/40)",
      "t23-01 t23-02 t23-03 t23-04 t23-13 t23-05 t23-06 t23-07 t23-08 t23-09 t23-10 t23-11 "
      "t23-12 t25-10",
      "Der Stand zur PPWR ändert sich gerade schnell. Vor Kundengesprächen den neuesten Stand prüfen.")

thema("produktsicherheit", "Recht, Steuern und Ausland", "Produktsicherheit und Pflichtangaben",
      "GPSR, Textilkennzeichnung, Widerruf, Gewährleistung, Kosmetik und DSA.",
      ["Die GPSR (EU-Produktsicherheitsverordnung) gilt seit 13.12.2024. Jedes Angebot braucht Hersteller mit Anschrift und elektronischer Adresse, Warnhinweise und Angaben zur Identifikation. Sitzt der Hersteller außerhalb der EU, braucht es eine verantwortliche Person in der EU.",
       "Warnhinweise müssen gut sichtbar im Angebot stehen, nicht versteckt hinter PDF-Link oder QR-Code.",
       "Fehlende Angaben führen zu blockierten Artikeln und Abmahnungen. Deshalb sammelt HBOD die Daten im Onboarding mit dem Formular GPSR Data.",
       "Textilien: Faserzusammensetzung am Produkt und im Angebot. Kosmetik: verantwortliche Person in der EU und Notifizierung im CPNP.",
       "Widerrufsrecht 14 Tage, Gewährleistung 2 Jahre. Für Produktmängel und Rückrufe haftet laut Vertrag die Marke.",
       "Der DSA verlangt von Marktplätzen, ihre Verkäufer zu kennen: Ausweis, Zahlungskonto, Handelsregister und eine Selbstbescheinigung."],
      "Ohne GPSR-Daten kein Livegang.",
      "Recherche (Händlerbund, GPSR Art. 19), DSA Art. 30, Vertrag § 6 und § 7, Allgemeinwissen",
      "t24-01 t24-02 t24-03 t24-04 t24-05 t24-06 t24-07 t24-11 t24-08 t24-09 t21-12 t24-10 "
      "t24-12 t23-12",
      "Rechtsfragen sind Grundprinzipien zum Verstehen, keine Rechtsberatung.")
