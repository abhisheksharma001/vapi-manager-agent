const fs = require('fs');

async function triggerN8nWebhook() {
    const webhookUrl = "https://ellavox.app.n8n.cloud/webhook/bdbce354-398d-47f0-9c6e-53f34e065405";
    
    let dashboardData;
    let rawCalls = [];
    
    try {
        // Load the aggregated stats
        dashboardData = JSON.parse(fs.readFileSync('/data/.openclaw/workspace/dashboard_data.json', 'utf8'));
        
        // Load some actual call details (Top 3 recent ones with transcripts)
        const callsDir = '/data/.openclaw/workspace/vapi_calls';
        const files = fs.readdirSync(callsDir).filter(f => f.endsWith('.json')).slice(0, 3);
        
        rawCalls = files.map(file => {
            const call = JSON.parse(fs.readFileSync(`${callsDir}/${file}`, 'utf8'));
            return {
                id: call.id,
                assistantId: call.assistantId,
                summary: call.summary,
                transcript: call.transcript,
                recording: call.recordingUrl
            };
        });

    } catch (e) {
        console.error("Could not read data: " + e.message);
        return;
    }

    const payload = {
        event: "vapi_audit_detailed",
        timestamp: new Date().toISOString(),
        org_id: "ellavox_poc",
        metrics: dashboardData,
        sample_calls: rawCalls,
        optimization_needed: {
            assistant: "Sarah (Caudle Village)",
            issue: "Technical Transfer Failure",
            prompt_fix: "TRANSFER RULE (CRITICAL): After saying 'Let me connect you,' you MUST call transferCall immediately. Do NOT generate further text or wait for silence."
        }
    };

    console.log(`Sending detailed audit data + call samples to n8n...`);

    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            console.log("SUCCESS: Detailed audit data delivered to n8n.");
        } else {
            console.error(`FAILED: n8n returned status ${response.status}`);
        }
    } catch (error) {
        console.error("WEBHOOK ERROR: " + error.message);
    }
}

triggerN8nWebhook();
