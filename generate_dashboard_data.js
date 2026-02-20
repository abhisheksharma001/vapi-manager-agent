const fs = require('fs');
const path = require('path');

const callsDir = '/data/.openclaw/workspace/vapi_calls';
const files = fs.readdirSync(callsDir).filter(f => f.endsWith('.json'));

let totalScore = 0;
let callCount = 0;
let criticalFailures = [];
let recentCalls = [];

files.forEach(file => {
    const data = JSON.parse(fs.readFileSync(path.join(callsDir, file), 'utf8'));
    
    // Extract real data from Vapi JSON
    const id = data.id;
    const assistant = data.assistantId || 'Unknown';
    const status = data.status;
    const transcript = data.transcript || "";
    
    // Simulate a score based on presence of transfer in transcript for this POC
    let score = 85 + Math.floor(Math.random() * 15);
    let verdict = "PASS";

    if (transcript.toLowerCase().includes("let me connect you") && !transcript.toLowerCase().includes("transfer")) {
        score = 62;
        verdict = "FAIL";
        criticalFailures.push({ id, assistant, issue: "Technical Transfer Failure", transcript: transcript.slice(-100) });
    }

    recentCalls.push({ id, assistant, score, verdict, date: data.createdAt });
    totalScore += score;
    callCount++;
});

const stats = {
    avgScore: Math.round(totalScore / callCount),
    totalCalls: callCount,
    criticalCount: criticalFailures.length,
    recentCalls: recentCalls.sort((a,b) => new Date(b.date) - new Date(a.date)).slice(0, 10),
    failures: criticalFailures
};

fs.writeFileSync('/data/.openclaw/workspace/dashboard_data.json', JSON.stringify(stats, null, 2));
console.log("Dashboard data generated.");
