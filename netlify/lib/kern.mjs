// Gemeinsame Logik für die Sync-Funktionen der HBOD Lern-App.
// Speicher-Schnittstelle: { getWithMetadata(key, {type:"json"}), setJSON(key, data, opts), get(key, {type:"text"}), set(key, text, opts) }
// Netlify Blobs erfüllt sie direkt; für lokale Tests gibt es einen Speicher im Arbeitsspeicher.

export const CODE_RE = /^[A-HJ-NP-Z2-9]{4}(-[A-HJ-NP-Z2-9]{4}){3}$/;
const QID_RE = /^t\d{2}-\d{2}$/;
const MAX_BODY = 900 * 1024;

const neuer = (a, b) => String(a || "") > String(b || "");
const jetzt = () => new Date().toISOString();

async function sha(text) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
export const schluessel = async (code) => "u-" + (await sha("hbod-lernapp|" + code)).slice(0, 48);
export const lesetoken = async (code) => (await sha("hbod-lernapp-lesen|" + code)).slice(0, 32);

export function leer() {
  return { version: 1, antworten: {}, laeufe: {}, notizen: {}, bewertungen: {}, aktivitaet: {}, einstellungen: null, lauf: null, resetZeit: "", erstellt: jetzt(), aktualisiert: "" };
}

export function zusammenfuehren(doc, d) {
  if (!d || typeof d !== "object") return doc;
  for (const [q, a] of Object.entries(d.antworten || {})) {
    if (!QID_RE.test(q) || !a || typeof a !== "object") continue;
    if (doc.resetZeit && !neuer(a.zeit, doc.resetZeit)) continue;
    const cur = doc.antworten[q];
    if (!cur || neuer(a.zeit, cur.zeit)) doc.antworten[q] = a;
  }
  for (const [k, liste] of Object.entries(d.laeufe || {})) {
    if (!Array.isArray(liste) || !/^[a-z0-9-]{1,40}$/.test(k)) continue;
    const cur = Array.isArray(doc.laeufe[k]) ? doc.laeufe[k] : [];
    const seen = new Set(cur.map((l) => l.datum));
    for (const l of liste) {
      if (!l || !l.datum || seen.has(l.datum)) continue;
      if (doc.resetZeit && !neuer(l.datum, doc.resetZeit)) continue;
      cur.push(l); seen.add(l.datum);
    }
    cur.sort((a, b) => (a.datum < b.datum ? -1 : 1));
    doc.laeufe[k] = cur.slice(-60);
  }
  for (const [id, n] of Object.entries(d.notizen || {})) {
    if (!/^[a-z0-9]{4,40}$/.test(id) || !n || typeof n !== "object") continue;
    const cur = doc.notizen[id];
    if (!cur || neuer(n.zeit, cur.zeit)) doc.notizen[id] = n;
  }
  // Alte Bewertungen (leicht/mittel/schwer, bis Version 2.3) je Frage: die neueste gewinnt. Seit 3.0 steht die Bewertung in der Antwort.
  if (!doc.bewertungen || typeof doc.bewertungen !== "object") doc.bewertungen = {};
  for (const [q, b] of Object.entries(d.bewertungen || {})) {
    if (!QID_RE.test(q) || !b || typeof b !== "object" || !(b.stufe == null || ["leicht", "mittel", "schwer"].includes(b.stufe))) continue;
    if (doc.resetZeit && !neuer(b.zeit, doc.resetZeit)) continue;
    const cur = doc.bewertungen[q];
    if (!cur || neuer(b.zeit, cur.zeit)) doc.bewertungen[q] = b;
  }
  for (const [tag, anz] of Object.entries(d.aktivitaet || {})) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(tag)) continue;
    if (doc.resetZeit && tag < doc.resetZeit.slice(0, 10)) continue;
    doc.aktivitaet[tag] = Math.max(doc.aktivitaet[tag] || 0, Number(anz) || 0);
  }
  if (d.einstellungen && typeof d.einstellungen === "object" && neuer(d.einstellungen.zeit, doc.einstellungen && doc.einstellungen.zeit)) doc.einstellungen = d.einstellungen;
  if (d.lauf && typeof d.lauf === "object" && neuer(d.lauf.zeit, doc.lauf && doc.lauf.zeit)) doc.lauf = d.lauf;
  return doc;
}

