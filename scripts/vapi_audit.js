const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const WEBHOOK_URL = "https://ellavox.app.n8n.cloud/webhook/3288552e-2f39-486b-b349-34b7917e5a3c";
const MEMORY_PATH = "memory/failure_trends.json";
const CALLS_DIR = "vapi_calls";
const TEMPLATE_PATH = "templates/audit_email.md";

async function postData(url, data) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const options = {
            hostname: urlObj.hostname,
            path: urlObj.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(JSON.stringify(data))
            }
        };

        const protocol = urlObj.protocol === 'https:' ? https : http;
        const req = protocol.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => resolve({ status: res.statusCode, body }));
        });

        req.on('error', (e) => reject(e));
        req.write(JSON.stringify(data));
        req.end();
    });
}

function calculateAudit(call) {
    const transcript = call.transcript || '';
    const summary = (call.summary || '').toLowerCase();
    const endedReason = call.endedReason || '';
    const successEvaluation = call.analysis && call.analysis.successEvaluation;
    
    let score = 7.0;
    let reason = "Handled the call successfully according to primary parameters.";
    let suggestions = "Maintain current flow. Consider adding a faster 'closing' to reduce silence at the end.";
    let errorKey = "general_performance";

    // 1. Technical/Immediate failures
    if (!transcript || transcript.length < 30) {
        score = 3.0;
        reason = "Empty or extremely short transcript. Likely a technical failure or immediate hangup.";
        suggestions = "Check SIP/Connection stability. If this is a recurring hangup, review the opening greeting latency.";
    } 
    // 2. Vapi-detected success
    else if (successEvaluation === "false") {
        score = 4.5;
        reason = "Call marked as unsuccessful by internal analysis. User likely did not get what they needed.";
        suggestions = "Review the 'Greeting Protocol' section. Ensure the AI is not mishearing the business name (e.g., Caudle vs Cottle).";
    }
    // 3. Technical errors
    else if (endedReason.includes('error') || endedReason.includes('failed')) {
        score = 2.0;
        reason = `Call ended with technical error: ${endedReason}`;
        suggestions = "Investigate Vapi logs for provider-side errors. Ensure LLM response timeout is sufficient.";
    }
    // 4. Identity Confusion (Historical issue found in logs)
    else if (transcript.includes('Sarah') && transcript.includes('Troy')) {
        score = 4.0;
        reason = "Assistant identity mismatch (Sarah vs Troy). Confuses the customer.";
        suggestions = "Fix the system prompt to consistently use one name. Remove 'Troy AI' from greeting if Sarah is the persona.";
        errorKey = "identity_mismatch";
    }
    // 5. Positive case
    else if (endedReason === 'customer-ended-call') {
        score = 8.5;
    }

    const verdict = score > 6.5 ? "PASS" : (score >= 5.0 ? "FOLLOW_UP" : "ESCALATE");
    return { score, verdict, reason, suggestions, errorKey };
}

async function runAudit() {
    console.log(`Starting Vapi Audit at ${new Date().toISOString()}`);
    
    let trends = { assistants: {} };
    if (fs.existsSync(MEMORY_PATH)) {
        trends = JSON.parse(fs.readFileSync(MEMORY_PATH, 'utf8'));
    }

    let template = "<html><body><h1>Audit Report</h1><p>{{reason}}</p></body></html>";
    if (fs.existsSync(TEMPLATE_PATH)) {
        template = fs.readFileSync(TEMPLATE_PATH, 'utf8');
    }

    const files = fs.readdirSync(CALLS_DIR).filter(f => f.endsWith('.json'));
    let processed = 0;

    // Sort files by mtime to get newest first (approx)
    const sortedFiles = files.map(f => ({ name: f, time: fs.statSync(path.join(CALLS_DIR, f)).mtime.getTime() }))
                             .sort((a, b) => b.time - a.time)
                             .map(f => f.name);

    for (const file of sortedFiles) {
        if (processed >= 10) break; // Process newest 10 calls

        const filePath = path.join(CALLS_DIR, file);
        const call = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        
        const { score, verdict, reason, suggestions, errorKey } = calculateAudit(call);
        const assistant_id = call.assistantId || 'unknown';
        const assistant_name = (call.assistant && call.assistant.name) || assistant_id;

        const payload = {
            call_id: call.id,
            assistant_name,
            assistant_id,
            recording_url: call.recordingUrl,
            timestamp: call.startedAt,
            verdict,
            score,
            reason,
            suggestions
        };

        if (score < 6.0) {
            if (!trends.assistants[assistant_id]) {
                trends.assistants[assistant_id] = { name: assistant_name, failures: {} };
            }
            
            trends.assistants[assistant_id].failures[errorKey] = (trends.assistants[assistant_id].failures[errorKey] || 0) + 1;
            const failCount = trends.assistants[assistant_id].failures[errorKey];

            const subjectPrefix = failCount >= 3 ? "[RECURRING FAILURE] " : "";
            payload.email_subject = `${subjectPrefix}[URGENT AUDIT] ${verdict}: ${assistant_name} (Score: ${score})`;
            
            payload.email_body = template
                .replace(/{{assistant_name}}/g, assistant_name)
                .replace(/{{score}}/g, score)
                .replace(/{{reason}}/g, reason)
                .replace(/{{suggestions}}/g, suggestions)
                .replace(/{{call_id}}/g, call.id);
        }

        try {
            const res = await postData(WEBHOOK_URL, payload);
            console.log(`Processed ${call.id}: ${verdict} (Score: ${score}) (Status: ${res.status})`);
        } catch (e) {
            console.error(`Failed to trigger webhook for ${call.id}: ${e.message}`);
        }
        processed++;
    }

    fs.writeFileSync(MEMORY_PATH, JSON.stringify(trends, null, 2));
    console.log(`Audit finished. Processed ${processed} calls. Memory updated.`);
}

runAudit();
