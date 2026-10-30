// Nur-Lese-Bericht als Text, z. B. um ihn Claude in einem Chat zu geben: /api/bericht?t=<Lesetoken>
import { getStore } from "@netlify/blobs";
import { bericht } from "../lib/kern.mjs";

export default async (req) => {
  const store = getStore({ name: "lernfortschritt", consistency: "strong" });
  const ladeFragen = async () => {
    const r = await fetch(new URL("/fragen.json", req.url));
    return r.json();
  };
  try {
    return await bericht(req, store, ladeFragen);
  } catch (e) {
    console.error("bericht", e);
    return new Response("Der Bericht konnte nicht erstellt werden.", { status: 500, headers: { "content-type": "text/plain; charset=utf-8" } });
  }
};

export const config = { path: "/api/bericht" };
