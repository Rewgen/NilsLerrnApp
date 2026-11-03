"""Baut public/fragen.json aus den Fragen-Dateien q_a.py bis q_f.py, den Themen (themen.py),
der Pflegeliste für doppelte und verwandte Fragen (pflege.py) und Claudes Rückmeldungen (rueckmeldungen.py).

Aufruf (im Ordner inhalte):  python3 build.py

Jede Frage bekommt einen Fingerabdruck (fp) aus Fragetext, Antworten und Lösung.
Ändert sich eine Frage inhaltlich, ändert sich der Fingerabdruck. Die App setzt
den Fortschritt dann nur für genau diese Frage zurück und markiert sie als
"überarbeitet". Erklärung, Quelle und Hinweis zählen nicht zum Fingerabdruck.
"""
import hashlib, importlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import dsl  # noqa: E402

for m in ["q_a", "q_b", "q_c", "q_d", "q_e", "q_f"]:
    importlib.import_module(m)
import themen  # noqa: E402
import pflege  # noqa: E402
import rueckmeldungen  # noqa: E402
import aehnlich  # noqa: E402

VERSION = "2.3"
STAND = "2026-11-03"

# Was sich geändert hat (neueste zuerst). Wird in der App unter "Hilfe" angezeigt.
AENDERUNGEN = [
    {"datum": "2026-11-03", "version": "2.3", "punkte": [
        "Neu: Fragen bewerten mit Leicht, Mittel oder Schwer. Schwere Fragen kommen öfter, leichte seltener. Unter Heute, im Thema und bei Fehler kannst du nur die schweren lernen.",
        "Neu: Der Plus-Knopf unten rechts öffnet ein kleines Fenster für neue Fragen, Themen oder Erkenntnisse. Die App zeigt dir sofort, was es dazu schon gibt. Claude prüft das vor dem Einbau noch einmal genau.",
        "Neu: \"Anmerken\" unter jeder Frage, z. B. wenn eine Antwort nicht stimmt, etwas unklar ist oder eine Frage doppelt vorkommt. Auf Wunsch wird die Frage bis zur Prüfung nicht mehr abgefragt.",
        "Neu: Claude antwortet direkt an deiner Anmerkung in der App. Sie gilt dann als erledigt, du kannst sie wieder öffnen.",
        "Tagesrunde: höchstens 3 von 5 Fragen sind Wiederholungen, mindestens 2 sind neu. Richtige Antworten kommen nach 2, 4, 8, 15 und 30 Tagen wieder. Dieselbe Frage kommt nicht zweimal am selben Tag.",
        "Doppelte Fragen geprüft: 5 fast gleiche ausgeblendet (T02-10, T12-08, T13-11, T28-07, T31-10). 23 Gruppen ähnlicher Fragen kommen nie mehr am selben Tag dran.",
    ]},
    {"datum": "2026-11-03", "version": "2.2", "punkte": [
        "Neu: Themen zum Vertiefen, z. B. GMV, Provision, Retouren, Zalando oder EPR. Jedes Thema hat eine Kurzerklärung und sammelt die passenden Fragen aus allen Tests. Du lernst es in Runden zu 5 Fragen.",
        "Neu: Unter jeder Erklärung führt \"Thema vertiefen\" direkt zum passenden Thema.",
        "Neu: \"In Claude erklären lassen\" unter jeder Erklärung. Du legst einmal fest, in welchem Claude-Chat (z. B. im Projekt HBOD). Die App kopiert Frage, deine Antwort, Lösung und Erklärung und öffnet genau diesen Chat.",
        "Die Tagesrunde hat jetzt 5 statt 15 Fragen. Du kannst weiter 10, 15 oder 20 wählen.",
        "Der Bericht für Claude zeigt jetzt auch den Stand je Thema.",
    ]},
    {"datum": "2026-10-30", "version": "2.1", "punkte": [
        "Neu: Schnelle Runde mit 5 oder 10 Fragen unter \"Heute\", auch je Modul und je Test. Ohne Freitext, mit Serie für richtige Antworten in Folge.",
        "Neu: Am PC wählst du mit den Tasten 1 bis 9 eine Antwort, Enter prüft und geht weiter.",
        "Wiederholungsplan genauer: Richtig vor dem Termin festigt, zählt aber erst am Termin. Gemeistert heißt dreimal zum Termin richtig.",
        "Faktencheck im Internet: Stand zur PPWR-Aussetzung nach Parlament (20.10.) und Rat (21.10.2026) neu.",
        "Korrigiert: Die Schweiz erhebt seit 2024 keinen Zoll mehr auf Kleidung, Anmeldung und Einfuhrsteuer bleiben. Dazu Plattformbesteuerung seit 2025.",
        "Korrigiert: Der DSA verlangt Ausweis, Zahlungskonto, Handelsregister und Selbstbescheinigung, Steuerdaten kommen aus DAC7.",
        "Ergänzt: Kleinsendungen ab 1.11.2026 mit 2 € Bearbeitungsgebühr und Produktkennung, UK-Regel für Ware im Land, Textil-EPR bis etwa April 2028.",
        "Genauer: adidas-Wäschelizenz liegt bei Schiessers Mutter Delta Galil, Schreibweise JTL-eazyAuction, Hinweis zur Kaufland-Anbindung.",
    ]},
    {"datum": "2026-10-30", "version": "2.0", "punkte": [
        "Die App läuft jetzt als eigene Website. Mit einem Lern-Code ist dein Fortschritt auf Handy und PC gleich.",
        "Neu: Tagesrunde mit Wiederholungsplan. Was du richtig weißt, kommt nach 1, 3, 7, 14 und 30 Tagen wieder, Fehler am nächsten Tag.",
        "Neu: \"Ich bin unsicher\" vor dem Prüfen, Lernzettel je Test und Selbstbewertung von Freitexten mit Kernpunkten.",
        "Alles aus dem entfernten KAM-Dokument geprüft: Quellen ersetzt durch Gesprächsaufnahmen, Vertrag, Company Profile und Excel.",
        "Versandpreise auf die Preisliste 10/2026 aktualisiert (Österreich 5,52 €, Schweiz 8,19 €, Großbritannien 11,19 €).",
        "Korrigiert: UVP ist keine feste Obergrenze, ABOUT-YOU-Länder, Black-Friday-Entscheidung, Betreuungsrhythmus, Defektware, Size Availability, Brand Info.",
        "Entfernt: Galeria-Insolvenz und alle Fragen zum Markencheck.",
        "Neu: Fragen zu deinen Mail-Regeln, zur OTTO-Verkäuferinfo, zu Lizenzen und zu Vertbaudet.",
    ]},
    {"datum": "2026-10-29", "version": "1.0", "punkte": ["Erste Version mit 32 Tests."]},
]


