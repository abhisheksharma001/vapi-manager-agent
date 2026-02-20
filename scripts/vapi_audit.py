import os
import json
import datetime
import urllib.request
from pathlib import Path

WEBHOOK_URL = "https://ellavox.app.n8n.cloud/webhook/3288552e-2f39-486b-b349-34b7917e5a3c"
MEMORY_PATH = "memory/failure_trends.json"
CALLS_DIR = "vapi_calls"
TEMPLATE_PATH = "templates/audit_email.md"

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_email_template():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, 'r') as f:
            return f.read()
    return "<html><body><h1>Audit Report</h1><p>{{reason}}</p></body></html>"

def calculate_audit(call):
    transcript = call.get('transcript', '')
    summary = call.get('summary', '').lower()
    ended_reason = call.get('endedReason', '')
    
    score = 7.0 
    
    if not transcript or len(transcript) < 20:
        score = 3.0
        reason = "Empty or extremely short transcript. Likely technical failure or hangup."
        suggestions = "Check SIP stability. Review greeting latency."
    elif "error" in ended_reason or "failed" in ended_reason:
        score = 2.0
        reason = f"Call ended with technical error: {ended_reason}"
        suggestions = "Investigate Vapi logs for provider-side errors."
    elif "Sarah" in transcript and "Troy" in transcript:
        score = 4.5
        reason = "Assistant identity mismatch (Sarah vs Troy)."
        suggestions = "Fix the system prompt to consistently use one name."
    elif score >= 7.0:
        score = 8.5 if "customer-ended-call" in ended_reason else 7.5
        reason = "Call handled successfully."
        suggestions = "Maintain current flow."

    if score > 6.5: verdict = "PASS"
    elif score >= 5.0: verdict = "FOLLOW_UP"
    else: verdict = "ESCALATE"
    
    return score, verdict, reason, suggestions

def run_audit():
    print(f"Starting Vapi Audit at {datetime.datetime.now()}")
    trends = load_json(MEMORY_PATH)
    if 'assistants' not in trends: trends['assistants'] = {}
    
    template = get_email_template()
    calls_processed = 0
    
    # Sort files to process newest first (by modification time or filename if UUID-based)
    all_calls = sorted(Path(CALLS_DIR).glob("*.json"), key=os.path.getmtime, reverse=True)
    
    for call_file in all_calls:
        try:
            with open(call_file, 'r') as f:
                call = json.load(f)
        except:
            continue
        
        call_id = call.get('id')
        assistant_id = call.get('assistantId', 'unknown')
        assistant_name = call.get('assistant', {}).get('name', assistant_id)
        
        score, verdict, reason, suggestions = calculate_audit(call)
        
        payload = {
            "call_id": call_id,
            "assistant_name": assistant_name,
            "assistant_id": assistant_id,
            "recording_url": call.get('recordingUrl'),
            "timestamp": call.get('startedAt'),
            "verdict": verdict,
            "score": score,
            "reason": reason,
            "suggestions": suggestions
        }
        
        if score < 6.0:
            error_key = "identity_mismatch" if "identity mismatch" in reason else "general_performance"
            
            if assistant_id not in trends['assistants']:
                trends['assistants'][assistant_id] = {"name": assistant_name, "failures": {}}
            
            trends['assistants'][assistant_id]['failures'][error_key] = trends['assistants'][assistant_id]['failures'].get(error_key, 0) + 1
            fail_count = trends['assistants'][assistant_id]['failures'][error_key]
            
            subject_prefix = "[RECURRING FAILURE] " if fail_count >= 3 else ""
            payload['email_subject'] = f"{subject_prefix}[URGENT AUDIT] {verdict}: {assistant_name} (Score: {score})"
            
            body = template.replace("{{assistant_name}}", assistant_name) \
                           .replace("{{score}}", str(score)) \
                           .replace("{{reason}}", reason) \
                           .replace("{{suggestions}}", suggestions) \
                           .replace("{{call_id}}", call_id)
            payload['email_body'] = body

        # Trigger Webhook using urllib
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), 
                                    headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"Processed {call_id}: {verdict} ({response.status})")
        except Exception as e:
            print(f"Failed to trigger webhook for {call_id}: {e}")
            
        calls_processed += 1
        if calls_processed >= 5: break 

    save_json(MEMORY_PATH, trends)
    print(f"Audit finished. Processed {calls_processed} calls.")

if __name__ == "__main__":
    run_audit()
