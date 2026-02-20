const fs = require('fs');

async function triggerAuditWebhook() {
    const webhookUrl = "https://ellavox.app.n8n.cloud/webhook/bdbce354-398d-47f0-9c6e-53f34e065405";
    
    const analysisPath = 'vapi_audit_results.json';
    if (!fs.existsSync(analysisPath)) {
        console.error("Analysis file not found.");
        return;
    }
    
    const analysisText = fs.readFileSync(analysisPath, 'utf8');

    const payload = {
        event: "vapi_manager_audit_run",
        timestamp: new Date().toISOString(),
        org_id: "ellavox_poc",
        audit_results: analysisText,
        summary: "Hourly Vapi Manager Audit: Call 019c5293-9990-7ee0-a638-9f11d6aac18b analyzed."
    };

    console.log(`Sending audit results to n8n...`);

    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            console.log("SUCCESS: Audit results delivered to n8n.");
        } else {
            const text = await response.text();
            console.error(`FAILED: n8n returned status ${response.status} - ${text}`);
        }
    } catch (error) {
        console.error("WEBHOOK ERROR: " + error.message);
    }
}

triggerAuditWebhook();
