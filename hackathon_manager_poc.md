# Hackathon POC: OpenClaw "Manager Agent"

## Core Concept
A tenant-scoped (per-organization) AI oversight layer that acts as a "manager" for worker agents. Instead of treating an agent's last message as the end of the job, this Manager Agent reviews the interaction to ensure quality, security, and completeness.

## Objectives
1. **Oversight:** Catch mistakes, dropped action items, and hallucinations.
2. **Actionability:** Trigger internal follow-ups (Slack/Email/Jira) when needed.
3. **Security:** Prevent prompt injection and ensure data isolation between orgs.

## Architecture (POC)

### 1. Ingestion Layer
- **Input:** Full conversation transcript (User + Agent) + Tool Execution Logs.
- **Metadata:** Org ID, Customer Tier, Active Tools.

### 2. The Brain (OpenClaw / Gemini 3 Pro)
- **Role:** Evaluator.
- **Prompt Strategy:** "You are a QA Manager. Review this transcript. Did the agent solve the user's intent? Did it use tools correctly? Check for security risks."
- **Output Structure:**
  ```json
  {
    "verdict": "PASS" | "FOLLOW_UP" | "ESCALATE",
    "reason": "Agent failed to ask for order ID before checking status.",
    "security_risk": "None",
    "suggested_actions": ["email_support", "log_ticket"]
  }
  ```

### 3. Action Layer
- **Internal Comms:** Send alerts to internal Slack channels or Support Email.
- **Sanitized Web Search:** Verify facts if the agent made claims (e.g., "Is our API actually down?").
- **CRM/Ticket Update:** Draft a Jira ticket or update HubSpot if the interaction requires human intervention.

## Key Features to Build
- **Tenant Isolation:** Ensure Manager A only sees Org A's data.
- **Prompt Injection Guardrails:** The Manager must detect if the *user* tried to trick the *worker agent* (e.g., "Ignore previous instructions").
- **Playbooks:** Different evaluation rules for Support vs. Sales agents.

## Why OpenClaw?
- **Native Tooling:** Can easily connect to Slack, Email, and Web.
- **State Awareness:** Can maintain "Org Context" over time (long-term memory).
- **Security:** Self-hosted / Private deployment ensures customer data doesn't leak.
