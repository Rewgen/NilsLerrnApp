"""Baut public/fragen.json aus den Fragen-Dateien q_a.py bis q_f.py.

Aufruf (im Ordner inhalte):  python3 build.py

Jede Frage bekommt einen Fingerabdruck (fp) aus Fragetext, Antworten und Lösung.
Ändert sich eine Frage inhaltlich, ändert sich der Fingerabdruck. Die App setzt
den Fortschritt dann nur für genau diese Frage zurück und markiert sie als
"überarbeitet". Erklärung, Quelle und Hinweis zählen nicht zum Fingerabdruck.
"""
import hashlib, importlib, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import dsl  # noqa: E402

for m in ["q_a", "q_b", "q_c", "q_d", "q_e", "q_f"]:
    importlib.import_module(m)

VERSION = "2.0"
STAND = "2026-10-30"

# Was sich geändert hat (neueste zuerst). Wird in der App unter "Hilfe" angezeigt.
AENDERUNGEN = [
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

daten = {
    "version": VERSION,
    "stand": STAND,
    "titel": "HBOD Lern-App",
    "bestehen_ab": 0.8,
    "aenderungen": AENDERUNGEN,
    "module": dsl.MODULE,
    "tests": dsl.TESTS,
}
ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, "..", "public", "fragen.json")
with open(ziel, "w", encoding="utf-8") as fh:
    json.dump(daten, fh, ensure_ascii=False, separators=(",", ":"))
print("Tests:", len(dsl.TESTS), "Fragen:", n, typen)
print("Fehler:", fehler or "keine")
if fehler:
    sys.exit(1)
