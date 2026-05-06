# Progress Tracking

**When to apply:** End of a study session, after a concept-check scores ≥4, or when user asks "update my progress" / "where am I?".

## Update Protocol

### After a study session:
1. List topics covered this session
2. For each: was the concept-check score ≥4? → `[x]` · was it `[~]` (understood but needs reinforcement)? · still `[ ]`?
3. Propose specific edits to `progress/tracker.md`:
   ```
   Change line: `| decorators | [ ] |` → `| decorators | [x] | Session 2026-05-05 |`
   ```
4. Ask: "Any topic you want to mark differently? Be honest — `[x]` means you could answer it cold in an interview."

### Rules for status:
- `[x]` ONLY if: explained correctly without notes + score ≥4/5 on concept-check + applied in code or interview drill
- `[~]` if: understood conceptually but not yet applied, or score 3/5
- `[ ]` if: not studied or score ≤2/5

---

## Progress Review Protocol

### When user asks "where am I?" or "what should I study next?":

1. Read `progress/tracker.md`
2. Count: `[x]` mastered · `[~]` in progress · `[ ]` not started — per phase
3. Report:
   ```
   Phase 1: 8/28 mastered, 2 in progress
   Phase 2: 3/45 mastered (all from days 1-11)
   Phase 3–6: not started
   ```
4. Recommend next session: "Highest priority next: [topic] in Phase [N] — it appears in [N] interview questions."
5. Flag blockers: "You have `[~]` on generators since last session — 10 min review before moving on?"

---

## Phase Completion Check

Before marking a phase as complete, run through its completion criteria checklist from the phase file. All items must be `[x]`. If any are `[~]`, schedule a reinforcement session for those topics.

---

## Weekly Review (optional, every 7 days)

Ask Claude: "Weekly review"

Claude will:
1. Show topics moved to `[x]` this week
2. Show topics still `[~]` from last week (flag if stuck for >2 sessions)
3. Estimate: "At current pace, Phase [N] completes in ~[X] sessions"
4. Suggest: one topic to reinforce + one new topic to start next session