function zuruecksetzen(doc) {
  const z = jetzt();
  return Object.assign(leer(), { notizen: doc.notizen || {}, einstellungen: doc.einstellungen || null, erstellt: doc.erstellt || z, resetZeit: z });
}

const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const text = (t, status = 200) => new Response(t, { status, headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" } });

// ---------- /api/fortschritt ----------
export async function fortschritt(req, store) {
  const url = new URL(req.url);
  if (req.method === "GET") {
    const code = (url.searchParams.get("code") || "").toUpperCase();
    if (!CODE_RE.test(code)) return json({ fehler: "ungueltiger_code" }, 400);
    const key = await schluessel(code);
    const r = await store.getWithMetadata(key, { type: "json" });
    const doc = (r && r.data) || leer();
    return json(Object.assign(doc, { lesetoken: await lesetoken(code) }));
  }
  if (req.method !== "POST") return json({ fehler: "methode" }, 405);
  const roh = await req.text();
  if (roh.length > MAX_BODY) return json({ fehler: "zu_gross" }, 413);
  let body;
  try { body = JSON.parse(roh); } catch (e) { return json({ fehler: "json" }, 400); }
  const code = String(body.code || "").toUpperCase();
  if (!CODE_RE.test(code)) return json({ fehler: "ungueltiger_code" }, 400);
  const key = await schluessel(code);
  const token = await lesetoken(code);
  // optimistisch schreiben: lesen, zusammenführen, nur schreiben, wenn sich nichts dazwischen geändert hat
  for (let versuch = 0; versuch < 6; versuch++) {
    const r = await store.getWithMetadata(key, { type: "json" });
    let doc = (r && r.data) || leer();
    if (body.zuruecksetzen === true) doc = zuruecksetzen(doc);
    doc = zusammenfuehren(doc, body.aenderungen);
    doc.aktualisiert = jetzt();
    const opts = r && r.etag ? { onlyIfMatch: r.etag } : { onlyIfNew: true };
    const w = await store.setJSON(key, doc, opts);
    if (w && w.modified === false) continue;
    try { await store.set("r-" + token, key, { onlyIfNew: true }); } catch (e) { /* Lese-Link ist optional */ }
    return json(Object.assign(doc, { lesetoken: token }));
  }
  return json({ fehler: "konflikt" }, 409);
}

// ---------- /api/bericht ----------
function loesungText(f) {
  if (f.typ === "single") return f.optionen[f.loesung];
  if (f.typ === "multi") return f.loesung.map((i) => f.optionen[i]).join(" | ");
  if (f.typ === "wahr") return f.loesung ? "Richtig" : "Falsch";
  if (f.typ === "zahl") return String(f.loesung).replace(".", ",") + (f.einheit ? " " + f.einheit : "");
  if (f.typ === "zuordnen") return f.paare.map((p) => p[0] + " → " + p[1]).join(" | ");
  if (f.typ === "reihe") return f.elemente.join(" → ");
  if (f.typ === "text") return f.muster;
  return "";
}

// ---------- Notizen: Typ und Status (gleich wie in der App) ----------
export const NOTIZ_TYP = { pruefen: "Antwort prüfen", unklar: "Unklar", doppelt: "Doppelt", ergaenzung: "Ergänzung", frage: "Wunsch: neue Frage", thema: "Wunsch: neues Thema", erkenntnis: "Erkenntnis", sonstiges: "Anmerkung" };
export function notizTyp(n) {
  if (n && n.typ && NOTIZ_TYP[n.typ]) return n.typ;
  if (n && n.art === "wunsch") return "frage";
  return n && n.frage_id ? "sonstiges" : "erkenntnis";
}
// Erledigt, wenn Nils es so gesetzt hat oder Claude im Katalog geantwortet hat (außer Nils hat danach wieder geöffnet)
export function notizStatus(n, rueck) {
  if (!n) return "offen";
  if (n.status === "geloescht") return "geloescht";
  if (n.status === "erledigt") return "erledigt";
  const r = rueck && rueck[n.id];
  if (r && !(n.wieder && n.wieder > r.zeit)) return "erledigt";
  return "offen";
}

// "Schwer" = zuletzt falsch oder als schwer bewertet (Anki-Bewertung ab Version 3, ältere Bewertungen gelten weiter)
export function istSchwer(a, alteBewertung) {
  if (!a) return !!(alteBewertung && alteBewertung.stufe === "schwer");
  if (a.bew) return a.bew === "falsch" || a.bew === "schwer";
  return a.punkte < 1 || !!(alteBewertung && alteBewertung.stufe === "schwer");
}

export function berichtText(doc, daten) {
  const stapel = daten.stapel || [];
  const fragen = {};
  for (const s of stapel) for (const f of s.fragen) fragen[f.id] = f;
  const alle = fragen;
  const rueck = daten.rueckmeldungen || {};
  const gueltig = (q, a) => a && fragen[q] && (!a.fp || a.fp === fragen[q].fp);
  const alteBew = (q) => { const b = (doc.bewertungen || {})[q]; return b && fragen[q] && (!b.fp || b.fp === fragen[q].fp) ? b : null; };
  const z = [];
  z.push("HBOD Lern-App: Bericht für die Besprechung mit Claude");
  z.push("Erstellt: " + jetzt() + " · Fragenkatalog " + daten.version + " (Stand " + daten.stand + ")");
  let beantw = 0, meister = 0, gesamt = 0;
  for (const q of Object.keys(fragen)) { gesamt++; const a = doc.antworten[q]; if (gueltig(q, a)) { beantw++; if ((a.box || 0) >= 3) meister++; } }
  z.push(`Gesamt: ${meister} von ${gesamt} Fragen gemeistert, ${beantw} schon gesehen.`);
  const tage = Object.keys(doc.aktivitaet || {}).sort();
  if (tage.length) z.push("Zuletzt gelernt am " + tage[tage.length - 1] + ".");
  z.push("");
  z.push("== Stand je Stapel ==");
  for (const m of daten.module || []) {
    for (const sid of m.stapel) {
      const s = stapel.find((x) => x.id === sid); if (!s) continue;
      let b = 0, me = 0, sw = 0;
      for (const f of s.fragen) { const a = doc.antworten[f.id]; if (gueltig(f.id, a)) { b++; if ((a.box || 0) >= 3) me++; if (istSchwer(a, alteBew(f.id))) sw++; } }
      if (!b) continue;
      z.push(`${m.id} · ${s.titel}: ${me} von ${s.fragen.length} gemeistert, ${b} gesehen, ${sw} schwer`);
    }
  }
  z.push("");
  z.push("== Schwere Fragen (zuletzt falsch oder als schwer bewertet) ==");
  let nf = 0;
  for (const f of Object.values(fragen)) {
    const a = doc.antworten[f.id];
    const g = gueltig(f.id, a) ? a : null;
    if (!istSchwer(g, alteBew(f.id))) continue;
    nf++;
    if (nf > 80) continue;
    z.push(`${f.id.toUpperCase()} ${f.frage}`);
    if (g) z.push("  Zuletzt: " + (g.bew === "schwer" ? "richtig, aber schwer" : g.punkte < 1 ? "falsch, Antwort: " + (g.gegeben || "—") : "als schwer markiert") + " · " + String(g.zeit || "").slice(0, 10));
    if (f.typ !== "text") z.push("  Lösung: " + loesungText(f));
  }
  if (nf > 80) z.push(`… und ${nf - 80} weitere.`);
  if (!nf) z.push("Keine.");
  z.push("");
  const notizen = Object.values(doc.notizen || {}).filter((n) => n && notizStatus(n, rueck) !== "geloescht").sort((a, b) => (a.datum < b.datum ? -1 : 1));
  const offen = notizen.filter((n) => notizStatus(n, rueck) === "offen");
  const erledigt = notizen.filter((n) => notizStatus(n, rueck) === "erledigt");
  z.push("== Offene Anmerkungen und Wünsche ==");
  z.push("Für Claude: Vor jedem Einbau mit python3 inhalte/suche.py prüfen, ob es das schon gibt. Danach die Rückmeldung mit der ID in eckigen Klammern in inhalte/rueckmeldungen.py eintragen.");
  if (!offen.length) z.push("Keine.");
  for (const n of offen) {
    const typ = notizTyp(n);
    const f = n.frage_id ? alle[n.frage_id] : null;
    z.push("");
    z.push(`[${n.id}] ${String(n.datum || "").slice(0, 10)} · ${NOTIZ_TYP[typ]}${n.frage_id ? " · " + n.frage_id.toUpperCase() : ""}${n.pause ? " (bis zur Prüfung pausiert)" : ""}`);
    if (f) {
      z.push("  Frage: " + f.frage);
      z.push("  Lösung laut App: " + loesungText(f));
    } else if (n.frage_id) z.push("  Frage (gibt es nicht mehr im Katalog): " + (n.frage || n.frage_id));
    else if (n.frage) z.push("  Frage: " + n.frage);
    if (n.betrifft) z.push("  Betrifft: " + n.betrifft);
    if (n.doppelt_zu) z.push("  Doppelt zu: " + n.doppelt_zu.toUpperCase() + (alle[n.doppelt_zu] ? " – " + alle[n.doppelt_zu].frage : ""));
    if (n.text) z.push("  Nils: " + n.text);
    if (n.antwort) z.push("  Antwort laut Nils: " + n.antwort);
    if (n.quelle) z.push("  Quelle laut Nils: " + n.quelle);
    if (Array.isArray(n.aehnlich) && n.aehnlich.length) z.push("  Die App fand ähnlich: " + n.aehnlich.map((x) => (/^t\d{2}-\d{2}$/.test(x) ? String(x).toUpperCase() : String(x))).join(", "));
  }
  z.push("");
  z.push("== Erledigt ==");
  if (!erledigt.length) z.push("Keine.");
  else {
    z.push(`${erledigt.length} erledigt, davon ${erledigt.filter((n) => rueck[n.id]).length} mit Rückmeldung von Claude. Die letzten:`);
    for (const n of erledigt.slice(-15)) z.push(`[${n.id}] ${String(n.datum || "").slice(0, 10)} ${NOTIZ_TYP[notizTyp(n)]}${n.frage_id ? " " + n.frage_id.toUpperCase() : ""}: ${String(n.text || "").slice(0, 120)}${rueck[n.id] ? " → Claude: " + rueck[n.id].text : ""}`);
  }
  return z.join("\n");
}

export async function bericht(req, store, ladeFragen) {
  const url = new URL(req.url);
  const t = url.searchParams.get("t") || "";
  if (!/^[0-9a-f]{32}$/.test(t)) return text("Ungültiger Link.", 400);
  const key = await store.get("r-" + t, { type: "text" });
  if (!key) return text("Kein Bericht gefunden. Öffne die Lern-App einmal mit deinem Lern-Code.", 404);
  const r = await store.getWithMetadata(key, { type: "json" });
  const doc = (r && r.data) || leer();
  const daten = await ladeFragen();
  return text(berichtText(doc, daten));
}

// ---------- Speicher im Arbeitsspeicher (nur für lokale Tests) ----------
export function speicherImRAM() {
  const m = new Map(); let n = 0;
  return {
    async getWithMetadata(k) { const e = m.get(k); return e ? { data: JSON.parse(e.v), etag: e.etag, metadata: {} } : null; },
    async get(k) { const e = m.get(k); return e ? e.v : null; },
    async setJSON(k, d, o = {}) { return this.set(k, JSON.stringify(d), o); },
    async set(k, v, o = {}) {
      const e = m.get(k);
      if (o.onlyIfNew && e) return { modified: false };
      if (o.onlyIfMatch && (!e || e.etag !== o.onlyIfMatch)) return { modified: false };
      const etag = "e" + (++n); m.set(k, { v: String(v), etag }); return { modified: true, etag };
    },
  };
}
