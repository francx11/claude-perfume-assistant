# Concept Check

**When to apply:** User says "check if I understood X" or "explain X to me" or wants to verify their understanding before marking a topic as [x].

## Protocol

### Step 1: Ask them to explain it
"Explain [concept] in your own words, as if I had never heard of it."

Do NOT confirm or deny correctness yet. Let them finish.

### Step 2: Test an edge case
Pick one of these challenge types:
- **Contrast:** "What is the difference between [concept] and [similar thing]?"
- **Break it:** "What happens when [edge case or failure mode]?"
- **Apply it:** "How would you use [concept] in PerfumeShop or Loopgate?"
- **Scale it:** "This works for 100 records. What changes with 10 million?"

### Step 3: Ask for the interview answer
"Now give me the version you'd say in an interview — 2 sentences max."

Score the answer:
- **5/5**: Correct, precise, includes a concrete example
- **4/5**: Correct and clear, missing one key nuance
- **3/5**: Mostly correct, vague or missing the "why"
- **2/5**: Partially correct, mixed with misconception
- **1/5**: Fundamental misunderstanding

### Step 4: Fill the gap
Only if score ≤3: give one clarifying insight. Then ask them to try the interview answer again.

### Step 5: Tracker update
If score ≥4: "Mark [topic] as `[x]` in `progress/tracker.md`."
If score 3: "Mark as `[~]` — revisit in next session."

---

## Example

User: "Check if I understood decorators."

Claude asks:
1. "Explain decorators in your own words."
2. "What happens when you stack two decorators: `@A` then `@B`? Which runs first?"
3. "Give the 2-sentence interview answer."
4. Score + fill gap if needed.
5. Propose tracker update.
