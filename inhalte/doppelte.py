"""Zeigt Fragenpaare, die sich sehr ähneln, mit ihrem Stand in inhalte/pflege.py.

    python3 inhalte/doppelte.py          (Schwelle 0,42 wie in build.py)
    python3 inhalte/doppelte.py 0.33     (mehr Paare zeigen)

Stand je Paar: NEU (noch nicht bearbeitet), verwandt, geprüft.
Rechenaufgaben mit gleichem Muster und anderen Zahlen sind gewollt und werden nicht verglichen.
Neue Paare: eine Frage löschen (ID in pflege.GELOESCHT), als VERWANDT verknüpfen oder als GEPRUEFT markieren.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aehnlich import DOPPEL_SCHWELLE, Index, frage_text, lade_katalog, loesung_text  # noqa: E402


def main():
    schwelle = float(sys.argv[1]) if len(sys.argv) > 1 else DOPPEL_SCHWELLE
    dsl, fragen, pflege, verwandt_von, geprueft = lade_katalog()
    nach_id = {f["id"]: f for f in fragen}
    idx = Index([(f["id"], frage_text(f)) for f in fragen if f["typ"] != "zahl"])
    paare = idx.paare(schwelle)
    neu = 0
    for s, a, b in paare:
        if verwandt_von.get(a) and verwandt_von.get(a) == verwandt_von.get(b):
            stand = "verwandt"
        elif frozenset((a, b)) in geprueft:
            stand = "geprüft"
        else:
            stand = "NEU"
            neu += 1
        print(f"{s:.2f}  {stand:8s}  {a.upper()} ↔ {b.upper()}")
        for q in (a, b):
            f = nach_id[q]
            print(f"      {q.upper()}: {f['frage'][:110]}")
            print(f"             → {loesung_text(f)[:110]}")
    print(f"\n{len(paare)} Paare ab {schwelle:.2f}, davon {neu} neu. Verwandte Gruppen: {len(pflege.VERWANDT)}, gelöschte IDs: {len(pflege.GELOESCHT)}.")


if __name__ == "__main__":
    main()
