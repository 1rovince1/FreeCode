from langgraph.graph import StateGraph, START, END

from coding_harness.states import MainAgentState
from coding_harness.nodes.main_agent_node import main_agent
from coding_harness.nodes.tool_call_node import tool_call
from coding_harness.conditional_edges.main_to_tool import tool_call_decision_edge

code_harness = StateGraph(MainAgentState)

# nodes
code_harness.add_node("main_agent", main_agent)
code_harness.add_node("tool_call", tool_call)

# edges
code_harness.add_edge(START, "main_agent")
code_harness.add_conditional_edges(
    "main_agent",
    tool_call_decision_edge,
    {
        False: END,
        True: "tool_call"
    }
)
code_harness.add_edge("tool_call", "main_agent")

# compilation
compiled_harness = code_harness.compile()