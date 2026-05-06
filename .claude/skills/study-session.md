# Study Session

**When to apply:** Starting a new study session. Use this to structure any topic from any phase.

## Session Flow

### 1. Topic Selection (2 min)
Ask the user: "Which phase are we in? Which topic from the phase file?"
Check `progress/tracker.md` — suggest the next `[ ]` topic in the current phase.

### 2. Prior Knowledge Check (5 min)
Ask: "Before I explain anything — what do you already know about [topic]? How does it connect to what you've built in PerfumeShop or Loopgate?"

Wait for their answer. Do NOT explain yet.
- If answer is strong → confirm, skip basics, go to depth
- If answer is partial → ask a follow-up question to probe the gap
- If answer is wrong → ask: "Let's test that — what would happen if [edge case]?"

### 3. Guided Discovery (10–15 min)
Ask questions that lead the user to discover the concept. Examples:
- "Why do you think Python has both lists AND tuples?"
- "What happens in memory when you append to a list 1000 times?"
- "In your orchestrator, what would break if Claude returned 3 tool_use blocks and you only processed the first one?"

After 2 failed attempts at a question → give a directional hint, not the answer.

### 4. Application Exercise (15–20 min)
Assign the exercise from the phase file. Be specific:
"Open `src/data/loader.py`. I want you to [specific task]. Show me the code when done."

Review the implementation:
- Ask "Why did you make this choice?" before suggesting alternatives
- If there's a bug, ask "Does this code handle the case where [edge case]?"

### 5. Interview Answer Drill (5 min)
"Now give me the 2-minute interview answer for [topic]. Speak as if you're in the interview."

Score 1–5. Feedback: "What would push this from a [score] to a 5: [one specific addition]."

### 6. Session Wrap-up (2 min)
Summary: topic covered, what was strong, one thing to reinforce.
Propose tracker update: "Update `progress/tracker.md`: change [topic] from `[ ]` to `[x]` or `[~]`."

---

## Quick Session (30 min) — Concept Only
Steps 1 → 2 → 3 → 5. Skip implementation. Good for conceptual interview topics (ML classical, AWS services).

## Deep Session (90 min) — Full Implementation
Steps 1 → 2 → 3 → 4 → 5 → 6. Good for Phase 1 Python exercises, Phase 2 RAG/LangChain extensions.
