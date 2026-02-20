const fs = require('fs');
const path = require('path');

async function fetchVapiCalls() {
    const apiKey = "b14958b8-1c44-4bfb-b8f8-dac3d616963f";
    
    // Calculate timestamp for 24 hours ago
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000);
    const createdAtAfter = yesterday.toISOString();
    
    const url = `https://api.vapi.ai/call?limit=50`;
    
    console.log(`Fetching calls created after ${createdAtAfter}...`);
    
    try {
        const response = await fetch(url, {
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const calls = await response.json();
        console.log(`Successfully fetched ${calls.length} calls.`);
        
        const dir = path.join(__dirname, 'vapi_calls');
        if (!fs.existsSync(dir)){
            fs.mkdirSync(dir);
        }
        
        for (const call of calls) {
            const callId = call.id;
            fs.writeFileSync(path.join(dir, `${callId}.json`), JSON.stringify(call, null, 2));
        }
        
        return calls;
    } catch (e) {
        console.error(`Error fetching calls: ${e.message}`);
        return [];
    }
}

fetchVapiCalls();
