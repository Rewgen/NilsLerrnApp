from dsl import *

modul("F", "Praxisfälle", "Gemischte Fälle aus dem Alltag, bei denen du Wissen aus allen Bereichen verbindest")

stapel("t32", "F", "Praxisfälle aus dem Alltag",
    "Erkläre Kunden komplexe Dinge in einfachen Worten.", [
    T("t32-01", "Ein Kunde fragt: \"Was macht ihr eigentlich anders als Amazon FBA?\" Erkläre es in 3 bis 5 Sätzen.",
      "Bei FBA bleibt die Marke selbst Verkäufer auf Amazon und macht Produktseiten, Preise, Werbung, Steuern und Kundenkontakt selbst. Amazon übernimmt nur Lager, Versand und Retouren, und das nur für Amazon. HBOD verkauft im eigenen Namen auf über 40 Marktplätzen, nicht nur auf Amazon. Wir übernehmen zusätzlich Produktdaten, Preise je Marktplatz, Werbung, Kundenservice sowie Steuer- und Zollthemen. Alle Kanäle laufen aus einem Lager, und Sie bekommen eine Monatsabrechnung.",
      ["FBA: Marke bleibt Verkäufer und macht alles außer Logistik selbst", "FBA gilt nur für Amazon", "HBOD verkauft im eigenen Namen auf vielen Marktplätzen", "HBOD übernimmt zusätzlich Content, Preise, Werbung, Service, Steuer/Zoll", "Ein Lager für alle Kanäle, eine Abrechnung"],
      erklaerung="", quelle="Einarbeitungs-Chat, Unternehmenspräsentation 2026", hinweis="Aus dem Einarbeitungs-Chat. Intern bestätigen."),
    T("t32-03", "Ein Kunde fragt: \"Warum stehen bei euch 17,40 € pro Warenkorb, aber 18,12 € pro Artikel? Das passt doch nicht.\" Erkläre den Rechenweg einfach.",
      "Die 17,40 € gelten für eine ganze Bestellung. Im Schnitt enthält eine Bestellung 1,2 Artikel. Bei 20 % Retouren behält der Kunde davon aber nur 0,96 Artikel, weil ein Teil zurückkommt. Geld bleibt nur für die behaltenen Artikel übrig, deshalb teilen wir 17,40 € durch 0,96 und kommen auf 18,12 € pro Artikel. Die Kosten der Retouren sind damit schon auf die behaltenen Artikel verteilt.",
      ["17,40 € gelten pro Bestellung (Warenkorb)", "1,2 Artikel pro Bestellung, davon bei 20 % Retouren 0,96 behalten", "17,40 ÷ 0,96 = 18,12 €", "Retourenkosten sind auf die behaltenen Artikel umgelegt"],
      erklaerung="", quelle="Beispielkalkulation (Einweisung)"),
    Z("t32-04", "Gleicher Fall: Netto-Verkaufspreis 37,73 €, Auszahlung pro Artikel 18,12 €. Wie hoch ist die Auszahlungsquote in Prozent?", 48.0,
      "18,12 ÷ 37,73 = 48,0 %. Laut Faustregel sehr gut.", einheit="%", dez=1, toleranz=0.11, quelle="Beispielkalkulation (Einweisung)"),
    T("t32-05", "Ein Kunde fragt: \"Lohnt sich für mich Zalando oder Amazon mehr?\" Antworte ehrlich und hilfreich (3 bis 5 Sätze).",
      "Das hängt vor allem von der Retourenquote, der Provision und dem Preis ab. Amazon zahlt bei gleichem Preis oft deutlich mehr aus, weil dort viel weniger zurückgeschickt wird. Zalando bringt dafür viel Reichweite für Mode, und Kunden lassen sich dort inspirieren. Deshalb rechnen wir den Preis für jeden Marktplatz einzeln, damit Ihre Mindestauszahlung überall erreicht wird. Gern zeige ich Ihnen das an zwei Ihrer Artikel.",
      ["Abhängig von Retourenquote, Provision und Preis", "Amazon oft höhere Auszahlung wegen weniger Retouren", "Zalando: Reichweite und Inspiration für Mode", "Preis je Marktplatz berechnen (MPE, Mindestauszahlung)", "Konkrete Beispielrechnung anbieten"],
      erklaerung="", quelle="Gespräch mit Kollegen (Erfahrungswert), Unternehmenspräsentation 2026", hinweis="Erfahrungswert aus einem Gespräch. Intern bestätigen."),
    T("t32-06", "Eine Marke aus der Schweiz möchte über HBOD in der EU verkaufen. Welche Themen sprichst du im Erstgespräch an? Nenne mindestens vier.",
      "Die Ware muss für das Lager in Mülheim in die EU eingeführt werden, also Zoll und Einfuhrumsatzsteuer. Wer Importeur ist und wie die Steuer läuft, klären wir mit unserer Buchhaltung. Für die GPSR braucht die Marke eine verantwortliche Person in der EU. Auch Verpackungsregeln und Registrierungen spielen eine Rolle. Die Ware muss für die HBOD-Kanäle vollständig bei uns eingelagert werden. Dazu kommen Kanalfreigaben, Stammdaten und eine Beispielkalkulation.",
      ["Einfuhr in die EU: Zoll und Einfuhrumsatzsteuer, Importeur klären", "GPSR: verantwortliche Person in der EU", "Verpackung/EPR und Registrierungen", "Einlagerung bei HBOD als Voraussetzung", "Steuerfragen mit der Buchhaltung klären statt selbst zusagen"],
      erklaerung="", quelle="Modul Recht und Steuern"),
    T("t32-07", "Erkläre einem Kunden in einfachen Worten, wie die Monatsabrechnung von HBOD aufgebaut ist.",
      "Einmal im Monat sammeln wir alle Verkäufe von allen Marktplätzen und schicken Ihnen eine Gutschrift. Ausgangspunkt ist der Umsatz nach Retouren. Davon gehen die Marktplatzprovisionen, unsere Provision und die Logistik ab, also Picking, Verpackung, Versand, Retourenbearbeitung und Lager. Was übrig bleibt, ist Ihre Auszahlung. Dazu bekommen Sie eine Aufstellung mit jeder einzelnen Transaktion.",
      ["Monatliche Gutschrift über alle Marktplätze", "Basis ist der Umsatz nach Retouren", "Abzüge: Marktplatzprovision, HBOD-Provision, Logistik, Retourenkosten, Lager", "Ergebnis ist die Auszahlung", "Aufstellung mit jeder Transaktion für Transparenz"],
      erklaerung="", quelle="Einweisung Produktkalkulation, Unternehmenspräsentation 2026"),
    T("t32-08", "Ein Kunde fragt: \"Seid ihr eigentlich ein Fulfillment-Dienstleister?\" Antworte in 2 bis 4 Sätzen so, dass der Unterschied klar wird.",
      "Wir machen Fulfillment, aber nicht nur. Ein reiner Fulfillment-Dienstleister lagert und versendet nur, das Marktplatzkonto und den Verkauf managen Sie dann selbst. Wir verkaufen Ihre Ware im eigenen Namen auf über 40 Marktplätzen und übernehmen auch Produktseiten, Preise, Werbung, Kundenservice und die Abrechnung. Deshalb sprechen wir von Full-Service.",
      ["Fulfillment ja, aber nicht nur", "Reines Fulfillment: nur Logistik, Marke managt Verkauf und Konto selbst", "HBOD verkauft im eigenen Namen und übernimmt das Operative", "Begriff Full-Service erklären"],
      erklaerung="", quelle="Einarbeitung"),
])
