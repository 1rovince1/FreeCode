from langsmith import traceable

from harnesses.coding_harness.states import MainAgentState

@traceable
async def take_user_input_node(state: MainAgentState):
    if not state.get("current_conversation_state", None):
        state["main_agent_messages"] = [{
            "role": "assistant",
            "content": "Hi, how can I help you?"
        }]
    agent_message = state.get("main_agent_messages")[-1]["content"]
    print(f"Agent: {agent_message}")
    user_query = input("Query: ")
    state["current_user_query"] = user_query
    user_message = {
        "role": "user",
        "content": user_query
    }
    state["main_agent_messages"].append(user_message)
    return state