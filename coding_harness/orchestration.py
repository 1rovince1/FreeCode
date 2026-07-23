from langgraph.graph import StateGraph, START, END

from coding_harness.states import MainAgentState
from coding_harness.nodes.main_agent_node import main_agent
# from coding_harness.nodes.take_input import take_user_input_node
# from coding_harness.nodes.continuation_agent import continuation_agent_node, should_continue_decision_node
from coding_harness.nodes.tool_call_node import tool_call
from coding_harness.conditional_edges.main_to_tool import tool_call_decision_edge

code_harness = StateGraph(MainAgentState)

# code_harness.add_node("user_input_agent", take_user_input_node)
code_harness.add_node("main_agent", main_agent)
# code_harness.add_node("should_continue_agent", continuation_agent_node)
code_harness.add_node("tool_call", tool_call)

# code_harness.add_edge(START, "main_agent")
# code_harness.add_edge("main_agent", END)

# code_harness.add_edge(START, "user_input_agent")
# code_harness.add_edge("user_input_agent", "main_agent")
# code_harness.add_edge("main_agent", "should_continue_agent")
# code_harness.add_conditional_edges(
#     "should_continue_agent",
#     should_continue_decision_node,
#     {
#         "complete": END,
#         "ongoing": "user_input_agent"
#     }
# )

code_harness.add_edge(START, "main_agent")
# code_harness.add_edge("main_agent", END)
code_harness.add_conditional_edges(
    "main_agent",
    tool_call_decision_edge,
    {
        False: END,
        True: "tool_call"
    }
)
code_harness.add_edge("tool_call", "main_agent")

compiled_harness = code_harness.compile()

# from PIL import Image
# img = Image.open(compiled_harness.get_graph(xray=True).draw_mermaid_png())
# img.save("graph.png")

# compiled_harness.get_graph(xray=True).draw_png(output_file_path="graph.png")

# compiled_harness.ainvoke({"main_agent_messages": []})