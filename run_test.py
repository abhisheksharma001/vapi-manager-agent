import json

# PHASE 1: MOCK ANALYZER OUTPUT (Generated from ASSISTANT_PROMPT)
BLUEPRINT = {
    "industry_type": "leasing",
    "call_direction": "inbound",
    "compliance_sensitivity": "medium",
    "mandatory_collections": ["caller_name", "apartment_number", "issue_description"],
    "mandatory_validations": ["apartment_number_confirmation"],
    "required_sequence_rules": ["greeting_first", "name_before_issue"],
    "forbidden_behaviors": ["never_interrupt"],
    "prompt_quality_audit": {
        "prompt_quality_score": 85,
        "prompt_risk_level": "low"
    },
    "scoring_framework": {
        "base_categories": [
            {"name": "Listening & Turn-Taking", "weight": 20, "strictness": "strict"},
            {"name": "Workflow Adherence", "weight": 20, "strictness": "intent_based"},
            {"name": "Data Accuracy & Validation", "weight": 15, "strictness": "strict_on_accuracy_flexible_on_phrasing"},
            {"name": "Compliance & Safety", "weight": 20, "strictness": "strict"},
            {"name": "Naturalness & Tone", "weight": 15, "strictness": "flexible"},
            {"name": "Task Completion & Conversion", "weight": 10, "strictness": "intent_based"}
        ]
    }
}

# PHASE 2: MOCK SCORER OUTPUT (Generated from BLUEPRINT + TRANSCRIPT)
SCORING_RESULT = {
    "overall_score": 75,
    "severity": "minor",
    "caller_satisfaction": {
        "level": "moderate",
        "positive_signals_count": 1,
        "negative_signals_count": 0,
        "evidence": {"positive_quotes": ["Thanks, bye"]}
    },
    "category_scores": [
        {"name": "Listening & Turn-Taking", "weight": 20, "score_awarded": 20, "reasoning": "No interruptions detected."},
        {"name": "Workflow Adherence", "weight": 20, "score_awarded": 18, "reasoning": "Sequence followed, all info collected."},
        {"name": "Data Accuracy & Validation", "weight": 15, "score_awarded": 5, "reasoning": "Mandatory validation of apartment number was skipped."},
        {"name": "Compliance & Safety", "weight": 20, "score_awarded": 20, "reasoning": "No compliance issues."},
        {"name": "Naturalness & Tone", "weight": 15, "score_awarded": 12, "reasoning": "Slightly robotic transitions."},
        {"name": "Task Completion & Caller Satisfaction", "weight": 10, "score_awarded": 0, "reasoning": "Task completed but critical validation missing."}
    ],
    "violations": [
        {
            "type": "skipped_mandatory_validation",
            "severity": "major",
            "evidence": "Agent moved to closing without confirming '402'."
        }
    ]
}

# Final JSON output as requested by Phase 3 (Optimizer)
OPTIMIZER_OUTPUT = {
    "management_email_html": """
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding: 20px;">
    <div style="background-color:#ffffff; border-radius:8px; border:1px solid #e5e7eb; padding: 20px; max-width: 600px; margin: auto;">
        <h2 style="background-color:#111827; color:#ffffff; padding:15px; border-radius: 4px;">📊 Call Quality Report</h2>
        <div style="background-color:#fef3c7; border-left:4px solid #f59e0b; padding:15px; margin: 15px 0;">
            <p><strong>Call Score:</strong> <span style="font-size:18px; color:#f59e0b;">75/100</span></p>
            <p><strong>Caller Experience:</strong> Moderate</p>
            <p><strong>Issue Type:</strong> Script needs clearer rules</p>
        </div>
        <h3>What Happened</h3>
        <p>The caller reported a leak in apartment 402. While the agent collected all necessary information, they failed to confirm the apartment number before ending the call, which is a mandatory requirement. The caller was satisfied, but the lack of validation increases the risk of incorrect maintenance dispatch.</p>
        <h3>Recommended Action</h3>
        <p><strong>Short-term:</strong> Review dispatch for apartment 402.<br><strong>Long-term:</strong> Strengthen the validation instruction in the system prompt.</p>
    </div>
</body>
</html>
""",
    "developer_email_html": """
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding: 20px;">
    <div style="background-color:#ffffff; border-radius:8px; border:1px solid #e5e7eb; padding: 20px; max-width: 720px; margin: auto;">
        <h2 style="background-color:#111827; color:#ffffff; padding:15px; border-radius: 4px;">🔧 Developer Implementation Guide</h2>
        <p><strong>Call Score: 75/100</strong> • Root Cause: Script has gaps</p>
        <h3 style="color:#dc2626;">❌ Issue #1: Skipped Mandatory Validation</h3>
        <div style="background:#fef2f2; border:1px solid #fee2e2; padding:15px; border-radius:6px;">
            <p><strong>Where in Call:</strong> Before closing the conversation.</p>
            <p><strong>What Agent Said:</strong> "Got it. I'll get someone over there."</p>
            <p><strong>What It Should Say:</strong> "Got it. Just to confirm, you are in apartment 402, correct? I'll get someone over there."</p>
            <p><strong>Why It Matters:</strong> Ensures maintenance teams go to the correct location.</p>
        </div>
        <div style="background:#fffbeb; padding:15px; margin-top:10px; border-radius:6px;">
            <p><strong>Fix to Add in Prompt:</strong></p>
            <pre style="background:#422006; color:#fbbf24; padding:10px; border-radius:4px;">VALIDATION RULE (STRICT): You MUST explicitly read back the apartment number and wait for the caller to confirm it before ending the call or initiating a transfer.</pre>
            <p style="font-size:12px;">📍 Add this to: RULES section</p>
        </div>
    </div>
</body>
</html>
"""
}

print(json.dumps(OPTIMIZER_OUTPUT))
