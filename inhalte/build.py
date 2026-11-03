"""Baut public/fragen.json aus den Fragen-Dateien q_a.py bis q_f.py und den Themen in themen.py.

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

VERSION = "2.2"
STAND = "2026-11-03"

# Was sich geändert hat (neueste zuerst). Wird in der App unter "Hilfe" angezeigt.
AENDERUNGEN = [
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
}
ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, "..", "public", "fragen.json")
with open(ziel, "w", encoding="utf-8") as fh:
    json.dump(daten, fh, ensure_ascii=False, separators=(",", ":"))
print("Tests:", len(dsl.TESTS), "Fragen:", n, typen)
print("Themen:", len(themen.THEMEN), "· Fragen ohne Thema:", len(ids - in_thema))
print("Fehler:", fehler or "keine")
if fehler:
    sys.exit(1)
