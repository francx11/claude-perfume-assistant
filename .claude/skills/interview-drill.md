# Interview Drill

**When to apply:** User wants to practice specific interview questions, run a mini mock, or simulate a full interview.

## Usage Modes

### Mode 1: Single Question Drill
User: "Drill me on [topic]" or "Ask me about [interview question]"

1. Ask the question cold — no preamble, no hints
2. User answers (no notes, no looking up)
3. Score 1–5 with this rubric:
   - **5**: Correct + concrete example from own project + handles follow-up
   - **4**: Correct + clear, missing example or one nuance
   - **3**: Partially correct, too vague, or rehearsed but shallow
   - **2**: Mix of correct + incorrect, unsure
   - **1**: Wrong or "I don't know"
4. One follow-up question to go deeper (always)
5. "What would make this a 5?" — one specific improvement

### Mode 2: Level Drill (10 questions, same level)
User: "Drill me on basic Python" / "intermediate ML" / "advanced AWS"

1. Pick 5 questions randomly from that level in `study-plan/phase-6-interview-sim.md`
2. One at a time, no preamble
3. Score each immediately
4. Final: average score + 2 weakest areas to review

### Mode 3: Full Mock Interview (45 min)
User: "Full mock interview"

Structure:
- 5 min: "Tell me about your AI projects" — assess PerfumeShop + Loopgate pitch
- 10 min: 3 basic questions (Python + ML basics)
- 15 min: 4 intermediate questions (RAG, agents, AWS, LLMs)
- 10 min: 2 advanced questions (1 architectural design, 1 deep technical)
- 5 min: debrief (scores, top 3 areas to reinforce)

Track time — warn if answer exceeds 3 minutes.

### Mode 4: Architectural Design
User: "Design question"

1. Give an open-ended system design prompt (e.g., "Design a production RAG system on AWS")
2. User asks clarifying questions first (encourage this)
3. User draws/describes the architecture
4. Claude probes: "Why that service?" "What happens when X fails?" "How does this scale?"
5. Score: completeness (1-5) + AWS service knowledge (1-5) + reasoning quality (1-5)

---

## Scoring Reference Card

| Score | Meaning |
|-------|---------|
| 5 | Hire immediately — clear, correct, with example |
| 4 | Strong candidate — correct, could add more depth |
| 3 | Borderline — knows the concept, struggles with application |
| 2 | Needs work — partial understanding |
| 1 | Not ready — fundamental gap |

**Target before real interview:** avg ≥4 basic, ≥3.5 intermediate, ≥3 advanced.

---

## Follow-up Questions Bank

After any answer, use one of these to go deeper:
- "How would this work at 1000x scale?"
- "What would break first in production?"
- "How is this implemented in PerfumeShop or Loopgate?"
- "What's the alternative approach and when would you choose it?"
- "What monitoring would you add for this in production?"
