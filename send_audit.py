import urllib.request
import json
import os
from datetime import datetime

WEBHOOK_URL = "https://ellavox.app.n8n.cloud/webhook/3288552e-2f39-486b-b349-34b7917e5a3c"

def send_payload(payload):
    print(f"Sending payload for {payload['call_id']}...")
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.getcode()}")
    except Exception as e:
        print(f"Error: {e}")

payloads = [
  {
    "call_id": "019c7780-1284-7334-8eca-75c953d1631d",
    "assistant_name": "warm transfer testin Abh",
    "assistant_id": "0f11ec0b-8ddf-41d3-a4f9-ef8ff12d96e2",
    "recording_url": "https://storage.vapi.ai/019c7780-1284-7334-8eca-75c953d1631d-1771531454904-564d643f-1e24-46fd-b76c-76a1bed5b9d3-mono.wav",
    "timestamp": "2026-02-19T20:03:28.004Z",
    "verdict": "ESCALATE",
    "score": 4.5,
    "reason": "The assistant initiated the transfer process prematurely. While it greeted and asked for the name, it proceeded to transfer ('I have a caller on the line for you') without receiving or confirming a name from the user ('Let me see if she.').",
    "suggestions": "Improve intent recognition to ensure a name is captured and confirmed before triggering the transfer tool.",
    "email_subject": "Critical Failure: Premature Transfer on Call 019c7780-1284-7334-8eca-75c953d1631d",
    "email_body": "<html><body><h2>Audit Alert: ESCALATE</h2><p><strong>Assistant:</strong> warm transfer testin Abh</p><p><strong>Call ID:</strong> 019c7780-1284-7334-8eca-75c953d1631d</p><p><strong>Score:</strong> 4.5/10</p><p><strong>Issue:</strong> The assistant attempted a warm transfer without successfully identifying or confirming the caller's name, violating the protocol: Greet -> Ask Name -> Confirm -> Transfer.</p><p><strong>Transcript:</strong> AI: Hello? User: Hello? AI: Hello. Thanks for calling. May I have your name, please? User: Let me see if she. AI: No problem at all. AI: I have a caller on the line for you.</p></body></html>"
  },
  {
    "call_id": "019c7764-531d-766a-b08b-17bf01481a2c",
    "assistant_name": "Sarah (Poddle Village)",
    "assistant_id": "0bbece1d-a3b5-42aa-8b8b-c151536a17f5",
    "recording_url": "https://storage.vapi.ai/019c7764-531d-766a-b08b-17bf01481a2c-1771529605002-ee7bd739-358b-4be3-a13f-a5f592a102ff-mono.wav",
    "timestamp": "2026-02-19T19:33:09.533Z",
    "verdict": "FOLLOW_UP",
    "score": 6.0,
    "reason": "The assistant followed the standard greeting protocol correctly. The call ended due to the customer hanging up immediately after the greeting, providing no opportunity for further interaction.",
    "suggestions": "No assistant error detected; however, a score of 6.0 is assigned as the interaction was incomplete.",
    "email_subject": "Low Engagement Alert: Call 019c7764-531d-766a-b08b-17bf01481a2c",
    "email_body": "<html><body><h2>Audit Alert: FOLLOW_UP</h2><p><strong>Assistant:</strong> Sarah (Poddle Village)</p><p><strong>Call ID:</strong> 019c7764-531d-766a-b08b-17bf01481a2c</p><p><strong>Score:</strong> 6.0/10</p><p><strong>Observation:</strong> Assistant performed the greeting correctly, but the customer hung up immediately. This may indicate a 'ghost' call or lack of user interest.</p></body></html>"
  },
  {
    "call_id": "019c7248-81a2-766e-a0a8-5e312cfbe41f",
    "assistant_name": "Falcon Point Maintenance",
    "assistant_id": "b9ee9c05-864d-4e62-b907-92e5b00dd422",
    "recording_url": "https://storage.vapi.ai/019c7248-81a2-766e-a0a8-5e312cfbe41f-1771443888513-39e264c9-77a3-4e90-8f45-5879ee578cf6-mono.wav",
    "timestamp": "2026-02-18T19:44:40.354Z",
    "verdict": "FOLLOW_UP",
    "score": 6.0,
    "reason": "The assistant delivered the standard greeting protocol correctly. The customer hung up immediately, resulting in an incomplete session with no actionable data.",
    "suggestions": "Monitor for high hang-up rates at the greeting stage which might suggest latency or connection issues.",
    "email_subject": "Low Engagement Alert: Call 019c7248-81a2-766e-a0a8-5e312cfbe41f",
    "email_body": "<html><body><h2>Audit Alert: FOLLOW_UP</h2><p><strong>Assistant:</strong> Falcon Point Maintenance</p><p><strong>Call ID:</strong> 019c7248-81a2-766e-a0a8-5e312cfbe41f</p><p><strong>Score:</strong> 6.0/10</p><p><strong>Observation:</strong> Greeting was successful, but the session ended prematurely due to customer hang-up.</p></body></html>"
  }
]

if __name__ == '__main__':
    for p in payloads:
        send_payload(p)
