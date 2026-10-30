// Lokaler Testserver: liefert public/ aus und simuliert die Sync-Funktionen mit einem Speicher im Arbeitsspeicher.
// Start: npm run lokal  ->  http://localhost:8888
import http from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";
import { fortschritt, bericht, speicherImRAM } from "../netlify/lib/kern.mjs";

const ROOT = join(fileURLToPath(new URL(".", import.meta.url)), "..", "public");
const PORT = Number(process.env.PORT || 8888);
const store = speicherImRAM();
const TYP = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webmanifest": "application/manifest+json" };

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost:" + PORT);
  try {
    if (url.pathname === "/api/fortschritt" || url.pathname === "/api/bericht") {
      const chunks = []; for await (const c of req) chunks.push(c);
      const request = new Request(url, { method: req.method, headers: req.headers, body: ["GET", "HEAD"].includes(req.method) ? undefined : Buffer.concat(chunks) });
      const antwort = url.pathname === "/api/fortschritt"
        ? await fortschritt(request, store)
        : await bericht(request, store, async () => JSON.parse(await readFile(join(ROOT, "fragen.json"), "utf8")));
      res.writeHead(antwort.status, Object.fromEntries(antwort.headers));
      res.end(Buffer.from(await antwort.arrayBuffer()));
      return;
    }
    let p = normalize(decodeURIComponent(url.pathname)).replace(/^\/+/, "");
    if (!p || p.endsWith("/")) p += "index.html";
    const data = await readFile(join(ROOT, p));
    res.writeHead(200, { "content-type": TYP[extname(p)] || "application/octet-stream" });
    res.end(data);
  } catch (e) {
    res.writeHead(404, { "content-type": "text/plain" }); res.end("Nicht gefunden");
  }
}).listen(PORT, () => console.log("Lern-App lokal: http://localhost:" + PORT));
