# Kleine Hilfs-DSL, um den Fragenkatalog kompakt zu schreiben.
# Konvention: Bei S() ist die ERSTE Option immer die richtige (die App mischt die Reihenfolge).

TESTS = []
MODULE = []


def modul(mid, titel, beschreibung):
    MODULE.append({"id": mid, "titel": titel, "beschreibung": beschreibung, "tests": []})


def test(tid, mid, titel, beschreibung, fragen):
    for i, f in enumerate(fragen, 1):
        f["id"] = f"{tid}-{i:02d}"
    TESTS.append({"id": tid, "modul": mid, "titel": titel, "beschreibung": beschreibung, "fragen": fragen})
    for m in MODULE:
        if m["id"] == mid:
            m["tests"].append(tid)


def _base(typ, frage, erklaerung, quelle, hinweis):
    d = {"typ": typ, "frage": frage, "erklaerung": erklaerung}
    if quelle:
        d["quelle"] = quelle
    if hinweis:
        d["hinweis"] = hinweis
    return d


def S(frage, optionen, erklaerung, quelle="", hinweis=None):
    """Einfachauswahl. optionen[0] ist richtig."""
    d = _base("single", frage, erklaerung, quelle, hinweis)
    d["optionen"] = list(optionen)
    d["loesung"] = 0
    return d


def M(frage, richtig, falsch, erklaerung, quelle="", hinweis=None):
    """Mehrfachauswahl: alle richtigen ankreuzen."""
    d = _base("multi", frage, erklaerung, quelle, hinweis)
    d["optionen"] = list(richtig) + list(falsch)
    d["loesung"] = list(range(len(richtig)))
    return d


def W(frage, wahr, erklaerung, quelle="", hinweis=None):
    d = _base("wahr", frage, erklaerung, quelle, hinweis)
    d["loesung"] = bool(wahr)
    return d


def Z(frage, wert, erklaerung, einheit="€", dez=2, toleranz=None, quelle="", hinweis=None):
    d = _base("zahl", frage, erklaerung, quelle, hinweis)
    d["loesung"] = round(float(wert), dez)
    d["einheit"] = einheit
    d["dezimalen"] = dez
    d["toleranz"] = toleranz if toleranz is not None else (0.5 * 10 ** (-dez) + 1e-9 if dez > 0 else 0.5)
    return d


def R(frage, reihenfolge, erklaerung, quelle="", hinweis=None):
    """Reihenfolge: Elemente in der richtigen Reihenfolge angeben."""
    d = _base("reihe", frage, erklaerung, quelle, hinweis)
    d["elemente"] = list(reihenfolge)
    return d


def P(frage, paare, erklaerung, quelle="", hinweis=None):
    """Zuordnen: Liste von (links, rechts)."""
    d = _base("zuordnen", frage, erklaerung, quelle, hinweis)
    d["paare"] = [list(p) for p in paare]
    return d


def T(frage, muster, kernpunkte, erklaerung="", quelle="", hinweis=None, mail=False):
    """Freitext: wird in der App von Claude gegen Musterlösung und Kernpunkte bewertet."""
    d = _base("text", frage, erklaerung or "Vergleiche deine Antwort mit der Musterlösung und den Kernpunkten.", quelle, hinweis)
    d["muster"] = muster
    d["kernpunkte"] = list(kernpunkte)
    if mail:
        d["mail"] = True
    return d
