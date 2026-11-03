"""Ähnlichkeit von Fragen und Texten (TF-IDF). Genutzt von build.py, suche.py und doppelte.py.

Die App nutzt im Fenster "Hinzufügen" und beim Anmerken "Doppelt" dieselbe Idee in JavaScript.
"""
import math
import os
import re
import sys
from collections import Counter

STOP = set("""der die das ein eine einer eines einem einen und oder ist sind was wie wer wo warum wann welche
welcher welches bei mit von für auf aus im in an zu zum zur den dem des nicht kein keine es sie er man du ich wir ihr
hbod sich auch als dass so nur noch dann wenn über etwa je pro bis vom am um wird werden kann muss darf hat haben
gibt mehr sehr oft kreuze alles richtige richtig falsch marke kunde kunden ihre ihren deine deiner dein diese dieser
dieses""".split())


def woerter(text):
    return [w[:7] for w in re.findall(r"[a-zäöüß0-9]+", (text or "").lower())
            if len(w) > 2 and w not in STOP and not w.isdigit()]


def loesung_text(f):
    t = f["typ"]
    if t == "single":
        return f["optionen"][f["loesung"]]
    if t == "multi":
        return " ".join(f["optionen"][i] for i in f["loesung"])
    if t == "zuordnen":
        return " ".join(a + " " + b for a, b in f["paare"])
    if t == "reihe":
        return " ".join(f["elemente"])
    if t == "text":
        return f.get("muster", "")
    if t == "wahr":
        return "Richtig" if f["loesung"] else "Falsch"
    if t == "zahl":
        return str(f["loesung"]).replace(".", ",") + " " + f.get("einheit", "")
    return ""


def frage_text(f):
    # Fragetext doppelt gewichtet, dazu Lösung und Erklärung
    return " ".join([f["frage"], f["frage"], loesung_text(f), f.get("erklaerung", "")])


class Index:
    def __init__(self, eintraege):
        """eintraege: Liste von (schluessel, text)."""
        docs = {k: Counter(woerter(t)) for k, t in eintraege}
        self.df = Counter(w for c in docs.values() for w in c)
        self.n = max(1, len(docs))
        self.vec = {k: self._vektor(c) for k, c in docs.items()}

    def _vektor(self, counter):
        v = {w: (1 + math.log(n)) * math.log((self.n + 1) / (self.df.get(w, 0) + 0.5)) for w, n in counter.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / norm for w, x in v.items()}

    @staticmethod
    def _cos(a, b):
        if len(a) > len(b):
            a, b = b, a
        return sum(x * b.get(w, 0.0) for w, x in a.items())

    def suche(self, text, n=10, schwelle=0.08):
        q = self._vektor(Counter(woerter(text)))
        treffer = [(self._cos(q, v), k) for k, v in self.vec.items()]
        return [(s, k) for s, k in sorted(treffer, reverse=True)[:n] if s >= schwelle]

    def paare(self, schwelle):
        keys = list(self.vec)
        out = []
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                s = self._cos(self.vec[a], self.vec[b])
                if s >= schwelle:
                    out.append((s, a, b))
        return sorted(out, reverse=True)


DOPPEL_SCHWELLE = 0.42


def moegliche_doppel(fragen, verwandt_von, geprueft, schwelle=DOPPEL_SCHWELLE):
    """Paare sichtbarer Fragen (ohne Rechenaufgaben), die sich sehr ähneln und noch nicht bearbeitet sind.
    Rechenaufgaben mit gleichem Muster und anderen Zahlen sind gewollt und zählen nicht."""
    idx = Index([(f["id"], frage_text(f)) for f in fragen if f["typ"] != "zahl" and not f.get("aus")])
    out = []
    for s, a, b in idx.paare(schwelle):
        if verwandt_von.get(a) and verwandt_von.get(a) == verwandt_von.get(b):
            continue
        if frozenset((a, b)) in geprueft:
            continue
        out.append((s, a, b))
    return out


def lade_katalog():
    """Lädt Tests, Themen und Pflegelisten wie build.py (ohne fragen.json zu schreiben)."""
    hier = os.path.dirname(os.path.abspath(__file__))
    if hier not in sys.path:
        sys.path.insert(0, hier)
    import importlib
    import dsl
    for m in ["q_a", "q_b", "q_c", "q_d", "q_e", "q_f"]:
        importlib.import_module(m)
    import pflege
    import themen
    fragen = [f for t in dsl.TESTS for f in t["fragen"]]
    for f in fragen:
        if f["id"] in pflege.AUSBLENDEN:
            f["aus"] = pflege.AUSBLENDEN[f["id"]]
    verwandt_von = {}
    for i, (ids, _) in enumerate(pflege.VERWANDT, 1):
        for q in ids.split():
            verwandt_von[q] = f"v{i:02d}"
    geprueft = {frozenset(p.split()) for p in pflege.GEPRUEFT}
    return dsl, fragen, themen, pflege, verwandt_von, geprueft
