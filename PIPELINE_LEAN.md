# LEAN MANAGER PIPELINE (Optimization v1)

## PHASE 1: ANALYZER (Temp 0.2)
**Goal:** Extract core rules only.
**Output Format:**
```json
{
  "must_collect": [],
  "must_validate": [],
  "sequence": [],
  "forbidden": []
}
```

## PHASE 2: SCORER (Temp 0.1)
**Goal:** Deterministic violation counting.
**Output Format:**
```json
{
  "score": 0,
  "violations": [{"type": "", "evidence": ""}],
  "satisfaction": "level"
}
```

## PHASE 3: OPTIMIZER (Temp 0.3)
**Goal:** Concise action.
**Output Format:**
- **Management:** 2-sentence summary.
- **Developer:** One "Issue -> Fix" block per major violation.
