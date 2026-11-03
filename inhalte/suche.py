"""Sucht im Fragenkatalog nach ähnlichen Fragen und Themen.

Vor jedem Einbau eines Wunsches (neue Frage, neues Thema) ausführen, um zu prüfen, ob es das schon gibt:
    python3 inhalte/suche.py "Was ist GMV und wie unterscheidet es sich vom Umsatz?"
    python3 inhalte/suche.py "Kaufland Provision" 15     (optional: Anzahl Treffer)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aehnlich import Index, frage_text, lade_katalog, loesung_text  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    text = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    dsl, fragen, themen, pflege, verwandt_von, _ = lade_katalog()
    nach_id = {f["id"]: f for f in fragen}
    idx = Index([(f["id"], frage_text(f)) for f in fragen])
    print(f"Fragen ähnlich zu: {text!r}\n")
    treffer = idx.suche(text, n)
    if not treffer:
        print("  Keine ähnlichen Fragen gefunden.")
    for s, q in treffer:
        f = nach_id[q]
        zusatz = " [ausgeblendet: " + f["aus"] + "]" if f.get("aus") else (" [verwandt " + verwandt_von[q] + "]" if q in verwandt_von else "")
        print(f"  {s:.2f}  {q.upper()}{zusatz}  {f['frage']}")
        print(f"        Lösung: {loesung_text(f)[:160]}")
    tidx = Index([(t["id"], " ".join([t["titel"]] * 3 + [t["kurz"]] + t["punkte"])) for t in themen.THEMEN])
    tt = tidx.suche(text, 5)
    print("\nThemen:")
    if not tt:
        print("  Kein passendes Thema.")
    for s, tid in tt:
        t = next(x for x in themen.THEMEN if x["id"] == tid)
        print(f"  {s:.2f}  {t['titel']} ({tid}, {len(t['fragen'])} Fragen)")
    print("\nFaustregel: ab etwa 0,35 ist es meist dieselbe Tatsache. Trotzdem die Treffer lesen und selbst entscheiden.")


if __name__ == "__main__":
    main()
