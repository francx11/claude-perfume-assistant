"""
Phase 3 - Part B Exercise: LangGraph Orchestrator
Rebuilds OrchestratorAgent as a LangGraph StateGraph.

Graph:
  START → call_claude → [stop_reason == tool_use?]
                           ├── yes → execute_tools → call_claude (loop)
                           └── no  → END
"""

import logging
import os
import sys
from typing import Any, Dict, List

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dotenv import load_dotenv  # noqa: E402
from langgraph.graph import END, StateGraph  # noqa: E402
from typing_extensions import TypedDict  # noqa: E402

from src.agents.orchestrator import OrchestratorAgent  # noqa: E402
from src.api.claude_client import ClaudeClient  # noqa: E402
from src.data.loader import DataLoader  # noqa: E402
from src.tools.perfume_tools import PerfumeTools  # noqa: E402

load_dotenv()
logger = logging.getLogger(__name__)


# ── State ─────────────────────────────────────────────────────────────────────


class AgentState(TypedDict):
    """Shared state passed between all graph nodes."""

    messages: List[Dict[str, Any]]
    stop_reason: str
    iteration: int


# ── Helpers ───────────────────────────────────────────────────────────────────


def _build_components():
    """Instantiate Claude client, data loader, and perfume tools."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    claude_client = ClaudeClient(api_key=os.environ["ANTHROPIC_API_KEY"])
    data_loader = DataLoader(os.path.join(root, "data", "raw", "fragrantica.csv"))
    data_loader.load_data()
    perfume_tools = PerfumeTools(data_loader)
    orchestrator = OrchestratorAgent(claude_client, perfume_tools)
    return claude_client, perfume_tools, orchestrator


claude_client, perfume_tools, _orchestrator = _build_components()

SYSTEM_PROMPT = _orchestrator._build_system_prompt()
TOOLS = perfume_tools.get_tools_definitions()


# ── Nodes ─────────────────────────────────────────────────────────────────────


def call_claude(state: AgentState) -> AgentState:
    """Call Claude API with current message history."""
    response = claude_client.send_message(
        messages=state["messages"],
        tools=TOOLS,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
    )
    return {
        "messages": state["messages"] + [{"role": "assistant", "content": response["content"]}],
        "stop_reason": response["stop_reason"],
        "iteration": state["iteration"],
    }


def execute_tools(state: AgentState) -> AgentState:
    """Execute all tool_use blocks from the last Claude response."""
    last_msg = state["messages"][-1]
    tool_use_blocks = [b for b in last_msg["content"] if b["type"] == "tool_use"]

    tool_results = []
    for block in tool_use_blocks:
        result = _orchestrator._handle_tool_use(block)
        tool_results.append({"type": "tool_result", "tool_use_id": block["id"], "content": str(result)})

    return {
        "messages": state["messages"] + [{"role": "user", "content": tool_results}],
        "stop_reason": state["stop_reason"],
        "iteration": state["iteration"] + 1,
    }


# ── Conditional edge ──────────────────────────────────────────────────────────


def should_continue(state: AgentState) -> str:
    """Route to execute_tools or END based on stop_reason and iteration limit."""
    if state["stop_reason"] == "tool_use" and state["iteration"] < 5:
        return "execute_tools"
    return END


# ── Graph ─────────────────────────────────────────────────────────────────────


def build_graph():
    """Build and compile the LangGraph StateGraph."""
    graph = StateGraph(AgentState)

    graph.add_node("call_claude", call_claude)
    graph.add_node("execute_tools", execute_tools)

    graph.set_entry_point("call_claude")
    graph.add_conditional_edges("call_claude", should_continue)
    graph.add_edge("execute_tools", "call_claude")

    return graph.compile()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = build_graph()

    initial_state: AgentState = {
        "messages": [{"role": "user", "content": "Recomienda un perfume floral de verano"}],
        "stop_reason": "",
        "iteration": 0,
    }

    result = app.invoke(initial_state)

    final_text = next(
        (b["text"] for b in result["messages"][-1]["content"] if isinstance(b, dict) and b.get("type") == "text"),
        "Sin respuesta",
    )
    print("Respuesta:", final_text.encode("utf-8", errors="replace").decode("utf-8"))
    print(f"Iteraciones: {result['iteration']}")
