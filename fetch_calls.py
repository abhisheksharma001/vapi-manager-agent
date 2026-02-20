import urllib.request
import json
import os
from datetime import datetime, timedelta

def fetch():
    api_key = "b14958b8-1c44-4bfb-b8f8-dac3d616963f"
    url = f"https://api.vapi.ai/call?limit=3"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Mozilla/5.0"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(json.dumps(data))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fetch()