def fingerabdruck(f):
    teile = {k: f.get(k) for k in ("typ", "frage", "optionen", "loesung", "paare", "elemente",
                                     "muster", "kernpunkte", "einheit", "toleranz")}
    roh = json.dumps(teile, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(roh.encode("utf-8")).hexdigest()[:10]


ids, fehler, typen, n = set(), [], {}, 0
for t in dsl.TESTS:
    for f in t["fragen"]:
        n += 1
        typen[f["typ"]] = typen.get(f["typ"], 0) + 1
        if f["id"] in ids:
            fehler.append("doppelte id " + f["id"])
        ids.add(f["id"])
        if f["typ"] in ("single", "multi") and len(set(f["optionen"])) != len(f["optionen"]):
            fehler.append("doppelte Option " + f["id"])
        if f["typ"] == "zuordnen":
            rechts = [p[1] for p in f["paare"]]
            if len(set(rechts)) != len(rechts):
                fehler.append("doppelte rechte Seite " + f["id"])
        for k in ("frage", "erklaerung"):
            if not f.get(k):
                fehler.append(f"fehlt {k} " + f["id"])
        f["fp"] = fingerabdruck(f)

# ---------- Doppelte und verwandte Fragen (pflege.py) ----------
nach_id = {f["id"]: f for t in dsl.TESTS for f in t["fragen"]}
for q, grund in pflege.AUSBLENDEN.items():
    if q not in nach_id:
        fehler.append("AUSBLENDEN: unbekannte Frage " + q)
    elif not grund:
        fehler.append("AUSBLENDEN: Grund fehlt bei " + q)
    else:
        nach_id[q]["aus"] = grund
verwandt_von = {}
for i, (gruppe, titel) in enumerate(pflege.VERWANDT, 1):
    qs = gruppe.split()
    if len(qs) < 2 or not titel:
        fehler.append(f"VERWANDT: Gruppe {i} braucht mindestens 2 Fragen und einen Titel")
    for q in qs:
        if q not in nach_id:
            fehler.append(f"VERWANDT: unbekannte Frage {q}")
        elif q in verwandt_von:
            fehler.append(f"VERWANDT: {q} steht in mehreren Gruppen")
        elif nach_id[q].get("aus"):
            fehler.append(f"VERWANDT: {q} ist ausgeblendet")
        else:
            verwandt_von[q] = f"v{i:02d}"
            nach_id[q]["verwandt"] = f"v{i:02d}"
geprueft = set()
for p in pflege.GEPRUEFT:
    qs = p.split()
    if len(qs) != 2 or any(q not in nach_id for q in qs):
        fehler.append("GEPRUEFT: ungültiges Paar " + p)
    geprueft.add(frozenset(qs))
sichtbar = [f for f in nach_id.values() if not f.get("aus")]
neue_doppel = aehnlich.moegliche_doppel(sichtbar, verwandt_von, geprueft)

# ---------- Rückmeldungen von Claude ----------
rueck = {}
for r in rueckmeldungen.RUECKMELDUNGEN:
    if not re.fullmatch(r"[a-z0-9]{4,40}", r.get("id", "")):
        fehler.append("Rückmeldung: ungültige Notiz-ID " + str(r.get("id")))
    elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?Z?", r.get("zeit", "")):
        fehler.append(f"Rückmeldung {r['id']}: Zeit im Format 2026-11-04T09:30:00Z angeben")
    elif not r.get("text"):
        fehler.append(f"Rückmeldung {r['id']}: Text fehlt")
    else:
        z = r["zeit"] if r["zeit"].endswith("Z") else r["zeit"] + "Z"
        if len(z) == 17:
            z = z[:-1] + ":00Z"
        rueck[r["id"]] = {"zeit": z, "text": r["text"]}

# ---------- Themen prüfen ----------
themen_ids, in_thema = set(), set()
for th in themen.THEMEN:
    tid = th["id"]
    if not re.fullmatch(r"[a-z0-9-]{2,40}", tid):
        fehler.append("ungültige Themen-ID " + tid)
    if tid in themen_ids:
        fehler.append("doppelte Themen-ID " + tid)
    themen_ids.add(tid)
    if th["gruppe"] not in themen.GRUPPEN:
        fehler.append(f"Thema {tid}: unbekannte Gruppe {th['gruppe']}")
    for k in ("titel", "kurz", "punkte", "merksatz", "quelle"):
        if not th.get(k):
            fehler.append(f"Thema {tid}: fehlt {k}")
    if len(set(th["fragen"])) != len(th["fragen"]):
        fehler.append(f"Thema {tid}: doppelte Frage")
    for q in th["fragen"]:
        if q not in ids:
            fehler.append(f"Thema {tid}: unbekannte Frage {q}")
        elif nach_id[q].get("aus"):
            fehler.append(f"Thema {tid}: {q} ist ausgeblendet")
        in_thema.add(q)
    if len(th["fragen"]) < 6:
        fehler.append(f"Thema {tid}: nur {len(th['fragen'])} Fragen (mindestens 6)")

daten = {
    "version": VERSION,
    "stand": STAND,
    "titel": "HBOD Lern-App",
    "bestehen_ab": 0.8,
    "aenderungen": AENDERUNGEN,
    "module": dsl.MODULE,
    "tests": dsl.TESTS,
    "themengruppen": themen.GRUPPEN,
    "themen": themen.THEMEN,
    "verwandt": [{"id": f"v{i:02d}", "titel": titel, "fragen": g.split()} for i, (g, titel) in enumerate(pflege.VERWANDT, 1)],
    "rueckmeldungen": rueck,
}
ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, "..", "public", "fragen.json")
with open(ziel, "w", encoding="utf-8") as fh:
    json.dump(daten, fh, ensure_ascii=False, separators=(",", ":"))
print("Tests:", len(dsl.TESTS), "Fragen:", n, typen)
print("Sichtbar:", len(sichtbar), "· ausgeblendet:", len(pflege.AUSBLENDEN), "· verwandte Gruppen:", len(pflege.VERWANDT), "· Rückmeldungen:", len(rueck))
print("Themen:", len(themen.THEMEN), "· sichtbare Fragen ohne Thema:", len({f["id"] for f in sichtbar} - in_thema))
if neue_doppel:
    print(f"Hinweis: {len(neue_doppel)} mögliche neue Doppel, z. B.", ", ".join(f"{a.upper()}/{b.upper()}" for _, a, b in neue_doppel[:5]),
          "· Details: python3 inhalte/doppelte.py")
else:
    print("Mögliche neue Doppel: keine")
print("Fehler:", fehler or "keine")
if fehler:
    sys.exit(1)
