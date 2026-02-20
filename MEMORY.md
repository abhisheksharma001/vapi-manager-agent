# Hackathon Project: OpenClaw as Org "Manager Agent"

## THE WHY
Agents currently finish tasks without oversight. This project adds a "manager" layer to catch mistakes, ensure follow-ups, and loop in internal teams.

## CORE GOALS (POC)
1. **Tenant Scoping:** One Manager instance per `org_id`.
2. **Context Storage:** Org context + contacts + Ellavox support data.
3. **Ingestion:** Receive transcripts + tool calls + metadata.
4. **Evaluation:** Produce structured verdict (PASS / FOLLOW_UP / ESCALATE).
5. **Actioning:** Trigger internal-only tools (Slack, email, web enrichment).
6. **Security:** Prevent prompt injection, sanitize web queries, ensure no PII leaks.

## ANALYSIS WORKFLOW
### 1. The Analyzer (Phase 1)
- **Role:** Extract governance and create a scoring blueprint from the agent's system prompt.
- **Goal:** Determine "Intent-Based" evaluation criteria.
- **Temperature:** 0.2 (Balanced Extraction)

### 2. The Scorer (Phase 2)
- **Role:** Forensic auditor.
- **Goal:** Apply the blueprint to transcripts, count violations (behavioral vs. outcome), and calculate a score.
- **Temperature:** 0.1 (Deterministic Scoring)

### 3. The Optimizer (Phase 3)
- **Role:** Prompt Improvement Consultant.
- **Goal:** Generate two stakeholder reports (Management HTML Email & Developer Implementation Guide) with exact prompt fixes and call evidence.
- **Temperature:** 0.3 (Structured Recommendations)

## POC FINAL STATUS (2026-02-17)
- **Status:** COMPLETED & AUTOMATED.
- **Workflow:** Vapi Polling -> 3-Phase Lean Analysis -> n8n Webhook Trigger.
- **n8n Webhook:** `https://ellavox.app.n8n.cloud/webhook/bdbce354-398d-47f0-9c6e-53f34e065405`
- **Automation:** Hourly Cron Job `Hourly Vapi Manager Audit` is ACTIVE.
- **Key Discovery:** Identified critical transfer tool failure pattern in "Sarah" assistant; fix generated and delivered.
- **Tech Stack:** OpenClaw (Manager), Vapi (Source), n8n (Action Layer).
- **Credentials:** Securely stored in `.env`.

[[Talk to Abhi later about scaling this to multi-tenant and automated prompt injection via Vapi API.]]

