<h1 align="center">vapi-manager-agent</h1>

<p align="center">
  <b>Autonomous forensic auditor for AI voice agents.<br/>
  Extracts governance rules, scores call transcripts, generates prompt fixes.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=0d1117" alt="Python" />
  <img src="https://img.shields.io/badge/Vapi-voice%20AI-5eead4?style=flat-square&labelColor=0d1117" alt="Vapi" />
  <img src="https://img.shields.io/badge/n8n-automation-38bdf8?style=flat-square&labelColor=0d1117" alt="n8n" />
  <img src="https://img.shields.io/badge/type-Hackathon%20POC-a78bfa?style=flat-square&labelColor=0d1117" alt="Hackathon POC" />
</p>

---

## What it does

AI voice agents are hard to audit — they produce transcripts, but nothing automatically checks whether the agent followed its own instructions. This tool closes that gap.

Give it a Vapi voice agent. It:
1. **Analyzes** the system prompt and extracts a governance blueprint — the rules the agent is supposed to follow
2. **Scores** real call transcripts against that blueprint, flagging every violation
3. **Generates** developer-ready prompt fixes and a management-level report

The result: a full forensic audit of your voice agent's behaviour, end-to-end, with no human review required.

---

## How it works

```
Vapi voice agent (system prompt + call transcripts)
         │
         ▼
  ① Analyzer agent
     Extracts governance blueprint from system prompt
         │
         ▼
  ② Scorer agent
     Audits each transcript against the blueprint
     Flags violations with severity + context
         │
         ▼
  ③ Optimizer agent
     Generates prompt rewrites for each violation
     Produces a management summary report
```

---

## Stack

| Layer | Role |
|---|---|
| **OpenClaw** | Core multi-agent framework — orchestrates the three sub-agents |
| **Vapi** | Voice agent source — pulls system prompts and call transcripts |
| **n8n** | Action and alerting layer — routes reports and triggers |

---

## Background

Built as a hackathon proof-of-concept. The core insight: voice agent governance is a retrieval + reasoning problem — you have a spec (the system prompt) and evidence (the transcripts), and an LLM can act as a reliable judge between the two.

The three-agent pipeline (Analyze → Score → Optimize) keeps each step focused and auditable. OpenClaw provides the multi-agent orchestration layer so the agents can run in parallel across large transcript volumes.

---

## License

MIT
