from langgraph.graph import StateGraph, START, END

from coding_harness.states import MainAgentState
from coding_harness.nodes import (
    main_agent,
    tool_call,
    task_delegator,
    context_compressor
)
from coding_harness.conditional_edges import *


code_harness = StateGraph(MainAgentState)


# nodes
code_harness.add_node("main_agent", main_agent)
code_harness.add_node("tool_call", tool_call)
code_harness.add_node("task_delegator", task_delegator)
code_harness.add_node("context_compressor", context_compressor)

# edges
code_harness.add_edge(START, "main_agent")
code_harness.add_conditional_edges(
    "main_agent",
    tool_call_decision_edge,
    {
        "tool": "tool_call",
        "delegate": "task_delegator"
    }
)
# code_harness.add_edge("tool_call", "main_agent")
# code_harness.add_edge("task_delegator", "main_agent")
code_harness.add_conditional_edges(
    "tool_call",
    context_compression_decision_edge,
    {
        "compress": "context_compressor",
        "continue": "main_agent"
    }
)
code_harness.add_conditional_edges(
    "task_delegator",
    context_compression_decision_edge,
    {
        "compress": "context_compressor",
        "continue": "main_agent"
    }
)
code_harness.add_edge("context_compressor", "main_agent")


# compilation
compiled_harness = code_harness.compile()