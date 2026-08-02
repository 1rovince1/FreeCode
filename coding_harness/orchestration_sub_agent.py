from langgraph.graph import START, END, StateGraph
from coding_harness.states import SubAgentState
from coding_harness.nodes import (
    sub_agent,
    tool_call,
    context_compressor
)
from coding_harness.conditional_edges import *


sub_agent_orchestration = StateGraph(SubAgentState)


# nodes
sub_agent_orchestration.add_node("sub_agent", sub_agent)
sub_agent_orchestration.add_node("tool_call", tool_call)
sub_agent_orchestration.add_node("context_compressor", context_compressor)

# edges
sub_agent_orchestration.add_edge(START, "sub_agent")
sub_agent_orchestration.add_conditional_edges(
    "sub_agent",
    tool_call_decision_edge,
    {
        "tool": "tool_call"
    }
)
# sub_agent_orchestration.add_edge("tool_call", "sub_agent")
sub_agent_orchestration.add_conditional_edges(
    "tool_call",
    context_compression_decision_edge,
    {
        "compress": "context_compressor",
        "continue": "sub_agent"
    }
)
sub_agent_orchestration.add_edge("context_compressor", "sub_agent")


# compilation
compiled_sub_agent_orchestration = sub_agent_orchestration.compile()