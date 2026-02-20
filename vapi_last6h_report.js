// Vapi last-N-hours call review (hackathon POC)
// Usage: node vapi_last6h_report.js [hours=6]

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

const hours = Number(process.argv[2] ?? '6');
const VAPI_API_KEY = process.env.VAPI_API_KEY;
if (!VAPI_API_KEY) {
  console.error('Missing VAPI_API_KEY (set in .env)');
  process.exit(2);
}

const BASE = 'https://api.vapi.ai';
const sinceMs = Date.now() - hours * 60 * 60 * 1000;

const hdrs = {
  Authorization: `Bearer ${VAPI_API_KEY}`,
  'Content-Type': 'application/json',
};

async function getJson(path) {
  const res = await fetch(`${BASE}${path}`, { headers: hdrs });
  if (!res.ok) {
    const t = await res.text().catch(() => '');
    throw new Error(`${path} failed: ${res.status} ${res.statusText} ${t.slice(0, 400)}`);
  }
  return await res.json();
}

function toMs(x) {
  if (!x) return null;
  const ms = Date.parse(x);
  return Number.isFinite(ms) ? ms : null;
}

function short(str, n = 160) {
  if (!str) return '';
  const s = String(str).replace(/\s+/g, ' ').trim();
  return s.length > n ? s.slice(0, n - 1) + '…' : s;
}

function findSentiment(messages) {
  const txt = (messages || [])
    .map(m => `${m.role || ''}: ${m.message || ''}`)
    .join('\n')
    .toLowerCase();
  if (!txt) return 'unknown';
  const angry = /(angry|furious|this is terrible|worst|sucks|scam|lawsuit)/;
  const frustrated = /(frustrat|not happy|unhappy|complain|complaint|cancel|refund|chargeback|bad service|waste)/;
  const satisfied = /(thanks|thank you|great|perfect|awesome|that works|resolved|appreciate)/;
  if (angry.test(txt)) return 'angry';
  if (frustrated.test(txt)) return 'frustrated';
  if (satisfied.test(txt)) return 'satisfied';
  return 'neutral';
}

function verdictHeuristic(call) {
  // Hackathon POC heuristic until we add prompt-based scoring.
  const endedReason = String(call.endedReason || '').toLowerCase();
  const status = String(call.status || '').toLowerCase();
  const sentiment = findSentiment(call?.messages);

  const hasHardError = /(error|failed|timeout|no-answer|busy|call-start-error)/.test(endedReason);
  if (hasHardError) return { verdict: 'ESCALATE', emoji: '🚨', score: 35, priority: 'HIGH', reasons: [`endedReason=${call.endedReason}`], sentiment };

  if (sentiment === 'angry') return { verdict: 'ESCALATE', emoji: '🚨', score: 40, priority: 'HIGH', reasons: ['caller angry/complaint language detected'], sentiment };
  if (sentiment === 'frustrated') return { verdict: 'FOLLOW_UP', emoji: '⚠️', score: 60, priority: 'MEDIUM', reasons: ['caller frustration language detected'], sentiment };

  if (status && status !== 'ended' && status !== 'completed') {
    return { verdict: 'FOLLOW_UP', emoji: '⚠️', score: 65, priority: 'LOW', reasons: [`status=${call.status}`], sentiment };
  }

  return { verdict: 'PASS', emoji: '✅', score: 85, priority: 'LOW', reasons: [], sentiment };
}

async function main() {
  // list calls
  const calls = await getJson('/call');
  const arr = Array.isArray(calls) ? calls : [];

  // filter last N hours
  const recent = arr
    .map(c => {
      const endedAtMs = toMs(c.endedAt) ?? toMs(c.updatedAt) ?? toMs(c.createdAt);
      return { c, endedAtMs };
    })
    .filter(x => x.endedAtMs && x.endedAtMs >= sinceMs)
    .sort((a, b) => b.endedAtMs - a.endedAtMs);

  // assistant cache
  const assistantCache = new Map();
  async function getAssistant(assistantId) {
    if (!assistantId) return null;
    if (assistantCache.has(assistantId)) return assistantCache.get(assistantId);
    try {
      const a = await getJson(`/assistant/${assistantId}`);
      assistantCache.set(assistantId, a);
      return a;
    } catch (e) {
      assistantCache.set(assistantId, null);
      return null;
    }
  }

  const rows = [];
  for (const { c, endedAtMs } of recent) {
    const assistant = await getAssistant(c.assistantId);
    const agentName = assistant?.name ?? c.assistantId ?? 'unknown';

    const h = verdictHeuristic(c);
    rows.push({
      callId: c.id,
      assistantId: c.assistantId,
      agentName,
      endedAt: endedAtMs ? new Date(endedAtMs).toISOString() : null,
      caller: c?.customer?.number ?? c?.destination?.number ?? null,
      callerId: c?.destination?.callerId ?? null,
      recordingUrl: c?.artifact?.recording?.mono?.combinedUrl ?? c?.artifact?.recordingUrl ?? c?.artifact?.recording?.stereoUrl ?? c?.recordingUrl ?? null,
      summary: short(c?.analysis?.summary ?? ''),
      endedReason: c.endedReason ?? null,
      status: c.status ?? null,
      verdict: h.verdict,
      emoji: h.emoji,
      score: h.score,
      priority: h.priority,
      sentiment: h.sentiment,
      reasons: h.reasons,
      promptFetched: Boolean(assistant?.model?.messages?.length),
    });
  }

  const report = {
    windowHours: hours,
    since: new Date(sinceMs).toISOString(),
    totalCalls: rows.length,
    pass: rows.filter(r => r.verdict === 'PASS').length,
    followUp: rows.filter(r => r.verdict === 'FOLLOW_UP').length,
    escalate: rows.filter(r => r.verdict === 'ESCALATE').length,
    rows,
  };

  fs.writeFileSync('vapi_last6h_report.json', JSON.stringify(report, null, 2));
  console.log(`Wrote vapi_last6h_report.json (calls=${rows.length})`);
}

await main();
