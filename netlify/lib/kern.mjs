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
  return { version: 1, antworten: {}, laeufe: {}, notizen: {}, aktivitaet: {}, einstellungen: null, lauf: null, resetZeit: "", erstellt: jetzt(), aktualisiert: "" };
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

export function berichtText(doc, daten) {
  const fragen = {};
  for (const t of daten.tests) for (const f of t.fragen) fragen[f.id] = f;
  const gueltig = (q, a) => a && fragen[q] && (!a.fp || a.fp === fragen[q].fp);
  const z = [];
  z.push("HBOD Lern-App: Bericht für die Besprechung mit Claude");
  z.push("Erstellt: " + jetzt() + " · Fragenkatalog " + daten.version + " (Stand " + daten.stand + ")");
  let beantw = 0, richtig = 0, meister = 0, gesamt = 0;
  for (const q of Object.keys(fragen)) { gesamt++; const a = doc.antworten[q]; if (gueltig(q, a)) { beantw++; if (a.punkte >= 1) richtig++; if ((a.box || 0) >= 3) meister++; } }
  z.push(`Gesamt: ${beantw} von ${gesamt} beantwortet, ${richtig} zuletzt richtig, ${meister} gemeistert (dreimal zum Termin richtig).`);
  const tage = Object.keys(doc.aktivitaet || {}).sort();
  if (tage.length) z.push("Gelernt an " + tage.length + " Tagen, zuletzt am " + tage[tage.length - 1] + ".");
  const l = doc.laeufe || {}; const anz = (k) => (Array.isArray(l[k]) ? l[k].length : 0);
  const teile = [];
  if (anz("tagesrunden")) teile.push(anz("tagesrunden") + " Tagesrunden");
  if (anz("runden")) teile.push(anz("runden") + " schnelle Runden");
  if (anz("themen")) teile.push(anz("themen") + " Themenrunden");
  if (anz("pruefungen")) teile.push(anz("pruefungen") + " Prüfungssimulationen");
  if (teile.length) z.push("Durchgänge: " + teile.join(", ") + ".");
  z.push("");
  z.push("== Stand je Test ==");
  for (const t of daten.tests) {
    let b = 0, p = 0;
    for (const f of t.fragen) { const a = doc.antworten[f.id]; if (gueltig(f.id, a)) { b++; p += a.punkte || 0; } }
    if (!b) continue;
    z.push(`${t.id.toUpperCase()} ${t.titel}: ${b}/${t.fragen.length} beantwortet, ${Math.round((p / t.fragen.length) * 100)} % der Punkte`);
  }
  if (Array.isArray(daten.themen) && daten.themen.length) {
    z.push("");
    z.push("== Stand je Thema ==");
    let nt = 0;
    for (const th of daten.themen) {
      let b = 0, p = 0, m = 0;
      for (const q of th.fragen) { const a = doc.antworten[q]; if (gueltig(q, a)) { b++; p += a.punkte || 0; if ((a.box || 0) >= 3) m++; } }
      if (!b) continue;
      nt++;
      z.push(`${th.titel}: ${b}/${th.fragen.length} beantwortet, ${Math.round((p / th.fragen.length) * 100)} % der Punkte, ${m} gemeistert`);
    }
    if (!nt) z.push("Noch keine Fragen aus den Themen beantwortet.");
  }
  z.push("");
  z.push("== Fragen, die noch nicht sitzen (zuletzt falsch oder teilweise) ==");
  let nf = 0;
  for (const t of daten.tests) for (const f of t.fragen) {
    const a = doc.antworten[f.id];
    if (!gueltig(f.id, a) || a.punkte >= 1) continue;
    nf++;
    z.push(`${f.id.toUpperCase()} ${f.frage}`);
    z.push("  Meine Antwort: " + (a.gegeben || "—") + (a.unsicher ? " (unsicher)" : ""));
    if (f.typ !== "text") z.push("  Lösung: " + loesungText(f));
    z.push("  Versuche: " + (a.versuche || 1) + ", zuletzt " + String(a.zeit || "").slice(0, 10));
  }
  if (!nf) z.push("Keine.");
  z.push("");
  z.push("== Richtig, aber unsicher ==");
  let nu = 0;
  for (const t of daten.tests) for (const f of t.fragen) { const a = doc.antworten[f.id]; if (gueltig(f.id, a) && a.punkte >= 1 && a.unsicher) { nu++; z.push(`${f.id.toUpperCase()} ${f.frage}`); } }
  if (!nu) z.push("Keine.");
  z.push("");
  z.push("== Notizen und gemeldete Fehler ==");
  const notizen = Object.values(doc.notizen || {}).sort((a, b) => (a.datum < b.datum ? -1 : 1));
  if (!notizen.length) z.push("Keine.");
  for (const n of notizen) z.push(`[${n.status || "offen"}] ${String(n.datum || "").slice(0, 10)} ${n.frage_id ? n.frage_id.toUpperCase() + " " : ""}${n.text}`);
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
