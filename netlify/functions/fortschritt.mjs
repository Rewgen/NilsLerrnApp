// Speichert und liefert den Lernfortschritt (Netlify Blobs, Schlüssel = Hash des Lern-Codes).
import { getStore } from "@netlify/blobs";
import { fortschritt } from "../lib/kern.mjs";

export default async (req) => {
  const store = getStore({ name: "lernfortschritt", consistency: "strong" });
  try {
    return await fortschritt(req, store);
  } catch (e) {
    console.error("fortschritt", e);
    return new Response(JSON.stringify({ fehler: "server" }), { status: 500, headers: { "content-type": "application/json" } });
  }
};

export const config = { path: "/api/fortschritt" };
