const fs = require('fs');

async function triggerN8nWebhook() {
    const webhookUrl = "https://ellavox.app.n8n.cloud/webhook/bdbce354-398d-47f0-9c6e-53f34e065405";
    
    let dashboardData;
    try {
        dashboardData = JSON.parse(fs.readFileSync('/data/.openclaw/workspace/dashboard_data.json', 'utf8'));
    } catch (e) {
        console.error("Could not read dashboard data: " + e.message);
        return;
    }

    const payload = {
        event: "vapi_audit_completed",
        timestamp: new Date().toISOString(),
        org_id: "ellavox_poc",
        summary: dashboardData
    };

    console.log(`Sending audit data to n8n webhook: ${webhookUrl}...`);

    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            console.log("SUCCESS: Audit data delivered to n8n.");
        } else {
            console.error(`FAILED: n8n returned status ${response.status}`);
        }
    } catch (error) {
        console.error("WEBHOOK ERROR: " + error.message);
    }
}

triggerN8nWebhook();
