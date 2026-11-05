# Kurzschreibweise für den Fragenkatalog.
#
# Aufbau: Bereiche (modul, A bis F) enthalten Stapel (stapel), Stapel enthalten Fragen.
# Jede Frage hat eine feste ID (erster Parameter, z. B. "t01-05"). Die ID bleibt für immer gleich,
# auch wenn die Frage verschoben wird. Neue Fragen bekommen die nächste freie Nummer im Stapel.
# Gelöschte IDs nicht neu vergeben.
# Bei S() ist die ERSTE Option immer die richtige (die App mischt die Reihenfolge).

MODULE = []
STAPEL = []


def modul(mid, titel, beschreibung):
    MODULE.append({"id": mid, "titel": titel, "beschreibung": beschreibung, "stapel": []})


def stapel(sid, mid, titel, beschreibung, fragen, punkte=None, merksatz=None, quelle=None, hinweis=None):
    """Ein Stapel (wie in Anki). punkte/merksatz: Kurzerklärung "Das Wichtigste" zum Einlesen."""
    s = {"id": sid, "modul": mid, "titel": titel, "beschreibung": beschreibung, "fragen": fragen}
    if punkte:
        s["punkte"] = list(punkte)
    if merksatz:
        s["merksatz"] = merksatz
    if quelle:
        s["quelle"] = quelle
    if hinweis:
        s["hinweis"] = hinweis
    STAPEL.append(s)
    for m in MODULE:
        if m["id"] == mid:
            m["stapel"].append(sid)


def _base(qid, typ, frage, erklaerung, quelle, hinweis):
    d = {"id": qid, "typ": typ, "frage": frage, "erklaerung": erklaerung}
    if quelle:
        d["quelle"] = quelle
    if hinweis:
        d["hinweis"] = hinweis
    return d


def S(qid, frage, optionen, erklaerung, quelle="", hinweis=None):
    """Einfachauswahl. optionen[0] ist richtig."""
    d = _base(qid, "single", frage, erklaerung, quelle, hinweis)
    d["optionen"] = list(optionen)
    d["loesung"] = 0
    return d


def M(qid, frage, richtig, falsch, erklaerung, quelle="", hinweis=None):
    """Mehrfachauswahl: alle richtigen ankreuzen."""
    d = _base(qid, "multi", frage, erklaerung, quelle, hinweis)
    d["optionen"] = list(richtig) + list(falsch)
    d["loesung"] = list(range(len(richtig)))
    return d


def W(qid, frage, wahr, erklaerung, quelle="", hinweis=None):
    d = _base(qid, "wahr", frage, erklaerung, quelle, hinweis)
    d["loesung"] = bool(wahr)
    return d


def Z(qid, frage, wert, erklaerung, einheit="€", dez=2, toleranz=None, quelle="", hinweis=None):
    d = _base(qid, "zahl", frage, erklaerung, quelle, hinweis)
    d["loesung"] = round(float(wert), dez)
    d["einheit"] = einheit
    d["dezimalen"] = dez
    d["toleranz"] = toleranz if toleranz is not None else (0.5 * 10 ** (-dez) + 1e-9 if dez > 0 else 0.5)
    return d


def R(qid, frage, reihenfolge, erklaerung, quelle="", hinweis=None):
    """Reihenfolge: Elemente in der richtigen Reihenfolge angeben."""
    d = _base(qid, "reihe", frage, erklaerung, quelle, hinweis)
    d["elemente"] = list(reihenfolge)
    return d


def P(qid, frage, paare, erklaerung, quelle="", hinweis=None):
    """Zuordnen: Liste von (links, rechts)."""
    d = _base(qid, "zuordnen", frage, erklaerung, quelle, hinweis)
    d["paare"] = [list(p) for p in paare]
    return d


def T(qid, frage, muster, kernpunkte, erklaerung="", quelle="", hinweis=None, mail=False):
    """Freitext: Nils schreibt (optional), deckt die Musterlösung auf und bewertet sich selbst."""
    d = _base(qid, "text", frage, erklaerung or "Vergleiche deine Antwort mit der Musterlösung und den Kernpunkten.", quelle, hinweis)
    d["muster"] = muster
    d["kernpunkte"] = list(kernpunkte)
    if mail:
        d["mail"] = True
    return d
