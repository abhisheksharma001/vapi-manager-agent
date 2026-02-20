import os
import requests
import json
from datetime import datetime, timedelta

def fetch_vapi_calls():
    api_key = "b14958b8-1c44-4bfb-b8f8-dac3d616963f"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Calculate timestamp for 24 hours ago
    yesterday = datetime.utcnow() - timedelta(hours=24)
    created_at_after = yesterday.isoformat() + "Z"
    
    url = f"https://api.vapi.ai/call?limit=50&createdAtAfter={created_at_after}"
    
    print(f"Fetching calls created after {created_at_after}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        calls = response.json()
        
        print(f"Successfully fetched {len(calls)} calls.")
        
        # Create output directory
        os.makedirs("vapi_calls", exist_ok=True)
        
        for call in calls:
            call_id = call.get("id")
            with open(f"vapi_calls/{call_id}.json", "w") as f:
                json.dump(call, f, indent=2)
        
        return calls
    except Exception as e:
        print(f"Error fetching calls: {e}")
        return []

if __name__ == "__main__":
    fetch_vapi_calls()
