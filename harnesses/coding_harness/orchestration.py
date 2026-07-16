from langgraph.graph import StateGraph, START, END

from harnesses.coding_harness.states import MainAgentState
from harnesses.coding_harness.nodes.main_agent import main_agent
from harnesses.coding_harness.nodes.take_input import take_user_input
from harnesses.coding_harness.nodes.continual_agent import continual_agent, continue_or_not

code_harness = StateGraph(MainAgentState)

code_harness.add_node("user_input", take_user_input)
code_harness.add_node("main_agent", main_agent)
code_harness.add_node("should_continue", continual_agent)

# code_harness.add_edge(START, "main_agent")
# code_harness.add_edge("main_agent", END)

code_harness.add_edge(START, "user_input")
code_harness.add_edge("user_input", "main_agent")
code_harness.add_edge("main_agent", "should_continue")
code_harness.add_conditional_edges(
    "should_continue",
    continue_or_not,
    {
        "complete": END,
        "ongoing": "user_input"
    }
)

compiled_harness = code_harness.compile()

# from PIL import Image
# img = Image.open(compiled_harness.get_graph(xray=True).draw_mermaid_png())
# img.save("graph.png")

# compiled_harness.get_graph(xray=True).draw_png(output_file_path="graph.png")

# compiled_harness.ainvoke({"main_agent_messages": []})