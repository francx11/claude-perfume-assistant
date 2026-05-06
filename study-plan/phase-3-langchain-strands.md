# Phase 3: LangChain Ecosystem + Strands Agents

**Prerequisite:** Phase 2 complete (especially agent architecture concepts).
**Goal:** Hands-on with LangChain/LangGraph, observability (LangSmith/Langfuse), Strands Agents.

**Key insight going in:** You've already built an orchestrator, tool-use loop, and RAG system manually. LangChain is an abstraction layer over what you've already done. Learn the abstractions by mapping them to your own code.

---

## Part A: LangChain Core

### LCEL and Chains

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| LCEL (LangChain Expression Language) | "What is LCEL? How does it compose chains?" | [ ] |
| Runnable interface | "What is the Runnable interface in LangChain?" | [ ] |
| Prompt templates | "What is a PromptTemplate?" | [ ] |
| Output parsers | "What are output parsers? When are they needed?" | [ ] |

**Mental model:** LangChain's `chain = prompt | llm | parser` is LCEL pipe syntax. Your `orchestrator.process_query()` is the manual equivalent.

**Exercise:** Install LangChain and reproduce the simplest PerfumeShop flow:
```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

model = ChatAnthropic(model="claude-sonnet-4-6")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a perfume expert."),
    ("human", "{question}")
])
chain = prompt | model
result = chain.invoke({"question": "Recommend a fresh summer perfume"})
```

---

### Retrievers and RAG in LangChain

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| BaseRetriever | "How does LangChain abstract retrieval?" | [ ] |
| VectorStoreRetriever | "How do you connect a vector store to LangChain?" | [ ] |
| create_retrieval_chain | "What does create_retrieval_chain do?" | [ ] |
| Contextual compression | "What is contextual compression in LangChain?" | [ ] |

**Exercise:** Wrap your `RAGRetriever` as a LangChain `BaseRetriever`. Plug it into `create_retrieval_chain`. Compare the output quality with your manual implementation.

**Resources:** [LangChain – RAG](https://python.langchain.com/docs/tutorials/rag/)

---

### Memory and State

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Conversation history | "How does LangChain handle conversation memory?" | [ ] |
| RunnableWithMessageHistory | "What is RunnableWithMessageHistory?" | [ ] |

**Mental model:** Your `orchestrator.py` manages `conversation_history` as a list manually. LangChain wraps this in `RunnableWithMessageHistory`.

---

## Part B: LangGraph

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| StateGraph | "What is a StateGraph in LangGraph?" | [ ] |
| Nodes and edges | "How are nodes and edges defined in LangGraph?" | [ ] |
| Conditional routing | "How do you add conditional edges?" | [ ] |
| Human-in-the-loop | "How does LangGraph implement human-in-the-loop?" | [ ] |
| Persistence | "How does LangGraph persist state between runs?" | [ ] |

**Mental model:** Your orchestrator's `while stop_reason == "tool_use"` loop is a LangGraph graph with two nodes: `call_model` and `execute_tools`, with a conditional edge on `stop_reason`.

**Exercise:** Rebuild `OrchestratorAgent` as a LangGraph graph:
1. State: `{"messages": list, "iteration": int}`
2. Node `call_claude`: calls Claude API
3. Node `execute_tools`: runs PerfumeTools
4. Conditional edge: if `stop_reason == "tool_use"` → `execute_tools`, else → END
5. Add interrupt before `execute_tools` (human-in-the-loop) — this is Loopgate's pattern

**Resources:** [LangGraph docs](https://langchain-ai.github.io/langgraph/)

---

## Part C: Observability — LangSmith + Langfuse

### LangSmith

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Tracing | "How do you trace LangChain/LangGraph executions?" | [ ] |
| Evaluation datasets | "How do you build an evaluation dataset in LangSmith?" | [ ] |
| LLM-as-judge | "What is LLM-as-judge evaluation?" | [ ] |

**Exercise:** Enable LangSmith tracing for your LangGraph PerfumeShop:
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=...
```
Run 5 queries, inspect traces. Find one where the wrong tool was called.

**Resources:** [LangSmith docs](https://docs.smith.langchain.com/)

---

### Langfuse (open source alternative)

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Tracing vs LangSmith | "What is Langfuse? How does it compare to LangSmith?" | [ ] |
| Self-hosted | "When would you self-host Langfuse instead of using LangSmith?" | [ ] |
| Scores and evaluation | "How do you add evaluation scores in Langfuse?" | [ ] |

**Exercise:** Add Langfuse tracing to the manual `OrchestratorAgent` (no LangChain needed):
```python
from langfuse.decorators import observe

@observe()
def process_query(self, user_message: str):
    ...
```

**Resources:** [Langfuse docs](https://langfuse.com/docs)

---

## Part D: Strands Agents (AWS)

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Strands vs LangChain | "What is Strands Agents? How does it differ from LangChain?" | [ ] |
| Tool definition | "How do you define tools in Strands?" | [ ] |
| Agent loop | "How does the Strands agent loop work?" | [ ] |
| Bedrock integration | "How does Strands integrate with Amazon Bedrock?" | [ ] |

**Mental model:** Strands is AWS's alternative to LangChain, designed to work natively with Bedrock. Your `OrchestratorAgent` + `PerfumeTools` is the manual equivalent.

**Exercise:** Reproduce the `search_perfumes` tool in Strands syntax:
```python
from strands import Agent, tool

@tool
def search_perfumes(brand: str, notes: list[str]) -> list[dict]:
    """Search perfumes by brand and notes."""
    return data_loader.filter_perfumes({"brand": brand, "notes": notes})

agent = Agent(tools=[search_perfumes])
response = agent("Find a woody perfume from Dior")
```

**Resources:** [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)

---

## Completion Criteria

- [ ] LangGraph version of `OrchestratorAgent` working with same PerfumeTools
- [ ] LangSmith traces visible for at least 10 queries
- [ ] Langfuse `@observe()` added to manual orchestrator
- [ ] `search_perfumes` tool running in Strands
- [ ] Can explain LangGraph vs manual orchestrator tradeoffs in interview
- [ ] Can explain LangSmith vs Langfuse tradeoffs in interview
