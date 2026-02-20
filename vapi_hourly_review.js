// Fetch calls from Vapi and summarize those ended in the last N minutes.
// Usage: node vapi_hourly_review.js [minutes=60]

import fs from 'node:fs';

function loadDotEnv(path = '.env') {
  if (!fs.existsSync(path)) return;
  const text = fs.readFileSync(path, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (!m) continue;
    const key = m[1];
    let val = m[2] ?? '';
    val = val.replace(/^['"]|['"]$/g, '');
    if (!process.env[key]) process.env[key] = val;
  }
}

loadDotEnv();

const minutes = Number(process.argv[2] ?? '60');
const VAPI_API_KEY = process.env.VAPI_API_KEY;
if (!VAPI_API_KEY) {
  console.error('Missing VAPI_API_KEY (set in .env)');
  process.exit(2);
}

const sinceMs = Date.now() - minutes * 60 * 1000;

// Vapi API base (per docs examples)
const BASE = 'https://api.vapi.ai';

async function listCalls() {
  const url = `${BASE}/call`;
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${VAPI_API_KEY}`,
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) {
    const t = await res.text().catch(() => '');
    throw new Error(`Vapi list calls failed: ${res.status} ${res.statusText} ${t.slice(0, 300)}`);
  }
  return await res.json();
}

function toMs(x) {
  if (!x) return null;
  const ms = Date.parse(x);
  return Number.isFinite(ms) ? ms : null;
}

function short(str, n = 140) {
  if (!str) return '';
  const s = String(str).replace(/\s+/g, ' ').trim();
  return s.length > n ? s.slice(0, n - 1) + '…' : s;
}

try {
  const calls = await listCalls();
  const recent = (Array.isArray(calls) ? calls : [])
    .map(c => {
      const endedAtMs = toMs(c.endedAt) ?? toMs(c.updatedAt) ?? toMs(c.createdAt);
      return { c, endedAtMs };
    })
    .filter(x => x.endedAtMs && x.endedAtMs >= sinceMs)
    .sort((a, b) => b.endedAtMs - a.endedAtMs);

  const out = {
    windowMinutes: minutes,
    since: new Date(sinceMs).toISOString(),
    count: recent.length,
    calls: recent.slice(0, 25).map(({ c, endedAtMs }) => ({
      id: c.id,
      assistantId: c.assistantId,
      type: c.type,
      status: c.status,
      endedReason: c.endedReason,
      endedAt: endedAtMs ? new Date(endedAtMs).toISOString() : null,
      summary: short(c?.analysis?.summary ?? c?.analysis?.successEvaluation ?? ''),
      recordingUrl: c?.artifact?.recording?.mono?.combinedUrl ?? c?.artifact?.recordingUrl ?? c?.artifact?.recording?.stereoUrl ?? c?.recordingUrl ?? null,
    })),
  };

  const text = JSON.stringify(out, null, 2);
  fs.writeFileSync('vapi_hourly_review.json', text);
  console.log(text);
} catch (err) {
  console.error(String(err?.stack ?? err));
  process.exit(1);
}
