"""Baut public/fragen.json aus q_a.py bis q_f.py (Bereiche, Stapel, Fragen), pflege.py (verwandte Fragen)
und rueckmeldungen.py (Claudes Antworten auf Nils' Notizen).

Aufruf:  python3 inhalte/build.py

Jede Frage hat eine feste ID und einen Fingerabdruck (fp) aus Fragetext, Antworten und Lösung.
Ändert sich eine Frage inhaltlich, ändert sich der Fingerabdruck. Die App setzt den Fortschritt dann
nur für genau diese Frage zurück. Erklärung, Quelle und Hinweis zählen nicht zum Fingerabdruck.
"""
import hashlib, importlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import dsl  # noqa: E402

for m in ["q_a", "q_b", "q_c", "q_d", "q_e", "q_f"]:
    importlib.import_module(m)
import pflege  # noqa: E402
import rueckmeldungen  # noqa: E402
import aehnlich  # noqa: E402

VERSION = "3.0"
STAND = "2026-11-05"

# Was sich geändert hat (neueste zuerst). Wird in der App unter "Einstellungen" angezeigt.
# Keine Kunden- oder Firmeninterna hier eintragen: die Datei ist öffentlich abrufbar.
AENDERUNGEN = [
    {"datum": "2026-11-05", "version": "3.0", "punkte": [
        "Neu aufgebaut nach dem Vorbild Anki: Bereiche A bis F mit Stapeln. Jeder Stapel zeigt, wie viele Fragen neu und fällig sind und wie viele du schon gemeistert hast.",
        "Nach einer richtigen Antwort tippst du Schwer, Gut oder Leicht. Auf jedem Knopf steht, wann die Frage wiederkommt. Falsche Fragen kommen am Ende der Runde noch einmal.",
        "Weggefallen: Prüfungsmodus, Prüfungssimulation, Serien, Bestanden, Tage in Folge und die getrennte Themen-Seite. Die Kurzerklärungen stehen jetzt direkt im Stapel.",
        "Alle Kundennamen, Kundenzahlen, Vertragsdetails, interne Strategie, Vorfälle, Pläne und interne Technik entfernt. Kalkulationen nutzen neutrale Beispiele.",
        "Nach deiner Notiz korrigiert: GMV wird nicht überall gleich definiert. Zalando rechnet nach Retouren, allgemein ist meist der Wert vor Retouren gemeint.",
        "Neu aus deinen Notizen: Kommittent, Bedingungen des Kommissionsgeschäfts, Gelegenheitskommissionär, Blitz-Eigentum, Logistik und Fulfillment, GTIN-Arten, viele Klicks ohne Käufe und mehr Fragen zum Ankreuzen.",
        "Freitexte: Lösung aufdecken und selbst bewerten, ohne Kernpunkte abzuhaken.",
    ]},
    {"datum": "2026-11-03", "version": "2.3", "punkte": ["Bewertung, Anmerken, Wünsche mit Prüfung, Rückmeldungen von Claude und eine gemischte Tagesrunde."]},
    {"datum": "2026-11-03", "version": "2.2", "punkte": ["Themen, Claude-Chats und eine Tagesrunde mit 5 Fragen."]},
    {"datum": "2026-10-30", "version": "2.1", "punkte": ["Schnelle Runde, Tastatur am PC und ein Faktencheck im Internet."]},
    {"datum": "2026-10-30", "version": "2.0", "punkte": ["Eigene Website mit Sync zwischen Handy und PC."]},
    {"datum": "2026-10-29", "version": "1.0", "punkte": ["Erste Version."]},
]

QID = re.compile(r"t\d{2}-\d{2}")
SID = re.compile(r"t\d{2}")


def fingerabdruck(f):
    teile = {k: f.get(k) for k in ("typ", "frage", "optionen", "loesung", "paare", "elemente",
                                     "muster", "kernpunkte", "einheit", "toleranz")}
    roh = json.dumps(teile, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(roh.encode("utf-8")).hexdigest()[:10]


fehler, typen, nach_id = [], {}, {}
sids = set()
for s in dsl.STAPEL:
    if not SID.fullmatch(s["id"]) or s["id"] in sids:
        fehler.append("ungültige oder doppelte Stapel-ID " + s["id"])
    sids.add(s["id"])
    if not s["fragen"]:
        fehler.append(f"Stapel {s['id']} ist leer")
    for f in s["fragen"]:
        q = f["id"]
        if not QID.fullmatch(q):
            fehler.append("ungültige Frage-ID " + q)
        if q in nach_id:
            fehler.append("doppelte Frage-ID " + q)
        nach_id[q] = f
        typen[f["typ"]] = typen.get(f["typ"], 0) + 1
        if f["typ"] in ("single", "multi") and len(set(f["optionen"])) != len(f["optionen"]):
            fehler.append("doppelte Option " + q)
        if f["typ"] == "multi" and not f["loesung"]:
            fehler.append("Mehrfachauswahl ohne richtige Antwort " + q)
        if f["typ"] == "zuordnen":
            rechts = [p[1] for p in f["paare"]]
            if len(set(rechts)) != len(rechts):
                fehler.append("doppelte rechte Seite " + q)
        for k in ("frage", "erklaerung"):
            if not f.get(k):
                fehler.append(f"fehlt {k} " + q)
        if not f.get("quelle"):
            fehler.append("fehlt quelle " + q)
        f["fp"] = fingerabdruck(f)
for m in dsl.MODULE:
    if not m["stapel"]:
        fehler.append(f"Bereich {m['id']} hat keine Stapel")

# ---------- Verwandte und gelöschte Fragen (pflege.py) ----------
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
        else:
            verwandt_von[q] = f"v{i:02d}"
            nach_id[q]["verwandt"] = f"v{i:02d}"
geprueft = set()
for p in pflege.GEPRUEFT:
    qs = p.split()
    if len(qs) != 2 or any(q not in nach_id for q in qs):
        fehler.append("GEPRUEFT: ungültiges Paar " + p)
    geprueft.add(frozenset(qs))
for q in pflege.GELOESCHT:
    if q in nach_id:
        fehler.append(f"{q} steht in pflege.GELOESCHT und darf nicht neu vergeben werden")
neue_doppel = aehnlich.moegliche_doppel(list(nach_id.values()), verwandt_von, geprueft)

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

daten = {
    "version": VERSION,
    "stand": STAND,
    "titel": "HBOD Lern-App",
    "aenderungen": AENDERUNGEN,
    "module": dsl.MODULE,
    "stapel": dsl.STAPEL,
    "verwandt": [{"id": f"v{i:02d}", "titel": t, "fragen": g.split()} for i, (g, t) in enumerate(pflege.VERWANDT, 1)],
    "rueckmeldungen": rueck,
}
ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, "..", "public", "fragen.json")
if not fehler:
    with open(ziel, "w", encoding="utf-8") as fh:
        json.dump(daten, fh, ensure_ascii=False, separators=(",", ":"))
print("Bereiche:", len(dsl.MODULE), "· Stapel:", len(dsl.STAPEL), "· Fragen:", len(nach_id), typen)
print("Verwandte Gruppen:", len(pflege.VERWANDT), "· Rückmeldungen:", len(rueck))
if neue_doppel:
    print(f"Hinweis: {len(neue_doppel)} mögliche neue Doppel, z. B.", ", ".join(f"{a.upper()}/{b.upper()}" for _, a, b in neue_doppel[:5]),
          "· Details: python3 inhalte/doppelte.py")
else:
    print("Mögliche neue Doppel: keine")
print("Fehler:", fehler or "keine")
if fehler:
    sys.exit(1)
