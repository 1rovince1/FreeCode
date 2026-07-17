from pprint import pprint

from langsmith import traceable

from services.ollama_llm_service import call_llm
from harnesses.coding_harness.states import MainAgentState


prompt = """
Based on the given conversation history, calssify whether the conversation is ongoing, or the task is complete.
Return only one work in the response:
    - complete
    - ongoing
Do not give any explanation, just give the response as one word.
"""

@traceable
async def continuation_agent_node(state: MainAgentState):
    messages = [{
        "role": "system",
        "content": prompt
    }]
    messages.extend(state.get("main_agent_messages", []))

    response = await call_llm(
        messages=messages,
        model="gemma4:cloud"
    )
    # with open("response_continue_agent.txt", "w") as file:
    #     pprint(response, stream=file)

    # state["current_conversation_state"] = response.message.content
    state["current_conversation_state"] = response.content
    return state


async def should_continue_decision_node(state: MainAgentState):
    return state.get("current_conversation_state", "ongoing")