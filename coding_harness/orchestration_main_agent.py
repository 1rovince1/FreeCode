from langgraph.graph import StateGraph, START, END

from coding_harness.states import MainAgentState
from coding_harness.nodes import *
from coding_harness.conditional_edges import *


code_harness = StateGraph(MainAgentState)


# nodes
code_harness.add_node("main_agent", main_agent)
code_harness.add_node("tool_call", tool_call)
code_harness.add_node("task_dispatcher", task_dispatcher)

# edges
code_harness.add_edge(START, "main_agent")
code_harness.add_conditional_edges(
    "main_agent",
    tool_call_decision_edge,
    {
        "tool_call": "tool_call",
        "task_dispatcher": "task_dispatcher"
    }
)
code_harness.add_edge("tool_call", "main_agent")
code_harness.add_edge("task_dispatcher", "main_agent")


# compilation
compiled_harness = code_harness.compile()