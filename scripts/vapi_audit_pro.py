import os
import json
import datetime
import urllib.request
from pathlib import Path

# Config from user prompt
WEBHOOK_URL = "https://ellavox.app.n8n.cloud/webhook/3288552e-2f39-486b-b349-34b7917e5a3c"
RECIPIENT_EMAIL = "taruner420@gmail.com"
STREAK_FILE = "memory/streaks.json"
CALLS_DIR = "vapi_calls"
AUDIT_TEMPLATE = "templates/audit_email.md"
FOLLOWUP_TEMPLATE = "templates/followup_email.md"

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
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
            return f.read()
    return "Template missing at " + path

def calculate_verdict(call):
    transcript = call.get('transcript', '')
    ended_reason = call.get('endedReason', '')
    
    # Audit Logic
    if not transcript or len(transcript) < 30:
        return "ESCALATE", "Empty/Short transcript (Technical Failure).", "Check SIP/Connection."
    
    # Check for transfer failures or specific friction mentioned in the prompt context
    if "Sarah" in transcript and "Troy" in transcript:
         return "ESCALATE", "Identity mismatch detected (Sarah vs Troy).", "Sync system prompt names."

    if "voicemail" in transcript.lower() or "at the tone" in transcript.lower():
        return "PASS", "Voicemail handled correctly.", "No change needed."

    if ended_reason == "customer-ended-call":
        return "PASS", "Handled successfully.", "Maintain current flow."
    
    # Default to Follow Up if not clearly a pass or escalate
    return "FOLLOW_UP", f"Call ended by {ended_reason} - potential friction.", "Review closing sentiment and intent handling."

def run_audit():
    streaks = load_json(STREAK_FILE)
    if 'assistants' not in streaks: streaks['assistants'] = {}
    
    # Get 3 newest calls to keep it concise but thorough for the hourly run
    all_calls = sorted(Path(CALLS_DIR).glob("*.json"), key=os.path.getmtime, reverse=True)[:3]
    
    audit_results = []

    for call_file in all_calls:
        try:
            with open(call_file, 'r') as f:
                call = json.load(f)
        except:
            continue
        
        call_id = call.get('id')
        assistant_id = call.get('assistantId', 'unknown')
        assistant_name = call.get('assistant', {}).get('name', assistant_id)
        recording_url = call.get('recordingUrl')

        verdict, reason, suggestions = calculate_verdict(call)
        
        # Streak Logic
        if assistant_id not in streaks['assistants']:
            streaks['assistants'][assistant_id] = {"type": verdict, "count": 1}
            broken = False
        else:
            asst_streak = streaks['assistants'][assistant_id]
            if asst_streak['type'] == verdict:
                asst_streak['count'] += 1
                broken = False
            else:
                asst_streak['type'] = verdict
                asst_streak['count'] = 1
                broken = True
            
            # Auto-Escalation: 5 FOLLOW_UPs -> ESCALATE
            if asst_streak['type'] == "FOLLOW_UP" and asst_streak['count'] >= 5:
                verdict = "ESCALATE"
                reason = f"[AUTO-ESCALATED] Consecutive Follow-Up count reached {asst_streak['count']}."

        streak_info = {
            "type": streaks['assistants'][assistant_id]['type'],
            "count": streaks['assistants'][assistant_id]['count'],
            "broken": broken
        }

        # Email Payload
        email_payload = None
        if verdict == "ESCALATE":
            tmpl = get_template(AUDIT_TEMPLATE)
            subject = f"[URGENT] ESCALATE: {assistant_name} Audit Needed"
            body = tmpl.replace("{{assistant_name}}", assistant_name).replace("{{reason}}", reason).replace("{{recording_url}}", str(recording_url))
            email_payload = {"subject": subject, "body": body}
        elif verdict == "FOLLOW_UP":
            tmpl = get_template(FOLLOWUP_TEMPLATE)
            subject = f"FOLLOW_UP: {assistant_name} Audit Feedback"
            body = tmpl.replace("{{assistant_name}}", assistant_name).replace("{{reason}}", reason).replace("{{recording_url}}", str(recording_url))
            email_payload = {"subject": subject, "body": body}

        # FINAL PAYLOAD CONSTRUCTION
        payload = {
            "recipient_email": RECIPIENT_EMAIL, # CRITICAL
            "call_id": call_id,
            "assistant_name": assistant_name,
            "assistant_id": assistant_id,
            "recording_url": recording_url,
            "verdict": verdict,
            "streak_info": streak_info,
            "email_payload": email_payload,
            "suggestions": suggestions
        }

        # Trigger Webhook
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), 
                                    headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                audit_results.append(f"Call {call_id}: {verdict} (Asst: {assistant_name}, Streak: {streak_info['count']} {streak_info['type']})")
        except Exception as e:
            audit_results.append(f"Call {call_id}: WEBHOOK ERROR ({e})")

    save_json(STREAK_FILE, streaks)
    return "\n".join(audit_results)

if __name__ == "__main__":
    print(run_audit())
