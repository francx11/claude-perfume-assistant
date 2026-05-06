# Phase 1: Python Solid

**Prerequisite:** Days 1–11 completed (basic Python, pytest, pandas, FastAPI).
**Goal:** Close Python interview gaps, add professional tooling, learn patterns/SOLID.

---

## Topics

### 1. Python Data Structures [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| list vs tuple | "Difference between list and tuple?" | [ ] |
| set / frozenset | "What is a set? When do you use it?" | [ ] |
| dict internals | "How does Python dict work? Time complexity?" | [ ] |
| mutable default arg | "What's wrong with `def f(x=[])`?" | [ ] |

**Exercise:** In `src/data/loader.py`, find 2 places where a `set` would be more efficient than the current list. Explain why to Claude.

**Resources:** [Python docs - Data Structures](https://docs.python.org/3/tutorial/datastructures.html)

---

### 2. Functions: Generators, Lambda, Decorators [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| generator (yield) | "Difference between function and generator?" | [ ] |
| lambda | "What is a lambda expression? Give an example." | [ ] |
| decorator | "What is a decorator? Implement one." | [ ] |
| `__init__.py` | "What is `__init__.py`? What goes in it?" | [ ] |

**Exercise — generator:** Rewrite `DataLoader.get_all_perfumes()` as a generator (`yield` one perfume at a time) and explain the memory difference to Claude.

**Exercise — decorator:** Write a `@log_call` decorator that prints function name + args before any call. Apply it to `PerfumeTools.execute_tool()`.

**Resources:**
- [PEP 255 – Generators](https://peps.python.org/pep-0255/)
- [Real Python – Decorators](https://realpython.com/primer-on-python-decorators/)

---

### 3. PEP8 + Professional Tooling

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| PEP8 rules | "What does PEP8 cover? Key rules?" | [ ] |
| ruff | "How do you enforce code style?" | [ ] |
| uv | "How do you manage Python dependencies?" | [ ] |
| pre-commit | "How do you prevent bad commits?" | [ ] |
| interrogate | "How do you enforce docstring coverage?" | [ ] |

**Exercise:** Add `ruff` + `pre-commit` to this project:
1. `uv add --dev ruff pre-commit interrogate`
2. Create `.pre-commit-config.yaml` with ruff + interrogate hooks
3. Run against existing code, fix all warnings

**Resources:**
- [ruff docs](https://docs.astral.sh/ruff/)
- [uv docs](https://docs.astral.sh/uv/)
- [pre-commit docs](https://pre-commit.com/)

---

### 4. SOLID Principles

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| SRP | "What is the Single Responsibility Principle?" | [ ] |
| OCP | "What is Open/Closed Principle?" | [ ] |
| LSP | "What is Liskov Substitution?" | [ ] |
| ISP | "Interface Segregation?" | [ ] |
| DIP | "Dependency Inversion — what problem does it solve?" | [ ] |

**Exercise:** Identify one SOLID violation in `src/agents/orchestrator.py` (hint: it has one). Propose a fix to Claude and discuss the tradeoff.

**Resources:** [Real Python – SOLID](https://realpython.com/solid-principles-python/)

---

### 5. Design Patterns

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Strategy | "When would you use Strategy over if/else?" | [ ] |
| Factory | "What is a Factory? When is it useful?" | [ ] |
| Observer | "What is Observer/Event pattern?" | [ ] |
| Repository | "What is the Repository pattern?" | [ ] |
| Dependency Injection | "How does DI reduce coupling?" | [ ] |

**Exercise:** `PerfumeTools` uses a form of Strategy for tool dispatch. Explain this to Claude. Then identify which pattern `app.state` in FastAPI resembles and why.

**Resources:** [Refactoring Guru – Python patterns](https://refactoring.guru/design-patterns/python)

---

### 6. Scalable Logging [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| logging module | "How do you implement scalable logging?" | [ ] |
| structured logging | "What is structured logging? Why does it matter?" | [ ] |
| log levels | "When do you use DEBUG vs INFO vs ERROR?" | [ ] |

**Exercise:** Add structured logging to `src/agents/orchestrator.py`:
- Log each tool call (name + input) at INFO level
- Log tool results at DEBUG level
- Log errors at ERROR level with full traceback
- Use `structlog` or Python's `logging` with JSON formatter

**Resources:** [Python logging HOWTO](https://docs.python.org/3/howto/logging.html)

---

### 7. Error Handling in Distributed Systems [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| retry patterns | "How do you handle transient failures in a distributed system?" | [ ] |
| circuit breaker | "What is a circuit breaker pattern?" | [ ] |
| idempotency | "What is idempotency and why does it matter?" | [ ] |
| dead letter queue | "What is a DLQ?" | [ ] |

**Exercise:** The current `ClaudeClient` has no retry logic. Design (don't implement yet) a retry strategy for `RateLimitError` with exponential backoff. Discuss with Claude: when should you retry vs fail fast?

---

### 8. Data Pipeline Optimization [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| generators for large files | "How do you process a 10GB CSV in Python?" | [ ] |
| chunked processing | "How do you optimize a slow data pipeline?" | [ ] |
| profiling | "How do you find bottlenecks in Python code?" | [ ] |

**Exercise:** The current `DataLoader` loads the entire CSV into memory. What happens if Fragrantica CSV has 5M rows? Design a generator-based alternative. Don't implement — explain the approach to Claude and get feedback.

**Resources:** [Python docs – generators](https://docs.python.org/3/howto/functional.html#generators)

---

### 9. pytest Coverage

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| coverage.py | "What is test coverage? What's a good target?" | [ ] |
| hypothesis | "What is property-based testing?" | [ ] |

**Exercise:** Run `pytest tests/ --cov=src --cov-report=html` (requires `pytest-cov`). Find the module with lowest coverage. Write 2 new tests to increase it.

---

## Completion Criteria

- [ ] Can answer all [INTERVIEW CRITICAL] questions in this phase from memory, in under 2 minutes each
- [ ] `ruff` + `pre-commit` running in this project with zero violations
- [ ] `@log_call` decorator working on `execute_tool`
- [ ] Generator version of `get_all_perfumes` written and explained
- [ ] SOLID violation in orchestrator identified and fix proposed
- [ ] Test coverage >80% on `src/api/claude_client.py`
