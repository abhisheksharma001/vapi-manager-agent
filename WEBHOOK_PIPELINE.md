# PIPELINE: Webhook Integration (n8n)

## GOAL
Instead of sending emails or showing a dashboard, the Manager Agent will POST the structured audit data to an n8n webhook. This allows n8n to handle alerting, CRM logging, or prompt updates.

## WEBHOOK SCHEMA
```json
{
  "event": "audit_completed",
  "org_id": "ellavox_poc",
  "overall_stats": {
    "avg_score": 84,
    "total_audited": 50,
    "critical_failures": 3
  },
  "top_issue": {
    "call_id": "019c3100",
    "assistant_id": "sarah_receptionist",
    "issue": "Technical Transfer Failure",
    "fix_recommendation": "TRANSFER RULE (CRITICAL): After saying 'Let me connect you,' you MUST call transferCall immediately."
  }
}
```

## WORKFLOW
1. Vox polls Vapi every hour.
2. Vox runs the 3-phase analysis.
3. Vox POSTS the final JSON result to the configured n8n Webhook URL.
