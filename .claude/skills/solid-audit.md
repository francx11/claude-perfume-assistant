# SOLID Audit

**When to apply:** User asks to check or enforce SOLID principles in the project code.

## Goal
Audit `src/` for real SOLID violations. Fix only violations that add clear value — do not over-engineer small, working code. Report findings first, fix only with user approval.

---

## Step 1 — Read the key files

Read these files before doing anything:
- `src/agents/orchestrator.py`
- `src/tools/perfume_tools.py`
- `src/api/claude_client.py`
- `src/data/loader.py`
- `src/api/endpoints.py`

---

## Step 2 — Audit each SOLID principle

For each principle, check the actual code and note only **real violations** (not theoretical ones). A small project with 3 classes does not need interface segregation — use judgment.

### S — Single Responsibility
- Does any class handle more than one distinct concern?
- Signs: class name contains "And", methods that do unrelated things, >200 lines with mixed logic.

### O — Open/Closed
- Is there a `match/case` or `if/elif` chain that must be modified every time a new variant is added?
- The `execute_tool()` match/case in `PerfumeTools` is a known candidate.

### L — Liskov Substitution
- Are there subclasses that override methods by raising `NotImplementedError` or changing behavior incompatibly?
- Check any class inheritance in the codebase.

### I — Interface Segregation
- Are there base classes or ABCs with methods that some subclasses don't use?
- In a small project this is rarely violated — skip if no inheritance is present.

### D — Dependency Inversion
- Does any class instantiate its dependencies internally (`self.x = ConcreteClass()`)?
- Known candidate: `OrchestratorAgent.__init__` creating `ClaudeClient` and `PerfumeTools` directly.

---

## Step 3 — Report findings

Present a table:

| Principle | File | Line | Violation | Severity |
|-----------|------|------|-----------|----------|
| S | ... | ... | ... | Low/Med/High |

**Severity guide:**
- **High** — actively makes the code harder to test, extend, or maintain today.
- **Med** — will become a problem as the project grows.
- **Low** — theoretical; not worth fixing at current project scale.

Only recommend fixing **High** and **Med** violations.

---

## Step 4 — Propose fixes (one by one, with user approval)

For each High/Med violation:
1. Show the current code snippet.
2. Show the proposed fix.
3. Explain the tradeoff in one sentence.
4. Ask: "¿Aplico este fix?"

Do NOT batch all fixes. Apply them one at a time after approval.

---

## Step 5 — After all fixes

- Run `ruff check src/ --fix` and `ruff format src/` to keep style clean.
- Confirm tests still pass: `pytest tests/ -q`.
- Propose tracker update if any new SOLID topics were practiced.
