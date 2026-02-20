import os
import json
import datetime
import urllib.request
from pathlib import Path

# --- CONFIG (UPDATED VIA CRON) ---
WEBHOOK_URL = "https://ellavox.app.n8n.cloud/webhook/3288552e-2f39-486b-b349-34b7917e5a3c"
RECIPIENT_EMAIL = "taruner420@gmail.com"
STREAKS_FILE = "memory/streaks.json"
CALLS_DIR = "vapi_calls"
TEMPLATE_AUDIT = "templates/audit_email.md"
TEMPLATE_FOLLOWUP = "templates/followup_email.md"

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_template(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
            # Try to extract HTML block if it exists
            if "```html" in content:
                return content.split("```html")[1].split("```")[0].strip()
            return content
    return "<html><body><h1>Audit Report</h1><p>Reason: {{reason}}</p></body></html>"

def analyze_call(call):
    transcript = call.get('transcript', '')
    summary = call.get('summary', '').lower()
    analysis = call.get('analysis', {})
    
    verdict = "PASS"
    reason = "Handled successfully."
    suggestions = "No immediate changes needed."
    
    # 1. Identity Mismatch (Known bug: Sarah vs Troy)
    if "Sarah" in transcript and "Troy" in transcript:
        verdict = "ESCALATE"
        reason = "Assistant identity mismatch detected (Sarah vs Troy)."
        suggestions = "Check system prompt for conflicting identity variables. Sanitize 'Name' variable injection."
    
    # 2. Tech Failure / Connection Issues
    elif not transcript or len(transcript) < 30:
        verdict = "FOLLOW_UP"
        reason = "Silent or extremely short transcript. Possible connection drop."
        suggestions = "Check SIP connection, greeting latency, and carrier logs."
        
    # 3. Business Rule Violation (Tuesday Closure for Cottle Village)
    elif "Tuesday" in transcript.lower() and "closed" not in transcript.lower():
        verdict = "FOLLOW_UP"
        reason = "Failed to mention venue is closed on Tuesdays."
        suggestions = "Ensure 'Closed Day' validation rule is higher in prompt priority."

    # 4. Success Evaluation from Vapi Source
    elif analysis.get('successEvaluation') == 'false':
        verdict = "FOLLOW_UP"
        reason = f"Vapi success evaluation was False. Reason: {analysis.get('reason', 'Unknown')}"
        suggestions = "Review transcript to see where customer intent was dropped or misinterpreted."

    return verdict, reason, suggestions

def update_streak(assistant_id, verdict):
    streaks = load_json(STREAKS_FILE)
    if 'assistants' not in streaks: streaks['assistants'] = {}
    
    # Get or init streak for this assistant
    ast = streaks['assistants'].get(assistant_id, {"type": "PASS", "count": 0})
    
    broken = False
    if ast['type'] == verdict:
        ast['count'] += 1
    else:
        ast['type'] = verdict
        ast['count'] = 1
        broken = True
    
    # CRITICAL: If FOLLOW_UP reaches 5, promote to ESCALATE
    actual_verdict = verdict
    if ast['type'] == "FOLLOW_UP" and ast['count'] >= 5:
        actual_verdict = "ESCALATE"
        # Reset count or keep it? User said "promote", implying severity increase.
        # We'll mark the verdict as ESCALATE for this run.
        
    streaks['assistants'][assistant_id] = ast
    save_json(STREAKS_FILE, streaks)
    return ast, broken, actual_verdict

def run_audit():
    # Find most recent call file
    all_calls = sorted(Path(CALLS_DIR).glob("*.json"), key=os.path.getmtime, reverse=True)
    if not all_calls:
        print("No calls found to audit.")
        return

    call_file = all_calls[0]
    print(f"Auditing file: {call_file}")
    with open(call_file, 'r') as f:
        call = json.load(f)
        
    call_id = call.get('id')
    assistant_id = call.get('assistantId', 'unknown')
    assistant_name = call.get('assistant', {}).get('name', "Assistant")
    recording_url = call.get('recordingUrl', 'N/A')

    # Run logic
    raw_verdict, reason, suggestions = analyze_call(call)
    streak_data, broken, verdict = update_streak(assistant_id, raw_verdict)
    
    email_payload = None
    if verdict == "ESCALATE":
        template = get_template(TEMPLATE_AUDIT)
        subject = f"[URGENT] ESCALATE: {assistant_name} ({reason})"
        body = template.replace("{{assistant_name}}", assistant_name) \
                       .replace("{{reason}}", reason) \
                       .replace("{{suggestions}}", suggestions) \
                       .replace("{{call_id}}", str(call_id)) \
                       .replace("{{recording_url}}", str(recording_url))
        email_payload = {"subject": subject, "body": body}
        
    elif verdict == "FOLLOW_UP":
        template = get_template(TEMPLATE_FOLLOWUP)
        subject = f"[FOLLOW-UP] Minor Issue: {assistant_name}"
        body = template.replace("{{assistant_name}}", assistant_name) \
                       .replace("{{reason}}", reason) \
                       .replace("{{recording_url}}", str(recording_url)) \
                       .replace("{{streak_count}}", str(streak_data['count'])) \
                       .replace("{{streak_type}}", str(streak_data['type']))
        email_payload = {"subject": subject, "body": body}

    # Prepare final payload with mandatory recipient_email at top level
    payload = {
        "recipient_email": RECIPIENT_EMAIL,
        "call_id": call_id,
        "assistant_name": assistant_name,
        "assistant_id": assistant_id,
        "recording_url": recording_url,
        "verdict": verdict,
        "streak_info": {
            "type": streak_data['type'],
            "count": streak_data['count'],
            "broken": broken
        },
        "email_payload": email_payload,
        "suggestions": suggestions
    }

    print(f"Sending payload to {WEBHOOK_URL} for {call_id} (Verdict: {verdict})")
    
    req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), 
                                headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.status
            resp_body = response.read().decode('utf-8')
            print(f"Audit Result: {call_id} | Verdict: {verdict} | Webhook Status: {status} | Response: {resp_body}")
    except Exception as e:
        print(f"WEBHOOK ERROR: {e}")

if __name__ == "__main__":
    run_audit()
